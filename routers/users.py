from http import HTTPStatus
from oracledb import Connection
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from database import users
from database.core import get_connection
from schemas.users import (
    CreateUserSchema,
    PublicUserSchema,
    UpdatePasswordUserSchema,
    UpdateUserSchema,
)
from services.security import get_current_user
from services.security.security import verify_password


router = APIRouter(prefix="/users", tags=["users"])

DBConnection = Annotated[Connection, Depends(get_connection)]
CurrentUser = Annotated[dict, Depends(get_current_user)]


@router.get("/me", response_model=PublicUserSchema)
def get_user(current_user: CurrentUser):
    return current_user


@router.post("/", response_model=PublicUserSchema, status_code=201)
def create_user(user: CreateUserSchema, con: DBConnection):
    try:
        user = user.model_dump()
        return users.insert_user(con, user)
    except users.UserAlreadyExists as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@router.put("/{user_id}", response_model=PublicUserSchema)
def update_user(
    user_id: int, user: UpdateUserSchema, con: DBConnection, current_user: CurrentUser
):
    if current_user["id"] != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not enough permission"
        )

    try:
        user = user.model_dump()
        return users.update_user(con, user_id, user)
    except users.UserAlreadyExists as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@router.put("/{user_id}/password")
def update_user_password(
    user_id: int,
    user: UpdatePasswordUserSchema,
    con: DBConnection,
    current_user: CurrentUser,
):
    if current_user["id"] != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not enough permission"
        )

    if not verify_password(user.password, current_user["password"]):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Incorrect password"
        )

    try:
        user = user.model_dump()
        return users.update_user_password(con, user_id, user)
    except users.UserAlreadyExists as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
