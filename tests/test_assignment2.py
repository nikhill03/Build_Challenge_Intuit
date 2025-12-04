import csv
import tempfile
import unittest
from pathlib import Path

from assignments.assignment2_sales_analysis import (
    SalesAnalyzer,
    SalesRecord,
)


class TestSalesAnalyzerInMemory(unittest.TestCase):
    """
    Tests that use in-memory SalesRecord instances (no file IO).
    """

    def setUp(self) -> None:
        self.records = [
            SalesRecord("1", "2025-01-01", "APAC", "Alice", "Laptop", 5, 900.0),
            SalesRecord("2", "2025-01-02", "EMEA", "Bob", "Laptop", 3, 950.0),
            SalesRecord("3", "2025-01-03", "APAC", "Alice", "Mouse", 10, 20.0),
            SalesRecord("4", "2025-01-04", "NA", "Charlie", "Laptop", 2, 1000.0),
        ]
        self.analyzer = SalesAnalyzer(self.records)

    def test_total_revenue(self) -> None:
        expected = sum(r.revenue for r in self.records)
        self.assertAlmostEqual(self.analyzer.total_revenue(), expected)

    def test_revenue_by_region(self) -> None:
        result = self.analyzer.revenue_by_region()
        # Check a few regions explicitly
        apac_expected = sum(r.revenue for r in self.records if r.region == "APAC")
        self.assertAlmostEqual(result["APAC"], apac_expected)

    def test_units_sold_by_product(self) -> None:
        result = self.analyzer.units_sold_by_product()
        self.assertEqual(result["Laptop"], 5 + 3 + 2)
        self.assertEqual(result["Mouse"], 10)

    def test_revenue_by_salesperson(self) -> None:
        result = self.analyzer.revenue_by_salesperson()
        alice_expected = sum(r.revenue for r in self.records if r.salesperson == "Alice")
        self.assertAlmostEqual(result["Alice"], alice_expected)

    def test_top_n_products_by_revenue(self) -> None:
        top_1 = self.analyzer.top_n_products_by_revenue(1)
        # The product with highest revenue should be "Laptop"
        self.assertEqual(top_1[0][0], "Laptop")

    def test_average_order_value(self) -> None:
        # Each order_id is unique in this dataset, so average_order_value
        # should equal total_revenue / number_of_records
        total_rev = self.analyzer.total_revenue()
        self.assertAlmostEqual(
            self.analyzer.average_order_value(),
            total_rev / len(self.records),
        )


class TestSalesAnalyzerFromCSV(unittest.TestCase):
    """
    Tests that verify the from_csv class method using a temporary file.
    """

    def test_from_csv_reads_records(self) -> None:
        # Create a temporary CSV file
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test_sales.csv"
            fieldnames = [
                "order_id",
                "date",
                "region",
                "salesperson",
                "product",
                "units_sold",
                "unit_price",
            ]
            rows = [
                {
                    "order_id": "1",
                    "date": "2025-01-01",
                    "region": "APAC",
                    "salesperson": "Alice",
                    "product": "Laptop",
                    "units_sold": "5",
                    "unit_price": "900.0",
                },
                {
                    "order_id": "2",
                    "date": "2025-01-02",
                    "region": "EMEA",
                    "salesperson": "Bob",
                    "product": "Mouse",
                    "units_sold": "10",
                    "unit_price": "20.0",
                },
            ]

            with path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            analyzer = SalesAnalyzer.from_csv(path)
            self.assertEqual(len(analyzer.records), 2)
            self.assertEqual(analyzer.records[0].region, "APAC")
            self.assertEqual(analyzer.records[1].product, "Mouse")


if __name__ == "__main__":
    unittest.main()
