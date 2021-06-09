from bentley_ottmann_api.bentley_ottmann.algorithm import BentleyOttmann, Segment, Point


def find_intersections(lines: list) -> list:
    """
    Function finds all intersection points for lines..

    Args:
        lines: lines

    Returns:
        intersections points if exists.
    """
    segments = []
    for point_x, point_y in lines:
        segments.append(
            Segment(
                point_x=Point(coordinate_x=point_x[0], coordinate_y=point_x[1]),
                point_y=Point(coordinate_x=point_y[0], coordinate_y=point_y[1]),
            )
        )
    bentley_ottmann = BentleyOttmann(segments=segments)
    return bentley_ottmann.find_intersections()
