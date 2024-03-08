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

#Feedback
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#Preprocessing
import spacy
from spacy import displacy
from pathlib import Path
from urllib.parse import urlparse
import json
import string
from nltk.stem import WordNetLemmatizer

class BaseATS:
    def color_text_red(self,text):
      return colored(text, 'red')
  
    def highlight_common_words(self,text, common_words):
      words = text.split()
      #highlighted_words = [word if word.lower() not in common_words else color_text_red(word) for word in words]
      highlighted_words = [f'<span style="color:red">{word}</span>' if word.lower() in common_words else word for word in words]
      return ' '.join(highlighted_words)

    def save_uploaded_file(self,uploaded_file, destination_path):
      file_path = os.path.join(destination_path, uploaded_file.name)
      with open(file_path, "wb") as f:
          f.write(uploaded_file.getbuffer())
      return file_path

    def save_json_file(self,json_data, destination_path, filename):
      file_path = os.path.join(destination_path, filename)
      with open(file_path, "w") as f:
          json.dump(json_data, f)
      return file_path

    def delete_file(self,file_path):
      try:
          os.remove(file_path)
          #st.success(f"File {file_path} successfully deleted.")
      except Exception as e:
          st.error(f"Error deleting the file {file_path}: {e}")

    def read_pdf(self,file_path):
      try:
          with fitz.open(file_path) as pdf_document:
              text = ""
              for page_number in range(pdf_document.page_count):
                  page = pdf_document[page_number]
                  text += page.get_text()
              return text
      except Exception as e:
          return f"Error reading PDF: {str(e)}"

    def find_common_words(self,text1, text2):
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

    def find_common_words_dict(self,text1, text2):
      # Tokenize the texts
      tokens1 = word_tokenize(text1)
      tokens2 = word_tokenize(text2)
      # Remove stopwords
      stop_words = set(stopwords.words('english'))
      filtered_tokens1 = [word.lower() for word in tokens1 if word.isalpha() and word.lower() not in stop_words]
      filtered_tokens2 = [word.lower() for word in tokens2 if word.isalpha() and word.lower() not in stop_words]
      # Find common words
      common_words = set(filtered_tokens1).intersection(filtered_tokens2)
      common_dict = {"common_words": list(common_words)}
      dictionary = dict(enumerate(common_words))
      return dictionary

    def send_email(self,subject, message, to_email):
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

