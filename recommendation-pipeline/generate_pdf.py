from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

root = Path(r'c:\Users\krish_zha4a61\OneDrive\Documents\BITS\Data_Management\vs_assignment2\recommendation-pipeline')
md_path = root / 'docs' / 'final_report.md'
pdf_path = root / 'docs' / 'final_report.pdf'

styles = getSampleStyleSheet()
story = []
for line in md_path.read_text(encoding='utf-8').splitlines():
    story.append(Paragraph(line.replace('&', '&amp;'), styles['BodyText']))
    story.append(Spacer(1, 8))

doc = SimpleDocTemplate(
    str(pdf_path),
    pagesize=letter,
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40,
)
doc.build(story)
print(f'Generated PDF report at {pdf_path}')
