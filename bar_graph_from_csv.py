"""Salvatore Rosa

Bar Graph From .csv File

To run in terminal:
>python bar_graph_from_csv.py --file_name 'test-data.csv' --multiple 20

Please note --file_name is required and --multiple is optional (default 10).
"""

import csv
from argparse import ArgumentParser
from typing import NamedTuple, List
from itertools import chain, count


class Column(NamedTuple):
    """Represents a column in a .csv file.

    Attributes:
        name -- the name of the column (example: year).
        data -- a list containing all values belonging to the column (example: [1980, 1960, ...]).
    """

    name: str
    data: List[str]


def get_columns(reader) -> List[Column]:
    """Add names and data to each column."""
    column_names = next(reader)  # The first row in the .csv file.
    columns = [Column(column_name, []) for column_name in column_names]
    for row in reader:
        for column, value in zip(columns, row):
            column.data.append(value)
    return columns


def get_parser() -> ArgumentParser:
    """Return configured parser for command line interaction."""
    parser = ArgumentParser(description="Create bar graph from .csv file.")
    parser.add_argument(
        "--file_name",
        action="store",
        type=str,
        dest="csv_file",
        help="Path to your .csv file.",
        required=True,
    )
    parser.add_argument(
        "--multiple",
        action="store",
        type=int,
        dest="multiple",
        help="The number multiples to display on the x-axis.",
        default=10,
    )
    return parser


def get_largest_end_point(multiple: int, columns: List[Column]) -> int:
    """Return the largest end point to calculate the highest multiple
    to display on the x-axis of the graph."""
    largest_value = get_largest_value(columns)
    modifier = multiple
    if largest_value % multiple != 0:
        modifier = modifier * 2
    return largest_value // multiple * multiple + modifier


def get_largest_value(columns: List[Column]) -> int:
    """Return the largest value of all columns."""
    return max(map(int, list(chain.from_iterable([column.data for column in columns]))))


def get_smallest_end_point(multiple: int, columns: List[Column]) -> int:
    """Return the smallest end point to calculate the smallest multiple
    to display on the x-axis of the graph."""
    smallest_value = get_smallest_value(columns)
    return smallest_value - smallest_value % multiple


def get_smallest_value(columns: List[Column]) -> int:
    """Return the smallest value of all columns."""
    return min(map(int, list(chain.from_iterable([column.data for column in columns]))))


def get_left_margin_space(column: Column) -> int:
    """Return the length the left margin should be
    based off the longest value in the label column.
    """
    return max(map(len, column.data + [column.name]))


def draw_bar_graph(
    multiple: int, columns: List[Column], y_label_column: Column
) -> None:
    """Draw the bar graph to the terminal based off the data from the .csv file.
    Currently, values that are between two multiples will have a bar
    up to their midpoint.
    """
    # Get the multiples that will display on the x-axis of the graph.
    x_axis_values = [
        str(i)
        for i in range(
            get_smallest_end_point(multiple, columns),
            get_largest_end_point(multiple, columns),
            multiple,
        )
    ]
    offset = 8
    locations: List[int] = []
    draw_x_axis_labels(y_label_column, x_axis_values, offset, locations)
    print(Y_LABEL_COLUMN.name)
    for index in range(len(Y_LABEL_COLUMN.data)):
        print(Y_LABEL_COLUMN.data[index])
        for column in COLUMNS:
            if column.data[index] in x_axis_values:
                draw_bar_to_point_of_value(locations, x_axis_values, column, index)
            else:
                draw_bar_to_midpoint_of_two_values(
                    locations, x_axis_values, column, index, offset
                )


def draw_x_axis_labels(
    y_label_column: Column, x_axis_values: List[str], offset: int, locations: List[int]
) -> None:
    """Draw all the values of the x axis."""
    previous_value_length = 0
    left_margin = get_left_margin_space(y_label_column)
    x_axis_label = " " * left_margin
    for value, x in zip(x_axis_values, count(0, offset)):
        locations.append(left_margin + previous_value_length + x)
        x_axis_label += value + " " * (offset)
        previous_value_length += len(value)
    print(x_axis_label)


def draw_bar_to_point_of_value(
    locations: List[int], x_axis_values: List[str], column: Column, index: int
) -> None:
    """Draw a bar to the exact point of a value."""
    print(
        "|" * locations[x_axis_values.index(column.data[index])]
        + f" {column.name} {column.data[index]}"
    )


def draw_bar_to_midpoint_of_two_values(
    locations: List[int],
    x_axis_values: List[str],
    column: Column,
    index: int,
    offset: int,
) -> None:
    """Draw a bar up to the midpoint of two values."""
    for x_axis_value in x_axis_values:
        if int(column.data[index]) < int(x_axis_value):
            print(
                "|" * (locations[x_axis_values.index(x_axis_value)] - offset // 2)
                + f" {column.name} {column.data[index]}"
            )
            break


if __name__ == "__main__":
    CONFIG = get_parser().parse_args()
    with open(CONFIG.csv_file, newline="") as file:
        READER = csv.reader(file, dialect="excel")
        COLUMNS = get_columns(READER)
        Y_LABEL_COLUMN = COLUMNS.pop(0)
        draw_bar_graph(CONFIG.multiple, COLUMNS, Y_LABEL_COLUMN)
