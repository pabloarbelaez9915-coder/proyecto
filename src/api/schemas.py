from typing import Optional

from pydantic import ConfigDict, Field, create_model
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase


def build_schemas(model: type[DeclarativeBase]):
    model_name = model.__name__.removesuffix("Model")
    create_fields = {}
    update_fields = {}
    read_fields = {}

    for column in model.__table__.columns:
        field_type = column.type.python_type
        if column.nullable:
            field_type = Optional[field_type]

        if not column.primary_key:
            if column.nullable or column.default is not None:
                default = None
            else:
                default = ...

            field_options = {}
            if isinstance(column.type, String) and column.type.length is not None:
                field_options["max_length"] = column.type.length
            create_fields[column.name] = (
                field_type,
                Field(default=default, **field_options),
            )
            update_fields[column.name] = (
                Optional[column.type.python_type],
                Field(default=None, **field_options),
            )

        if column.name != "clave":
            read_fields[column.name] = (field_type, ...)

    return (
        create_model(f"{model_name}Create", **create_fields),
        create_model(f"{model_name}Update", **update_fields),
        create_model(
            f"{model_name}Read",
            __config__=ConfigDict(from_attributes=True),
            **read_fields,
        ),
    )
