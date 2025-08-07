import streamlit as st
import google.generativeai as genai
import docx2txt
from PyPDF2 import PdfReader
import io
from PIL import Image
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
import os

# ===== Load API Key from .env =====
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

# ===== UI Setup =====
st.set_page_config(page_title="QALBI AI", page_icon=":brain:", layout="centered")

st.title("QALBI AI: Educational Assistant")
st.markdown("""
Welcome to **QALBI AI**, your smart educational buddy.  
Ask a question, or upload an image/document for help!
""")

# ===== Input Section =====
uploaded_file = st.file_uploader("📎 Upload a file (image, PDF, TXT, or DOCX)", type=["png", "jpg", "jpeg", "pdf", "txt", "docx"])
query = st.text_input("🧠 Your Question", placeholder="E.g., What does this image represent?")
submit_button = st.button("✨ Get Answer")

# ===== Helper: Extract Text =====
def extract_text_from_file(file):
    if file.type == "application/pdf":
        pdf = PdfReader(file)
        text = "\n".join([page.extract_text() or "" for page in pdf.pages])
        return text.strip()

    elif file.type == "text/plain":
        return file.read().decode("utf-8")

    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return docx2txt.process(file)

    else:
        return None

# ===== Response Generation =====
if submit_button:
    if not query and not uploaded_file:
        st.warning("Please ask a question or upload a file/image.")
    else:
        st.subheader("🤖 QALBI AI Response")
        with st.spinner("Thinking..."):

            try:
                # Handle image input
                if uploaded_file and uploaded_file.type.startswith("image"):
                    image = Image.open(uploaded_file)
                    model = genai.GenerativeModel("gemini-2.5-flash-preview-04-17")
                    response = model.generate_content([query, image])

                # Handle document input
                elif uploaded_file:
                    text = extract_text_from_file(uploaded_file)
                    model = genai.GenerativeModel("gemini-2.5-flash-preview-04-17")
                    full_input = f"{text}\n\nQuestion: {query}" if query else text
                    response = model.generate_content(full_input)

                # Only text input
                else:
                    model = genai.GenerativeModel("gemini-2.5-flash-preview-04-17")
                    response = model.generate_content(query)

                st.markdown(response.text)

            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")

# ===== Footer =====
st.markdown("""---  
**Instructions**: Ask a question or upload a file/image. QALBI AI will generate a student-friendly explanation.  
Developed by **SK_AFTAB** | Powered by **Streamlit & Google Generative AI**
""")
