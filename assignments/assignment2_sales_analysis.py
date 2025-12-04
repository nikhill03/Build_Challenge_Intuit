from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple
from collections import defaultdict


@dataclass(frozen=True)
class SalesRecord:
    """Shows a single row in the sales CSV file."""

    order_id: str
    date: str           # keeping as string (YYYY-MM-DD)
    region: str
    salesperson: str
    product: str
    units_sold: int
    unit_price: float

    @property
    def revenue(self) -> float:
        """Compute total revenue for this record."""
        return self.units_sold * self.unit_price


class SalesAnalyzer:
    """
    Analytical queries on the sales dataset.

    analyzer = SalesAnalyzer.from_csv("data/sample_sales_data.csv")
    total = analyzer.total_revenue()

    """

    def __init__(self, records: Iterable[SalesRecord]) -> None:
        # Convert iterable to a list to iterate multiple times
        self.records: List[SalesRecord] = list(records)


    @classmethod
    def from_csv(cls, path: str | Path) -> "SalesAnalyzer":
        """
        Load records from CSV file and create a SalesAnalyzer instance.
        """
        file_path = Path(path)
        with file_path.open(mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            records: List[SalesRecord] = []

            for row in reader:
                record = SalesRecord(
                    order_id=row["order_id"],
                    date=row["date"],
                    region=row["region"],
                    salesperson=row["salesperson"],
                    product=row["product"],
                    units_sold=int(row["units_sold"]),
                    unit_price=float(row["unit_price"]),
                )
                records.append(record)

        return cls(records)

    def total_revenue(self) -> float:
        """
        Computes total revenue across all records.
        """
        return sum(map(lambda r: r.revenue, self.records))

    def revenue_by_region(self) -> Dict[str, float]:
        """
        Group revenue by region.
        Returns a dict: {region: total_revenue}.
        """
        totals: Dict[str, float] = defaultdict(float)

        # Using a simple for-loop; could also be done with reduce.
        for r in self.records:
            totals[r.region] += r.revenue

        return dict(totals)

    def units_sold_by_product(self) -> Dict[str, int]:
        """
        Total units sold for each product.
        Returns a dict: {product: units_sold}.
        """
        totals: Dict[str, int] = defaultdict(int)

        for r in self.records:
            totals[r.product] += r.units_sold

        return dict(totals)

    def revenue_by_salesperson(self) -> Dict[str, float]:
        """
        Group revenue by salesperson.
        Returns a dict: {salesperson: total_revenue}.
        """
        totals: Dict[str, float] = defaultdict(float)

        for r in self.records:
            totals[r.salesperson] += r.revenue

        return dict(totals)

    def top_n_products_by_revenue(self, n: int) -> List[Tuple[str, float]]:
        """
        Return the top N products sorted by revenue (descending).

        Returns a list of (product, total_revenue) tuples.
        """
        revenue_per_product = self.units_sold_by_product()
        # Convert units_sold to revenue using an average unit price per product.
        # Here we compute average price per product in a functional style.

        # Map from product -> (total_units, total_revenue)
        product_stats: Dict[str, Tuple[int, float]] = defaultdict(lambda: (0, 0.0))

        for r in self.records:
            units, rev = product_stats[r.product]
            product_stats[r.product] = (units + r.units_sold, rev + r.revenue)

        # Total revenue per product:
        revenue_per_product = {
            product: stats[1] for product, stats in product_stats.items()
        }

        # Sort by revenue descending
        sorted_products = sorted(
            revenue_per_product.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        return sorted_products[:n]

    def average_order_value(self) -> float:
        """
        Compute the average revenue per order_id.

        Steps:
        - Group records by order_id.
        - Sum revenue inside each group.
        - Average over number of orders.
        """
        # order_id -> total revenue for that order
        revenue_per_order: Dict[str, float] = defaultdict(float)

        for r in self.records:
            revenue_per_order[r.order_id] += r.revenue

        if not revenue_per_order:
            return 0.0

        total_orders = len(revenue_per_order)
        total_revenue = sum(revenue_per_order.values())
        return total_revenue / total_orders


def pretty_print_dict(title: str, data: Dict[str, float | int]) -> None:
    """
    Formats dictionary outputs for the console.
    """
    print(f"\n=== {title} ===")
    for key, value in data.items():
        print(f"{key:15} -> {value:.2f}" if isinstance(value, float) else f"{key:15} -> {value}")


def main() -> None:
    """
    Main entry point when running this file directly.

    Reads the sample CSV and prints:
    - Total revenue
    - Revenue by region
    - Units sold by product
    - Revenue by salesperson
    - Top 3 products by revenue
    - Average order value
    """
    default_csv = Path(__file__).parent.parent / "data" / "sample_sales_data.csv"
    analyzer = SalesAnalyzer.from_csv(default_csv)

    print("Loaded records:", len(analyzer.records))

    total_rev = analyzer.total_revenue()
    print(f"\nTotal revenue: {total_rev:.2f}")

    pretty_print_dict("Revenue by region", analyzer.revenue_by_region())
    pretty_print_dict("Units sold by product", analyzer.units_sold_by_product())
    pretty_print_dict("Revenue by salesperson", analyzer.revenue_by_salesperson())

    top_products = analyzer.top_n_products_by_revenue(3)
    print("\n=== Top 3 products by revenue ===")
    for product, rev in top_products:
        print(f"{product:15} -> {rev:.2f}")

    avg_order_val = analyzer.average_order_value()
    print(f"\nAverage order value: {avg_order_val:.2f}")


if __name__ == "__main__":
    main()
