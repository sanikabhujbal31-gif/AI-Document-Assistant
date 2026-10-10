from dotenv import load_dotenv
import streamlit as st
from pypdf import PdfReader
from google import genai
import os
st.set_page_config(
    page_title="AI Document Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


st.sidebar.title("📄 AI Document Assistant")

st.sidebar.markdown("---")

st.sidebar.subheader("About the Project")

st.sidebar.write(
    "An AI-powered application that allows users "
    "to upload PDF documents and ask questions "
    "about their content."
)

st.sidebar.markdown("---")

st.sidebar.subheader("Technologies Used")

st.sidebar.write("""
- Python
- Streamlit
- Gemini AI
- PyPDF
""")

st.sidebar.markdown("---")

st.sidebar.caption(
    "Minor Project | BSc Data Science and Artificial Intelligence"
)

st.title("📄 AI Document Assistant")

st.markdown(
    "### Your personal AI-powered PDF reading assistant"
)

st.write(
    "Upload a PDF document, ask a question, "
    "and receive an AI-generated answer based on its content."
)

st.divider()

uploaded_file = st.file_uploader(
    "📄 Upload your PDF document",
    type=["pdf"],
    help="Upload a PDF file to ask questions about it."
)

question = st.text_input(
    "💬 Ask a question about the document:",
    placeholder="Example: What is this document about?"
)

if st.button("🔍 Get Answer", use_container_width=True):
    if uploaded_file is None:
        st.warning("Please upload a PDF first.")
    
    elif question.strip() == "":
        st.warning("Please enter a question.")
    
    else:
        reader = PdfReader(uploaded_file)

        document_text = ""

        for page in reader.pages:
            text = page.extract_text()
            
            if text:
                document_text += text + "\n"

        st.success("✅ PDF uploaded successfully!")

    st.info(f"📄 Number of pages: {len(reader.pages)}")

    st.success("✅ Text extracted successfully!")
    prompt = f"""
Answer the user's question using only the information in the PDF.

PDF content:
{document_text}

User's question:
{question}

If the answer is not present in the PDF, say:
"I couldn't find the answer in the uploaded document."
"""
    
    try:
        with st.spinner("AI is analyzing your document... Please wait."):
            response = client.models.generate_content(
                model="gemini-3.7-flash",
                contents=prompt
            )

        st.subheader("🤖 AI Answer")
        st.success("Answer generated successfully!")
        st.markdown(response.text)

    except Exception as e:
        error_message = str(e)

        if "503" in error_message or "UNAVAILABLE" in error_message:
            st.warning(
                "The AI service is temporarily busy. "
                "Your PDF was uploaded and processed successfully. "
                "Please wait a little and try again."
            )
        else:
            st.error(f"Unable to generate an answer: {error_message}")