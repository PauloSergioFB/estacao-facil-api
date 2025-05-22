from pydantic import BaseModel

from .users import PublicUserSchema


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    user: PublicUserSchema

