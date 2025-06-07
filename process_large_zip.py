import os
import zipfile
import tempfile
import shutil
from pathlib import Path
from PyPDF2 import PdfMerger
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PDFProcessor:
    def __init__(self, zip_path, output_dir, max_size_mb=19):
        self.zip_path = zip_path
        self.output_dir = Path(output_dir)
        self.max_size_bytes = max_size_mb * 1024 * 1024  # Convert MB to bytes
        self.temp_dir = None
        self.current_merger = None
        self.current_size = 0
        self.merge_count = 0
        
    def setup(self):
        """Create necessary directories and initialize temporary storage"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir = Path(tempfile.mkdtemp())
        logging.info(f"Created temporary directory at {self.temp_dir}")
        
    def cleanup(self):
        """Clean up temporary files"""
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            logging.info("Cleaned up temporary directory")
            
    def get_pdf_size(self, pdf_path):
        """Get the size of a PDF file in bytes"""
        return os.path.getsize(pdf_path)
        
    def start_new_merge(self):
        """Initialize a new PDF merger"""
        if self.current_merger:
            self.save_current_merge()
        self.current_merger = PdfMerger()
        self.current_size = 0
        self.merge_count += 1
        
    def save_current_merge(self):
        """Save the current merged PDF"""
        if not self.current_merger:
            return
            
        output_path = self.output_dir / f"merged_{self.merge_count}.pdf"
        try:
            self.current_merger.write(str(output_path))
            logging.info(f"Saved merged PDF: {output_path}")
        finally:
            self.current_merger.close()
            self.current_merger = None
        
    def process_pdf(self, pdf_path):
        """Process a single PDF file"""
        pdf_size = self.get_pdf_size(pdf_path)
        
        # If single PDF is larger than max size, we need to handle it differently
        if pdf_size > self.max_size_bytes:
            logging.warning(f"PDF {pdf_path} is larger than max size. Consider splitting it.")
            return
            
        if self.current_size + pdf_size > self.max_size_bytes:
            self.save_current_merge()
            self.start_new_merge()
            
        if not self.current_merger:
            self.start_new_merge()
            
        try:
            self.current_merger.append(str(pdf_path))
            self.current_size += pdf_size
        except Exception as e:
            logging.error(f"Error processing PDF {pdf_path}: {str(e)}")
            self.save_current_merge()
            self.start_new_merge()
        
    def process_zip(self):
        """Process the ZIP file and merge PDFs"""
        try:
            self.setup()
            
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                # Extract only PDF files
                pdf_files = [f for f in zip_ref.namelist() if f.lower().endswith('.pdf')]
                logging.info(f"Found {len(pdf_files)} PDF files to process")
                
                for pdf_file in pdf_files:
                    # Extract to temporary directory
                    temp_pdf_path = self.temp_dir / Path(pdf_file).name
                    with zip_ref.open(pdf_file) as source, open(temp_pdf_path, 'wb') as target:
                        shutil.copyfileobj(source, target)
                    
                    self.process_pdf(temp_pdf_path)
                    
                    # Clean up the extracted file
                    temp_pdf_path.unlink()
            
            # Save the last merge if there is one
            if self.current_merger:
                self.save_current_merge()
                
        finally:
            self.cleanup()

def main():
    input_dir = Path("input")
    output_dir = Path("output")
    
    # Find the ZIP file in the input directory
    zip_files = list(input_dir.glob("*.zip"))
    if not zip_files:
        logging.error("No ZIP file found in input directory")
        return
        
    zip_path = zip_files[0]
    logging.info(f"Processing ZIP file: {zip_path}")
    
    processor = PDFProcessor(zip_path, output_dir)
    processor.process_zip()
    
if __name__ == "__main__":
    main() 