from http import HTTPStatus
from oracledb import Connection
from typing import Annotated

from database.core import get_connection
from fastapi import APIRouter, Depends, HTTPException
from schemas.subway import RouteResponse
from services.subway_route import find_subway_route, StationNotFound


router = APIRouter(prefix="/subway-route", tags=["subway-routes"])

DBConnection = Annotated[Connection, Depends(get_connection)]


@router.get("/", response_model=RouteResponse)
def get_subway_route(from_station: str, to_station: str, con: DBConnection):
    if from_station == to_station:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Invalid route request"
        )

    try:
        return find_subway_route(con, from_station, to_station)
    except StationNotFound as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
