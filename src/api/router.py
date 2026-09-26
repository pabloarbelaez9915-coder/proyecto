from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.api.schemas import build_schemas
from src.database import get_db


def build_crud_router(model: type, resource: str, id_field: str) -> APIRouter:
    create_schema, update_schema, read_schema = build_schemas(model)
    router = APIRouter(prefix=f"/{resource}", tags=[resource.capitalize()])

    def find_record(db: Session, record_id: str):
        return db.scalar(select(model).where(getattr(model, id_field) == record_id))

    def list_records(db: Session = Depends(get_db)):
        return db.query(model).all()

    def get_record(record_id: str, db: Session = Depends(get_db)):
        record = find_record(db, record_id)
        if record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró el registro {record_id}.",
            )
        return record

    def create_record(payload: BaseModel, db: Session = Depends(get_db)):
        record = model(**payload.model_dump(exclude_unset=True))
        db.add(record)
        try:
            db.commit()
            db.refresh(record)
        except IntegrityError as exc:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El registro entra en conflicto con datos existentes.",
            ) from exc
        return record

    def update_record(
        record_id: str,
        payload: BaseModel,
        db: Session = Depends(get_db),
    ):
        record = find_record(db, record_id)
        if record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró el registro {record_id}.",
            )

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(record, field, value)

        try:
            db.commit()
            db.refresh(record)
        except IntegrityError as exc:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="La actualización entra en conflicto con datos existentes.",
            ) from exc
        return record

    def delete_record(record_id: str, db: Session = Depends(get_db)) -> Response:
        record = find_record(db, record_id)
        if record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró el registro {record_id}.",
            )
        db.delete(record)
        try:
            db.commit()
        except IntegrityError as exc:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar porque otros registros dependen de este.",
            ) from exc
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    create_record.__annotations__["payload"] = create_schema
    update_record.__annotations__["payload"] = update_schema

    router.add_api_route(
        "",
        list_records,
        methods=["GET"],
        response_model=list[read_schema],
        status_code=status.HTTP_200_OK,
        name=f"listar_{resource}",
    )
    router.add_api_route(
        "/{record_id}",
        get_record,
        methods=["GET"],
        response_model=read_schema,
        status_code=status.HTTP_200_OK,
        name=f"obtener_{resource}",
    )
    router.add_api_route(
        "",
        create_record,
        methods=["POST"],
        response_model=read_schema,
        status_code=status.HTTP_201_CREATED,
        name=f"crear_{resource}",
    )
    router.add_api_route(
        "/{record_id}",
        update_record,
        methods=["PUT"],
        response_model=read_schema,
        status_code=status.HTTP_200_OK,
        name=f"actualizar_{resource}",
    )
    router.add_api_route(
        "/{record_id}",
        delete_record,
        methods=["DELETE"],
        status_code=status.HTTP_204_NO_CONTENT,
        name=f"eliminar_{resource}",
    )
    return router
