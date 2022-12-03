from PIL import Image
import pytesseract

# Get a searchable PDF
pdf = pytesseract.image_to_pdf_or_hocr(
    '/Users/jone30rw/Desktop/test1.png', extension='pdf')
with open('/Users/jone30rw/Desktop/test-ocr1.pdf', 'w+b') as f:
    f.write(pdf)  # pdf type is bytes by default
