import os
import pdfplumber

class PDFProcessor:
    def extract_text(self, pdf_path):
        """Extracts text from a PDF file."""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
            
        text_content = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text_content += extracted + "\n"
            return text_content.strip()
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {e}")
