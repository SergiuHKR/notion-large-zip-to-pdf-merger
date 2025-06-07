import os
from PyPDF2 import PdfMerger

def merge_pdfs():
    # Create output directory if it doesn't exist
    if not os.path.exists('output'):
        os.makedirs('output')
    
    # Initialize PDF merger
    merger = PdfMerger()
    
    # Get all PDF files from input directory
    input_dir = 'input'
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("No PDF files found in the input directory!")
        return
    
    # Sort files to ensure consistent order
    pdf_files.sort()
    
    # Add each PDF to the merger
    for pdf in pdf_files:
        file_path = os.path.join(input_dir, pdf)
        try:
            merger.append(file_path)
            print(f"Added: {pdf}")
        except Exception as e:
            print(f"Error adding {pdf}: {str(e)}")
    
    # Write the merged PDF to output directory
    output_path = os.path.join('output', 'merged.pdf')
    try:
        merger.write(output_path)
        merger.close()
        print(f"\nSuccessfully merged {len(pdf_files)} PDFs into: {output_path}")
    except Exception as e:
        print(f"Error saving merged PDF: {str(e)}")

if __name__ == "__main__":
    merge_pdfs() 