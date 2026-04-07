import streamlit as st
import os
import tempfile
from orchestrator import RAGOrchestrator
from vector_store.chroma_manager import VectorStoreManager
from utils.doc_parser import DocumentParser
from utils.security import ROOT_DIR

JAIL_TEMP_DIR = str(ROOT_DIR / "temp_uploads")
os.makedirs(JAIL_TEMP_DIR, exist_ok=True)

st.set_page_config(page_title="Local Multi-Agent RAG Resume Evaluator", layout="wide")
st.title("Resume RAG Evaluator")


st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize backend classes
@st.cache_resource
def get_orchestrator():
    return RAGOrchestrator()

@st.cache_resource
def get_db_manager():
    return VectorStoreManager()

orchestrator = get_orchestrator()
db_manager = get_db_manager()

# --- Sidebar: Vector Database Management ---
st.sidebar.header("📚 Silo A: Technical Docs")
st.sidebar.markdown("Upload architecture diagrams, standard operating procedures, and other technical documentation your candidate should be familiar with.")

# Updated to accept multiple files
uploaded_pdfs = st.sidebar.file_uploader(
    "Upload Technical PDFs", 
    type=["pdf"], 
    accept_multiple_files=True
)

if st.sidebar.button("Ingest to ChromaDB"):
    if uploaded_pdfs:
        # Initialize a progress bar and status text
        progress_bar = st.sidebar.progress(0)
        status_text = st.sidebar.empty()
        total_files = len(uploaded_pdfs)
        
        for index, uploaded_pdf in enumerate(uploaded_pdfs):
            status_text.text(f"Processing {uploaded_pdf.name} ({index + 1}/{total_files})...")
            
            # Save uploaded file temporarily to process with PyMuPDF
            with tempfile.NamedTemporaryFile(dir=JAIL_TEMP_DIR, delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_pdf.read())
                tmp_path = tmp_file.name
            
            # Ingest sequentially to protect system memory
            chunks_added = db_manager.ingest_technical_pdf(tmp_path, uploaded_pdf.name)
            os.remove(tmp_path)
            
            # Update progress bar
            progress_bar.progress((index + 1) / total_files)
            
        status_text.text("✅ All documents ingested successfully!")
        st.sidebar.success(f"Processed {total_files} files.")
    else:
        st.sidebar.warning("Please upload at least one PDF.")

# --- Main Area: Evaluation Pipeline ---
st.header("⚙️ Evaluation Pipeline")
st.markdown("Provide the candidate's resume and the job description to run a multi-agent evaluation against the technical documentation in Silo A.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Silo B: Candidate Resume")
    uploaded_resume = st.file_uploader(
        "Upload Resume", 
        type=["pdf", "docx", "txt", "md"]
    )
    
    resume_text = ""
    if uploaded_resume is not None:
        # Save temp file to parse it
        with tempfile.NamedTemporaryFile(dir=JAIL_TEMP_DIR, delete=False, suffix=f".{uploaded_resume.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_resume.read())
            tmp_path = tmp_file.name
        
        # Extract the text based on file type
        resume_text = DocumentParser.parse(tmp_path, uploaded_resume.name)
        os.remove(tmp_path) # Clean up
        
        # Give the user a quick sanity check that extraction worked
        with st.expander("Preview Extracted Resume Text"):
            st.text(resume_text[:1000] + "\n\n...[truncated for preview]")

with col2:
    st.subheader("💼 Silo C: Job Description")
    # Leaving JD as a text area for now, but you could easily replicate the uploader logic here!
    jd_text = st.text_area("Paste Job Description Text", height=200)

st.divider()

col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    run_eval = st.button("🚀 Run Multi-Agent Evaluation", type="primary", use_container_width=True)

if run_eval:
    if not resume_text or not jd_text:
        st.error("Please provide both a Resume (upload) and a Job Description (text).")
    else:
        with st.spinner("Orchestrator is coordinating agents..."):
            results = orchestrator.run_evaluation_pipeline(resume_text, jd_text)
            
            st.subheader("🕵️‍♀️ 1. HR Agent Extraction")
            st.markdown("*Extracting core technical skills, software experience, and infrastructure knowledge.*")
            st.json(results["hr_extraction"])
            
            st.subheader("🔍 2. Retrieval Agent Context (From Silo A)")
            st.markdown("*Retrieving specific, relevant technical context from the uploaded documentation.*")
            with st.expander("View Retrieved Technical Documentation"):
                st.write(results["retrieved_context"])
                
            st.subheader("⚖️ 3. Evaluator Agent Final Verdict")
            st.markdown("*Determining if the candidate is capable of operating in the specific environment.*")
            st.json(results["final_evaluation"])