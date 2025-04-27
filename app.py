# import streamlit as st
# import google.generativeai as genai

# # Configure the Gemini API with a secure API key placeholder
# # Replace with your actual API key in a secure environment
# API_KEY = "AIzaSyDfaWjommA_0hSTl33FHeF-vgXWrsWCSN0"
# genai.configure(api_key=API_KEY)

# # Initialize the generative model
# model = genai.GenerativeModel("gemini-2.5-flash-preview-04-17")

# # Streamlit app configuration
# st.set_page_config(page_title="QALBI AI", page_icon=":brain:", layout="centered")

# # App header
# st.title("QALBI AI: Educational Assistant")
# st.markdown("""
# Welcome to QALBI AI, an educational tool designed to provide clear and concise explanations for students. 
# Enter your question below, and receive an answer tailored to a school student's understanding.
# """)

# # Input form
# with st.form(key="question_form"):
#     query = st.text_input(
#         label="Your Question",
#         placeholder="E.g., What is a model context protocol?",
#         help="Type your question here, and QALBI AI will provide a student-friendly explanation."
#     )
#     submit_button = st.form_submit_button(label="Get Answer")

# # Handle form submission
# if submit_button and query:
#     st.subheader("QALBI AI Response")
#     with st.spinner("Generating response..."):
#         try:
#             # Generate response using the model
#             response = model.generate_content(query)
#             st.markdown(response.text)
#         except Exception as e:
#             st.error(f"An error occurred while generating the response: {str(e)}")

# # Footer
# st.markdown("""
# ---
# **Instructions**: Enter a question in the input field and click "Get Answer" to receive a response. 
# For optimal results, ensure your question is clear and specific.
# """)
# st.markdown("Developed by SK_AFTAB | Powered by Streamlit & Google Generative AI")

import streamlit as st
import google.generativeai as genai
import docx2txt
from PyPDF2 import PdfReader
import io
from PIL import Image

# ===== API Setup =====
API_KEY = "AIzaSyDfaWjommA_0hSTl33FHeF-vgXWrsWCSN0"
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
from deep_translator import GoogleTranslator

# # Language options
# lang_map = {
#     "English": "en",
#     "Hindi": "hi",
#     "Urdu": "ur",
#     "Tamil": "ta",
#     "Bengali": "bn",
# }
# chosen_lang = st.selectbox("🌐 Output Language", list(lang_map.keys()), index=0)

# # After response.text is available:
# translated_response = GoogleTranslator(source='auto', target=lang_map[chosen_lang]).translate("response.text")
# st.markdown(translated_response)


# from streamlit_mic_recorder import mic_recorder
# import speech_recognition as sr

# st.markdown("🎤 Or use your voice:")
# audio = mic_recorder(start_prompt="Start Recording", stop_prompt="Stop", key="voice")

# if audio and not query:
#     st.info("Transcribing your voice...")
#     try:
#         recognizer = sr.Recognizer()
#         with sr.AudioFile(io.BytesIO(audio["bytes"])) as source:
#             audio_data = recognizer.record(source)
#             query = recognizer.recognize_google(audio_data)
#             st.success(f"Recognized: {query}")
#     except Exception as e:
#         st.error("Could not recognize voice input. Try again.")

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

