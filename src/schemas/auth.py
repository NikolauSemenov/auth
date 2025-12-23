import dataclasses
from dataclasses import fields, field
from typing import ClassVar, Type

from marshmallow import Schema, EXCLUDE
from marshmallow_dataclass import dataclass


@dataclasses.dataclass(init=False)
class ClassSchema:
    def __init__(self, **kwargs):
        names = set([f.name for f in fields(self)])
        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class BaseSchema(ClassSchema): ...


@dataclass
class RegisterRequestSchema(BaseSchema):
    name: str = field(metadata=dict(required=True))
    password: str = field(metadata=dict(required=True))


@dataclass
class LoginResponseSchema(BaseSchema):
    access_token: str = field(metadata=dict(required=True))
    token_type: str = field(metadata=dict(required=True))
