from enum import Enum
from typing import Union


class Point:
    """
    Point class.
    """

    def __init__(
        self, coordinate_x: Union[int, float], coordinate_y: Union[int, float]
    ) -> None:
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y

    def get_coordinates(self) -> tuple[Union[int, float], Union[int, float]]:
        """
        Method gets point coordinates.

        Returns:
            coordinates
        """
        return self.coordinate_x, self.coordinate_y


class Segment:
    """
    Segment class.
    """

    def __init__(self, point_x: Point, point_y: Point) -> None:
        self.point_x, self.point_y = point_x, point_y
        self.first_point, self.second_point = self.get_first_and_second_point(
            point_x=point_x, point_y=point_y
        )
        self.value = 0
        self.calculate_value(value=self.first_point.coordinate_x)

    def get_first_and_second_point(
        self, point_x: Point, point_y: Point
    ) -> tuple[Point, Point]:
        """
        Method returns points in ordering.

        Args:
            point_x: x first point
            point_y: second point

        Returns:
            ordering points
        """
        if point_x.coordinate_x <= point_y.coordinate_x:
            return point_x, point_y
        return point_y, point_x

    def calculate_value(self, value: Union[int, float]) -> None:
        """
        Method calculates value.

        Args:
            value: value

        Returns:
            `None`
        """
        x1, y1 = self.first_point.get_coordinates()
        x2, y2 = self.second_point.get_coordinates()
        try:
            self.value = y1 + (((y2 - y1) / (x2 - x1)) * (value - x1))
        except ZeroDivisionError:
            self.value = 0
            return

    def set_value(self, value: Union[int, float]) -> None:
        """
        Method sets new value.

        Args:
            value: new value

        Returns:
            `None`
        """
        self.value = value

    def __lt__(self, other: "Segment") -> bool:
        return self.value > other.value

    def __eq__(self, other: "Segment") -> bool:
        return self.value == other.value


class EventType(Enum):
    POINT_LEFT = 0
    POINT_RIGHT = 1
    INTERSECTION = 2


class Event:
    """
    Event class.
    """

    def __init__(self, point: Point, segments: list[Segment], type_: EventType) -> None:
        self.point: Point = point
        self.type = type_
        self.segments = segments
        self.value = point.coordinate_x

    def get_point_coordinate(self):
        return self.point.get_coordinates()

    def get_segment_by_index(self, index: int) -> Segment:
        """
        Method returns segment by index.

        Args:
            index: index

        Returns:
            segment
        """
        return self.segments[index]

    def __lt__(self, other: "Event") -> bool:
        return self.value < other.value
