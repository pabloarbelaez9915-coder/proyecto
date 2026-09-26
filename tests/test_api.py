from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.api.main import app
from src.database import get_db
from src.models import Base


def test_membresia_crud_endpoints():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    test_session = sessionmaker(bind=engine, expire_on_commit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        session = test_session()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    try:
        created = client.post(
            "/api/v1/membresias",
            json={"nombre": "Inicial", "precio": "25.50"},
        )
        assert created.status_code == 201
        membership_id = created.json()["id_membresia"]

        listed = client.get("/api/v1/membresias")
        assert listed.status_code == 200
        assert len(listed.json()) == 1

        retrieved = client.get(f"/api/v1/membresias/{membership_id}")
        assert retrieved.status_code == 200
        assert retrieved.json()["nombre"] == "Inicial"

        updated = client.put(
            f"/api/v1/membresias/{membership_id}",
            json={"nombre": "Actualizada"},
        )
        assert updated.status_code == 200
        assert updated.json()["nombre"] == "Actualizada"

        deleted = client.delete(f"/api/v1/membresias/{membership_id}")
        assert deleted.status_code == 204
        assert client.get(f"/api/v1/membresias/{membership_id}").status_code == 404

        created_user = client.post(
            "/api/v1/usuarios",
            json={"nombre_usuario": "api-admin", "clave": "secreto"},
        )
        assert created_user.status_code == 201
        assert "clave" not in created_user.json()

        paths = client.get("/openapi.json").json()["paths"]
        assert len([path for path in paths if path.startswith("/api/v1/")]) == 20

        cors_response = client.options(
            "/api/v1/membresias",
            headers={
                "Origin": "https://cliente.example",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert cors_response.headers["access-control-allow-origin"] == "*"
    finally:
        app.dependency_overrides.clear()
        engine.dispose()
