from http import HTTPStatus
from oracledb import Connection
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from database import users
from database.core import get_connection
from schemas.security import TokenSchema
from services.security import create_access_token, get_current_user, verify_password


router = APIRouter(prefix="/auth", tags=["auth"])

DBConnection = Annotated[Connection, Depends(get_connection)]
CurrentUser = Annotated[dict, Depends(get_current_user)]
OAuthForm = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/token", response_model=TokenSchema)
def login_for_access_token(con: DBConnection, form_data: OAuthForm):
    user = users.get_user_by_email(con, form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Incorrect email or password"
        )

    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "Bearer", "user": user}

