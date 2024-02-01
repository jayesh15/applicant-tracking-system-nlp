from pydoc import doc
import streamlit as st
import os
import itertools

#File Processing
import pandas as pd
import PyPDF2
import fitz
import docx2txt
from streamlit_option_menu import option_menu

#
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import nltk
from termcolor import colored

#Fseedback
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def save_uploaded_file(uploaded_file, destination_path):
    file_path = os.path.join(destination_path, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

def color_text_red(text):
    return colored(text, 'red')

def highlight_common_words(text, common_words):
    words = text.split()
    #highlighted_words = [word if word.lower() not in common_words else color_text_red(word) for word in words]
    highlighted_words = [f'<span style="color:red">{word}</span>' if word.lower() in common_words else word for word in words]
    return ' '.join(highlighted_words)

def save_uploaded_file(uploaded_file, destination_path):
    file_path = os.path.join(destination_path, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def delete_file(file_path):
    try:
        os.remove(file_path)
        #st.success(f"File {file_path} successfully deleted.")
    except Exception as e:
        st.error(f"Error deleting the file {file_path}: {e}")

def read_pdf(file_path):
    try:
        with fitz.open(file_path) as pdf_document:
            text = ""
            for page_number in range(pdf_document.page_count):
                page = pdf_document[page_number]
                text += page.get_text()
            return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def find_common_words(text1, text2):
    # Tokenize the texts
    tokens1 = word_tokenize(text1)
    tokens2 = word_tokenize(text2)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens1 = [word.lower() for word in tokens1 if word.isalpha() and word.lower() not in stop_words]
    filtered_tokens2 = [word.lower() for word in tokens2 if word.isalpha() and word.lower() not in stop_words]
    # Find common words
    common_words = set(filtered_tokens1).intersection(filtered_tokens2)
    return common_words

def send_email(subject, message, to_email):
    # Set up the SMTP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = 'testnlpproejct@gmail.com'
    smtp_password = 'orme uats aueu irra'
    # Create a connection to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    # Compose the email
    email_message = MIMEMultipart()
    email_message['From'] = smtp_username
    email_message['To'] = to_email
    email_message['Subject'] = subject
    email_message.attach(MIMEText(message, 'plain'))
    # Send the email
    server.sendmail(smtp_username, to_email, email_message.as_string())
    # Close the connection
    server.quit()

def main():
    # Get the absolute path of the currently executing Python script in Streamlit
    script_path = os.path.realpath(__file__)

    # Get the folder path from the script path
    folder_path = os.path.dirname(script_path)

    # Print the results
    #st.write(f"The location of the Streamlit script is: {script_path}")
    #st.write(f"The folder path is: {folder_path}")

    with st.sidebar:
        choice = option_menu("Main Menu", ["Home","Files", 'About'], 
            icons=['house','cloud-upload', 'people'], menu_icon="list", default_index=0)
        

    if choice=='Home':
        st.subheader('Welcome to the Applicant Tracking System (ATS)')
        st.title("Application Tracking System")

        intro = "Welcome to our Applicant Tracking System (ATS), a tool that makes hiring easier. Whether you're an employer or job seeker, our system simplifies the recruitment process. We use advanced natural language processing (NLP) to analyze resumes and job descriptions, offering valuable insights for better hiring decisions. Explore the features to streamline your recruitment journey."
        st.markdown(intro, unsafe_allow_html=True)

        st.subheader('Key Features')
        intro1 = 'File Upload: Easily upload resumes and job descriptions in various formats such as PDF, DOCX, and TXT. Text Processing: Extract and review the content of uploaded resumes and job descriptions with just a click. Analysis and Comparison: Identify common words between resumes and job descriptions, allowing for a quick match analysis.  ATS Functionality: Utilize advanced features such as keyword matching and scoring to efficiently assess candidate suitability.'
        st.markdown(intro1, unsafe_allow_html=True)


    if choice=='Files':
        st.subheader('Resume And Job Description')

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
                    save_path = save_uploaded_file(docx_file, destination_path=folder_path)
                    st.session_state.raw_text = read_pdf(docx_file)
                    st.text(st.session_state.raw_text)
                    delete_file(save_path)
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
                    save_path = save_uploaded_file(docx_file1, destination_path=folder_path)
                    st.session_state.raw_text1 = read_pdf(docx_file1)
                    st.text(st.session_state.raw_text1)
                    delete_file(save_path)
                else:
                    st.session_state.raw_text1 = docx2txt.process(docx_file1)
                    st.text(st.session_state.raw_text1)

                st.session_state.processed_job_description = True
                
        # Check if both files are processed before finding common words
        if st.button("Common Words") and st.session_state.processed_resume and st.session_state.processed_job_description:
            common_words = find_common_words(st.session_state.raw_text1, st.session_state.raw_text)
            resume = st.session_state.raw_text
            jd = st.session_state.raw_text1
            result = highlight_common_words(resume,common_words)
            st.markdown(result, unsafe_allow_html=True)

        elif not st.session_state.processed_resume or not st.session_state.processed_job_description:
            st.warning("Please upload both Resume and Job Description before using ATS")
        

    if choice=="About":
        st.text('An NLP Project by ')
        st.subheader('Feedback')
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
                    send_email(subject, message, recipient_email)
                    st.success(f"Email sent successfully to {recipient_email}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
