from typing import Generator

import pytest
from playwright.sync_api import APIRequestContext, Playwright


BASE_URL = "https://dummyjson.com"


@pytest.fixture(scope="session")
def api_context(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    """
    Creates one API request context for all CRUD tests.
    """

    request_context = playwright.request.new_context(
        base_url=BASE_URL,
        extra_http_headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )

    yield request_context

    request_context.dispose()


def test_create_todo(api_context: APIRequestContext) -> None:
    """CREATE operation using POST."""

    request_body = {
        "todo": "Prepare Playwright API testing demonstration",
        "completed": False,
        "userId": 5,
    }

    response = api_context.post(
        "/todos/add",
        data=request_body,
    )

    print("\nCREATE STATUS:", response.status)

    response_body = response.json()
    print("CREATE RESPONSE:", response_body)

    assert response.status == 201
    assert response_body["todo"] == request_body["todo"]
    assert response_body["completed"] is False
    assert response_body["userId"] == 5
    assert "id" in response_body


def test_read_todo(api_context: APIRequestContext) -> None:
    """READ operation using GET."""

    response = api_context.get("/todos/1")

    print("\nREAD STATUS:", response.status)

    response_body = response.json()
    print("READ RESPONSE:", response_body)

    assert response.status == 200
    assert response_body["id"] == 1
    assert "todo" in response_body
    assert "completed" in response_body
    assert "userId" in response_body


def test_update_todo(api_context: APIRequestContext) -> None:
    """UPDATE operation using PUT."""

    request_body = {
        "completed": False,
    }

    response = api_context.put(
        "/todos/1",
        data=request_body,
    )

    print("\nUPDATE STATUS:", response.status)

    response_body = response.json()
    print("UPDATE RESPONSE:", response_body)

    assert response.status == 200
    assert str(response_body["id"]) == "1"
    assert response_body["completed"] is False


def test_delete_todo(api_context: APIRequestContext) -> None:
    """DELETE operation using DELETE."""

    response = api_context.delete("/todos/1")

    print("\nDELETE STATUS:", response.status)

    response_body = response.json()
    print("DELETE RESPONSE:", response_body)

    assert response.status == 200
    assert response_body["id"] == 1
    assert response_body["isDeleted"] is True
    assert "deletedOn" in response_body