import streamlit as st
from streamlit_option_menu import option_menu
import docx2txt
import os
import spacy
from spacy import displacy
import base64
from PIL import Image
import nltk
from Base import BaseATS

from Preprocessing_Parsing import ResumeProcessor
from JD import Job_Description
from Match import Matching

Base_ATS = BaseATS()
Job_Des = Job_Description()
Scoring = Matching()

def main():

    # Get the absolute path of the currently executing Python script in Streamlit
    script_path = os.path.realpath(__file__)
    # Get the folder path from the script path
    folder_path = os.path.dirname(script_path)
    json_path = folder_path+"/JSON"

    with st.sidebar:
        choice = option_menu("Main Menu", ["Home", "ATS Matcher", "FeedBack Page","About Us" ], 
            icons=['house', 'cloud-upload', 'gear', 'people'], menu_icon="list", default_index=0)

    if choice=="Home":
        
        st.title("Application Tracking System")

        intro = "Welcome to our Applicant Tracking System (ATS), a tool that makes hiring easier. If your an employer our system simplifies the recruitment process which is usually manual in nature. "
        intro1 = "We use advanced natural language processing (NLP) to analyze resumes and job descriptions, offering valuable insights for better hiring decisions. Explore the features to streamline your recruitment journey."
        st.markdown(intro, unsafe_allow_html=True)
        st.markdown(intro1, unsafe_allow_html=True)

        st.subheader('Key Features')
        intro2 = "1. Files Format Supported: Easily upload resumes and job descriptions in various formats, such as PDF, DOCX, and TXT. "
        intro3 = "2. Text Processing: Effortlessly extract and review the content of uploaded resumes and job descriptions with just a click. "
        intro4 = "3. Analysis and Comparison: Identify common words between resumes and job descriptions, enabling quick match analysis."
        intro5 = "4. ATS Functionality: Utilize advanced features, such as keyword matching and scoring, to efficiently assess candidate suitability."
        intro6 = "5. Reliability: The tool doesn't store any of your precious data, ensuring the privacy of your information remains intact."
        st.markdown(intro2, unsafe_allow_html=True)
        st.markdown(intro3, unsafe_allow_html=True)
        st.markdown(intro4, unsafe_allow_html=True)
        st.markdown(intro5, unsafe_allow_html=True)
        st.markdown(intro6, unsafe_allow_html=True)

    if choice=="ATS Matcher":
        st.title('Resume And Job Description')

        # Initialize session_state
        if 'processed_resume' not in st.session_state:
            st.session_state.processed_resume = False
        if 'processed_job_description' not in st.session_state:
            st.session_state.processed_job_description = False
        # Upload Resume
        docx_file = st.file_uploader('Upload Resume', type=['pdf', 'docx', 'txt'])
        if st.button("Process Resume"):
            if docx_file is not None:
                file_details = {'filename': docx_file.name, 'filetype': docx_file.type, 'filesize': docx_file.size}
                st.write(file_details)
                if docx_file.type == 'text/plain':
                    st.session_state.raw_text = str(docx_file.read(), 'utf-8')
                    st.text(st.session_state.raw_text)
                elif docx_file.type == 'application/pdf':
                    save_path = Base_ATS.save_uploaded_file(docx_file, destination_path=folder_path)
                    st.session_state.raw_text = Base_ATS.read_pdf(docx_file)
                    st.text(st.session_state.raw_text)
                    st.session_state.resume_path = save_path
                    Base_ATS.delete_file(save_path)
                else:
                    st.session_state.raw_text = docx2txt.process(docx_file)
                    st.text(st.session_state.raw_text)

                st.session_state.processed_resume = True

        # Upload Job Description
        docx_file1 = st.file_uploader('Upload Job Description', type=['pdf', 'docx', 'txt'])
        if st.button("Process Job Description"):
            if docx_file1 is not None:
                file_details = {'filename': docx_file1.name, 'filetype': docx_file1.type, 'filesize': docx_file1.size}
                st.write(file_details)
                if docx_file1.type == 'text/plain':
                    st.session_state.raw_text1 = str(docx_file1.read(), 'utf-8')
                    st.text(st.session_state.raw_text1)
                elif docx_file1.type == 'application/pdf':
                    save_path = Base_ATS.save_uploaded_file(docx_file1, destination_path=folder_path)
                    st.session_state.raw_text1 = Base_ATS.read_pdf(docx_file1)
                    st.text(st.session_state.raw_text1)
                    Base_ATS.delete_file(save_path)
                else:
                    st.session_state.raw_text1 = docx2txt.process(docx_file1)
                    st.text(st.session_state.raw_text1)

                st.session_state.processed_job_description = True

        st.header("Skill Relevance Overview")
        resume_processor=ResumeProcessor()
        if st.button("Process Resume", key="process_resume_button"):
            resume = st.session_state.raw_text
            jd = st.session_state.raw_text1
            
            resume_processor.load_skill_patterns("jz_skill_patterns.jsonl")
            remails = resume_processor.extract_emails(resume)
            rlinks = resume_processor.extract_links(resume)
            cleaned_resume = resume_processor.remove_links_and_emails(resume, rlinks, remails)
            cleaned_resume = resume_processor.preprocess_resume(cleaned_resume)
            st.session_state.cleaned_resume=cleaned_resume
            jemails = resume_processor.extract_emails(jd)
            st.session_state.jemails=jemails
            jlinks = resume_processor.extract_links(jd)
            st.session_state.jlinks=jlinks
            cleaned_jd = resume_processor.remove_links_and_emails(jd, jlinks, jemails)
            cleaned_jd = resume_processor.preprocess_resume(cleaned_jd)
            st.subheader('Common Words between Resume and Job Description')
            common = Base_ATS.find_common_words_dict(cleaned_resume,cleaned_jd)  
            st.write(common)
            # skill_pattern="D:\\Designing\\experimento\\jz_skill_patterns.jsonl"
            skill_pattern="jz_skill_patterns.jsonl"
            ner=spacy.load('en_core_web_lg')
            entity_ruler=ner.add_pipe("entity_ruler")
            entity_ruler.from_disk(skill_pattern)
            doc = ner(cleaned_resume)
            colors={
                    "SKILL": "linear-gradient(90deg, #9BE15D, #00E3AE)",
                    "ORG": "#ffd966",
                    "PERSON": "#e06666",
                    "GPE": "#9fc5e8",
                    "DATE": "#c27ba0",
                    "ORDINAL": "#674ea7"
                    }
            options={"ents": ["SKILL", "ORG", "PERSON", "GPE", "DATE", "ORDINAL"],"colors": colors,}
            html = displacy.render(doc, style="ent", options=options, page=False)
            st.subheader('Resume Analysis')
            st.markdown(html, unsafe_allow_html=True)
            resume_skills = resume_processor.extracting_entities(resume)["SKILL"]
            st.session_state.resume_skills=resume_skills
            st.write('')
        if st.button("Process JD ", key="process_jd_button"):
            jd = st.session_state.raw_text1
            job_emails=st.session_state.jemails
            job_links=st.session_state.jlinks
            # jemails = resume_processor.extract_emails(jd)
            # jlinks = resume_processor.extract_links(jd)
            cleaned_jd = resume_processor.remove_links_and_emails(jd, job_links, job_emails)
            cleaned_jd = resume_processor.preprocess_resume(cleaned_jd)
            cleaned_jd = resume_processor.remove_links_and_emails(jd, job_links, job_emails)
            cleaned_jd = resume_processor.preprocess_resume(cleaned_jd)
            st.subheader('Skills in Job Description')
            jd_skills = Job_Des.jd_skill(cleaned_jd)
            st.session_state.jd_skills=jd_skills
            st.write(jd_skills)
            st.write('')
        if st.button("Match Results"):
            resume_name = docx_file.name
            jd_name = docx_file1.name
            jobd_skills = st.session_state.jd_skills
            res_skills = st.session_state.resume_skills
            res_skills_str = ' '.join(res_skills)
            job_skills_str = ' '.join(jobd_skills)
            corpus = [res_skills_str, job_skills_str]
            # st.write(corpus)
            score, missing_skills = Scoring.cal_cosine_similarity(res_skills_str, job_skills_str, corpus)
            st.subheader('Match Results for Resume and Job Description')
            if score >= 50:  # Adjust threshold as needed
                st.write(f"<h5><b><span style='color: #fd971f;'>{os.path.basename(resume_name)} is Recommended for {os.path.basename(jd_name)}</span></b></h5>", unsafe_allow_html=True)
                st.write(f"<h5><b><span style='color: #fd971f;'>Score: {score}</span></b></h5>", unsafe_allow_html=True)
            else:
                st.write(f"<h5><b><span style='color: #fd971f;'>{os.path.basename(resume_name)} is Not Recommended for {os.path.basename(jd_name)}</span></b></h5>", unsafe_allow_html=True)
                st.write(f"<h5><b><span style='color: #fd971f;'>Score: {score}</span></b></h5>", unsafe_allow_html=True)
                if missing_skills:
                    st.subheader('Missing Skills')
                    st.write(missing_skills)
        elif not st.session_state.processed_resume or not st.session_state.processed_job_description:
            st.warning("Please upload both Resume and Job Description before using ATS")
    
    if choice=="FeedBack Page":
        st.title('Feedback')
        # Get user input
        recipient_email = st.text_input("Recipient Email:")
        subject = st.text_input("Subject:")
        message = st.text_area("Message:")
        # Button to send email
        if st.button("Send Email"):
            if not recipient_email or not subject or not message:
                st.warning("Please fill in all the fields.")
            else:
                try:
                    Base_ATS.send_email(subject, message, recipient_email)
                    st.success(f"Email sent successfully to {recipient_email}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    if choice=="About Us":
        st.title('About Us')
        st.text('An NLP Project by ')
        st.text('Meet Our Team')

if __name__ == "__main__":
    main()
