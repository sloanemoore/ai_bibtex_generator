from config import API_KEY
from openai import OpenAI
import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from PyPDF2 import PdfReader
import bibtexparser


def get_text(cv_file):
    reader = PdfReader(cv_file)
    count = len(reader.pages)
    all_text = ""
    for page in range(count):
        page_obj = reader.pages[page] 
        all_text += page_obj.extract_text()
    return all_text


@st.fragment()
def file_download_button():
  st.download_button(
    label="Download BibTeX File",
    data=bibtex_response,
    file_name=f"{name}_works_bibtex.bib",
    mime="text/plain",
  )


st.title("AI BibTeX Generator")
st.write(r"$\textsf{\normalsize}$")

name = st.text_input(r"$\textsf{\large Enter your name as you want it listed in the BibTeX citations.}$")
st.write(r"$\textsf{\small}$")

file_format = st.radio(r"$\textsf{\large Do you want to upload a PDF of your CV or copy and paste works directly?}$", ("Upload a PDF file", "Copy and paste works"))


text = ""
if file_format == "Upload a PDF file":
  file = st.file_uploader(r"$\textsf{\normalsize Upload a PDF of your CV and click 'Submit'.}$", type="pdf")
  if file is not None:
      text = get_text(file)
      file_type = "CV"
if file_format == "Copy and paste works":
  text = st.text_area(r"$\textsf{\normalsize Paste your works here and click 'Submit'. Add a heading before each set of works, e.g., 'Books', 'Articles', etc.}$")
  file_type = "list of works"

col1, col2 = st.columns([.75, .25])
with col1:
  submit_works_btn = st.button("Submit")
with col2:
  reset_btn = st.button("Clear Form and Files")
if reset_btn:
   streamlit_js_eval(js_expressions="parent.window.location.reload()")

st.write("")
st.divider()


if name and text and submit_works_btn:
  client = OpenAI(api_key=API_KEY)

  completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {"role": "system", "content": "You are a helpful research assistant."},
      {"role": "user", "content": f"Please find the works and publications in this {file_type} and provide BibTeX output in standard format for each work. The BibTeX output will be written to a BibTeX file, so do not include any text in your response that is not BibTeX, for example 'Here is the output you requested.' Please list this author, {name}, along with any others in the citations. Here is the contents of the file: {text}"}
    ]
  )

  bibtex_response = completion.choices[0].message.content


  works_library = bibtexparser.parse_string(bibtex_response)
  if len(works_library.failed_blocks) > 0:
    print("Some blocks failed to parse. Check the entries of `library.failed_blocks`.")
    st.write(r"$\textsf{\normalsize Something went wrong and a BibTeX file could not be created.}$")
  else:
    print("All blocks parsed successfully")
    bibtex_file = bibtexparser.write_file(f"{name}_works_bibtex_sm.bib", works_library)
    st.write(r"$\textsf{\normalsize Click the button below to download your BibTeX file. The content of the file is also listed below.}$")
    file_download_button()
    st.write(bibtex_response)

