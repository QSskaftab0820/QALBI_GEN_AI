import streamlit as st
import google.generativeai as genai

# Configure the Gemini API with a secure API key placeholder
# Replace with your actual API key in a secure environment
API_KEY = "AIzaSyDfaWjommA_0hSTl33FHeF-vgXWrsWCSN0"
genai.configure(api_key=API_KEY)

# Initialize the generative model
model = genai.GenerativeModel("gemini-2.5-flash-preview-04-17")

# Streamlit app configuration
st.set_page_config(page_title="QALBI AI", page_icon=":brain:", layout="centered")

# App header
st.title("QALBI AI: Educational Assistant")
st.markdown("""
Welcome to QALBI AI, an educational tool designed to provide clear and concise explanations for students. 
Enter your question below, and receive an answer tailored to a school student's understanding.
""")

# Input form
with st.form(key="question_form"):
    query = st.text_input(
        label="Your Question",
        placeholder="E.g., What is a model context protocol?",
        help="Type your question here, and QALBI AI will provide a student-friendly explanation."
    )
    submit_button = st.form_submit_button(label="Get Answer")

# Handle form submission
if submit_button and query:
    st.subheader("QALBI AI Response")
    with st.spinner("Generating response..."):
        try:
            # Generate response using the model
            response = model.generate_content(query)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"An error occurred while generating the response: {str(e)}")

# Footer
st.markdown("""
---
**Instructions**: Enter a question in the input field and click "Get Answer" to receive a response. 
For optimal results, ensure your question is clear and specific.
""")
st.markdown("Developed by SK_AFTAB | Powered by Streamlit & Google Generative AI")
