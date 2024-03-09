# Applicant Tracking System
                                                                                                    
Welcome to our Applicant Tracking System (ATS), a tool crafted to simplify the hiring process. Our system offers a seamless solution, transforming the traditionally manual and time-consuming task into an effortless endeavor.

This project utilizes Natural Language Processing (NLP) to align job applicants' resumes with job descriptions (JDs). With a user-friendly Streamlit interface, the system efficiently processes both documents, extracting key details using Named Entity Recognition (NER), such as skills, dates, organizations, and more. Moreover, it identifies any skills mentioned in the JD but missing from the resume, providing valuable insights for enhancing candidate profiles. Additionally, our system implements a feedback loop mechanism, enabling recruiters to provide guidance for candidates to improve their profiles and increase their chances of success.

## Core Features

1. **Streamlit Interface**: Experience a user-friendly interface with Streamlit, ensuring easy navigation and interaction for users.

2. **File Format Support**: Upload resumes and job descriptions effortlessly in TXT, DOCX, and PDF formats, simplifying the document input process.

3. **NER Entity Extraction**: Utilize Named Entity Recognition (NER) to accurately extract entities such as skills, names, dates, and organizations from resumes and job descriptions.

4. **Match Score Calculation**: Benefit from precise match scores between resumes and job descriptions, providing insights into candidate suitability for positions. The match score is calculated using TF-IDF (Term Frequency-Inverse Document Frequency) for vectorization and Cosine Similarity for measuring the similarity between the vectors.

5. **Missing Skills Detection and Feedback Loop**: Identify missing skills from job descriptions not found in resumes, enabling the implementation of a feedback loop to guide candidates in enhancing their profiles.

## Benefits

- **Efficiency**: Reduces manual effort in screening resumes, saving time and resources for recruiters.
- **Accuracy**: Ensures accurate matching of candidate skills with job requirements, leading to better hiring decisions.
- **Feedback Mechanism**: Provides constructive feedback to candidates for skill enhancement, improving their chances of securing desired positions.

The requirements for this project can be found in the `requirements.txt` file.
