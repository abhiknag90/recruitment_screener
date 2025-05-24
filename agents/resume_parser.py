from utils.openai_client import openai_client
from utils.file_handlers import FileHandler

class ResumeParserAgent:
    def __init__(self):
        self.name = "Resume Parser Agent"
    
    def parse_resume_file(self, file_path):
        """Parse resume file and extract structured information"""
        print(f"🔍 {self.name}: Parsing resume file...")
        
        # Extract text from file
        text = FileHandler.extract_text_from_file(file_path)
        if not text:
            return {"error": "Could not extract text from file"}
        
        # Parse using OpenAI
        parsed_data = openai_client.parse_resume(text)
        if not parsed_data:
            return {"error": "Could not parse resume with AI"}
        
        # Add metadata
        parsed_data["raw_text"] = text
        parsed_data["file_processed"] = True
        
        print(f"✅ {self.name}: Successfully parsed resume for {parsed_data.get('name', 'Unknown')}")
        return parsed_data
    
    def parse_resume_text(self, text):
        """Parse resume from raw text"""
        print(f"🔍 {self.name}: Parsing resume text...")
        
        parsed_data = openai_client.parse_resume(text)
        if not parsed_data:
            return {"error": "Could not parse resume with AI"}
        
        parsed_data["raw_text"] = text
        parsed_data["file_processed"] = False
        
        print(f"✅ {self.name}: Successfully parsed resume for {parsed_data.get('name', 'Unknown')}")
        return parsed_data
    
    def validate_parsed_data(self, data):
        """Validate that required fields are present"""
        required_fields = ['name', 'skills', 'experience']
        
        for field in required_fields:
            if field not in data or not data[field]:
                return False, f"Missing required field: {field}"
        
        return True, "Valid data"

# Create global instance
resume_parser = ResumeParserAgent()