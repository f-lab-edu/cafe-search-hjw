import json


def test_create_cafe_success(client):
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
    response = client.post(
        "/cafes",
        json.dumps(cafe_data),
        headers={"Authorization": "Bearer " + token["access_token"]},
    )

    assert response.status_code == 201
    assert response.json() == {"msg": "CREATE_SUCCESS"}


def test_create_cafe_exist_fail(client):
    user_data = {"username": "adminuser", "password": "adminpassword", "type_id": 1}
    client.post("/users/register", json.dumps(user_data))
    sign_in_response = client.post(
        "/users/signin",
        user_data,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    token = sign_in_response.json()

    cafe_data = {
        "name": "existcafe",
        "address": "existaddress",
        "lat": 41.40338,
        "lon": 2.17403,
        "rep_number": "010-1234-5678",
    }
    client.post(
        "/cafes",
        json.dumps(cafe_data),
        headers={"Authorization": "Bearer " + token["access_token"]},
    )
    response = client.post(
        "/cafes",
        json.dumps(cafe_data),
        headers={"Authorization": "Bearer " + token["access_token"]},
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "CAFE_ALREADY_EXIST"}


def test_create_cafe_permission_fail(client):
    user_data = {"username": "user", "password": "userpassword", "type_id": 2}
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
    response = client.post(
        "/cafes",
        json.dumps(cafe_data),
        headers={"Authorization": "Bearer " + token["access_token"]},
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "UNAUTHORIZED"}


def test_delete_cafe_success(client):
    user_data = {"username": "adminuser", "password": "adminpassword", "type_id": 1}
    client.post("/users/register", json.dumps(user_data))
    sign_in_response = client.post(
        "/users/signin",
        user_data,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    token = sign_in_response.json()

    cafe_data = {
        "name": "existcafe",
        "address": "existaddress",
        "lat": 41.40338,
        "lon": 2.17403,
        "rep_number": "010-1234-5678",
    }
    client.post(
        "/cafes",
        json.dumps(cafe_data),
        headers={"Authorization": "Bearer " + token["access_token"]},
    )
    response = client.delete(
        "/cafes/1",
        headers={"Authorization": "Bearer " + token["access_token"]},
    )

    assert response.status_code == 201
    assert response.json() == {"msg": "DELETE_SUCCESS"}


def test_delete_cafe_not_exist_fail(client):
    user_data = {"username": "adminuser", "password": "adminpassword", "type_id": 1}
    client.post("/users/register", json.dumps(user_data))
    sign_in_response = client.post(
        "/users/signin",
        user_data,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    token = sign_in_response.json()

    response = client.delete(
        "/cafes/1",
        headers={"Authorization": "Bearer " + token["access_token"]},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "CAFE_DOES_NOT_EXIST"}


def test_update_cafe_success(client):
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
    cafe_update_data = {
        "name": "updatecafe",
        "address": "updateaddress",
    }
    response = client.patch(
        "/cafes/1",
        json.dumps(cafe_update_data),
        headers={"Authorization": "Bearer " + token["access_token"]},
    )

    assert response.status_code == 200
    assert response.json() == {"msg": "UPDATE_SUCCESS"}


def test_update_cafe_invalid_field_fail(client):
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
    cafe_update_data = {
        "invalidfeid": "updatecafe",
    }
    response = client.patch(
        "/cafes/1",
        json.dumps(cafe_update_data),
        headers={"Authorization": "Bearer " + token["access_token"]},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "INVALIED_FIELD"}
