from utils.openai_client import openai_client

class InterviewGeneratorAgent:
    def __init__(self):
        self.name = "Interview Generator Agent"
    
    def generate_questions(self, candidate_data, job_description, num_questions=3):
        """Generate interview questions based on candidate and job"""
        print(f"🔍 {self.name}: Generating interview questions...")
        
        # Use AI to generate questions
        questions = openai_client.generate_interview_questions(candidate_data, job_description)
        
        if questions:
            print(f"✅ {self.name}: Generated {len(questions.get('technical_questions', []))} technical questions")
            return questions
        
        # Fallback to template questions
        return self._generate_template_questions(candidate_data, job_description)
    
    def _generate_template_questions(self, candidate_data, job_description):
        """Generate template questions as fallback"""
        skills = candidate_data.get('skills', [])
        experience = candidate_data.get('experience', [])
        
        technical_questions = []
        behavioral_questions = []
        experience_questions = []
        
        # Technical questions based on skills
        if 'python' in [s.lower() for s in skills]:
            technical_questions.append("Can you explain the difference between lists and tuples in Python?")
        if 'javascript' in [s.lower() for s in skills]:
            technical_questions.append("What is the difference between let, const, and var in JavaScript?")
        if 'sql' in [s.lower() for s in skills]:
            technical_questions.append("How would you optimize a slow-running SQL query?")
        
        # Add generic technical questions if none matched
        if not technical_questions:
            technical_questions = [
                "Walk me through how you would approach solving a complex technical problem.",
                "Describe a challenging project you worked on and how you overcame difficulties.",
                "How do you stay updated with new technologies in your field?"
            ]
        
        # Behavioral questions
        behavioral_questions = [
            "Tell me about a time when you had to work with a difficult team member.",
            "Describe a situation where you had to learn something new quickly.",
            "How do you handle tight deadlines and pressure?"
        ]
        
        # Experience questions
        if experience:
            experience_questions = [
                f"I see you worked at {experience[0].get('company', 'your previous company')}. What was your biggest achievement there?",
                "What motivates you to switch to a new role?",
                "Where do you see yourself in 5 years?"
            ]
        else:
            experience_questions = [
                "What interests you most about this role?",
                "What are your career goals?",
                "Why are you looking for a new opportunity?"
            ]
        
        return {
            "technical_questions": technical_questions[:3],
            "behavioral_questions": behavioral_questions[:3],
            "experience_questions": experience_questions[:3]
        }
    
    def customize_questions_by_role(self, questions, role_type):
        """Customize questions based on role type"""
        role_specific = {
            "software_engineer": {
                "technical": ["Explain your approach to code review and testing"],
                "behavioral": ["How do you handle technical debt in your projects?"]
            },
            "data_scientist": {
                "technical": ["How do you handle missing data in your datasets?"],
                "behavioral": ["Describe how you communicate complex findings to non-technical stakeholders"]
            },
            "product_manager": {
                "technical": ["How do you prioritize features in a product roadmap?"],
                "behavioral": ["Tell me about a time you had to make a decision with incomplete information"]
            }
        }
        
        # Add role-specific questions if role is identified
        if role_type.lower() in role_specific:
            questions["technical_questions"].extend(role_specific[role_type.lower()]["technical"])
            questions["behavioral_questions"].extend(role_specific[role_type.lower()]["behavioral"])
        
        return questions

# Create global instance
interview_generator = InterviewGeneratorAgent()