#!pip install python-docx PyPDF2 nltk docx2txt pymupdf
#!python -m spacy download en_core_web_lg
#Importing necessary libraries
from urllib.parse import urlparse
import docx
import fitz #PyMuPdf
from pathlib import Path
import string
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
import spacy
import pandas as pd
import re
from nltk.corpus import stopwords
import json
from spacy import displacy
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')
class ResumeProcessor:
  
  def __init__(self):
    self.ner=spacy.load('en_core_web_lg')
    self.entity_ruler=self.ner.add_pipe("entity_ruler")
  def load_skill_patterns(self,skills_file_path):
    self.entity_ruler.from_disk(skills_file_path)
  def read_text_file(self,resume_path):
    with open(resume_path,'r',encoding='utf-8') as resume:
      return resume.read()
  def read_docx_file(self,resume_path):
    doc=docx.Document(resume_path)
    return " ".join([paragraph.text for paragraph in doc.paragraphs])
  def read_pdf_file(Self,resume_path):
    text=""
    pdf=fitz.open(resume_path)
    for page_no in range(pdf.page_count):
      page=pdf[page_no]
      text +=page.get_text()
    return text
  def remove_punctuations(self,text):
    punctuations=set(string.punctuation)
    cleaned_text="".join(char for char in text if char not in punctuations)
    return cleaned_text
  def remove_extra_space(self,text):
    lines=[line.strip() for line in text.splitlines() if line.split()]
    return " ".join(lines)
  def remove_stopwords(self,text):
    model=spacy.load('en_core_web_sm')
    doc=model(text)
    tokens=[token.text for token in doc if not token.is_stop]
    cleaned_text=" ".join(tokens)
    return cleaned_text
  def preprocess_resume(self,file_content):
    #Removing punctuations
    file_content=self.remove_punctuations(file_content)
    #Removing extra spaces and lines
    file_content=self.remove_extra_space(file_content)
    #Removing stopwords
    cleaned_text=self.remove_stopwords(file_content)
    #Tokenization
    tokens=word_tokenize(cleaned_text.lower())
    #Lemmatization
    lemmatizer=WordNetLemmatizer()
    lemma_tokens=[lemmatizer.lemmatize(token) for token in tokens]
    #Joining lemmatized tokens to create processed_text
    processed_text=" ".join(lemma_tokens)
    return processed_text
  def extract_links(self,text):
    link_pattern=r'\b(?:https:?://|www\.)\S+\b'
    links=re.findall(link_pattern,text)
    return links
  def extract_emails(self,text):
    words=text.split()
    emails=[word for word in words if '@' in word and '.' in word]
    return emails
  def remove_links_and_emails(self,text,links,emails):
    #Removing links from the text
    for link in links:
      text=text.replace(link,'')
    #Removing emails from teh text
    for email in emails:
      text=text.replace(email,'')
    return text
  def reading_resume(self,resume_path):
    #Reading extension of the input file
    file_extension=Path(resume_path).suffix.lower()
    #Reading the content based on extension
    if file_extension==".txt":
      file_content=self.read_text_file(resume_path)
    elif file_extension==".docx":
      file_content=self.read_docx_file(resume_path)
    elif file_extension==".pdf":
      file_content=self.read_pdf_file(resume_path)
    else:
      print(f'{file_extension} is not accepted. Please input valid file extension such as pdf,txt or docx')
      pass
    #Extarcting emails from text
    emails=self.extract_emails(file_content)
    #Extracting links from text
    links=self.extract_links(file_content)
    #Removing extracted emails and links from the text
    cleaned_text=self.remove_links_and_emails(file_content,links,emails)
    #Preprocessing the text
    processed_text=self.preprocess_resume(cleaned_text)
    return processed_text,links,emails
  def extracting_entities(self,processed_text):
    #Performing NER using en_core_web_lg model with added pipe skills_file
    content=self.ner(processed_text)
    labelled_entities={}
    for ent in content.ents:
      entity_type=ent.label_
      entity_text=ent.text
      #Making sure entities dont repeat themselves
      if entity_type not in labelled_entities:
        labelled_entities[entity_type]=set()
      labelled_entities[entity_type].add(entity_text)
    #Converting set to lists in a dict for JSON representation
    labelled_entities={key:list(values) for key,values in labelled_entities.items()}
    return labelled_entities
  def visualizing_ner(self,processed_text):
    content=self.ner(processed_text)
    colors={
    "SKILL": "linear-gradient(90deg,#A6E3E9, #70C7C7)",
    "ORG": "#FFD699",
    "PERSON": "#FFB6C1",
    "GPE": "#9fc5e8",
    "DATE": "#FFECB3",
    "CARDINAL": "#C8B4E3"}
    options={"entities":['SKILL','ORG','ORDINAL','PERSON','DATE','GPE'],
             "colors":colors}
    html=displacy.render(content,style='ent',jupyter=True,options=options)
    return html
  # def visualizing_ner_streamlit(self, processed_text, output_path=None):
  #   content = self.ner(processed_text)
  #   colors = {
  #       "SKILL": "linear-gradient(90deg, #A6E3E9, #70C7C7)",
  #       "ORG": "#FFD699",
  #       "PERSON": "#FFB6C1",
  #       "GPE": "#9fc5e8",
  #       "DATE": "#FFECB3",
  #       "CARDINAL": "#C8B4E3"
  #   }
  #   options = {"entities": ['SKILL', 'ORG', 'ORDINAL', 'PERSON', 'DATE', 'GPE'],
  #              "colors": colors}
  #   html = displacy.render(content, style='ent', jupyter=False, options=options)
  #   with open(output_path, "w", encoding="utf-8") as f:
  #       f.write(html)
  #   return output_path

#resume_processor=ResumeProcessor()
#resume_processor.load_skill_patterns("jz_skill_patterns.jsonl")
#resume_path="Resume_Shravani.pdf"
#processed_resume,extracted_links,extarcted_mails=resume_processor.reading_resume(resume_path)

#processed_resume

#Visualizing NER
#resume_processor.visualizing_ner(processed_resume)

#labelled_entities=resume_processor.extracting_entities(processed_resume)
#print(json.dumps(labelled_entities,indent=2))

