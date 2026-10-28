import pytest
from fastapi.testclient import TestClient
from backend.main import app


@pytest.fixture
def client():
    with TestClient(app, base_url="http://127.0.0.1") as c:
        yield c


def test_health_check_endpoint(client):
  response = client.get("/api/health")
  assert response.status_code == 200
  data = response.json()
  assert data["status"] == "healthy"
  assert "embedding_model" in data


def test_list_jobs_endpoint(client):
  response = client.get("/api/jobs")
  assert response.status_code == 200
  jobs = response.json()
  assert len(jobs) >= 2


def test_list_resumes_endpoint(client):
  response = client.get("/api/resumes")
  assert response.status_code == 200
  resumes = response.json()
  assert len(resumes) >= 4


def test_screening_endpoint(client):
  payload = {"job_id": "job_senior_nlp_engineer"}
  response = client.post("/api/match/screen", json=payload)
  assert response.status_code == 200
  data = response.json()
  assert data["total_evaluated"] >= 4
  assert len(data["candidates"]) >= 4


def test_evaluation_report_endpoint(client):
  response = client.get("/api/evaluation/report")
  assert response.status_code == 200
  data = response.json()
  assert "benchmarks" in data
  assert len(data["benchmarks"]) == 4
