from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from conf_shed.models import Presentation, Shedule


def test_prdelete(app: FastAPI, db_session: Session, client: TestClient):
    response = client.post("/pr-delete/1")
    assert response.status_code == 200
    message = response.json()
    assert message["message"] == "Отсутствует презентация с таким номером!"