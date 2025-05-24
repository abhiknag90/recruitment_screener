#!/usr/bin/env python3
"""
Test script for AI Recruitment Screener
Run this to verify your setup is working correctly
"""

import os
from dotenv import load_dotenv

def test_environment():
    """Test environment setup"""
    print("🔍 Testing Environment Setup...")
    
    # Load environment variables
    load_dotenv()
    
    # Check OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your_openai_api_key_here':
        print("❌ OpenAI API key not set properly in .env file")
        return False
    else:
        print("✅ OpenAI API key found")
    
    return True

def test_imports():
    """Test if all modules can be imported"""
    print("\n🔍 Testing Module Imports...")
    
    try:
        from agents.resume_parser import resume_parser
        print("✅ Resume Parser Agent imported")
        
        from agents.skills_matcher import skills_matcher
        print("✅ Skills Matcher Agent imported")
        
        from agents.interview_generator import interview_generator
        print("✅ Interview Generator Agent imported")
        
        from agents.candidate_ranker import candidate_ranker
        print("✅ Candidate Ranker Agent imported")
        
        from utils.openai_client import openai_client
        print("✅ OpenAI Client imported")
        
        from utils.file_handlers import FileHandler
        print("✅ File Handler imported")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_openai_connection():
    """Test OpenAI API connection"""
    print("\n🔍 Testing OpenAI Connection...")
    
    try:
        from utils.openai_client import openai_client
        
        if not openai_client or not openai_client.client:
            print("❌ OpenAI client not initialized properly")
            return False
        
        # Simple test message
        messages = [
            {"role": "user", "content": "Hello, this is a test. Reply with 'Test successful'"}
        ]
        
        response = openai_client.chat_completion(messages)
        
        if response:
            print("✅ OpenAI API connection successful")
            print(f"Response: {response}")
            return True
        else:
            print("❌ OpenAI API connection failed - no response")
            return False
            
    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
        return False

def test_file_processing():
    """Test file processing capabilities"""
    print("\n🔍 Testing File Processing...")
    
    try:
        from utils.file_handlers import FileHandler
        
        # Create a test text file
        test_content = """
        John Doe
        Software Engineer
        Email: john.doe@email.com
        Phone: (555) 123-4567
        
        Skills: Python, JavaScript, React, SQL
        
        Experience:
        - Software Engineer at TechCorp (2 years)
        - Built web applications using React and Python
        - Managed database systems
        
        Education:
        - Bachelor of Science in Computer Science
        """
        
        # Write test file
        with open('test_resume.txt', 'w') as f:
            f.write(test_content)
        
        # Test extraction
        extracted_text = FileHandler.extract_text_from_file('test_resume.txt')
        
        if extracted_text:
            print("✅ File processing successful")
            print(f"Extracted {len(extracted_text)} characters")
        else:
            print("❌ File processing failed")
            return False
        
        # Clean up
        os.remove('test_resume.txt')
        return True
        
    except Exception as e:
        print(f"❌ File processing error: {e}")
        return False

def test_resume_parsing():
    """Test resume parsing with AI"""
    print("\n🔍 Testing Resume Parsing...")
    
    try:
        from agents.resume_parser import resume_parser
        
        test_resume = """
        Jane Smith
        Senior Data Scientist
        jane.smith@email.com
        (555) 987-6543
        
        Skills: Python, Machine Learning, TensorFlow, SQL, R
        
        Experience:
        - Senior Data Scientist at DataCorp (3 years)
        - Built ML models for prediction and classification
        - Analyzed large datasets using Python and R
        
        Education:
        - Master of Science in Data Science
        """
        
        result = resume_parser.parse_resume_text(test_resume)
        
        if result and 'error' not in result:
            print("✅ Resume parsing successful")
            print(f"Parsed candidate: {result.get('name', 'Unknown')}")
            print(f"Skills found: {len(result.get('skills', []))}")
            return True
        else:
            print("❌ Resume parsing failed")
            return False
            
    except Exception as e:
        print(f"❌ Resume parsing error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 AI Recruitment Screener - System Test")
    print("=" * 50)
    
    tests = [
        test_environment,
        test_imports,
        test_openai_connection,
        test_file_processing,
        test_resume_parsing
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your system is ready.")
        print("\nTo start the application, run:")
        print("streamlit run main.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nCommon fixes:")
        print("1. Make sure your OpenAI API key is set in .env file")
        print("2. Install all dependencies: pip install -r requirements.txt")
        print("3. Check your internet connection")

if __name__ == "__main__":
    main()