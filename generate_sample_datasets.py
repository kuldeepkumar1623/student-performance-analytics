"""
generate_sample_datasets.py
Generates students.xlsx and students.pdf from students.csv
so the user has sample files in CSV, Excel, and PDF formats.
"""

import pandas as pd
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def create_samples():
    df = pd.read_csv('students.csv')
    
    # 1. Create Excel file
    excel_path = 'students.xlsx'
    df.to_excel(excel_path, index=False)
    print(f"[OK] Generated Excel dataset: {excel_path}")

    # 2. Create PDF file with table
    pdf_path = 'students.pdf'
    doc = SimpleDocTemplate(pdf_path, pagesize=landscape(letter),
                            rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=12
    )
    elements.append(Paragraph("Student Performance Dataset", title_style))
    elements.append(Spacer(1, 10))

    # Convert DataFrame to table data
    table_data = [list(df.columns)]
    for _, row in df.iterrows():
        # Handle NaN values for presentation
        formatted_row = []
        for val in row:
            if pd.isna(val):
                formatted_row.append("")
            else:
                formatted_row.append(str(val))
        table_data.append(formatted_row)

    t = Table(table_data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4f46e5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9fafb')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
    ]))
    elements.append(t)
    doc.build(elements)
    print(f"[OK] Generated PDF dataset: {pdf_path}")

if __name__ == '__main__':
    create_samples()

