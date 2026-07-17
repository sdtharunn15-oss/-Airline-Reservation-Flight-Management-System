import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def test_client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return TestClient(app)


@pytest.fixture
def admin_token(test_client):
    test_client.post(
        "/auth/register",
        json={
            "username": "admin",
            "email": "admin@test.com",
            "password": "admin123",
            "role": "Admin",
        },
    )

    response = test_client.post(
        "/auth/login",
        json={
            "username": "admin",
            "password": "admin123",
        },
    )

    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def passenger_token(test_client):
    test_client.post(
        "/auth/register",
        json={
            "username": "john",
            "email": "john@test.com",
            "password": "john123",
            "role": "Passenger",
        },
    )

    response = test_client.post(
        "/auth/login",
        json={
            "username": "john",
            "password": "john123",
        },
    )

    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}