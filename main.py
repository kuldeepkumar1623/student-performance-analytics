"""
main.py - Student Performance Analytics System
================================================
This is the main entry point of the application.
It calls functions from functions.py in a logical sequence
to load, clean, analyse and visualise student performance data.

Run this file:
    python main.py
"""

# -- Imports ---------------------------------------------------------------
from functions import (
    load_dataset,
    display_overview,
    check_missing_values,
    check_duplicates,
    clean_data,
    calculate_total_and_average,
    add_grade_and_status,
    performance_statistics,
    top_students,
    pass_fail_summary,
    attendance_analysis,
    department_analysis,
    save_results,
    create_charts,
)

import sys
import os

# -- Configuration ---------------------------------------------------------
# Default dataset (can be overridden via CLI: python main.py <file.csv|.xlsx|.pdf>)
DEFAULT_DATASET = "students.csv"
OUTPUT_CSV = "student_performance_results.csv"   # Analysed results
CHARTS_DIR = "charts"                            # Folder for chart images


def main():
    """
    Complete workflow executed when the script is run.
    Each step is numbered and printed so you can follow along.
    """
    # Check if a custom dataset path was passed via command line
    dataset_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DATASET

    print("=" * 60)
    print("   STUDENT PERFORMANCE ANALYTICS SYSTEM")
    print("=" * 60)
    print(f"Target Dataset File: {dataset_path}")

    # -- Step 1: Load the dataset ------------------------------------------
    print("\n>> Step 1: Loading dataset (supports .csv, .xlsx, .pdf)...")
    df = load_dataset(dataset_path)

    if df is None:
        # If the file is missing or empty, exit gracefully
        print("\n[STOP] Cannot proceed without a valid dataset. Exiting.")
        return

    if df.empty:
        print("\n[STOP] The dataset contains zero rows. Nothing to analyse. Exiting.")
        return

    # -- Step 2: Display dataset overview ----------------------------------
    print("\n>> Step 2: Dataset overview...")
    display_overview(df)

    # -- Step 3: Check for missing values ----------------------------------
    print("\n>> Step 3: Checking for missing values...")
    check_missing_values(df)

    # -- Step 4: Check for duplicate records -------------------------------
    print("\n>> Step 4: Checking for duplicates...")
    check_duplicates(df)

    # -- Step 5: Clean the data --------------------------------------------
    print("\n>> Step 5: Cleaning the data...")
    df_clean = clean_data(df)

    # -- Step 6: Calculate total and average marks -------------------------
    print("\n>> Step 6: Calculating total and average marks...")
    df_clean = calculate_total_and_average(df_clean)

    # -- Step 7: Assign grades and pass/fail status ------------------------
    print("\n>> Step 7: Assigning grades and pass/fail status...")
    df_clean = add_grade_and_status(df_clean)

    # -- Step 8: Display cleaned results -----------------------------------
    print("\n" + "=" * 60)
    print("  CLEANED & ANALYSED STUDENT DATA")
    print("=" * 60)
    display_cols = [
        "Student_ID", "Name", "Department",
        "Mathematics", "Python", "Data_Science",
        "Attendance", "Total_Marks", "Average_Marks",
        "Grade", "Status",
    ]
    print(df_clean[display_cols].to_string(index=False))

    # -- Step 9: Performance statistics ------------------------------------
    print("\n>> Step 9: Performance statistics...")
    performance_statistics(df_clean)

    # -- Step 10: Top students ---------------------------------------------
    print("\n>> Step 10: Top performing students...")
    top_students(df_clean, n=5)

    # -- Step 11: Pass/fail summary ----------------------------------------
    print("\n>> Step 11: Pass/fail summary...")
    pass_fail_summary(df_clean)

    # -- Step 12: Attendance analysis --------------------------------------
    print("\n>> Step 12: Attendance vs performance analysis...")
    attendance_analysis(df_clean)

    # -- Step 13: Department-wise analysis ---------------------------------
    print("\n>> Step 13: Department-wise analysis...")
    department_analysis(df_clean)

    # -- Step 14: Save results to CSV --------------------------------------
    print("\n>> Step 14: Saving results...")
    save_results(df_clean, OUTPUT_CSV)

    # -- Step 15: Generate charts ------------------------------------------
    print("\n>> Step 15: Generating charts...")
    create_charts(df_clean, CHARTS_DIR)

    # -- Done --------------------------------------------------------------
    print("\n" + "=" * 60)
    print("  ANALYSIS COMPLETE!")
    print("=" * 60)
    print(f"   - Results CSV : {OUTPUT_CSV}")
    print(f"   - Charts      : {CHARTS_DIR}/")
    print("=" * 60)


# -- Entry Point -----------------------------------------------------------
if __name__ == "__main__":
    main()

