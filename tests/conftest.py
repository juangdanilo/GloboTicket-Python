from datetime import date
from pathlib import Path
from typing import Generator
from unittest.mock import patch

import pytest
import sqlalchemy
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker

from globoticket.api import app, get_session
from globoticket.models import Base, DBCategory, DBEvent

# Configuración de la base de datos en memoria para pruebas
test_db = sqlalchemy.create_engine(
    "sqlite+pysqlite:///:memory:",
    connect_args={"check_same_thread": False},
    echo=True,
)

test_sessionmaker = sessionmaker(bind=test_db)


def setup_test_db() -> None:
    """Crea tablas y datos de prueba en la base de datos."""
    Base.metadata.create_all(bind=test_db)
    session = Session(test_db)
    cat = DBCategory(name="t")
    ev = DBEvent(product_code="123456", price=5.50, date=date(2024, 1, 1), category=cat)
    session.add(cat)
    session.add(ev)
    session.commit()


def get_test_session() -> Generator[Session, None, None]:
    """Crea una sesión de base de datos para una prueba.
    Después de la prueba: cierra la sesión y elimina todas las tablas."""
    setup_test_db()
    session = test_sessionmaker()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_db)


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    """Crea un TestClient que utiliza la base de datos de prueba."""
    app.dependency_overrides[get_session] = get_test_session
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


@pytest.fixture(autouse=True, scope="session")
def test_frontmatter() -> Generator[None, None, None]:
    """Sobrescribe la ubicación de los archivos frontmatter."""
    with patch(
        "globoticket.frontmatter.FRONTMATTER_DIRECTORY",
        new=Path(__file__).parent / "product_info",
    ):
        yield
