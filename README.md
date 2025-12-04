# 🚀 Build Challenge – Python Implementation

### 📂 Project Structure

```bash
build_challenge_python/
├── assignments/
│   ├── assignment1_producer_consumer.py
│   └── assignment2_sales_analysis.py
├── tests/
│   ├── test_assignment1.py
│   └── test_assignment2.py
├── data/
│   └── sample_sales_data.csv
└── README.md

```

---

This project contains two core programming assignments focused on ** producer-consumer pattern** and **data analysis using appropriate API on CSV** in Python 👨‍💻.  
It demonstrates clean code design, multithreading, CSV ingestion, functional aggregation, and complete unit testing.

---

## 📌 Assignments Summary

| Assignment       | Description                                                | Core Concepts                             |
| ---------------- | ---------------------------------------------------------- | ----------------------------------------- |
| **Assignment 1** | Producer–Consumer Queue with Thread Synchronization        | `threading`, `Condition`, blocking queue  |
| **Assignment 2** | CSV-based Sales Data Analysis using Functional Programming | `csv`, grouping, aggregations, statistics |

---

---

# 🧩 Assignment 1 — Producer–Consumer System

### 🎯 Objective

Implement a **bounded queue** and **thread-safe producer-consumer architecture** using Python concurrency.

### 🧠 Key Skills Demonstrated

- Multithreading using `threading.Thread`
- Safe condition-based synchronization (`wait()`, `notify_all()`)
- Avoiding race conditions and deadlocks
- Sentinel-based shutdown strategy
- End-to-end correctness validation using tests

---

### 📌 Features

| Feature                  | Description                                     |
| ------------------------ | ----------------------------------------------- |
| Custom Bounded Queue     | Blocks producer when full & consumer when empty |
| Thread-Safe Data Sharing | Controlled access via `Condition` lock          |
| Order Preservation       | Output order == input order                     |
| Graceful Thread Exit     | Via sentinel object                             |
| Unit Tests Included      | Automated reliability checks                    |

---

### ▶️ Run Assignment 1

```bash
python -m assignments.assignment1_producer_consumer
```

### 🖥 Expected Output

```bash
Source data:      [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Destination data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Transfer successful: True
```

### 🧪 Run Assignment 1 Unit Tests

```bash
python -m unittest tests.test_assignment1
```

---

# 🧩 Assignment 2 — Sales Data Analysis System

### 🎯 Objective

Process and analyze a structured CSV sales dataset to compute business insights using Python.

---

## 📦 Dataset Details

📁 File: `data/sample_sales_data.csv`  
📌 Total Rows: 200

| Column Name | Description                   |
| ----------- | ----------------------------- |
| order_id    | Order identifier              |
| date        | Order date (YYYY-MM-DD)       |
| region      | Sales region (APAC, EMEA, NA) |
| salesperson | Sales representative          |
| product     | Product name                  |
| units_sold  | Units sold                    |
| unit_price  | Price per unit                |

---

## 🧮 Analytics Functions Implemented

| Method                         | Purpose                             |
| ------------------------------ | ----------------------------------- |
| `total_revenue()`              | Overall revenue across dataset      |
| `revenue_by_region()`          | Which region performs best          |
| `units_sold_by_product()`      | Demand statistics                   |
| `revenue_by_salesperson()`     | Salesperson performance leaderboard |
| `top_n_products_by_revenue(n)` | Best revenue-contributing products  |
| `average_order_value()`        | Revenue per order                   |

---

## ▶️ Run Assignment 2

```bash
python -m assignments.assignment2_sales_analysis
```

## 🖥 Sample Output Snapshot

```bash
Loaded records: 200
Total revenue: 309459.00
=== Revenue by region ===
APAC -> 104325.00
EMEA -> 104110.00
NA -> 101024.00
=== Units sold by product ===
Laptop -> 246
Mouse -> 177
Keyboard -> 254
Monitor -> 266
=== Revenue by salesperson ===
Alice -> 78830.00
Bob -> 78190.00
Charlie -> 81394.00
Diana -> 71045.00
=== Top 3 products by revenue ===
Laptop -> 227680.00
Monitor -> 58850.00
Keyboard -> 16139.00
Average order value: 5429.11

```

## 🧪 Run Assignment 2 Unit Tests

```bash
python -m unittest tests.test_assignment2
```

# 🛠 Setup Instructions

## Create Virtual Environment

```bash
python -m venv .task
source .task/bin/activate
```

---

## 👤 Author

**Nikhil Kumar**  
Software Engineer | Python Developer

---
