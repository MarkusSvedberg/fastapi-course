from starlette import status

from todoapp.test.utils import *

pytestmark = pytest.mark.usefixtures("user_overrides")

def test_read_all_authenticated(test_todo):
    response = client.get("/todos/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{ "title": "Learn to code!", "description": "Need to learn everyday!", "priority":5, "complete":False, "owner_id": 1, "id": 1 }]

def test_read_one_authenticated(test_todo):
    response = client.get("/todos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == { "title": "Learn to code!", "description": "Need to learn everyday!", "priority":5, "complete":False, "owner_id": 1, "id": 1 }

def test_read_one_authenticated_not_found():
    response = client.get("/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == { "detail": "Todo not found" }

def test_create_todo(test_todo):
    request_data = { "title": "Learn to code 2!", "description": "Need to learn everyday!", "priority":5, "complete":False}

    response = client.post("/todos/", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    response = client.get("/todos/2")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == { "title": "Learn to code 2!", "description": "Need to learn everyday!", "priority":5, "complete":False, "owner_id": 1, "id": 2 }

def test_update_todo(test_todo):
    request_data = { "title": "Changed title", "description": "Need to learn everyday!", "priority":5, "complete":False}

    response = client.put("/todos/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get("/todos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == { "title": "Changed title", "description": "Need to learn everyday!", "priority":5, "complete":False, "owner_id": 1, "id": 1 }

def test_update_todo_not_found(test_todo):
    request_data = { "title": "Changed title", "description": "Need to learn everyday!", "priority":5, "complete":False}

    response = client.put("/todos/999", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}

def test_delete_todo(test_todo):
    response = client.delete("/todos/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get("/todos/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_todo_not_found(test_todo):
    response = client.delete("/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}
