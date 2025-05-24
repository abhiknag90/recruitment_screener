import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

class OpenAIClient:
    def __init__(self):
        # Get API key - prioritize environment variable to avoid early Streamlit import
        api_key = os.getenv('OPENAI_API_KEY')
        
        # Only try Streamlit secrets if env var is not found
        if not api_key:
            try:
                import streamlit as st
                api_key = st.secrets.get("OPENAI_API_KEY")
            except:
                pass
        
        if not api_key:
            print("Warning: OpenAI API key not found.")
            self.client = None
            return
        
        # Import OpenAI here to catch import errors
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
            print("✅ OpenAI client initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing OpenAI client: {e}")
            self.client = None
    
    def chat_completion(self, messages, model="gpt-3.5-turbo", temperature=0.7):
        """Generic chat completion method"""
        if not self.client:
            print("OpenAI client not initialized")
            return None
            
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            return None
    
    def parse_resume(self, resume_text):
        """Parse resume using OpenAI"""
        messages = [
            {
                "role": "system",
                "content": """You are a resume parser. Extract structured information from resumes and return it as valid JSON.
                
                Required JSON format:
                {
                    "name": "Full Name",
                    "email": "email@example.com",
                    "phone": "phone number",
                    "skills": ["skill1", "skill2", "skill3"],
                    "experience": [
                        {
                            "company": "Company Name",
                            "role": "Job Title",
                            "duration": "X years/months",
                            "responsibilities": ["responsibility1", "responsibility2"]
                        }
                    ],
                    "education": ["Degree/Institution"],
                    "total_experience_years": 0
                }
                
                If information is not found, use null or empty arrays."""
            },
            {
                "role": "user",
                "content": f"Parse this resume:\n\n{resume_text}"
            }
        ]
        
        response = self.chat_completion(messages, temperature=0.3)
        if not response:
            return None
            
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return None
    
    def match_skills(self, candidate_skills, job_requirements):
        """Match candidate skills with job requirements"""
        messages = [
            {
                "role": "system",
                "content": """You are a skills matching expert. Compare candidate skills with job requirements.
                
                Return JSON with:
                {
                    "match_score": 0-100,
                    "matched_skills": ["skill1", "skill2"],
                    "missing_skills": ["skill3", "skill4"],
                    "additional_skills": ["skill5", "skill6"],
                    "explanation": "Brief explanation of the match"
                }"""
            },
            {
                "role": "user",
                "content": f"Candidate Skills: {candidate_skills}\n\nJob Requirements: {job_requirements}"
            }
        ]
        
        response = self.chat_completion(messages, temperature=0.3)
        if not response:
            return {"match_score": 0, "matched_skills": [], "missing_skills": [], "additional_skills": [], "explanation": "Error in analysis"}
            
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"match_score": 0, "matched_skills": [], "missing_skills": [], "additional_skills": [], "explanation": "Error in analysis"}
    
    def generate_interview_questions(self, candidate_data, job_description):
        """Generate interview questions based on candidate and job"""
        messages = [
            {
                "role": "system",
                "content": """Generate relevant interview questions based on the candidate's background and job requirements.
                
                Return JSON with:
                {
                    "technical_questions": ["question1", "question2"],
                    "behavioral_questions": ["question1", "question2"],
                    "experience_questions": ["question1", "question2"]
                }"""
            },
            {
                "role": "user",
                "content": f"Candidate: {candidate_data}\n\nJob Description: {job_description}"
            }
        ]
        
        response = self.chat_completion(messages, temperature=0.7)
        if not response:
            return {"technical_questions": [], "behavioral_questions": [], "experience_questions": []}
            
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"technical_questions": [], "behavioral_questions": [], "experience_questions": []}

# Create global instance with error handling
openai_client = None
try:
    openai_client = OpenAIClient()
except Exception as e:
    print(f"Error creating OpenAI client: {e}")
    openai_client = None