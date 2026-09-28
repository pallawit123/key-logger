from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from pathlib import Path
import shutil
import os
import sys

# User details
FULL_NAME = "Pallav Timalsina"
DOMAIN = "Cybersecurity"
EMAIL = "pallawit948@gmail.com"
PHONE = "[PHONE]"
SUFFIX = "Month1"

WORKSPACE = Path(__file__).resolve().parent
DOCX_NAME = f"{FULL_NAME.replace(' ', '_')}_{DOMAIN}_{SUFFIX}.docx"
PDF_NAME = f"{FULL_NAME.replace(' ', '_')}_{DOMAIN}_{SUFFIX}.pdf"

LOG_FILE = WORKSPACE / "keystrokes_demo.log"
SOURCE_CODE = WORKSPACE / "safe_keylogger_demo.py"
SCREENSHOTS = [p for p in WORKSPACE.iterdir() if p.suffix.lower() in ['.png', '.jpg', '.jpeg']]

# Create document
doc = Document()

# Front page
doc.add_heading('Safe Keystroke Capture Demo (Window-Limited)', level=0)
p = doc.add_paragraph()
run = p.add_run(f"\nFull Name: {FULL_NAME}\n")
run.font.size = Pt(12)
run = p.add_run(f"Internship Domain: {DOMAIN}\n")
run.font.size = Pt(12)
run = p.add_run(f"Email: {EMAIL}\n")
run.font.size = Pt(12)
run = p.add_run(f"Phone: {PHONE}\n")
run.font.size = Pt(12)

# Table of contents placeholder
doc.add_page_break()

doc.add_heading('Executive Summary', level=1)
doc.add_paragraph('This project demonstrates a safe, window-limited keystroke capture demo implemented in Python using Tkinter. It is intended for educational purposes only — to show how key events can be captured inside an application window, how logs are recorded, and to highlight the risks and mitigations for keylogging attacks. The demo explicitly requires user interaction to start logging and only records keystrokes typed into its own text area.')

doc.add_heading('Environment & Tools', level=1)
doc.add_paragraph('- OS: Windows (tested)')
doc.add_paragraph('- Python: 3.10+ (Tkinter included in standard installers)')
doc.add_paragraph('- Libraries: Python standard library (tkinter, datetime, pathlib, sys)')

doc.add_heading('Design & Implementation', level=1)
doc.add_paragraph('The application is a Tkinter GUI that contains a text widget, a Start/Stop Logging button, and status/paths. It logs keystrokes typed into the text widget while logging is enabled. Timestamps are timezone-aware UTC and writes are wrapped in try/except.')

doc.add_heading('Code Listing', level=1)
if SOURCE_CODE.exists():
    doc.add_paragraph(SOURCE_CODE.name)
    with SOURCE_CODE.open('r', encoding='utf-8') as f:
        code = f.read()
    pre = doc.add_paragraph()
    run = pre.add_run(code)
    run.font.name = 'Courier New'
    run.font.size = Pt(9)
else:
    doc.add_paragraph('Source code not found.')


doc.add_heading('Testing & Results', level=1)
doc.add_paragraph('Run the script with:')
codep = doc.add_paragraph()
codep.add_run('python safe_keylogger_demo.py')

if LOG_FILE.exists():
    doc.add_paragraph('Sample log output:')
    with LOG_FILE.open('r', encoding='utf-8') as f:
        lines = f.readlines()[-10:]
    for line in lines:
        doc.add_paragraph(line.strip())

if SCREENSHOTS:
    doc.add_heading('Screenshots', level=1)
    for img in SCREENSHOTS:
        doc.add_paragraph(img.name)
        try:
            doc.add_picture(str(img), width=Inches(6))
        except Exception as e:
            doc.add_paragraph(f'Could not insert image {img.name}: {e}')


doc.add_heading('Risks, Legal & Ethical Considerations', level=1)
doc.add_paragraph('Capturing keystrokes without clear, informed consent is illegal in many jurisdictions and is a serious privacy violation. This demo is for learning only. Do not deploy it against other users or production systems.')

doc.add_heading('Recommendations', level=1)
doc.add_paragraph('- Use MFA, password managers, EDR, application allowlisting, and user education to mitigate keylogger risks.')

# Save docx
docx_path = WORKSPACE / DOCX_NAME
pdf_path = WORKSPACE / PDF_NAME

doc.save(docx_path)
print(f'Created {docx_path}')

# Convert to PDF if docx2pdf is available
try:
    import subprocess
    # Using libreoffice for conversion if available
    if shutil.which('soffice'):
        subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', str(docx_path), '--outdir', str(WORKSPACE)], check=True)
        print(f'Converted to PDF at {pdf_path}')
    else:
        print('LibreOffice not found; PDF conversion skipped. You can convert the DOCX to PDF manually.')
except Exception as e:
    print('PDF conversion failed or not available:', e)
