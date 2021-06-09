from io import BytesIO
from itertools import chain
from random import randint
from typing import Any, Union
from typing import Iterable

import matplotlib.pyplot as plt
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

from bentley_ottmann_api.bentley_ottmann import find_intersections
from bentley_ottmann_api.models import Lines, Boards, BentleyOttmannPoints
from bentley_ottmann_api.schemas import RandomBoard, LineOut


def commit_and_refresh_model_instance(
    session: Session, instance: Any, refresh: bool = True, commit: bool = True
) -> Any:
    """
    Function commits and refreshes model instance.

    Args:
        session: db session
        instance: instance to save
        refresh: refresh instance if `True` default: `True`
        commit: if `True` data will be saved in the database
                otherwise an object not saved in the database will be returned

    Returns:
        new created object in db
    """
    session.add(instance)
    if commit:
        session.commit()
    if refresh:
        session.refresh(instance=instance)
    return instance


def get_query_result_without_nested(
    result: Union[tuple, list], many: bool = False
) -> Any:
    """
    Function parsed query result.

    Args:
        result: db query result
        many: if `True` objects will be returned in the list otherwise
              single object

    Returns:
        parsed db query result
    """
    return list(chain(*result)) if many else result[0] if result else None


def get(db: Session, model: Any, many: bool = False, **query_data: Any) -> Any:
    """
    Function makes query without join.

    Args:
        db: session db
        model: model class
        query_data: query data
        many: if `True` all objects in the database will be returned
              otherwise one object will be returned

    Returns:
        objects or object from db
    """
    result = db.execute(select(model).filter_by(**query_data))  # type: ignore
    return get_query_result_without_nested(
        result=result.all() if many else result.one_or_none(), many=many
    )


def create(
    db: Session,
    model: Any,
    refresh: bool = True,
    commit: bool = True,
    **model_data: Any,
) -> Any:
    """
    Function inserts new record to database.

    Args:
        db: session db
        model: model class
        refresh: refresh instance if `True` default: `True`
        commit: if `True` data will be saved in the database
                otherwise an object not saved in the database will be returned
    Returns:
        new created object in db
    """
    instance_model = model(**model_data)
    return commit_and_refresh_model_instance(
        session=db, instance=instance_model, refresh=refresh, commit=commit
    )


def get_boards_by_name(db: Session, name: str) -> Boards:
    """
    Function returns boards by name.

    Args:
        db: database session
        name: boards name

    Returns:
        board if exists otherwise None
    """
    return get(db=db, model=Boards, name=name)


def get_all_boards(db: Session) -> list[Boards]:
    """
    Function returns all board.

    Args:
        db: database session

    Returns:
        all boards if exists otherwise empty list
    """
    return get(db=db, model=Boards, many=True)


def create_board(db: Session, name: str) -> Boards:
    """
    Function creates board.

    Args:
        db: database session
        name: board name

    Returns:
        new created instances
    """
    return create(db=db, model=Boards, name=name)


def create_line_and_add_to_bord(
    db: Session, point_x: list[float], point_y: list[float], board: Boards
) -> Lines:
    """
    Function creates new line and adds its to board.

    Args:
        db: database sessions
        point_x: coordinate point x
        point_y: coordinate point y
        board: board

    Returns:
        new line
    """
    line = create(db=db, model=Lines, point_x=point_x, point_y=point_y)
    board.lines.append(line)
    commit_and_refresh_model_instance(session=db, instance=board, refresh=False)
    return line


def _get_random_point(min_x: int, max_x: int, min_y: int, max_y: int) -> list[float]:
    """
    Functions returns random point.

    Args:
        min_x: min x
        max_x: max x
        min_y: min y
        max_y: max y

    Returns:
        random point
    """
    return [
        randint(min_x, max_x),
        randint(min_y, max_y),
    ]


def create_random_lines(
    db: Session, random_board_data: RandomBoard, board: Boards
) -> None:
    """
    Function creates random lines.

    Args:
        db: database session
        random_board_data: random board data
        board: board

    Returns:
        `None`
    """
    for _ in range(random_board_data.max_items):
        create_line_and_add_to_bord(
            db=db,
            point_x=_get_random_point(
                min_x=random_board_data.min_range_x,
                max_x=random_board_data.max_range_x,
                min_y=random_board_data.min_range_y,
                max_y=random_board_data.max_range_y,
            ),
            point_y=_get_random_point(
                min_x=random_board_data.min_range_x,
                max_x=random_board_data.max_range_x,
                min_y=random_board_data.min_range_y,
                max_y=random_board_data.max_range_y,
            ),
            board=board,
        )


def delete_lines(db: Session, lines: list[LineOut]) -> None:
    """
    Function deletes lines

    Args:
        db: database session
        lines: lines

    Returns:
        `None`
    """
    for line in lines:
        db.delete(instance=line)
        db.commit()


def delete_boards(db: Session, board: Boards) -> None:
    """
    Function deletes boards.

    Args:
        db: database session
        board: board

    Returns:
        `None`
    """
    delete_lines(lines=board.lines, db=db)
    db.delete(board)
    db.commit()


def draw_lines(lines: Iterable) -> plt:
    """
    Function draw lines.

    Args:
        lines: lines to draw

    Returns:
        image
    """
    plt.figure()
    plt.title("Lines")
    for x_point, y_point in lines:
        plt.plot([x_point[0], y_point[0]], [x_point[1], y_point[1]])
    return plt


def get_draw_response(plt_image: plt) -> StreamingResponse:
    """
    Method gets response from plt image.

    Args:
        plt_image: plt image

    Returns:

    """
    buf = BytesIO()
    plt_image.savefig(buf, format="png")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


def delete_old_intersection_points(db: Session, board: Boards) -> None:
    """
    Method deletes old intersection points.

    Args:
        db: db session
        board: board

    Returns:
        `None`
    """
    for point in board.bentley_ottmann_points:
        db.delete(point)
        db.commit()


def find_intersection_for_board(db: Session, board: Boards) -> None:
    """
    Method finds all intersections point for board.

    Args:
        db: db session
        board: board

    Returns:
        `None`
    """
    delete_old_intersection_points(db=db, board=board)
    points = find_intersections(
        lines=[(line.point_x, line.point_y) for line in board.lines]
    )
    for idx, point in enumerate(points, 1):
        create(
            db=db, model=BentleyOttmannPoints, point=point, board=board, name=f"P{idx}"
        )


def draw_lines_and_intersection_points(board: Boards) -> plt:
    """
    Method draws lines and intersection points.

    Args:
        board: board

    Returns:
        plt image
    """
    plt = draw_lines(lines=(line.get_coordinates() for line in board.lines))
    plt.title("Intersection Lines")
    for idx, point_instance in enumerate(board.bentley_ottmann_points, 1):
        x, y = point_instance.point[0], point_instance.point[1]
        plt.scatter(x, y, color="black")
        plt.text(x + 0.2, y, point_instance.name, verticalalignment="top")
    return plt
