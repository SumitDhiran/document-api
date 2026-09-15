from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_document():
    create_response = client.post(
        "/documents",
        params={
            "name": "test.txt",
            "content": "hello from CI",
        },
    )

    assert create_response.status_code == 200

    document = create_response.json()

    assert document["name"] == "test.txt"
    assert document["content"] == "hello from CI"

    get_response = client.get("/documents")

    assert get_response.status_code == 200

    documents = get_response.json()

    assert any(
        doc["id"] == document["id"]
        for doc in documents
    )
