
from Preprocessing_Parsing import ResumeProcessor

class Job_Description:
    def jd_skill(self,jd):
        resume_processor = ResumeProcessor()
        resume_processor.load_skill_patterns("D:\\Designing\\experimento\\jz_skill_patterns.jsonl")
        jd_skills = resume_processor.extracting_entities(jd)["SKILL"]
        return jd_skills

    def find_not_in_resume(self,resume, jd):
        resume_processor = ResumeProcessor()
        resume_processor.load_skill_patterns("D:\\Designing\\experimento\\jz_skill_patterns.jsonl")
        # Extract Resume Skills
        resume_skills = resume_processor.extracting_entities(resume)["SKILL"]
        # Extracting Job Description Skills
        jd_skills = resume_processor.extracting_entities(jd)["SKILL"]
        return [skill for skill in jd_skills if skill not in resume_skills]
        