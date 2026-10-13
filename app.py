"""
app.py — Student Performance Analytics System (Pure Python Web Dashboard)
========================================================================
Interactive Python Web Dashboard built using Streamlit, Pandas, NumPy, and Matplotlib.
Supports multi-format dataset ingestion: CSV, Excel (.xlsx, .xls), and PDF (.pdf).

Run the dashboard:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import io

# Import core analytics functions from functions.py
from functions import (
    clean_data,
    calculate_total_and_average,
    add_grade_and_status,
    performance_statistics,
    top_students,
    pass_fail_summary,
    attendance_analysis,
    department_analysis,
    SUBJECT_COLUMNS,
    PASS_MARK
)

# Page configuration
st.set_page_config(
    page_title="Student Performance Analytics System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for polished look
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .sub-header {
        color: #64748b;
        font-size: 1rem;
        margin-bottom: 25px;
    }
    .kpi-box {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 18px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
    }
    .kpi-title {
        color: #64748b;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    .kpi-val {
        color: #1e293b;
        font-size: 1.8rem;
        font-weight: 800;
        margin-top: 4px;
    }
    .kpi-desc {
        color: #94a3b8;
        font-size: 0.8rem;
    }
    div[data-testid="stMetricValue"] {
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Helper: Load Dataset from File Uploader or Local File
# ---------------------------------------------------------------------------
def load_uploaded_dataset(uploaded_file):
    """Parses uploaded file (CSV, Excel, or PDF) into a DataFrame."""
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    
    if ext == '.csv':
        return pd.read_csv(uploaded_file)
    
    elif ext in ['.xlsx', '.xls']:
        return pd.read_excel(uploaded_file)
    
    elif ext == '.pdf':
        import pdfplumber
        all_rows = []
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        if row and any(cell is not None and str(cell).strip() != '' for cell in row):
                            all_rows.append([str(c).strip() if c is not None else '' for c in row])
        
        if not all_rows:
            st.error("No tabular student data found in the PDF.")
            return None
        
        header = all_rows[0]
        data = all_rows[1:]
        df = pd.DataFrame(data, columns=header)
        df.replace('', np.nan, inplace=True)
        return df
    
    else:
        st.error(f"Unsupported file format: {ext}")
        return None


# ---------------------------------------------------------------------------
# Main App Layout
# ---------------------------------------------------------------------------
def main():
    st.markdown('<div class="main-header">🎓 Student Performance Analytics System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Python Academic Intelligence Engine • NumPy & Pandas Analysis • Multi-Format Ingestion</div>', unsafe_allow_html=True)

    # Sidebar: Data Ingestion Controls
    st.sidebar.header("📁 Dataset Ingestion")
    
    data_source_mode = st.sidebar.radio(
        "Choose Input Source:",
        ["Sample Dataset (Local)", "Upload Custom Dataset (CSV/Excel/PDF)"]
    )

    df_raw = None
    dataset_name = ""

    if data_source_mode == "Sample Dataset (Local)":
        sample_choice = st.sidebar.selectbox(
            "Select Sample Dataset Format:",
            ["students.csv (CSV)", "students.xlsx (Excel)", "students.pdf (PDF)"]
        )
        if "csv" in sample_choice:
            df_raw = pd.read_csv("students.csv")
            dataset_name = "students.csv"
        elif "xlsx" in sample_choice:
            df_raw = pd.read_excel("students.xlsx")
            dataset_name = "students.xlsx"
        elif "pdf" in sample_choice:
            from functions import load_dataset
            df_raw = load_dataset("students.pdf")
            dataset_name = "students.pdf"
            
        st.sidebar.success(f"Loaded: {dataset_name} ({len(df_raw)} records)")

    else:
        uploaded_file = st.sidebar.file_uploader(
            "Upload student records:",
            type=["csv", "xlsx", "xls", "pdf"],
            help="Upload a student dataset in CSV, Excel, or PDF format."
        )
        if uploaded_file is not None:
            df_raw = load_uploaded_dataset(uploaded_file)
            dataset_name = uploaded_file.name
            if df_raw is not None:
                st.sidebar.success(f"Loaded: {dataset_name} ({len(df_raw)} records)")
        else:
            st.sidebar.info("Upload a file above or switch back to Sample Dataset.")
            df_raw = pd.read_csv("students.csv")
            dataset_name = "students.csv (Default)"

    if df_raw is None or df_raw.empty:
        st.warning("No student records available to analyze. Please provide a valid dataset.")
        return

    # Data Processing Pipeline (functions.py)
    with st.spinner("Processing & Analyzing Student Data..."):
        df_clean = clean_data(df_raw)
        df_analyzed = calculate_total_and_average(df_clean)
        df_analyzed = add_grade_and_status(df_analyzed)

    # -----------------------------------------------------------------------
    # Section 1: KPI Metric Cards
    # -----------------------------------------------------------------------
    total_students = len(df_analyzed)
    pass_count = int((df_analyzed["Status"] == "Pass").sum())
    fail_count = total_students - pass_count
    pass_pct = np.round((pass_count / total_students) * 100, 1) if total_students > 0 else 0.0
    overall_avg = np.round(np.mean(df_analyzed["Average_Marks"].to_numpy()), 2)

    top_student = df_analyzed.nlargest(1, "Average_Marks").iloc[0]
    low_student = df_analyzed.nsmallest(1, "Average_Marks").iloc[0]

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Students", f"{total_students}", f"{len(df_analyzed['Department'].unique())} Depts")
    with col2:
        st.metric("Pass Rate", f"{pass_pct}%", f"{pass_count} Passed / {fail_count} Failed")
    with col3:
        st.metric("Batch Average", f"{overall_avg} / 100", "Mean Score")
    with col4:
        st.metric("Highest Scorer", f"{top_student['Average_Marks']}", f"{top_student['Name']}")
    with col5:
        st.metric("Lowest Scorer", f"{low_student['Average_Marks']}", f"{low_student['Name']}", delta_color="inverse")

    st.markdown("---")

    # -----------------------------------------------------------------------
    # Section 2: Visual Charts Row
    # -----------------------------------------------------------------------
    tab1, tab2, tab3 = st.tabs(["📊 Performance Visualizations", "🏫 Department Breakdown", "📋 Student Records Table"])

    with tab1:
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("Subject-wise Average Marks")
            subject_means = {sub: float(np.mean(df_analyzed[sub].to_numpy())) for sub in SUBJECT_COLUMNS}
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            bars = ax1.bar(subject_means.keys(), subject_means.values(), color=['#4f46e5', '#10b981', '#f59e0b'])
            ax1.set_ylim(0, 100)
            ax1.set_ylabel("Average Marks")
            for bar in bars:
                h = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width() / 2, h + 1.5, f"{h:.1f}", ha='center', fontsize=9, fontweight='bold')
            fig1.tight_layout()
            st.pyplot(fig1)

        with c2:
            st.subheader("Grade Distribution (A to F)")
            grade_counts = df_analyzed["Grade"].value_counts().sort_index()
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            colors_palette = ['#10b981', '#3b82f6', '#f59e0b', '#8b5cf6', '#ec4899', '#ef4444']
            ax2.pie(grade_counts.values, labels=grade_counts.index, autopct='%1.1f%%',
                    startangle=140, colors=colors_palette[:len(grade_counts)])
            fig2.tight_layout()
            st.pyplot(fig2)

        c3, c4 = st.columns(2)
        with c3:
            st.subheader("Pass vs Fail Status")
            status_counts = df_analyzed["Status"].value_counts()
            fig3, ax3 = plt.subplots(figsize=(6, 4))
            bar_colors = ['#10b981' if s == 'Pass' else '#ef4444' for s in status_counts.index]
            bars3 = ax3.bar(status_counts.index, status_counts.values, color=bar_colors, width=0.5)
            ax3.set_ylabel("Student Count")
            for b in bars3:
                h = b.get_height()
                ax3.text(b.get_x() + b.get_width() / 2, h + 0.3, str(int(h)), ha='center', fontsize=10, fontweight='bold')
            fig3.tight_layout()
            st.pyplot(fig3)

        with c4:
            st.subheader("Attendance vs Performance Correlation")
            corr = np.corrcoef(df_analyzed["Attendance"].to_numpy(), df_analyzed["Average_Marks"].to_numpy())[0, 1]
            fig4, ax4 = plt.subplots(figsize=(6, 4))
            status_colors = {'Pass': '#10b981', 'Fail': '#ef4444'}
            for status_val, group in df_analyzed.groupby('Status'):
                ax4.scatter(group['Attendance'], group['Average_Marks'],
                            label=status_val, color=status_colors.get(status_val, '#333'), s=50, edgecolors='black', linewidths=0.5)
            ax4.set_xlabel("Attendance (%)")
            ax4.set_ylabel("Average Marks")
            ax4.set_title(f"Correlation: r = {corr:.3f}", fontsize=11, fontweight='bold')
            ax4.legend()
            fig4.tight_layout()
            st.pyplot(fig4)

    # -----------------------------------------------------------------------
    # Section 3: Department Breakdown
    # -----------------------------------------------------------------------
    with tab2:
        st.subheader("Department-wise Academic Insights")
        depts = sorted(df_analyzed["Department"].unique())
        dept_cols = st.columns(len(depts))
        
        for idx, dept in enumerate(depts):
            dept_df = df_analyzed[df_analyzed["Department"] == dept]
            d_total = len(dept_df)
            d_pass = int((dept_df["Status"] == "Pass").sum())
            d_avg = np.round(np.mean(dept_df["Average_Marks"].to_numpy()), 2)
            d_pass_pct = np.round((d_pass / d_total) * 100, 1)
            d_top = dept_df.nlargest(1, "Average_Marks").iloc[0]

            with dept_cols[idx]:
                st.markdown(f"""
                <div class="kpi-box">
                    <div style="font-size: 1.1rem; font-weight: 700; color: #4f46e5; margin-bottom: 8px;">{dept}</div>
                    <div style="font-size: 0.9rem; color: #64748b;">Enrolled: <strong>{d_total}</strong></div>
                    <div style="font-size: 0.9rem; color: #64748b;">Avg Marks: <strong>{d_avg} / 100</strong></div>
                    <div style="font-size: 0.9rem; color: #64748b;">Pass Rate: <strong>{d_pass_pct}% ({d_pass}/{d_total})</strong></div>
                    <div style="font-size: 0.85rem; color: #10b981; margin-top: 6px;">Top: <strong>{d_top['Name']} ({d_top['Average_Marks']})</strong></div>
                </div>
                """, unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # Section 4: Filterable Table & Export
    # -----------------------------------------------------------------------
    with tab3:
        st.subheader("Student Performance Records")
        
        # Search & Filter bar
        fc1, fc2, fc3 = st.columns([2, 1, 1])
        with fc1:
            search_query = st.text_input("🔍 Search by Student Name or ID:", "")
        with fc2:
            dept_filter = st.selectbox("Department Filter:", ["All Departments"] + list(depts))
        with fc3:
            status_filter = st.selectbox("Status Filter:", ["All Status", "Pass", "Fail"])

        # Apply filters
        df_display = df_analyzed.copy()
        if search_query:
            df_display = df_display[
                df_display["Name"].str.contains(search_query, case=False, na=False) |
                df_display["Student_ID"].str.contains(search_query, case=False, na=False)
            ]
        if dept_filter != "All Departments":
            df_display = df_display[df_display["Department"] == dept_filter]
        if status_filter != "All Status":
            df_display = df_display[df_display["Status"] == status_filter]

        st.dataframe(
            df_display[[
                "Student_ID", "Name", "Department",
                "Mathematics", "Python", "Data_Science",
                "Attendance", "Total_Marks", "Average_Marks",
                "Grade", "Status"
            ]],
            use_container_width=True,
            hide_index=True
        )

        # Download buttons
        dc1, dc2 = st.columns(2)
        with dc1:
            csv_data = df_analyzed.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Analyzed Results (CSV)",
                data=csv_data,
                file_name="student_performance_results.csv",
                mime="text/csv"
            )
        with dc2:
            excel_buffer = io.BytesIO()
            df_analyzed.to_excel(excel_buffer, index=False)
            st.download_button(
                label="📥 Download Analyzed Results (Excel)",
                data=excel_buffer.getvalue(),
                file_name="student_performance_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


if __name__ == "__main__":
    main()
