"""
functions.py - Reusable Functions for Student Performance Analytics System
==========================================================================
This file contains all the helper functions used by main.py.
Each function has a clear docstring explaining what it does,
what it takes as input, and what it returns.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")          # Use non-interactive backend so charts save without a GUI window
import matplotlib.pyplot as plt
import os
import sys


# ---------------------------------------------------------------------------
# 1. DATA LOADING
# ---------------------------------------------------------------------------

def load_dataset(filepath):
    """
    Load student dataset from CSV, Excel (.xlsx, .xls), or PDF (.pdf) into a Pandas DataFrame.

    Parameters
    ----------
    filepath : str
        Path to the dataset file (e.g. 'students.csv', 'students.xlsx', 'students.pdf').

    Returns
    -------
    pd.DataFrame or None
        The loaded DataFrame, or None if the file is missing / unreadable.
    """
    if not os.path.exists(filepath):
        print(f"[ERROR] File '{filepath}' not found.")
        print("   Make sure the file path is correct.")
        return None

    ext = os.path.splitext(filepath)[1].lower()

    try:
        if ext == '.csv':
            df = pd.read_csv(filepath)
            print(f"[OK] CSV dataset loaded successfully from '{filepath}'")
            return df

        elif ext in ['.xlsx', '.xls']:
            df = pd.read_excel(filepath)
            print(f"[OK] Excel dataset loaded successfully from '{filepath}'")
            return df

        elif ext == '.pdf':
            import pdfplumber
            all_rows = []
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for table in tables:
                        for row in table:
                            if row and any(cell is not None and str(cell).strip() != '' for cell in row):
                                all_rows.append([str(c).strip() if c is not None else '' for c in row])

            if not all_rows:
                print(f"[ERROR] No tabular student data detected in PDF '{filepath}'.")
                return None

            header = all_rows[0]
            data = all_rows[1:]
            df = pd.DataFrame(data, columns=header)
            # Replace empty strings with NaN
            df.replace('', np.nan, inplace=True)
            print(f"[OK] PDF dataset table extracted successfully from '{filepath}' ({len(df)} rows)")
            return df

        else:
            print(f"[ERROR] Unsupported file extension '{ext}'. Please provide a .csv, .xlsx, or .pdf file.")
            return None

    except pd.errors.EmptyDataError:
        print(f"[ERROR] File '{filepath}' is empty.")
        return None
    except Exception as e:
        print(f"[ERROR] Error loading '{filepath}': {e}")
        return None


# ---------------------------------------------------------------------------
# 2. DATASET OVERVIEW
# ---------------------------------------------------------------------------

def display_overview(df):
    """
    Print a quick overview of the dataset:
      - First 5 rows
      - Shape (rows x columns)
      - Column names
      - Data types
    """
    print("\n" + "=" * 60)
    print("  DATASET OVERVIEW")
    print("=" * 60)

    print("\n--- First 5 Records ---")
    print(df.head().to_string(index=False))

    print(f"\n--- Shape ---")
    print(f"   Rows   : {df.shape[0]}")
    print(f"   Columns: {df.shape[1]}")

    print(f"\n--- Column Names ---")
    for col in df.columns:
        print(f"   - {col}")

    print(f"\n--- Data Types ---")
    for col, dtype in df.dtypes.items():
        print(f"   {col:25s} -> {dtype}")


# ---------------------------------------------------------------------------
# 3. DATA QUALITY CHECKS
# ---------------------------------------------------------------------------

def check_missing_values(df):
    """
    Report how many missing (NaN) values exist in each column.

    Returns
    -------
    pd.Series
        Count of missing values per column.
    """
    missing = df.isnull().sum()
    total_missing = missing.sum()

    print("\n" + "=" * 60)
    print("  MISSING VALUES CHECK")
    print("=" * 60)

    if total_missing == 0:
        print("   No missing values found. Dataset is complete.")
    else:
        print(f"   Total missing values: {total_missing}")
        for col, count in missing.items():
            if count > 0:
                print(f"   - {col}: {count} missing")
    return missing


def check_duplicates(df):
    """
    Report duplicate rows based on Student_ID.

    Returns
    -------
    pd.DataFrame
        DataFrame of duplicate rows (may be empty).
    """
    duplicates = df[df.duplicated(subset="Student_ID", keep=False)]

    print("\n" + "=" * 60)
    print("  DUPLICATE RECORDS CHECK")
    print("=" * 60)

    if duplicates.empty:
        print("   No duplicate Student_IDs found.")
    else:
        print(f"   Found {len(duplicates)} rows with duplicate Student_IDs:")
        print(duplicates.to_string(index=False))
    return duplicates


# ---------------------------------------------------------------------------
# 4. DATA CLEANING
# ---------------------------------------------------------------------------

def validate_marks(value, column_name, student_id):
    """
    Check whether a single marks/attendance value is valid (0-100).
    Returns the value as a float if valid, or np.nan if invalid.

    IMPORTANT: We never silently convert bad data to zero.
    Instead we mark it as NaN so it can be handled transparently.
    """
    try:
        num = float(value)
    except (ValueError, TypeError):
        print(f"   [!] Invalid value '{value}' in {column_name} for {student_id} -> set to NaN")
        return np.nan

    if num < 0 or num > 100:
        print(f"   [!] Out-of-range value {num} in {column_name} for {student_id} -> set to NaN")
        return np.nan

    return num


def clean_data(df):
    """
    Clean the dataset step-by-step with full explanations.

    Cleaning decisions
    ------------------
    1. Strip whitespace from text columns (Name, Department).
    2. Validate that marks and attendance are numbers in [0, 100].
       Invalid values are set to NaN - NOT silently zeroed.
    3. Drop exact duplicate rows (keep first occurrence).
    4. Fill remaining NaN marks with the column median so that
       students are not unfairly penalised. We document every fill.
    5. Fill remaining NaN attendance with the column median.

    Parameters
    ----------
    df : pd.DataFrame
        Raw dataset.

    Returns
    -------
    pd.DataFrame
        Cleaned dataset (a copy - the original is not modified).
    """
    print("\n" + "=" * 60)
    print("  DATA CLEANING")
    print("=" * 60)

    df_clean = df.copy()

    # Step 1: Strip whitespace from text columns
    print("\n   Step 1 - Stripping whitespace from Name and Department columns.")
    df_clean["Name"] = df_clean["Name"].astype(str).str.strip()
    df_clean["Department"] = df_clean["Department"].astype(str).str.strip()

    # Step 2: Validate numeric columns
    numeric_cols = ["Mathematics", "Python", "Data_Science", "Attendance"]
    print("   Step 2 - Validating numeric columns (marks 0-100, attendance 0-100).")
    for col in numeric_cols:
        df_clean[col] = df_clean.apply(
            lambda row: validate_marks(row[col], col, row["Student_ID"]),
            axis=1,
        )

    # Step 3: Remove duplicate Student_IDs (keep first)
    before = len(df_clean)
    df_clean = df_clean.drop_duplicates(subset="Student_ID", keep="first")
    removed = before - len(df_clean)
    print(f"   Step 3 - Removed {removed} duplicate row(s).")

    # Step 4: Fill missing marks with column median
    print("   Step 4 - Filling missing marks with column median (fair imputation).")
    for col in ["Mathematics", "Python", "Data_Science"]:
        n_missing = df_clean[col].isnull().sum()
        if n_missing > 0:
            median_val = np.nanmedian(df_clean[col].values)
            df_clean[col] = df_clean[col].fillna(median_val)
            print(f"            - {col}: filled {n_missing} NaN(s) with median = {median_val:.1f}")

    # Step 5: Fill missing attendance with column median
    print("   Step 5 - Filling missing attendance with column median.")
    n_missing = df_clean["Attendance"].isnull().sum()
    if n_missing > 0:
        median_att = np.nanmedian(df_clean["Attendance"].values)
        df_clean["Attendance"] = df_clean["Attendance"].fillna(median_att)
        print(f"            - Attendance: filled {n_missing} NaN(s) with median = {median_att:.1f}")

    # Ensure numeric types after cleaning
    for col in numeric_cols:
        df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")

    print("\n   [OK] Data cleaning complete.")
    return df_clean


# ---------------------------------------------------------------------------
# 5. FEATURE ENGINEERING - Total, Average, Grade, Pass/Fail
# ---------------------------------------------------------------------------

SUBJECT_COLUMNS = ["Mathematics", "Python", "Data_Science"]
PASS_MARK = 40   # Minimum marks required in EACH subject to pass


def calculate_total_and_average(df):
    """
    Add 'Total_Marks' and 'Average_Marks' columns.

    Uses NumPy for the numerical computation.
    """
    # Convert subject columns to a NumPy array for calculation
    marks_array = df[SUBJECT_COLUMNS].to_numpy(dtype=float)

    df["Total_Marks"] = np.sum(marks_array, axis=1)
    df["Average_Marks"] = np.round(np.mean(marks_array, axis=1), 2)

    print("\n   [OK] Total_Marks and Average_Marks calculated using NumPy.")
    return df


def assign_grade(average):
    """
    Assign a letter grade based on average marks.

    Grading System
    --------------
    A  : average >= 90
    B  : 80 <= average < 90
    C  : 70 <= average < 80
    D  : 60 <= average < 70
    E  : 40 <= average < 60
    F  : average < 40
    """
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    elif average >= 40:
        return "E"
    else:
        return "F"


def determine_pass_fail(row):
    """
    A student passes ONLY if they score >= 40 in EVERY subject.

    This is independent of the grade - a student can get grade D
    overall but still fail if one subject is below 40.
    """
    for subject in SUBJECT_COLUMNS:
        if row[subject] < PASS_MARK:
            return "Fail"
    return "Pass"


def add_grade_and_status(df):
    """
    Apply grading and pass/fail logic to every student.
    """
    df["Grade"] = df["Average_Marks"].apply(assign_grade)
    df["Status"] = df.apply(determine_pass_fail, axis=1)

    print("   [OK] Grades and Pass/Fail status assigned.")
    return df


# ---------------------------------------------------------------------------
# 6. PERFORMANCE STATISTICS
# ---------------------------------------------------------------------------

def performance_statistics(df):
    """
    Print and return key performance metrics:
      - Highest, lowest and overall average marks
      - Subject-wise averages (using NumPy)
    """
    marks_array = df["Average_Marks"].to_numpy()

    highest = np.max(marks_array)
    lowest = np.min(marks_array)
    overall_avg = np.round(np.mean(marks_array), 2)

    print("\n" + "=" * 60)
    print("  PERFORMANCE STATISTICS")
    print("=" * 60)
    print(f"   Highest Average Marks : {highest}")
    print(f"   Lowest Average Marks  : {lowest}")
    print(f"   Overall Average Marks : {overall_avg}")

    # Subject-wise averages using NumPy
    print("\n   --- Subject-wise Average Marks ---")
    for subject in SUBJECT_COLUMNS:
        avg = np.round(np.mean(df[subject].to_numpy()), 2)
        print(f"   - {subject:15s} : {avg}")

    return {"highest": highest, "lowest": lowest, "overall_avg": overall_avg}


def top_students(df, n=5):
    """
    Display the top N students ranked by Average_Marks.
    """
    top = df.nlargest(n, "Average_Marks")

    print(f"\n" + "=" * 60)
    print(f"  TOP {n} STUDENTS")
    print("=" * 60)
    display_cols = ["Student_ID", "Name", "Department",
                    "Total_Marks", "Average_Marks", "Grade", "Status"]
    print(top[display_cols].to_string(index=False))
    return top


def pass_fail_summary(df):
    """
    Calculate and display:
      - Total students
      - Pass count and fail count
      - Pass percentage
    """
    total = len(df)
    pass_count = int((df["Status"] == "Pass").sum())
    fail_count = int((df["Status"] == "Fail").sum())
    pass_pct = np.round((pass_count / total) * 100, 2) if total > 0 else 0.0

    print("\n" + "=" * 60)
    print("  PASS / FAIL SUMMARY")
    print("=" * 60)
    print(f"   Total Students   : {total}")
    print(f"   Passed           : {pass_count}")
    print(f"   Failed           : {fail_count}")
    print(f"   Pass Percentage  : {pass_pct}%")

    return {
        "total": total,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "pass_pct": pass_pct,
    }


# ---------------------------------------------------------------------------
# 7. ATTENDANCE ANALYSIS
# ---------------------------------------------------------------------------

def attendance_analysis(df):
    """
    Analyse the relationship between attendance and performance.

    We group students into attendance buckets and calculate the
    average marks for each bucket, showing a clear trend.
    Also uses NumPy correlation to quantify the relationship.
    """
    print("\n" + "=" * 60)
    print("  ATTENDANCE vs PERFORMANCE ANALYSIS")
    print("=" * 60)

    # NumPy correlation between attendance and average marks
    correlation = np.corrcoef(
        df["Attendance"].to_numpy(),
        df["Average_Marks"].to_numpy(),
    )[0, 1]
    print(f"\n   Correlation (Attendance <-> Average Marks): {correlation:.4f}")

    if correlation > 0.5:
        print("   -> Strong positive correlation: higher attendance is linked to better marks.")
    elif correlation > 0.2:
        print("   -> Moderate positive correlation.")
    else:
        print("   -> Weak or no clear correlation.")

    # Bucket analysis
    bins = [0, 60, 75, 90, 100]
    labels = ["Low (0-60%)", "Medium (61-75%)", "Good (76-90%)", "Excellent (91-100%)"]
    df["Attendance_Bucket"] = pd.cut(df["Attendance"], bins=bins, labels=labels, include_lowest=True)

    bucket_stats = df.groupby("Attendance_Bucket", observed=False)["Average_Marks"].agg(
        ["mean", "count"]
    )
    bucket_stats.columns = ["Avg_Marks", "Student_Count"]
    bucket_stats["Avg_Marks"] = np.round(bucket_stats["Avg_Marks"].to_numpy(), 2)

    print("\n   --- Attendance Bucket Summary ---")
    print(bucket_stats.to_string())

    # Remove the helper column so it doesn't pollute the saved CSV
    df.drop(columns=["Attendance_Bucket"], inplace=True)

    return correlation


# ---------------------------------------------------------------------------
# 8. DEPARTMENT-WISE ANALYSIS
# ---------------------------------------------------------------------------

def department_analysis(df):
    """
    Print average marks and pass percentage per department.
    """
    print("\n" + "=" * 60)
    print("  DEPARTMENT-WISE ANALYSIS")
    print("=" * 60)

    departments = df["Department"].unique()
    for dept in sorted(departments):
        dept_df = df[df["Department"] == dept]
        avg = np.round(np.mean(dept_df["Average_Marks"].to_numpy()), 2)
        pass_count = int((dept_df["Status"] == "Pass").sum())
        total = len(dept_df)
        pass_pct = np.round((pass_count / total) * 100, 2) if total > 0 else 0.0
        print(f"\n   {dept}")
        print(f"      Students       : {total}")
        print(f"      Average Marks  : {avg}")
        print(f"      Passed         : {pass_count} / {total} ({pass_pct}%)")


# ---------------------------------------------------------------------------
# 9. SAVE RESULTS
# ---------------------------------------------------------------------------

def save_results(df, output_path):
    """
    Save the analyzed DataFrame to a CSV file and JSON files.

    The saved file includes all original columns plus:
    Total_Marks, Average_Marks, Grade, Status.
    """
    try:
        df.to_csv(output_path, index=False)
        print(f"\n[OK] Results saved to '{output_path}'")
        
        # Also export JSON for the React frontend
        json_path = "student_performance_results.json"
        df.to_json(json_path, orient="records", indent=2)
        print(f"[OK] JSON results saved to '{json_path}'")

        # Sync to frontend src/data if directory exists
        frontend_data_path = os.path.join("frontend", "src", "data", "studentsData.json")
        if os.path.exists(os.path.dirname(frontend_data_path)):
            df.to_json(frontend_data_path, orient="records", indent=2)
            print(f"[OK] Synced data to React frontend: '{frontend_data_path}'")
    except Exception as e:
        print(f"[ERROR] Error saving results: {e}")


# ---------------------------------------------------------------------------
# 10. CHARTS (Optional - Matplotlib)
# ---------------------------------------------------------------------------

def create_charts(df, charts_dir="charts"):
    """
    Generate and save the following charts:
      1. Subject-wise average marks (bar chart)
      2. Grade distribution (pie chart)
      3. Pass vs Fail (bar chart)
      4. Attendance vs Average Marks (scatter plot)

    Charts are saved as PNG files inside the `charts/` folder.
    """
    # Create the charts directory if it does not exist
    os.makedirs(charts_dir, exist_ok=True)

    print("\n" + "=" * 60)
    print("  GENERATING CHARTS")
    print("=" * 60)

    # ---- Chart 1: Subject-wise average marks ----
    subject_avgs = {sub: np.mean(df[sub].to_numpy()) for sub in SUBJECT_COLUMNS}

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(subject_avgs.keys(), subject_avgs.values(), color=["#4C72B0", "#55A868", "#C44E52"])
    ax.set_title("Subject-wise Average Marks", fontsize=14, fontweight="bold")
    ax.set_ylabel("Average Marks")
    ax.set_ylim(0, 100)
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 1,
                f"{height:.1f}", ha="center", fontsize=10)
    fig.tight_layout()
    path1 = os.path.join(charts_dir, "subject_averages.png")
    fig.savefig(path1, dpi=150)
    plt.close(fig)
    print(f"   [OK] Saved: {path1}")

    # ---- Chart 2: Grade distribution ----
    grade_counts = df["Grade"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(7, 7))
    colors = ["#2ecc71", "#3498db", "#f1c40f", "#e67e22", "#e74c3c", "#95a5a6"]
    ax.pie(grade_counts.values, labels=grade_counts.index, autopct="%1.1f%%",
           startangle=140, colors=colors[:len(grade_counts)])
    ax.set_title("Grade Distribution", fontsize=14, fontweight="bold")
    fig.tight_layout()
    path2 = os.path.join(charts_dir, "grade_distribution.png")
    fig.savefig(path2, dpi=150)
    plt.close(fig)
    print(f"   [OK] Saved: {path2}")

    # ---- Chart 3: Pass vs Fail ----
    status_counts = df["Status"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 5))
    bar_colors = ["#2ecc71" if s == "Pass" else "#e74c3c" for s in status_counts.index]
    bars = ax.bar(status_counts.index, status_counts.values, color=bar_colors)
    ax.set_title("Pass vs Fail Count", fontsize=14, fontweight="bold")
    ax.set_ylabel("Number of Students")
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.3,
                str(int(height)), ha="center", fontsize=12)
    fig.tight_layout()
    path3 = os.path.join(charts_dir, "pass_fail.png")
    fig.savefig(path3, dpi=150)
    plt.close(fig)
    print(f"   [OK] Saved: {path3}")

    # ---- Chart 4: Attendance vs Performance (scatter) ----
    fig, ax = plt.subplots(figsize=(8, 5))
    colours_map = {"Pass": "#2ecc71", "Fail": "#e74c3c"}
    for status, group in df.groupby("Status"):
        ax.scatter(group["Attendance"], group["Average_Marks"],
                   label=status, color=colours_map.get(status, "#333"),
                   s=60, edgecolors="black", linewidths=0.5)
    ax.set_xlabel("Attendance (%)")
    ax.set_ylabel("Average Marks")
    ax.set_title("Attendance vs Performance", fontsize=14, fontweight="bold")
    ax.legend()
    fig.tight_layout()
    path4 = os.path.join(charts_dir, "attendance_vs_performance.png")
    fig.savefig(path4, dpi=150)
    plt.close(fig)
    print(f"   [OK] Saved: {path4}")

    print("\n   All charts saved to the 'charts/' folder.")

