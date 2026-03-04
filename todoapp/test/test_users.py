from todoapp.test.utils import * 
from starlette import status

pytestmark = pytest.mark.usefixtures("user_overrides")

def test_return_user(test_user):
    response = client.get("/users/get_user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == "markus"
    assert response.json()['email'] == "test@test.com"
    assert response.json()['first_name'] == "markus"
    assert response.json()['last_name'] == "svedberg"
    assert response.json()['phone_number'] == "076 123 24 69"
    assert response.json()['role'] == "admin"

def test_change_pass_success(test_user):
    response = client.put("/users/change_password", json={"old_password":"testpassword", "new_password": "newpassword", "verify_password": "newpassword"})

    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_pass_invalid_curr_pass(test_user):
    response = client.put("/users/change_password", json={"old_password":"abcd", "new_password": "newpassword", "verify_password": "newpassword"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_change_pass_invalid_ver_pass(test_user):
    response = client.put("/users/change_password", json={"old_password":"testpassword", "new_password": "newpassword", "verify_password": "notcorrect"})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

def test_change_phone_number_success(test_user):
    num = "222222222"
    response = client.put(f"/users/change_phone_number/{num}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get("/users/get_user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['phone_number'] == num
