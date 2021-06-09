from typing import Any

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

from bentley_ottmann_api.crud import (
    get_boards_by_name,
    create_board,
    get_all_boards,
    create_line_and_add_to_bord,
    create_random_lines,
    delete_lines,
    delete_boards,
    draw_lines,
    get_draw_response,
    find_intersection_for_board,
    draw_lines_and_intersection_points,
)
from bentley_ottmann_api.dependencies import get_db, MainSession
from bentley_ottmann_api.models import Boards
from bentley_ottmann_api.schemas import (
    LineIn,
    LineOut,
    BoardOut,
    BoardIn,
    BoardOutAll,
    RandomBoard,
    Point,
)

app = FastAPI(title="ComputationalLineAPI")


@app.on_event("startup")
async def startup_event() -> None:
    boards_name = ["initial_board01", "initial_board02", "initial_board03"]
    db = MainSession()
    lines = {
        "initial_board01": [
            [(0.8, 6.1), (11.72, 9.32)],
            [(6.84, 3.56), (15.06, 8.38)],
            [(3.5, 8.17), (10.44, 4.08)],
            [(13.32, 4.22), (2.42, 12.67)],
        ],
        "initial_board02": [
            [(0.8, 6.1), (11.72, 9.32)],
            [(6.84, 3.56), (15.06, 8.38)],
            [(3.5, 8.17), (10.44, 4.08)],
            [(13.32, 4.22), (2.42, 12.67)],
            [(5.39, 5.68), (8.39, 11.23)],
            [(9.5, 3.91), (11, 10.06)],
        ],
        "initial_board03": [
            [(2.0681655529586, 6.7721029389621), (3.8750905945826, 4.7795349136096)],
            [(3.7637048043455, 5.0765636875751), (2.5013325149917, 2.9107288774094)],
            [(2.4146991225851, 3.1706290546293), (4.4196433468528, 1.6731089858861)],
            [(4.1844955674634, 1.7597423782927), (7.1547833071193, 2.8612240817484)],
            [(6.870130732069, 2.9354812752398), (8.887451155252, 1.3637040130053)],
            [(8.5904223812864, 1.4008326097509), (12.7364490178894, 5.1384446821513)],
            [(12.7735776146351, 4.8785445049314), (11.1399193578244, 8.7399185664841)],
            [(11.4369481317899, 8.5666517816708), (7.0681499147127, 9.6557572862113)],
            [(7.3032976941021, 9.7300144797027), (5.2736010720039, 8.3067516044509)],
            [(5.5582536470543, 8.3686325990271), (3.1696472564143, 9.0369473404497)],
            [(3.5161808260408, 9.160709329602), (2.092917950789, 6.5493313584879)],
            [(5.0434037721806, 9.2448674822256), (2.0347498158874, 5.3649291223001)],
            [(3.2599935084955, 2.1656817027123), (6.47285474689, 9.7758064156891)],
        ],
    }
    for board_name in boards_name:
        if board := get_boards_by_name(db=db, name=board_name):
            delete_boards(db=db, board=board)
        new_board = create_board(db=db, name=board_name)
        for point_x, point_y in lines[board_name]:
            create_line_and_add_to_bord(
                db=db, point_x=point_x, point_y=point_y, board=new_board
            )


def get_bord_or_http404(db: Session, name: str) -> Boards:
    """
    Function gets boards or raise HTTP exception 404.

    Args:
        db: database session
        name: board name

    Returns:
        boards if exists
    """
    if not (board := get_boards_by_name(db=db, name=name)):
        raise HTTPException(detail="Not found board object.", status_code=404)
    return board


@app.post(path="/boards/", status_code=201, response_model=BoardOut, tags=["board"])
async def create_boards(board_in: BoardIn, db: Session = Depends(get_db)) -> Any:
    """
    Endpoint creates empty boards.
    """
    if get_boards_by_name(name=board_in.name, db=db):
        raise HTTPException(
            status_code=400, detail="Board about this name already exists."
        )
    return create_board(db=db, name=board_in.name)


@app.get(
    path="/boards/", status_code=200, response_model=list[BoardOutAll], tags=["board"]
)
async def read_boards(db: Session = Depends(get_db)) -> list[Any]:
    """
    Endpoint read all boards.
    """
    return get_all_boards(db=db)


@app.post(
    path="/boards/{name}/line/", status_code=201, response_model=LineOut, tags=["line"]
)
async def create_line(name: str, line_in: LineIn, db: Session = Depends(get_db)) -> Any:
    """
    Endpoint creates line, and adds its to board.
    """
    return create_line_and_add_to_bord(
        db=db,
        point_x=line_in.point_x,
        point_y=line_in.point_y,
        board=get_bord_or_http404(db=db, name=name),
    )


@app.post(path="/boards/{name}/draw/", status_code=200, tags=["draw"])
async def draw(name: str, db: Session = Depends(get_db)) -> StreamingResponse:
    """
    Endpoint draws all lines in boards.
    """
    board = get_bord_or_http404(db=db, name=name)
    return get_draw_response(
        plt_image=draw_lines(lines=(line.get_coordinates() for line in board.lines))
    )


@app.get(
    path="/boards/{name}/", status_code=200, response_model=BoardOut, tags=["board"]
)
async def retrieve_board(name: str, db: Session = Depends(get_db)) -> Any:
    """
    Endpoint shows all coordinates lines.
    """
    return get_bord_or_http404(db=db, name=name)


@app.post(path="/boards/{name}/generate-random-lines/", status_code=200, tags=["line"])
async def generate_random_lines(
    random_board_data: RandomBoard, name: str, db: Session = Depends(get_db)
) -> None:
    """
    Endpoint generates random lines for boards.
    """
    return create_random_lines(
        random_board_data=random_board_data,
        db=db,
        board=get_bord_or_http404(db=db, name=name),
    )


@app.delete("/boards/{name}/clear-lines/", status_code=204, tags=["line"])
async def clear_lines(name: str, db: Session = Depends(get_db)) -> None:
    """
    Endpoint clears all lines from board.
    """
    board = get_bord_or_http404(db=db, name=name)
    delete_lines(lines=board.lines, db=db)


@app.delete("/boards/{name}/", status_code=204, tags=["board"])
async def delete_board(name: str, db: Session = Depends(get_db)):
    """
    Endpoint deletes all boards with all lines.
    """
    delete_boards(db=db, board=get_bord_or_http404(db=db, name=name))


@app.post(
    "/boards/{name}/intersection-points/", status_code=201, tags=["intersection points"]
)
async def find_intersection_points(name: str, db: Session = Depends(get_db)) -> None:
    """
    Endpoint finds all intersections points.
    """
    find_intersection_for_board(db=db, board=get_bord_or_http404(db=db, name=name))


@app.get(
    "/boards/{name}/intersection-points/",
    status_code=200,
    response_model=list[Point],
    tags=["intersection points"],
)
async def get_intersection_points(name: str, db: Session = Depends(get_db)) -> Any:
    """
    Endpoint gets all intersections points.
    """
    board = get_bord_or_http404(db=db, name=name)
    return board.bentley_ottmann_points


@app.post("/boards/{name}/intersection-points/draw/", status_code=201, tags=["draw"])
async def draw_intersection_points(
    name: str, db: Session = Depends(get_db)
) -> StreamingResponse:
    """
    Endpoint draws intersection points.
    """
    return get_draw_response(
        plt_image=draw_lines_and_intersection_points(
            board=get_bord_or_http404(db=db, name=name)
        )
    )
