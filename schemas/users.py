from pydantic import BaseModel


class BaseUserSchema(BaseModel):
    first_name: str
    last_name: str
    email: str


class CreateUserSchema(BaseUserSchema):
    password: str


class UpdateUserSchema(BaseUserSchema): ...


class UpdatePasswordUserSchema(BaseModel):
    password: str
    new_password: str


class PublicUserSchema(BaseUserSchema):
    id: int
