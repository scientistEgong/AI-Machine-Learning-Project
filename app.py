"""
============================================================
PDF Report Generator

Project : AI-Powered Plant Disease Detection

Purpose
-------
Generate professional downloadable PDF diagnosis reports.

Inputs
-------
- Predicted disease class
- Confidence score
- Disease information
- Uploaded image

Output
------
PDF report saved in reports folder
============================================================
"""

# ==========================================================
# PROJECT ROOT SETUP
# ==========================================================

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ==========================================================
# IMPORTS
# ==========================================================

from pathlib import Path
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from config import REPORTS_DIR

# ==========================================================
# CREATE REPORT DIRECTORY
# ==========================================================

# Ensure reports directory exists (create parents if necessary)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================================
# PDF GENERATOR
# ==========================================================

def generate_pdf_report(
    disease_name,
    confidence,
    disease_details,
    image_path=None
):
    """
    Generate plant disease diagnosis PDF report.

    Parameters
    ----------
    disease_name : str
        Predicted class name
    confidence : float
        Prediction confidence (0.0 to 100.0)
    disease_details : dict
        Loaded from disease_info.py
    image_path : str
        Optional uploaded image path

    Returns
    -------
    Path
        Generated PDF location
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"plant_disease_report_{timestamp}.pdf"
    pdf_path = REPORTS_DIR / filename

    # Set up document with 0.75 in (54 pt) margins
    document = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    # Base Styles
    base_styles = getSampleStyleSheet()

    # Brand Colors
    PRIMARY_COLOR = colors.HexColor("#1B4D3E")  # Forest Green
    TEXT_COLOR = colors.HexColor("#2B2B2B")     # Charcoal
    BG_LIGHT = colors.HexColor("#F4F6F5")       # Light grayish-green background tint

    # Custom Paragraph Styles
    title_style = ParagraphStyle(
        'ReportTitle',
        parent=base_styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PRIMARY_COLOR,
        alignment=0,  # Left-aligned
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'ReportSubtitle',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=12,
        textColor=colors.HexColor("#7F8C8D"),
        spaceAfter=15
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=base_styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=PRIMARY_COLOR,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'ReportBody',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14.5,
        textColor=TEXT_COLOR
    )

    bullet_style = ParagraphStyle(
        'ReportBullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    footer_style = ParagraphStyle(
        'ReportFooter',
        parent=base_styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#95A5A6"),
        alignment=1  # Centered
    )

    content = []

    # ------------------------------------------------------
    # HEADER SECTION
    # ------------------------------------------------------
    content.append(Paragraph("AI Plant Health Diagnosis", title_style))
    content.append(Paragraph(f"Official report generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", subtitle_style))
    content.append(HRFlowable(width="100%", thickness=2, color=PRIMARY_COLOR, spaceAfter=20))

    # ------------------------------------------------------
    # DIAGNOSIS SUMMARY (Side-by-side Layout)
    # ------------------------------------------------------
    # Clean the class name (replace underscores with spaces)
    clean_disease_name = disease_name.replace("_", " - ")

    summary_text = f"""
    <b>Target Analyzed:</b> {clean_disease_name}<br/><br/>
    <b>Confidence Score:</b> {confidence:.2f}%<br/><br/>
    <b>Status:</b> {"Action Required" if "Healthy" not in disease_name else "Healthy Crop"}
    """
    
    summary_paragraph = Paragraph(summary_text, body_style)

    # Dynamic image box sizing
    image_element = Paragraph("<i>No crop snapshot included in report.</i>", body_style)
    if image_path and Path(image_path).exists():
        try:
            # Scale down image to standard 180x180 box keeping relative aspects clean
            image_element = Image(image_path, width=180, height=180)
            image_element.hAlign = 'CENTER'
        except Exception:
            pass

    # Layout Table
    summary_table_data = [
        [summary_paragraph, image_element]
    ]

    summary_table = Table(summary_table_data, colWidths=[280, 220])
    summary_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (0,0), BG_LIGHT),
        ('PADDING', (0,0), (-1,-1), 12),
        ('BOX', (0,0), (0,0), 1, colors.HexColor("#BDC3C7")),
        # Use white for inner grid color to keep it invisible across viewers
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.white),
    ]))

    content.append(summary_table)
    content.append(Spacer(1, 15))

    # ------------------------------------------------------
    # DIAGNOSIS DETAILS
    # ------------------------------------------------------
    sections = [
        ("Description", disease_details.get("description", "Unavailable.")),
        ("Symptoms", disease_details.get("symptoms", [])),
        ("Causes & Spreading Agents", disease_details.get("causes", [])),
        ("Recommended Treatments", disease_details.get("treatment", [])),
        ("Prevention & Control Protocols", disease_details.get("prevention", []))
    ]

    for title, value in sections:
        content.append(Paragraph(title, section_heading))
        content.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#BDC3C7"), spaceAfter=8))

        if isinstance(value, list):
            if value:
                for item in value:
                    content.append(Paragraph(f"• &nbsp; {item}", bullet_style))
            else:
                content.append(Paragraph("No standard protocols configured.", body_style))
        else:
            content.append(Paragraph(value, body_style))

        content.append(Spacer(1, 12))

    # ------------------------------------------------------
    # FOOTER SYSTEM
    # ------------------------------------------------------
    content.append(Spacer(1, 20))
    content.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#BDC3C7"), spaceAfter=10))
    content.append(
        Paragraph(
            "Disclaimer: This report was generated by an artificial intelligence model. Use as guidance in consultation with regional agricultural extensions.", 
            footer_style
        )
    )

    # Build PDF Document
    document.build(content)
    return pdf_path

# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":
    print("="*60)
    print("PDF Report Generator - Touch-Up Edition")
    print("="*60)
    print(f"Reports folder: {REPORTS_DIR}")
    print("\nModule loaded successfully and ready.")