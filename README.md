# 📊 Student Performance Analytics System

A beginner-friendly Python mini-project that reads student records from a CSV dataset, processes the data using **Pandas** and **NumPy**, and generates meaningful academic performance analysis with optional **Matplotlib** charts.

---

## 📌 Project Overview

This project analyses student academic performance across multiple subjects (Mathematics, Python, Data Science). It loads raw CSV data, cleans it, calculates grades and pass/fail status, generates statistics, and saves the results — all from the terminal with a single command.

## 🎯 Objectives

- Practice loading and manipulating CSV data with Pandas.
- Use NumPy for numerical calculations (averages, totals, correlations).
- Apply conditional logic for grading and pass/fail determination.
- Clean real-world-style messy data (missing values, validation).
- Visualise results with Matplotlib bar charts, pie charts and scatter plots.
- Structure code into reusable functions for maintainability.

## ✨ Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | Multi-Format Ingestion | Ingests `.csv`, `.xlsx`, `.xls` (Excel), and `.pdf` (Table Extraction) |
| 2 | Dataset Overview | Displays shape, columns, data types and first records |
| 3 | Quality Checks | Detects missing values and duplicate Student_IDs |
| 4 | Data Cleaning | Validates ranges, fills NaNs with median, explains every step |
| 5 | Total & Average | Calculates per-student total and average marks (NumPy) |
| 6 | Grading | Assigns A–F grades based on average marks |
| 7 | Pass/Fail | Student must score ≥ 40 in **every** subject to pass |
| 8 | Statistics | Highest, lowest and overall average performance |
| 9 | Subject Averages | Mean marks per subject |
| 10 | Top Students | Ranks students by average marks |
| 11 | Pass Summary | Total, pass count, fail count, pass percentage |
| 12 | Attendance Analysis | Correlation and bucket comparison with marks |
| 13 | Department Analysis | Per-department average and pass rate |
| 14 | Save Results | Exports analysed data to `student_performance_results.csv` & JSON |
| 15 | Charts | Bar, pie and scatter charts saved to `charts/` |
| 16 | React Frontend Dashboard | Interactive drag & drop analytics supporting CSV, Excel & PDF |

## 🛠 Technologies Used

| Technology | Purpose |
|------------|---------|
| Python 3.x | Core programming language |
| Pandas | Data loading, filtering and manipulation |
| NumPy | Numerical calculations (sum, mean, correlation) |
| Matplotlib | Chart generation (bar, pie, scatter) |
| OpenPyXL | Excel (.xlsx) parsing |
| PDFPlumber & PyPDF | PDF table extraction & document generation |
| React 18 + Vite | Interactive web dashboard |
| SheetJS & PapaParse | Client-side Excel & CSV parsing |

##  Dataset Description

`students.csv` contains **25 student records** with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| Student_ID | String | Unique identifier (S001, S002, …) |
| Name | String | Student's full name |
| Department | String | CS, DS, or IT |
| Mathematics | Float | Marks out of 100 |
| Python | Float | Marks out of 100 |
| Data_Science | Float | Marks out of 100 |
| Attendance | Float | Attendance percentage (0–100) |

The dataset intentionally includes **two missing values** (rows 23 and 24) to demonstrate data cleaning.

## 📂 Project Folder Structure

```
student-performance-analytics/
│
├── main.py                            # Main entry point — run this file
├── functions.py                       # All reusable helper functions
├── students.csv                       # Raw student dataset
├── student_performance_results.csv    # Generated after running main.py
├── requirements.txt                   # Python dependencies
├── README.md                          # This file
├── Project_Documentation.md           # Detailed project documentation
├── .gitignore                         # Files excluded from Git
└── charts/                            # Generated chart images
    ├── subject_averages.png
    ├── grade_distribution.png
    ├── pass_fail.png
    └── attendance_vs_performance.png
```

## 🚀 Installation Instructions

### Prerequisites
- **Python 3.9+** installed ([download](https://www.python.org/downloads/))
- **VS Code** (recommended editor)
- **Git** installed ([download](https://git-scm.com/downloads))



```
============================================================
   STUDENT PERFORMANCE ANALYTICS SYSTEM
============================================================

▶ Step 1: Loading dataset...
✅ Dataset loaded successfully from 'students.csv'

▶ Step 5: Cleaning the data...
   Step 2 — Validating numeric columns (marks 0-100, attendance 0-100).
   Step 4 — Filling missing marks with column median (fair imputation).
            • Data_Science: filled 1 NaN(s) with median = 70.0
   Step 5 — Filling missing attendance with column median.
            • Attendance: filled 1 NaN(s) with median = 76.0

▶ Step 11: Pass/fail summary...
   Total Students   : 25
   Passed           : 19
   Failed           : 6
   Pass Percentage  : 76.0%

🎉 ANALYSIS COMPLETE!
   • Results CSV : student_performance_results.csv
   • Charts      : charts/
```

## 📊 Grading System

| Grade | Condition |
|-------|-----------|
| A | Average ≥ 90 |
| B | 80 ≤ Average < 90 |
| C | 70 ≤ Average < 80 |
| D | 60 ≤ Average < 70 |
| E | 40 ≤ Average < 60 |
| F | Average < 40 |

**Pass Condition:** A student must score **≥ 40 in every subject** (Mathematics, Python, Data Science).

## 📄 License

This project is created for educational purposes as part of a Python with AI course assignment.

---

*Built with ❤ using Python, Pandas, NumPy and Matplotlib.*

