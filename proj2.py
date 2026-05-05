# Brayden Morgan, CSC 202-13
from __future__ import annotations
import sys
import csv
from typing import *
from dataclasses import dataclass
import unittest
import math

sys.setrecursionlimit(10_000)


EXPECTED_HEADER: list[str] = [
    "country",
    "year",
    "electricity_and_heat_co2_emissions",
    "electricity_and_heat_co2_emissions_per_capita",
    "energy_co2_emissions",
    "energy_co2_emissions_per_capita",
    "total_co2_emissions_excluding_lucf",
    "total_co2_emissions_excluding_lucf_per_capita",
]

NUMERIC_FIELDS: list[str] = [
    "year",
    "electricity_and_heat_co2_emissions",
    "electricity_and_heat_co2_emissions_per_capita",
    "energy_co2_emissions",
    "energy_co2_emissions_per_capita",
    "total_co2_emissions_excluding_lucf",
    "total_co2_emissions_excluding_lucf_per_capita",
]


@dataclass(frozen=True)
class Row:
    """a single co2 emissions data row from the csv file"""

    country: str
    year: int
    electricity_and_heat_co2_emissions: Optional[float]
    electricity_and_heat_co2_emissions_per_capita: Optional[float]
    energy_co2_emissions: Optional[float]
    energy_co2_emissions_per_capita: Optional[float]
    total_co2_emissions_excluding_lucf: Optional[float]
    total_co2_emissions_excluding_lucf_per_capita: Optional[float]


@dataclass(frozen=True)
class Node:
    """a linked-list node storing one row and the rest of the list"""

    value: Row
    next: Optional[Node]


def parse_optional_float(text: str) -> Optional[float]:
    """convert a csv field to a float using None for missing data"""
    if text == "":
        return None
    return float(text)


def parse_row(fields: list[str]) -> Row:
    """convert a list of csv string fields into a row"""
    if len(fields) != len(EXPECTED_HEADER):
        raise ValueError("expected {} fields, got {}: {}".format(
            len(EXPECTED_HEADER), len(fields), fields
        ))

    return Row(
        country=fields[0],
        year=int(fields[1]),
        electricity_and_heat_co2_emissions=parse_optional_float(fields[2]),
        electricity_and_heat_co2_emissions_per_capita=parse_optional_float(fields[3]),
        energy_co2_emissions=parse_optional_float(fields[4]),
        energy_co2_emissions_per_capita=parse_optional_float(fields[5]),
        total_co2_emissions_excluding_lucf=parse_optional_float(fields[6]),
        total_co2_emissions_excluding_lucf_per_capita=parse_optional_float(fields[7]),
    )


def build_list(rows: list[Row], index: int) -> Optional[Node]:
    """recursively build linked list from rows starting at index"""
    if index >= len(rows):
        return None
    return Node(rows[index], build_list(rows, index + 1))


def read_csv_lines(filename: str) -> Optional[Node]:
    """read an emissions csv file, return its rows as linked list"""
    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile)
        try:
            header = next(reader)
        except StopIteration:
            raise ValueError("missing header row")

        if header != EXPECTED_HEADER:
            raise ValueError("unexpected first line: got: {}".format(header))

        rows: list[Row] = []
        for line in reader:
            rows.append(parse_row(line))

    return build_list(rows, 0)


def listlen(data: Optional[Node]) -> int:
    """return the number of nodes in a linked list of rows"""
    if data is None:
        return 0
    return 1 + listlen(data.next)


def get_field(row: Row, field_name: str) -> Union[str, int, float, None]:
    """return the value of a row field by its csv field name"""
    if field_name == "country":
        return row.country
    if field_name == "year":
        return row.year
    if field_name == "electricity_and_heat_co2_emissions":
        return row.electricity_and_heat_co2_emissions
    if field_name == "electricity_and_heat_co2_emissions_per_capita":
        return row.electricity_and_heat_co2_emissions_per_capita
    if field_name == "energy_co2_emissions":
        return row.energy_co2_emissions
    if field_name == "energy_co2_emissions_per_capita":
        return row.energy_co2_emissions_per_capita
    if field_name == "total_co2_emissions_excluding_lucf":
        return row.total_co2_emissions_excluding_lucf
    if field_name == "total_co2_emissions_excluding_lucf_per_capita":
        return row.total_co2_emissions_excluding_lucf_per_capita
    raise ValueError("unknown field name: {}".format(field_name))


def is_valid_filter(field_name: str, comparison: str) -> bool:
    """return whether a field/comparison pair is allowed for filtering"""
    if field_name == "country":
        return comparison == "equal"
    if field_name in NUMERIC_FIELDS:
        return comparison in ["less_than", "greater_than", "equal"]
    return False


def row_matches(row: Row, field_name: str, comparison: str,
                value: Union[str, float, int]) -> bool:
    """return whether one row satisfies a filter comparison"""
    actual = get_field(row, field_name)

    if actual is None:
        return False

    if comparison == "equal":
        return actual == value
    if comparison == "less_than":
        return actual < value
    if comparison == "greater_than":
        return actual > value

    raise ValueError("unknown comparison: {}".format(comparison))


def filter_rows(data: Optional[Node], field_name: str, comparison: str,
                value: Union[str, float, int]) -> Optional[Node]:
    """return a linked list of rows matching requested filter"""
    if not is_valid_filter(field_name, comparison):
        raise ValueError("invalid filter: {} {}".format(field_name, comparison))

    if data is None:
        return None

    filtered_rest = filter_rows(data.next, field_name, comparison, value)
    if row_matches(data.value, field_name, comparison, value):
        return Node(data.value, filtered_rest)
    return filtered_rest
