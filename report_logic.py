import os
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
)
from reportlab.lib import colors
from PIL import Image as PILImage


# =============================
# CONFIGURATION
# =============================
MAX_IMAGE_WIDTH_INCH = 6.0
MAX_IMAGE_PX = 1200

BASE_FONT = "Times-Roman"
BOLD_FONT = "Times-Bold"

styles = getSampleStyleSheet()

# =============================
# STYLES
# =============================
styles.add(ParagraphStyle(
    name='HeaderMain',
    fontName=BOLD_FONT, fontSize=16, alignment=1, spaceAfter=6
))
styles.add(ParagraphStyle(
    name='HeaderSub',
    fontName=BASE_FONT, fontSize=13, alignment=1, spaceAfter=2
))
styles.add(ParagraphStyle(
    name='SectionTitle',
    fontName=BOLD_FONT, fontSize=12.5, alignment=0, spaceBefore=14, spaceAfter=6
))
styles.add(ParagraphStyle(
    name='SubsectionTitle',
    fontName=BOLD_FONT, fontSize=11.5, alignment=0, spaceBefore=8, spaceAfter=4
))
styles.add(ParagraphStyle(
    name='NormalText',
    fontName=BASE_FONT, fontSize=11, leading=15
))
styles.add(ParagraphStyle(
    name='TableKey',
    fontName=BOLD_FONT, fontSize=11, leading=14
))
styles.add(ParagraphStyle(
    name='TableValue',
    fontName=BASE_FONT, fontSize=11, leading=14
))
styles.add(ParagraphStyle(
    name='CenteredBold',
    fontName=BOLD_FONT, fontSize=16, alignment=1, spaceBefore=6, spaceAfter=6
))
styles.add(ParagraphStyle(
    name='PhotoHeading',
    fontName=BOLD_FONT, fontSize=14, alignment=1, spaceBefore=6, spaceAfter=8
))


# =============================
# UTILITIES
# =============================

def ensure_image_resized(path):
    """Resize image if too large."""
    try:
        if not path or not os.path.exists(path):
            return None
        img = PILImage.open(path)
        w, h = img.size
        if w > MAX_IMAGE_PX:
            ratio = MAX_IMAGE_PX / float(w)
            new_size = (int(w * ratio), int(h * ratio))
            img = img.resize(new_size, PILImage.LANCZOS)
            new_path = f"{os.path.splitext(path)[0]}_resized{os.path.splitext(path)[1]}"
            img.save(new_path, quality=85)
            return new_path
        return path
    except Exception as e:
        print("Image resize error:", e)
        return path


def image_flowable(path, max_width_inch=MAX_IMAGE_WIDTH_INCH):
    """Return ReportLab Image flowable scaled to max width."""
    if not path or not os.path.exists(path):
        return None
    try:
        max_w_pts = max_width_inch * 72
        img = Image(path)
        iw, ih = img.drawWidth, img.drawHeight
        if iw > max_w_pts:
            scale = max_w_pts / iw
            img.drawWidth *= scale
            img.drawHeight *= scale
        img.hAlign = 'CENTER'
        return img
    except Exception as e:
        print("Error creating image flowable:", e)
        return None


def make_table_from_dict(dct, colWidths=[2.5 * inch, 4.5 * inch]):
    """Create a consistent table layout for key-value pairs."""
    if not dct:
        return []
    data = []
    for k, v in dct.items():
        keyp = Paragraph(str(k), styles['TableKey'])
        valp = Paragraph(str(v), styles['TableValue'])
        data.append([keyp, valp])
    tbl = Table(data, colWidths=colWidths, hAlign='LEFT')
    tbl.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    return [tbl, Spacer(1, 0.12 * inch)]


def format_date_and_time(info):
    """Format date/time fields for single or multi-day display."""
    start_date = info.get("Start Date", "")
    end_date = info.get("End Date", "")
    start_time = info.get("Start Time", "")
    end_time = info.get("End Time", "")

    date_str = ""
    if start_date and end_date:
        if start_date == end_date:
            date_str = f"{format_date_label(start_date)}"
        else:
            date_str = f"{format_date_label(start_date)} – {format_date_label(end_date)}"
    elif start_date:
        date_str = format_date_label(start_date)

    time_str = ""
    if start_time and end_time:
        if start_time == end_time:
            time_str = start_time
        else:
            time_str = f"{start_time} – {end_time}"
    elif start_time:
        time_str = start_time

    if date_str:
        info["Date/s"] = date_str
    if time_str:
        info["Time"] = time_str

    for key in ["Start Date", "End Date", "Start Time", "End Time"]:
        info.pop(key, None)


def format_date_label(date_text):
    """Convert YYYY-MM-DD to readable date format."""
    try:
        dt = datetime.strptime(date_text, "%Y-%m-%d")
        return dt.strftime("%d %B %Y")
    except Exception:
        return date_text


# =============================
# PAGE NUMBERING
# =============================

def add_page_number(canvas, doc):
    """Add page number bottom-right."""
    page_num = canvas.getPageNumber()
    text = f"Page {page_num}"
    canvas.setFont(BASE_FONT, 10)
    canvas.drawRightString(8.0 * inch, 0.5 * inch, text)


# =============================
# MAIN PDF GENERATION
# =============================

def generate_report_pdf(data):
    buffer = BytesIO()
    story = []

    # HEADER
    story.append(Paragraph("CHRIST (Deemed to be University), Bangalore", styles['HeaderMain']))
    story.append(Paragraph("School of Engineering and Technology", styles['HeaderSub']))
    story.append(Paragraph("Department of AI, ML & Data Science", styles['HeaderSub']))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("<b>Activity Report</b>", styles['CenteredBold']))
    story.append(Spacer(1, 0.2 * inch))

    # GENERAL INFORMATION
    story.append(Paragraph("General Information", styles['SectionTitle']))
    general_info = data.get("general_info", {})
    format_date_and_time(general_info)
    story.extend(make_table_from_dict(general_info))

    # SPEAKER DETAILS
    story.append(Paragraph("Speaker/Guest/Presenter Details", styles['SectionTitle']))
    for sp in data.get("speakers", []):
        speaker_info = {
            "Name": sp.get("name", ""),
            "Title/Position": sp.get("title", ""),
            "Organization": sp.get("organization", ""),
            "Contact Info": sp.get("contact", ""),
            "Title of Presentation": sp.get("presentation_title", "")
        }
        story.extend(make_table_from_dict(speaker_info))

    # PARTICIPANTS
    story.append(Paragraph("Participants profile", styles['SectionTitle']))
    for p in data.get("participants", []):
        pdata = {
            "Type of Participants": p.get("type", ""),
            "No. of Participants": p.get("count", "")
        }
        story.extend(make_table_from_dict(pdata))

    # SYNOPSIS (TABLE FORMAT)
    story.append(Paragraph("Synopsis of the Activity (Description)", styles['SectionTitle']))
    synopsis = data.get("synopsis", {})
    syn_dict = {}
    if synopsis.get("highlights"):
        syn_dict["Highlights of the Activity"] = synopsis["highlights"]
    if synopsis.get("key_takeaways"):
        syn_dict["Key Takeaways"] = synopsis["key_takeaways"]
    if synopsis.get("summary"):
        syn_dict["Summary of the Activity"] = synopsis["summary"]
    if synopsis.get("follow_up"):
        syn_dict["Follow-up plan"] = synopsis["follow_up"]
    story.extend(make_table_from_dict(syn_dict))

    # REPORT PREPARED BY
    story.append(Paragraph("Report prepared by", styles['SectionTitle']))
    for p in data.get("preparers", []):
        pdata = {
            "Name of the Organiser": p.get("name", ""),
            "Designation/Title": p.get("designation", "")
        }
        story.extend(make_table_from_dict(pdata))
        if p.get("signature_path"):
            sig = image_flowable(p.get("signature_path"), 1.5)
            if sig:
                story.append(Paragraph("Digital Signature:", styles['TableKey']))
                story.append(sig)
                story.append(Spacer(1, 0.2 * inch))

    # SPEAKER PROFILE
    story.append(Paragraph("Speaker Profile", styles['SectionTitle']))
    profile = data.get("speaker_profile", {})
    if profile.get("bio"):
        story.append(Paragraph(profile["bio"], styles['NormalText']))
        story.append(Spacer(1, 0.15 * inch))
    if profile.get("image_path"):
        img = image_flowable(profile["image_path"], 2.5)
        if img:
            story.append(img)
            story.append(Spacer(1, 0.15 * inch))

    # PHOTOS SECTION
    photos = data.get("photos", [])
    if photos:
        story.append(PageBreak())
        title = general_info.get("Title of the Activity", "")
        date_display = general_info.get("Date/s", "")
        story.append(Paragraph("Photos of the activity", styles["PhotoHeading"]))
        story.append(Paragraph(f"({title} – {date_display})", styles["PhotoHeading"]))
        story.append(Spacer(1, 0.2 * inch))

        for p in photos:
            img = image_flowable(p)
            if img:
                story.append(img)
                story.append(Spacer(1, 0.25 * inch))
    else:
        story.append(Paragraph("No photos available.", styles["NormalText"]))

    # BUILD
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=0.9 * inch,
        rightMargin=0.9 * inch,
        topMargin=0.9 * inch,
        bottomMargin=0.9 * inch
    )
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    pdf = buffer.getvalue()
    buffer.close()

    return pdf
