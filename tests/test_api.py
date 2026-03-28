from http.client import responses
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

def test_list_tasks_empty():
    """GET /tasks powinien zwrócić listę (nawet pustą)"""
    with patch("app.main.SessionLocal") as mock_session:
        mock_session.return_value.__enter__ = lambda s: s
        mock_session.return_value.query.return_value.all.return_value = []
        mock_session.return_value.close.return_value = None

        response = client.get("/tasks")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

def test_create_task_missing_data():
    """POST /task bez body powinien zwrócić 422"""
    response = client.post("/tasks", json={})
    assert response.status_code == 422

def test_get_task_not_found():
    """GET /task/{id} dla nieistniejacego taska powinien zwrocic 404"""
    with patch("app.main.SessionLocal") as mock_session:
        mock_session.return_value.query.return_value.filter.return_value.first.return_value = None
        mock_session.return_value.close.return_value = None

        response = client.get("/task/nonexistent-id")
        assert response.status_code == 404