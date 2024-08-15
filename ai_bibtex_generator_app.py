from openai import OpenAI
from config import API_KEY
import streamlit as st
from PyPDF2 import PdfReader


def get_text(cv_file):
    reader = PdfReader(cv_file)
    count = len(reader.pages)
    all_text = ""
    for page in range(count):
        page_obj = reader.pages[page] 
        all_text += page_obj.extract_text()
    return all_text



st.title("Generate BibTeX from PDF")
cv_file = st.file_uploader('Choose your .pdf file', type="pdf")
if cv_file is not None:
    cv_text = get_text(cv_file)

    client = OpenAI(api_key=API_KEY)

    completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role": "system", "content": "You are a helpful research assistant."},
        {"role": "user", "content": f"Please find the works and publications in this CV and provide a BibTeX output for each work. Here is the CV: {cv_text}"}
      ]
    )


    st.write(completion.choices[0].message.content)