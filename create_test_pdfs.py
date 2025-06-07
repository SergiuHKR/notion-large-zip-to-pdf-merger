from reportlab.pdfgen import canvas
import os

def create_test_pdf(filename, text):
    c = canvas.Canvas(filename)
    c.drawString(100, 750, text)
    c.save()

# Create input directory if it doesn't exist
if not os.path.exists('input'):
    os.makedirs('input')

# Create three test PDFs
create_test_pdf('input/test1.pdf', 'This is test PDF 1')
create_test_pdf('input/test2.pdf', 'This is test PDF 2')
create_test_pdf('input/test3.pdf', 'This is test PDF 3')

print("Created test PDFs in the input folder") 