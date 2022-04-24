import json


def test_create_user_success(client):
    data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/users/register", json.dumps(data))

    assert response.status_code == 201
    assert response.json() == {"msg": "CREATE_SUCCESS"}


def test_create_user_exist_fail(client):
    data = {"username": "existuser", "password": "existpassword"}
    client.post("/users/register", json.dumps(data))
    response = client.post("/users/register", json.dumps(data))

    assert response.status_code == 409
    assert response.json() == {"detail": "USER_ALREADY_EXIST"}


def test_sign_in_success(client):
    data = {"username": "testuser", "password": "testpassword"}
    client.post("/users/register", json.dumps(data))
    response = client.post(
        "/users/signin",
        data,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200


def test_sign_in_not_exist_fail(client):
    data = {"username": "testuser", "password": "testpassword"}
    response = client.post(
        "/users/signin",
        data,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "USER_DOES_NOT_EXIST"}


def test_sign_in_invalid_password_fail(client):
    data = {"username": "testuser", "password": "testpassword"}
    client.post("/users/register", json.dumps(data))
    data["password"] = "wrong_password"
    response = client.post(
        "/users/signin",
        data,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "INVALID_PASSWORD"}


def test_delete_user_success(client):
    data = {"username": "testuser", "password": "testpassword"}
    client.post("/users/register", json.dumps(data))
    sign_in_response = client.post(
        "/users/signin",
        data,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    token = sign_in_response.json()
    response = client.delete(
        "/users/testuser",
        headers={"Authorization": "Bearer " + token["access_token"]},
    )

    assert response.status_code == 201
    assert response.json() == {"msg": "DELETE_SUCCESS"}


def test_delete_user_permission_fail(client):
    client.post(
        "/users/register",
        json.dumps({"username": "existuser", "password": "existpassword"}),
    )

    data = {"username": "testuser", "password": "testpassword"}
    client.post("/users/register", json.dumps(data))
    sign_in_response = client.post(
        "/users/signin",
        data,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    token = sign_in_response.json()
    response = client.delete(
        "/users/existuser",
        headers={"Authorization": "Bearer " + token["access_token"]},
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "UNAUTHORIZED"}
