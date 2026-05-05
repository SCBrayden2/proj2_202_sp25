# Brayden Morgan, CSC 202-13
import unittest
from proj2 import (
    Row,
    Node,
    parse_optional_float,
    parse_row,
    read_csv_lines,
    listlen,
    filter_rows,
)


class TestProject2(unittest.TestCase):
    def test_parse_optional_float_missing(self) -> None:
        self.assertIsNone(parse_optional_float(""))

    def test_parse_optional_float_present(self) -> None:
        self.assertEqual(parse_optional_float("12.5"), 12.5)

    def test_parse_row(self) -> None:
        row = parse_row([
            "USA", "1990", "100.0", "1.5",
            "200.0", "2.5", "300.0", "3.5"
        ])
        self.assertEqual(row.country, "USA")
        self.assertEqual(row.year, 1990)
        self.assertEqual(row.energy_co2_emissions, 200.0)

    def test_parse_row_missing_numeric(self) -> None:
        row = parse_row([
            "Brazil", "2019", "40.0", "", "60.0", "", "80.0", ""
        ])
        self.assertIsNone(row.electricity_and_heat_co2_emissions_per_capita)
        self.assertIsNone(row.energy_co2_emissions_per_capita)
        self.assertIsNone(row.total_co2_emissions_excluding_lucf_per_capita)

    def test_node_and_listlen(self) -> None:
        row1 = Row("A", 2000, None, None, None, None, None, None)
        row2 = Row("B", 2001, None, None, None, None, None, None)
        data = Node(row1, Node(row2, None))
        self.assertEqual(listlen(data), 2)
        self.assertEqual(listlen(None), 0)

    def test_read_csv_lines(self) -> None:
        data = read_csv_lines("sample.csv")
        self.assertEqual(listlen(data), 6)
        self.assertIsNotNone(data)
        if data is not None:
            self.assertEqual(data.value.country, "USA")
            self.assertEqual(data.value.year, 2020)

    def test_filter_country_equal(self) -> None:
        data = read_csv_lines("sample.csv")
        filtered = filter_rows(data, "country", "equal", "USA")
        self.assertEqual(listlen(filtered), 2)
        self.assertIsNotNone(filtered)
        if filtered is not None:
            self.assertEqual(filtered.value.country, "USA")

    def test_filter_numeric_greater_than(self) -> None:
        data = read_csv_lines("sample.csv")
        filtered = filter_rows(data, "energy_co2_emissions", "greater_than", 75.0)
        self.assertEqual(listlen(filtered), 3)

    def test_filter_numeric_less_than_skips_missing(self) -> None:
        data = read_csv_lines("sample.csv")
        filtered = filter_rows(
            data,
            "electricity_and_heat_co2_emissions",
            "less_than",
            60.0,
        )
        self.assertEqual(listlen(filtered), 3)

    def test_filter_year_equal(self) -> None:
        data = read_csv_lines("sample.csv")
        filtered = filter_rows(data, "year", "equal", 2020)
        self.assertEqual(listlen(filtered), 3)

    def test_invalid_country_comparison(self) -> None:
        data = read_csv_lines("sample.csv")
        with self.assertRaises(ValueError):
            filter_rows(data, "country", "greater_than", "Mexico")

    def test_invalid_field(self) -> None:
        data = read_csv_lines("sample.csv")
        with self.assertRaises(ValueError):
            filter_rows(data, "not_a_field", "equal", 0)


if __name__ == "__main__":
    unittest.main()

