import json


def test_apply_like_success(client):
    user_data = {"username": "adminuser", "password": "adminpassword", "type_id": 1}
    client.post("/users/register", json.dumps(user_data))
    sign_in_response = client.post(
        "/users/signin",
        user_data,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    token = sign_in_response.json()

    cafe_data = {
        "name": "testcafe",
        "address": "testaddress",
        "lat": 41.40338,
        "lon": 2.17403,
        "rep_number": "010-1234-5678",
    }
    client.post(
        "/cafes",
        json.dumps(cafe_data),
        headers={"Authorization": "Bearer " + token["access_token"]},
    )

    like_data = {
        "cafe_id": 1,
    }
    response = client.post(
        "/likes",
        json.dumps(like_data),
        headers={"Authorization": "Bearer " + token["access_token"]},
    )

    assert response.status_code == 201
    assert response.json() == {"msg": "APPLY_SUCCESS"}


def test_apply_like_cafe_not_exist_fail(client):
    user_data = {"username": "testuser", "password": "testpassword", "type_id": 2}
    client.post("/users/register", json.dumps(user_data))
    sign_in_response = client.post(
        "/users/signin",
        user_data,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    token = sign_in_response.json()

    like_data = {
        "cafe_id": 1,
    }
    response = client.post(
        "/likes",
        json.dumps(like_data),
        headers={"Authorization": "Bearer " + token["access_token"]},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "CAFE_DOES_NOT_EXIST"}
