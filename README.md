<h1 align="center">Cafe Search: HJW</h1>

## 프로젝트 소개 

<p>모여서 각자 코딩하는 장소를 위한 카페 검색 서버입니다. 와이파이/주차/흡연실 등 다양한 조건 검색, 위치 기반 검색, 키워드 검색을 통해 원하는 카페의 정보를 얻을 수 있습니다. </p>
<p>Conventional Git Commit, Versioning 등 실무에서 통용되는 표준을 지키려고 노력했습니다. 서버에 대한 많은 공부를 위해 프론트엔드와 병행보단 백엔드 구축에 집중하여 구현했습니다.</p>


## 프로젝트 구조

![cafe-search](https://user-images.githubusercontent.com/71869837/162135341-e184d38a-836f-46ea-8135-56bff896214c.png)

## 프로젝트 실행 방법

### 필수 패키지 설치
> `pip install -r requrements.txt`


### 환경변수 지정
```python3
SERVER_HOST: str = "localhost"
SERVER_PORT: int = 8000
RELOAD: bool = True

DB_USER: str
DB_PASSWORD: str
DB_HOST: str
DB_NAME: str
DB_PORT: str

TOKEN_SECRET_KEY: str
HASHING_ALGORITHM: str
TOKEN_EXPIRATION: int
```
디렉토리 최상단에 .env 파일을 작성하면 자동으로 연동됩니다.

### 서버 실행
> `python main.py`
