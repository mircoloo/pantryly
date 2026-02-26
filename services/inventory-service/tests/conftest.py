import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.models import Base
from app.api.v1.products import _get_user_id

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # fondamentale per in-memory condiviso
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
    

def override_user_id():
    return 1  

@pytest.fixture
def client(db):  # db fixture vista prima
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[_get_user_id] = override_user_id

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()