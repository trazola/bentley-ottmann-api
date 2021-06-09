from pydantic import BaseModel, Field, PositiveInt


class BaseLine(BaseModel):
    point_x: list[float] = Field(..., min_items=2, max_items=2)
    point_y: list[float] = Field(..., min_items=2, max_items=2)


class LineIn(BaseLine):
    pass


class LineOut(BaseLine):
    id: int

    class Config:
        orm_mode = True


class BaseBoard(BaseModel):
    name: str


class BoardIn(BaseBoard):
    pass


class BoardOut(BaseBoard):
    lines: list[LineOut] = []

    class Config:
        orm_mode = True


class BoardOutAll(BaseBoard):
    class Config:
        orm_mode = True


class RandomBoard(BaseModel):
    max_range_x: int = 10
    min_range_x: int = 1
    max_range_y: int = 3
    min_range_y: int = 1
    max_items: PositiveInt = 20


class Point(BaseBoard):
    point: list[float] = Field(..., min_items=2, max_items=2)
    name: str

    class Config:
        orm_mode = True
