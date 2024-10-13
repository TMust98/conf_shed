from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session



def test_get_conf_shed(app: FastAPI, db_session: Session, client: TestClient):
    response = client.get("/api/confshed/1")
    assert response.status_code == 200
    confs = response.json()
    assert confs["status"] == "success"