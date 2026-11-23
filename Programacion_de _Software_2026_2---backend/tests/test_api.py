from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.api.main import app
from src.api.auth import get_current_user
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
    app.dependency_overrides[get_current_user] = lambda: {"uid": "test-user"}
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
        resources = (
            "usuarios",
            "membresias",
            "sedes",
            "clientes",
            "entrenadores",
            "clases",
            "rutinas",
            "equipos",
            "asistencias",
            "pagos",
        )
        assert len([path for path in paths if path.startswith("/api/v1/")]) == 20
        for resource in resources:
            collection_path = paths[f"/api/v1/{resource}"]
            record_path = paths[f"/api/v1/{resource}/{{record_id}}"]
            assert {"get", "post"} <= collection_path.keys()
            assert {"get", "put", "delete"} <= record_path.keys()

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


def test_api_rejects_requests_without_firebase_token():
    client = TestClient(app)

    response = client.get("/api/v1/membresias")

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_api_rejects_invalid_firebase_token(monkeypatch):
    from src.api import auth

    def reject_token(*_args, **_kwargs):
        raise ValueError("invalid token")

    monkeypatch.setattr(auth, "_get_firebase_app", lambda: None)
    monkeypatch.setattr(auth.auth, "verify_id_token", reject_token)
    client = TestClient(app)

    response = client.get(
        "/api/v1/membresias",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401


def test_api_reports_missing_firebase_admin_credentials(monkeypatch):
    from google.auth.exceptions import DefaultCredentialsError

    from src.api import auth

    def missing_app():
        raise ValueError("Firebase Admin has not been initialized.")

    def missing_credentials():
        raise DefaultCredentialsError("No credentials found.")

    monkeypatch.setattr(auth.firebase_admin, "get_app", missing_app)
    monkeypatch.setattr(auth.credentials, "ApplicationDefault", missing_credentials)
    monkeypatch.delenv("FIREBASE_SERVICE_ACCOUNT", raising=False)
    monkeypatch.delenv("FIREBASE_PROJECT_ID", raising=False)
    client = TestClient(app)

    response = client.get(
        "/api/v1/membresias",
        headers={"Authorization": "Bearer firebase-id-token"},
    )

    assert response.status_code == 503
