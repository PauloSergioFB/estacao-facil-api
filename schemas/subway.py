from typing import List

from pydantic import BaseModel


class ShortStation(BaseModel):
    id: int
    name: str


class RouteStepEmbark(BaseModel):
    type: str
    line: str
    direction: str
    from_station: ShortStation
    to_station: ShortStation
    via: List[ShortStation]


class RouteStepTransfer(BaseModel):
    type: str
    at: ShortStation
    from_line: str
    to_line: str


class RouteResponse(BaseModel):
    steps: List[RouteStepEmbark | RouteStepTransfer]
    estimated_duration: int
