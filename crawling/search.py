import time
import os
from pathlib import Path

import aiohttp
import asyncio
import aiofiles
from aiocsv import AsyncWriter

from settings import API_KEY, GU_LIST


api_key = API_KEY
BASE_DIR = str(Path(__file__).resolve().parent)


# 카페 리스트에 대표번호가 없어서 장소 상세 검색 API 사용
async def get_phone_number(session, place_id, lock):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?key={api_key}&place_id={place_id}&language=ko"
    async with session.get(url) as response:
        if response.status == 200:
            result = await response.json()
            item = result["result"]
            async with lock:
                async with aiofiles.open(
                    f"{BASE_DIR}/csv/phone_numbers.csv", mode="a+", encoding="utf-8", newline=""
                ) as file:
                    writer = AsyncWriter(file)
                    await writer.writerow(
                        [item["place_id"], item.get("formatted_phone_number")]
                    )

    await asyncio.sleep(2)


# Google Place API 사용
async def get_cafe_list(session, gu, lock):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?key={api_key}&query={gu} 카페&language=ko"
    url2 = f"https://maps.googleapis.com/maps/api/place/textsearch/json?key={api_key}&pagetoken="
    page_token = ""
    # 하나의 검색어에 최대 3 page 까지 가능
    for i in range(3):
        url = url if i == 0 else url2 + page_token
        async with session.get(url) as response:
            if response.status == 200:
                result = await response.json()
                items = result["results"]
                page_token = result.get("next_page_token")

                await asyncio.gather(
                    *[
                        get_phone_number(session, item["place_id"], lock)
                        for item in items
                    ]
                )
                async with lock:
                    async with aiofiles.open(
                        f"{BASE_DIR}/csv/cafes.csv", mode="a+", encoding="utf-8", newline=""
                    ) as file:
                        writer = AsyncWriter(file)
                        await writer.writerows(
                            [
                                [
                                    item["place_id"],
                                    item.get("name"),
                                    item.get("formatted_address"),
                                    item["geometry"]["location"]["lat"],
                                    item["geometry"]["location"]["lng"],
                                ]
                                for item in items
                            ]
                        )

        await asyncio.sleep(2)


async def main():
    try:
        os.mkdir(f"{BASE_DIR}/csv")
        Path(f"{BASE_DIR}/csv/cafes.csv").touch()
        Path(f"{BASE_DIR}/csv/phone_numbers.csv").touch()
    except FileExistsError:
        pass
    # 서울시 25개 구
    gu_list = GU_LIST
    # csv file 쓰기 작업시 데이터 누락 방지
    lock = asyncio.Lock()

    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[get_cafe_list(session, gu, lock) for gu in gu_list])


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    start = time.time()
    asyncio.run(main())
    delta = time.time() - start
    print(f"소요시간: {delta:.03}")
