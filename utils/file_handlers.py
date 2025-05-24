import PyPDF2
from docx import Document
import os
import tempfile

class FileHandler:
    @staticmethod
    def extract_text_from_pdf(file_path):
        """Extract text from PDF file"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return None
    
    @staticmethod
    def extract_text_from_docx(file_path):
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error reading DOCX: {e}")
            return None
    
    @staticmethod
    def extract_text_from_txt(file_path):
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except Exception as e:
            print(f"Error reading TXT: {e}")
            return None
    
    @staticmethod
    def extract_text_from_file(file_path):
        """Extract text from file based on extension"""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return FileHandler.extract_text_from_pdf(file_path)
        elif file_extension == '.docx':
            return FileHandler.extract_text_from_docx(file_path)
        elif file_extension == '.txt':
            return FileHandler.extract_text_from_txt(file_path)
        else:
            return None
    
    @staticmethod
    def save_uploaded_file(uploaded_file):
        """Save uploaded file temporarily and return path"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                return tmp_file.name
        except Exception as e:
            print(f"Error saving file: {e}")
            return None
    
    @staticmethod
    def cleanup_temp_file(file_path):
        """Clean up temporary file"""
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error cleaning up file: {e}")