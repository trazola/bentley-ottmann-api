from sqlalchemy import Column, Integer, Float, String, Table, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import relationship


@as_declarative()
class Model:
    """
    Base model for all models.
    """

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)


board_line_association = Table(
    "board_line_association",
    Model.metadata,
    Column("line_id", Integer, ForeignKey("lines.id")),
    Column("board_id", Integer, ForeignKey("boards.id")),
)


class Lines(Model):
    __tablename__ = "lines"
    point_x = Column(postgresql.ARRAY(Float))
    point_y = Column(postgresql.ARRAY(Float))
    boards = relationship(
        "Boards", secondary=board_line_association, back_populates="lines"
    )

    def get_coordinates(self):
        return [self.point_x, self.point_y]


class Boards(Model):
    __tablename__ = "boards"
    name = Column(String, unique=True)
    lines = relationship(
        "Lines", secondary=board_line_association, back_populates="boards"
    )
    bentley_ottmann_points = relationship(
        "BentleyOttmannPoints",
        back_populates="board",
        cascade="all, delete",
        passive_deletes=True,
    )


class BentleyOttmannPoints(Model):
    __tablename__ = "bentlet_ottmann_points"
    point = Column(postgresql.ARRAY(Float))
    board_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE"))
    board = relationship("Boards", back_populates="bentley_ottmann_points")
    name = Column(String)
