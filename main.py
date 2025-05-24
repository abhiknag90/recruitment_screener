import streamlit as st

# IMPORTANT: set_page_config must be the FIRST Streamlit command
st.set_page_config(
    page_title="AI Recruitment Screener",
    page_icon="🎯",
    layout="wide"
)

import os
import sys
import json
from datetime import datetime

# Add current directory to Python path for Streamlit Cloud
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import agents
try:
    from agents.resume_parser import resume_parser
    from agents.skills_matcher import skills_matcher
    from agents.interview_generator import interview_generator
    from agents.candidate_ranker import candidate_ranker
    from utils.file_handlers import FileHandler
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.error("Please check if all required files are present in the repository.")
    st.stop()

class RecruitmentScreener:
    def __init__(self):
        self.results_history = []
    
    def process_single_candidate(self, resume_file, job_description):
        """Process a single candidate through all agents"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'candidate_data': None,
            'skills_match': None,
            'interview_questions': None,
            'final_ranking': None,
            'success': False
        }
        
        try:
            # Step 1: Parse Resume
            st.write("🔄 **Step 1: Parsing Resume...**")
            
            # Save uploaded file temporarily
            temp_file_path = FileHandler.save_uploaded_file(resume_file)
            if not temp_file_path:
                st.error("Failed to save uploaded file")
                return results
            
            # Parse resume
            candidate_data = resume_parser.parse_resume_file(temp_file_path)
            
            # Clean up temp file
            FileHandler.cleanup_temp_file(temp_file_path)
            
            if 'error' in candidate_data:
                st.error(f"Resume parsing failed: {candidate_data['error']}")
                return results
            
            results['candidate_data'] = candidate_data
            st.success(f"✅ Resume parsed for: **{candidate_data.get('name', 'Unknown')}**")
            
            # Step 2: Match Skills
            st.write("🔄 **Step 2: Matching Skills...**")
            
            job_requirements = skills_matcher.extract_job_requirements(job_description)
            skills_match = skills_matcher.calculate_match_score(
                candidate_data.get('skills', []),
                job_requirements
            )
            
            results['skills_match'] = skills_match
            st.success(f"✅ Skills match calculated: **{skills_match['match_score']}%**")
            
            # Step 3: Generate Interview Questions
            st.write("🔄 **Step 3: Generating Interview Questions...**")
            
            interview_questions = interview_generator.generate_questions(
                candidate_data,
                job_description
            )
            
            results['interview_questions'] = interview_questions
            st.success("✅ Interview questions generated")
            
            # Step 4: Calculate Final Ranking
            st.write("🔄 **Step 4: Calculating Final Score...**")
            
            final_ranking = candidate_ranker.calculate_final_score(
                candidate_data,
                skills_match,
                job_description
            )
            
            results['final_ranking'] = final_ranking
            results['success'] = True
            
            st.success(f"✅ Final score: **{final_ranking['final_score']}/100**")
            
        except Exception as e:
            st.error(f"Error processing candidate: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def display_results(self, results):
        """Display comprehensive results"""
        if not results['success']:
            st.error("Processing failed - no results to display")
            return
        
        candidate_data = results['candidate_data']
        skills_match = results['skills_match']
        questions = results['interview_questions']
        ranking = results['final_ranking']
        
        # Main Results Header
        st.header("📊 Screening Results")
        
        # Candidate Overview
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👤 Candidate Profile")
            st.write(f"**Name:** {candidate_data.get('name', 'N/A')}")
            st.write(f"**Email:** {candidate_data.get('email', 'N/A')}")
            st.write(f"**Phone:** {candidate_data.get('phone', 'N/A')}")
            st.write(f"**Experience:** {candidate_data.get('total_experience_years', 0)} years")
        
        with col2:
            st.subheader("🎯 Final Score")
            score = ranking['final_score']
            recommendation = ranking['recommendation']
            
            # Color-coded score display
            if score >= 80:
                st.success(f"## {score}/100")
                st.success(f"**{recommendation['status']}** - {recommendation['confidence']} Confidence")
            elif score >= 65:
                st.info(f"## {score}/100")
                st.info(f"**{recommendation['status']}** - {recommendation['confidence']} Confidence")
            elif score >= 50:
                st.warning(f"## {score}/100")
                st.warning(f"**{recommendation['status']}** - {recommendation['confidence']} Confidence")
            else:
                st.error(f"## {score}/100")
                st.error(f"**{recommendation['status']}** - {recommendation['confidence']} Confidence")
        
        # Skills Analysis
        st.subheader("🛠️ Skills Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**✅ Matched Skills**")
            matched_skills = skills_match.get('matched_skills', [])
            if matched_skills:
                for skill in matched_skills:
                    st.write(f"• {skill}")
            else:
                st.write("No direct matches found")
        
        with col2:
            st.write("**❌ Missing Skills**")
            missing_skills = skills_match.get('missing_skills', [])
            if missing_skills:
                for skill in missing_skills[:5]:  # Show top 5
                    st.write(f"• {skill}")
            else:
                st.write("No missing skills identified")
        
        with col3:
            st.write("**➕ Additional Skills**")
            additional_skills = skills_match.get('additional_skills', [])
            if additional_skills:
                for skill in additional_skills[:5]:  # Show top 5
                    st.write(f"• {skill}")
            else:
                st.write("No additional skills found")
        
        # Component Scores Breakdown
        st.subheader("📈 Score Breakdown")
        
        component_scores = ranking['component_scores']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Skills Match", f"{component_scores['skills_score']}/100")
        
        with col2:
            st.metric("Experience", f"{component_scores['experience_score']}/100")
        
        with col3:
            st.metric("Education", f"{component_scores['education_score']}/100")
        
        with col4:
            st.metric("Other Factors", f"{component_scores['additional_score']}/100")
        
        # Interview Questions
        st.subheader("❓ Suggested Interview Questions")
        
        tab1, tab2, tab3 = st.tabs(["Technical", "Behavioral", "Experience"])
        
        with tab1:
            technical_q = questions.get('technical_questions', [])
            if technical_q:
                for i, q in enumerate(technical_q, 1):
                    st.write(f"{i}. {q}")
            else:
                st.write("No technical questions generated")
        
        with tab2:
            behavioral_q = questions.get('behavioral_questions', [])
            if behavioral_q:
                for i, q in enumerate(behavioral_q, 1):
                    st.write(f"{i}. {q}")
            else:
                st.write("No behavioral questions generated")
        
        with tab3:
            experience_q = questions.get('experience_questions', [])
            if experience_q:
                for i, q in enumerate(experience_q, 1):
                    st.write(f"{i}. {q}")
            else:
                st.write("No experience questions generated")
        
        # Strengths and Improvements
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💪 Strengths")
            strengths = ranking.get('strengths', [])
            for strength in strengths:
                st.write(f"✅ {strength}")
        
        with col2:
            st.subheader("📚 Areas for Improvement")
            improvements = ranking.get('areas_for_improvement', [])
            for improvement in improvements:
                st.write(f"📈 {improvement}")
        
        # Next Steps
        st.subheader("🎯 Recommended Next Steps")
        st.info(f"**Action:** {recommendation['next_step']}")
        
        # Download Results
        st.subheader("💾 Export Results")
        
        # Prepare data for download
        export_data = {
            'candidate_name': candidate_data.get('name', 'Unknown'),
            'final_score': ranking['final_score'],
            'recommendation': recommendation['status'],
            'skills_match_score': skills_match['match_score'],
            'matched_skills': skills_match.get('matched_skills', []),
            'missing_skills': skills_match.get('missing_skills', []),
            'interview_questions': questions,
            'strengths': ranking.get('strengths', []),
            'improvements': ranking.get('areas_for_improvement', []),
            'timestamp': results['timestamp']
        }
        
        json_data = json.dumps(export_data, indent=2)
        
        st.download_button(
            label="📥 Download Results (JSON)",
            data=json_data,
            file_name=f"screening_results_{candidate_data.get('name', 'candidate')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

def main():
    st.title("🎯 AI Recruitment Screener")
    st.markdown("**Powered by Multi-Agent AI System**")
    
    # Sidebar for instructions
    with st.sidebar:
        st.header("📋 How to Use")
        st.markdown("""
        1. **Upload Resume**: PDF, DOCX, or TXT format
        2. **Enter Job Description**: Paste the job requirements
        3. **Click Process**: Let AI agents analyze the candidate
        4. **Review Results**: Get comprehensive screening report
        """)
        
        st.header("🤖 AI Agents")
        st.markdown("""
        - **Resume Parser**: Extracts structured data
        - **Skills Matcher**: Compares skills with job requirements
        - **Interview Generator**: Creates relevant questions
        - **Candidate Ranker**: Provides final scoring
        """)
        
        st.header("⚙️ Settings")
        if st.button("Clear History"):
            st.session_state.clear()
            st.success("History cleared!")
    
    # Main interface
    screener = RecruitmentScreener()
    
    # Input section
    st.header("📝 Input")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📄 Upload Resume")
        uploaded_file = st.file_uploader(
            "Choose resume file",
            type=['pdf', 'docx', 'txt'],
            help="Upload candidate's resume in PDF, DOCX, or TXT format"
        )
    
    with col2:
        st.subheader("💼 Job Description")
        job_description = st.text_area(
            "Enter job description and requirements",
            height=200,
            placeholder="Paste the job description here including required skills, experience, and qualifications..."
        )
    
    # Process button
    if st.button("🚀 Process Candidate", type="primary", use_container_width=True):
        if not uploaded_file:
            st.error("Please upload a resume file")
        elif not job_description.strip():
            st.error("Please enter a job description")
        else:
            # Show progress
            with st.spinner("Processing candidate through AI agents..."):
                results = screener.process_single_candidate(uploaded_file, job_description)
            
            # Store results in session state
            st.session_state['last_results'] = results
            
            # Display results
            if results['success']:
                screener.display_results(results)
            else:
                st.error("Processing failed. Please try again.")
    
    # Display previous results if available
    if 'last_results' in st.session_state and st.session_state['last_results']['success']:
        st.header("📊 Previous Results")
        if st.button("Show Last Results"):
            screener.display_results(st.session_state['last_results'])

if __name__ == "__main__":
    main()