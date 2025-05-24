from utils.openai_client import openai_client
import re

class SkillsMatcherAgent:
    def __init__(self):
        self.name = "Skills Matcher Agent"
    
    def extract_job_requirements(self, job_description):
        """Extract skills and requirements from job description"""
        print(f"🔍 {self.name}: Extracting job requirements...")
        
        # Simple keyword extraction (can be enhanced with AI)
        common_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git',
            'sql', 'mongodb', 'postgresql', 'mysql', 'redis',
            'machine learning', 'data science', 'artificial intelligence',
            'html', 'css', 'bootstrap', 'tailwind', 'sass',
            'django', 'flask', 'spring', 'express', '.net',
            'agile', 'scrum', 'devops', 'ci/cd', 'testing'
        ]
        
        job_lower = job_description.lower()
        found_skills = []
        
        for skill in common_skills:
            if skill in job_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def calculate_match_score(self, candidate_skills, job_requirements):
        """Calculate how well candidate skills match job requirements"""
        print(f"🔍 {self.name}: Calculating skill match score...")
        
        # Use AI for intelligent matching
        match_result = openai_client.match_skills(candidate_skills, job_requirements)
        
        if match_result:
            print(f"✅ {self.name}: Match score calculated - {match_result['match_score']}%")
            return match_result
        
        # Fallback to basic matching if AI fails
        return self._basic_skill_matching(candidate_skills, job_requirements)
    
    def _basic_skill_matching(self, candidate_skills, job_requirements):
        """Basic skill matching as fallback"""
        if not candidate_skills or not job_requirements:
            return {
                "match_score": 0,
                "matched_skills": [],
                "missing_skills": job_requirements if job_requirements else [],
                "additional_skills": candidate_skills if candidate_skills else [],
                "explanation": "No skills to compare"
            }
        
        # Convert to lowercase for comparison
        candidate_lower = [skill.lower() for skill in candidate_skills]
        job_lower = [skill.lower() for skill in job_requirements]
        
        # Find matches
        matched = []
        for job_skill in job_lower:
            for candidate_skill in candidate_lower:
                if job_skill in candidate_skill or candidate_skill in job_skill:
                    matched.append(job_skill)
                    break
        
        # Calculate score
        if job_requirements:
            match_score = int((len(matched) / len(job_requirements)) * 100)
        else:
            match_score = 0
        
        # Find missing and additional skills
        missing = [skill for skill in job_requirements if skill.lower() not in [m.lower() for m in matched]]
        additional = [skill for skill in candidate_skills if skill.lower() not in job_lower]
        
        return {
            "match_score": match_score,
            "matched_skills": matched,
            "missing_skills": missing,
            "additional_skills": additional,
            "explanation": f"Matched {len(matched)} out of {len(job_requirements)} required skills"
        }
    
    def get_skill_recommendations(self, missing_skills):
        """Get recommendations for missing skills"""
        if not missing_skills:
            return []
        
        recommendations = []
        for skill in missing_skills[:5]:  # Top 5 missing skills
            recommendations.append({
                "skill": skill,
                "priority": "High" if skill.lower() in ['python', 'javascript', 'sql', 'aws'] else "Medium",
                "learning_resource": f"Consider learning {skill} through online courses"
            })
        
        return recommendations

# Create global instance
skills_matcher = SkillsMatcherAgent()