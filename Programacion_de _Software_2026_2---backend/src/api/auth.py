import json
import os
from typing import Any

import firebase_admin
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth, credentials
from firebase_admin.exceptions import FirebaseError
from google.auth.exceptions import DefaultCredentialsError

bearer_scheme = HTTPBearer(auto_error=False)


def _get_firebase_app() -> firebase_admin.App:
    try:
        return firebase_admin.get_app()
    except ValueError:
        pass

    project_id = os.getenv("FIREBASE_PROJECT_ID")
    service_account_json = os.getenv("FIREBASE_SERVICE_ACCOUNT")
    try:
        if service_account_json:
            service_account = json.loads(service_account_json)
            if not isinstance(service_account, dict):
                raise ValueError("La cuenta de servicio debe ser un objeto JSON.")
            project_id = project_id or service_account.get("project_id")
            credential = credentials.Certificate(service_account)
        else:
            credential = credentials.ApplicationDefault()
    except (DefaultCredentialsError, TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="La configuración de credenciales de Firebase no es válida.",
        ) from exc

    if not project_id:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Configura FIREBASE_PROJECT_ID para validar sesiones.",
        )

    try:
        return firebase_admin.initialize_app(
            credential,
            options={"projectId": project_id},
        )
    except (DefaultCredentialsError, ValueError, FirebaseError) as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No fue posible inicializar Firebase Admin. Revisa sus credenciales.",
        ) from exc


def get_current_user(
    token: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict[str, Any]:
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Se requiere una sesión válida de Firebase.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    app = _get_firebase_app()
    try:
        return auth.verify_id_token(token.credentials, app=app, check_revoked=True)
    except (ValueError, FirebaseError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token de Firebase no es válido o expiró.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
