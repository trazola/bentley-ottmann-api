from typing import Union

from bentley_ottmann_api.bentley_ottmann.data_structures import AVLTree, PriorityQueue
from bentley_ottmann_api.bentley_ottmann.geometry import (
    Point,
    Segment,
    EventType,
    Event,
)


class BentleyOttmann:
    """
    Bentley Ottman algorithm.
    """

    def __init__(self, segments: list[Segment]) -> None:
        self.priority_queue = self.get_priority_queue_with_data(segments=segments)
        self.tree_set = AVLTree()
        self.output = set()

    def get_priority_queue_with_data(self, segments: list[Segment]) -> PriorityQueue:
        """
        Method creates initial queue.
        
        Args:
            segments: segments 

        Returns:
            queue with data
        """
        queue = PriorityQueue()
        for segment in segments:
            queue.enqueue(
                data=Event(
                    point=segment.first_point,
                    segments=[segment],
                    type_=EventType.POINT_LEFT,
                )
            )
            queue.enqueue(
                data=Event(
                    point=segment.second_point,
                    segments=[segment],
                    type_=EventType.POINT_RIGHT,
                )
            )
        return queue

    def recalculate(self, value: Union[int, float]) -> None:
        """
        Method recalculates segment's values in tree.
        
        Args:
            value: new value 

        Returns:
            `None`
        """
        for segment in self.tree_set.inorder(node=self.tree_set.root_node):
            segment.calculate_value(value=value)

    def intersection(
        self, first_segment: Segment, second_segment: Segment, value: Union[int, float]
    ) -> bool:
        """
        Method checks id segments intersections.
        
        Args:
            first_segment: first segment
            second_segment: second segment
            value: event value

        Returns:
            `True` if two segments intersections otherwise `False`
        """
        x1, y1 = first_segment.first_point.get_coordinates()
        x2, y2 = first_segment.second_point.get_coordinates()
        x3, y3 = second_segment.first_point.get_coordinates()
        x4, y4 = second_segment.second_point.get_coordinates()
        if r := ((x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3)):
            t = ((x3 - x1) * (y4 - y3) - (y3 - y1) * (x4 - x3)) / r
            u = ((x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)) / r
            if t >= 0 and t <= 1 and u >= 0 and u <= 1:
                x_c = x1 + t * (x2 - x1)
                y_c = y1 + t * (y2 - y1)
                if x_c > value:
                    self.priority_queue.enqueue(
                        data=Event(
                            point=Point(coordinate_x=x_c, coordinate_y=y_c),
                            segments=[first_segment, second_segment],
                            type_=EventType.INTERSECTION,
                        )
                    )
                    return True
        return False

    def remove_duplicate(self, first_segment: Segment, second_segment: Segment) -> None:
        """
        Method removes duplicates intersections point from queue.

        Args:
            first_segment: first segment
            second_segment: second segment

        Returns:
            `None`
        """
        for event in self.priority_queue:
            if event.type == EventType.INTERSECTION:
                event_first_seg = event.get_segment_by_index(index=0)
                event_second_seg = event.get_segment_by_index(index=1)
                if (
                    event_first_seg == first_segment
                    and event_second_seg == second_segment
                ) or (
                    event_first_seg == second_segment
                    and event_second_seg == first_segment
                ):
                    self.priority_queue.remove_by_object_id(data=event)

    def find_intersections_left_point(self, event: Event) -> None:
        """
        Method finds intersections for left points.
        
        Args:
            event: event

        Returns:
            `None`
        """
        for segment in event.segments:
            self.recalculate(value=event.value)
            self.tree_set.insert(key=segment)
            if lower := self.tree_set.lower(key=segment):
                self.intersection(
                    first_segment=lower, second_segment=segment, value=event.value
                )
            if higher := self.tree_set.higher(key=segment):
                self.intersection(
                    first_segment=higher, second_segment=segment, value=event.value
                )
            lower = self.tree_set.lower(key=segment)
            higher = self.tree_set.higher(key=segment)
            if lower and higher:
                self.remove_duplicate(first_segment=lower, second_segment=higher)

    def find_intersections_right_point(self, event: Event) -> None:
        """
        Method finds intersections for right points.

        Args:
            event: event

        Returns:
            `None`
        """
        for segment in event.segments:
            lower, higher = (
                self.tree_set.lower(key=segment),
                self.tree_set.higher(key=segment),
            )
            if lower and higher:
                self.intersection(
                    first_segment=lower, second_segment=higher, value=event.value
                )
            self.tree_set.remove_key(key=segment)

    def swap(self, first_segment: Segment, second_segment: Segment) -> None:
        """
        Method swap segments value in tree.
        
        Args:
            first_segment: first segment
            second_segment: second segment

        Returns:
            `None`
        """
        self.tree_set.remove_key(first_segment)
        self.tree_set.remove_key(second_segment)
        first_segment.value, second_segment.value = (
            second_segment.value,
            first_segment.value,
        )
        self.tree_set.insert(first_segment)
        self.tree_set.insert(second_segment)

    def find_intersections_point_intersections(self, event: Event) -> None:
        """
        Method adds intersections for output.

        Args:
            event: event

        Returns:
            `None`
        """
        first_segment, second_segment = event.segments[0], event.segments[1]
        self.swap(first_segment=first_segment, second_segment=second_segment)
        if first_segment.value < second_segment.value:
            if higher_first := self.tree_set.higher(key=first_segment):
                self.intersection(
                    first_segment=higher_first,
                    second_segment=first_segment,
                    value=event.value,
                )
                self.remove_duplicate(
                    first_segment=higher_first, second_segment=second_segment
                )
            if lower_second := self.tree_set.lower(key=second_segment):
                self.intersection(
                    first_segment=lower_second,
                    second_segment=second_segment,
                    value=event.value,
                )
                self.remove_duplicate(
                    first_segment=lower_second, second_segment=first_segment
                )
        else:
            if higher_second := self.tree_set.higher(key=second_segment):
                self.intersection(
                    first_segment=higher_second,
                    second_segment=second_segment,
                    value=event.value,
                )
                self.remove_duplicate(
                    first_segment=higher_second, second_segment=first_segment
                )
            if lower_first := self.tree_set.lower(key=first_segment):
                self.intersection(
                    first_segment=lower_first,
                    second_segment=first_segment,
                    value=event.value,
                )
                self.remove_duplicate(
                    first_segment=lower_first, second_segment=second_segment
                )
        self.output.add(event.point.get_coordinates())

    def find_intersections(self) -> list[tuple[Union[int, float], Union[int, float]]]:
        """
        Method finds intersections.

        Returns:
            Intersections point if exists.
        """
        intersections = {
            EventType.POINT_LEFT: self.find_intersections_left_point,
            EventType.POINT_RIGHT: self.find_intersections_right_point,
            EventType.INTERSECTION: self.find_intersections_point_intersections,
        }
        while self.priority_queue:
            event = self.priority_queue.dequeue()
            intersections.get(event.type)(event=event)
        return sorted(self.output)
