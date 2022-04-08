import json


def test_create_comment_success(client):
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

    comment_data = {
        "cafe_id": 1,
        "content": "testcomment",
    }
    response = client.post(
        "/comments",
        json.dumps(comment_data),
        headers={"Authorization": "Bearer " + token["access_token"]},
    )

    assert response.status_code == 201
    assert response.json() == {"msg": "CREATE_SUCCESS"}


def test_create_comment_cafe_not_exist_fail(client):
    user_data = {"username": "user", "password": "userpassword", "type_id": 2}
    client.post("/users/register", json.dumps(user_data))
    sign_in_response = client.post(
        "/users/signin",
        user_data,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    token = sign_in_response.json()

    comment_data = {
        "cafe_id": 1,
        "content": "testcomment",
    }
    response = client.post(
        "/comments",
        json.dumps(comment_data),
        headers={"Authorization": "Bearer " + token["access_token"]},
    )

    assert response.status_code == 404
    assert response.json() == {"msg": "CAFE_DOES_NOT_EXIST"}


def test_delete_comment_success(client):
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

    comment_data = {
        "cafe_id": 1,
        "content": "testcomment",
    }
    client.post(
        "/comments",
        json.dumps(comment_data),
        headers={"Authorization": "Bearer " + token["access_token"]},
    )
    response = client.delete(
        "/comments/1",
        headers={"Authorization": "Bearer " + token["access_token"]},
    )

    assert response.status_code == 201
    assert response.json() == {"msg": "DELETE_SUCCESS"}


def test_delete_comment_not_exist_fail(client):
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
        "/comments/1",
        headers={"Authorization": "Bearer " + token["access_token"]},
    )

    assert response.status_code == 404
    assert response.json() == {"msg": "COMMENT_DOES_NOT_EXIST"}


def test_update_comment_success(client):
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

    comment_data = {
        "cafe_id": 1,
        "content": "testcomment",
    }
    client.post(
        "/comments",
        json.dumps(comment_data),
        headers={"Authorization": "Bearer " + token["access_token"]},
    )
    response = client.patch(
        "/comments/1",
        json.dumps({"content": "updatecomment"}),
        headers={"Authorization": "Bearer " + token["access_token"]},
    )

    assert response.status_code == 200
    assert response.json() == {"msg": "UPDATE_SUCCESS"}


def test_update_comment_permission_fail(client):
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

    user_data = {"username": "testuser1", "password": "testpassword", "type_id": 2}
    client.post("/users/register", json.dumps(user_data))
    sign_in_response = client.post(
        "/users/signin",
        user_data,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    user1_token = sign_in_response.json()
    comment_data = {
        "cafe_id": 1,
        "content": "testcomment",
    }
    client.post(
        "/comments",
        json.dumps(comment_data),
        headers={"Authorization": "Bearer " + user1_token["access_token"]},
    )

    user_data = {"username": "testuser2", "password": "testpassword", "type_id": 2}
    client.post("/users/register", json.dumps(user_data))
    sign_in_response = client.post(
        "/users/signin",
        user_data,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    user2_token = sign_in_response.json()
    response = client.patch(
        "/comments/1",
        json.dumps({"content": "updatecomment"}),
        headers={"Authorization": "Bearer " + user2_token["access_token"]},
    )

    assert response.status_code == 403
    assert response.json() == {"msg": "UNAUTHORIZED"}


def test_update_comment_invalid_field_fail(client):
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

    comment_data = {
        "cafe_id": 1,
        "content": "testcomment",
    }
    client.post(
        "/comments",
        json.dumps(comment_data),
        headers={"Authorization": "Bearer " + token["access_token"]},
    )
    response = client.patch(
        "/comments/1",
        json.dumps({"invalidfield": "updatecomment"}),
        headers={"Authorization": "Bearer " + token["access_token"]},
    )

    assert response.status_code == 422
