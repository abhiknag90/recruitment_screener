class CandidateRankerAgent:
    def __init__(self):
        self.name = "Candidate Ranker Agent"
        self.weights = {
            'skills_match': 0.4,      # 40% weight
            'experience': 0.3,        # 30% weight
            'education': 0.15,        # 15% weight
            'additional_factors': 0.15 # 15% weight
        }
    
    def calculate_final_score(self, candidate_data, skills_match_result, job_description=""):
        """Calculate final score for candidate"""
        print(f"🔍 {self.name}: Calculating final candidate score...")
        
        scores = {
            'skills_score': self._calculate_skills_score(skills_match_result),
            'experience_score': self._calculate_experience_score(candidate_data),
            'education_score': self._calculate_education_score(candidate_data),
            'additional_score': self._calculate_additional_score(candidate_data)
        }
        
        # Calculate weighted final score
        final_score = (
            scores['skills_score'] * self.weights['skills_match'] +
            scores['experience_score'] * self.weights['experience'] +
            scores['education_score'] * self.weights['education'] +
            scores['additional_score'] * self.weights['additional_factors']
        )
        
        # Generate recommendation
        recommendation = self._generate_recommendation(final_score, scores)
        
        result = {
            'final_score': round(final_score, 1),
            'component_scores': scores,
            'recommendation': recommendation,
            'strengths': self._identify_strengths(scores, candidate_data),
            'areas_for_improvement': self._identify_improvements(scores, skills_match_result)
        }
        
        print(f"✅ {self.name}: Final score calculated - {result['final_score']}/100")
        return result
    
    def _calculate_skills_score(self, skills_match_result):
        """Calculate skills matching score"""
        if not skills_match_result:
            return 0
        return skills_match_result.get('match_score', 0)
    
    def _calculate_experience_score(self, candidate_data):
        """Calculate experience score based on years and relevance"""
        experience = candidate_data.get('experience', [])
        total_years = candidate_data.get('total_experience_years', 0)
        
        if not experience and total_years == 0:
            return 20  # Entry level
        
        # Base score on years of experience
        if total_years <= 1:
            base_score = 30
        elif total_years <= 3:
            base_score = 50
        elif total_years <= 5:
            base_score = 70
        elif total_years <= 10:
            base_score = 85
        else:
            base_score = 95
        
        # Bonus for number of different companies/roles
        diversity_bonus = min(len(experience) * 5, 15)
        
        return min(base_score + diversity_bonus, 100)
    
    def _calculate_education_score(self, candidate_data):
        """Calculate education score"""
        education = candidate_data.get('education', [])
        
        if not education:
            return 40  # Some points for work experience
        
        education_text = ' '.join(education).lower()
        
        # Score based on degree level
        if 'phd' in education_text or 'doctorate' in education_text:
            return 100
        elif 'master' in education_text or 'mba' in education_text:
            return 85
        elif 'bachelor' in education_text or 'degree' in education_text:
            return 75
        elif 'associate' in education_text or 'diploma' in education_text:
            return 60
        else:
            return 50
    
    def _calculate_additional_score(self, candidate_data):
        """Calculate score for additional factors"""
        score = 50  # Base score
        
        # Email presence
        if candidate_data.get('email'):
            score += 10
        
        # Phone presence
        if candidate_data.get('phone'):
            score += 10
        
        # Skills diversity
        skills = candidate_data.get('skills', [])
        if len(skills) > 5:
            score += 15
        elif len(skills) > 3:
            score += 10
        
        # Experience descriptions
        experience = candidate_data.get('experience', [])
        if experience and any(exp.get('responsibilities') for exp in experience):
            score += 15
        
        return min(score, 100)
    
    def _generate_recommendation(self, final_score, scores):
        """Generate hiring recommendation"""
        if final_score >= 80:
            return {
                'status': 'Strong Hire',
                'confidence': 'High',
                'next_step': 'Schedule technical interview immediately'
            }
        elif final_score >= 65:
            return {
                'status': 'Hire',
                'confidence': 'Medium-High',
                'next_step': 'Schedule phone screening followed by technical interview'
            }
        elif final_score >= 50:
            return {
                'status': 'Maybe',
                'confidence': 'Medium',
                'next_step': 'Phone screening to assess cultural fit and communication'
            }
        else:
            return {
                'status': 'Pass',
                'confidence': 'Low',
                'next_step': 'Send polite rejection email'
            }
    
    def _identify_strengths(self, scores, candidate_data):
        """Identify candidate strengths"""
        strengths = []
        
        if scores['skills_score'] >= 70:
            strengths.append("Strong technical skill match")
        
        if scores['experience_score'] >= 70:
            strengths.append("Relevant work experience")
        
        if scores['education_score'] >= 80:
            strengths.append("Strong educational background")
        
        skills = candidate_data.get('skills', [])
        if len(skills) > 8:
            strengths.append("Diverse technical skill set")
        
        if not strengths:
            strengths.append("Potential for growth")
        
        return strengths
    
    def _identify_improvements(self, scores, skills_match_result):
        """Identify areas for improvement"""
        improvements = []
        
        if scores['skills_score'] < 50:
            improvements.append("Technical skills need development")
        
        if scores['experience_score'] < 50:
            improvements.append("Limited relevant experience")
        
        missing_skills = skills_match_result.get('missing_skills', [])
        if missing_skills:
            improvements.append(f"Missing key skills: {', '.join(missing_skills[:3])}")
        
        return improvements
    
    def rank_multiple_candidates(self, candidates_results):
        """Rank multiple candidates by their scores"""
        print(f"🔍 {self.name}: Ranking {len(candidates_results)} candidates...")
        
        # Sort by final score (descending)
        ranked = sorted(candidates_results, key=lambda x: x['final_score'], reverse=True)
        
        # Add rank to each candidate
        for i, candidate in enumerate(ranked):
            candidate['rank'] = i + 1
        
        print(f"✅ {self.name}: Candidates ranked successfully")
        return ranked

# Create global instance
candidate_ranker = CandidateRankerAgent()