import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from conf_shed.config import DB_USER_TEST, DB_PASS_TEST, DB_HOST_TEST, DB_PORT_TEST, DB_NAME_TEST
from conf_shed.models import metadata
from fastapi.testclient import TestClient
from conf_shed.main import app as app_test
from fastapi import FastAPI
from starlette.requests import Request


SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"
engine_test = create_engine(SQLALCHEMY_DATABASE_URL)
TestSessionLocal = sessionmaker(autoflush=False, bind=engine_test)


def get_db(request: Request):
    return request.state.db


@pytest.fixture(autouse=True)
def app():
    metadata.create_all(engine_test)  # Create the tables.
    yield app_test
    metadata.drop_all(engine_test)


@pytest.fixture
def db_session(app: FastAPI):
    connection = engine_test.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(app: FastAPI, db_session: TestSessionLocal):
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client