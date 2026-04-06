# RESRAG (Resume RAG Evaluator)

RESRAG is a Local Multi-Agent Retrieval-Augmented Generation (RAG) system designed to evaluate candidate resumes against technical documentation and job descriptions. It leverages local Large Language Models (LLMs) via Ollama and a vector database (ChromaDB) to perform an in-depth, reality-based assessment of a candidate's technical skills.

The application uses Streamlit for its user interface, allowing users to upload technical PDFs (Silo A), candidate resumes (Silo B), and paste job descriptions (Silo C) to run a comprehensive multi-agent evaluation.

## Agents Involved

The system orchestrates three distinct AI agents to perform the evaluation:

1.  **HR Agent (Extraction):**
    *   **Role:** Acts as an expert HR Analyst.
    *   **Function:** Extracts core technical skills, software experience, and infrastructure knowledge from the candidate's Resume and the Job Description. It outputs these as candidate skills, job requirements, and identified gaps.
2.  **Retrieval Agent (Context Gathering):**
    *   **Role:** Bridges the gap between HR requirements and technical realities.
    *   **Function:** Takes the job requirements identified by the HR Agent, formulates a search query, and searches the Vector Database (Silo A - containing technical documentation). It retrieves specific, relevant technical context from the uploaded documentation.
3.  **Evaluator Agent (Final Verdict):**
    *   **Role:** Acts as a Senior Technical Evaluator.
    *   **Function:** Compares the candidate's extracted skills against the job requirements, heavily factoring in the retrieved *actual* technical documentation. It determines if the candidate is truly capable of operating in the specific environment described by the technical docs, outputting a match score, a detailed justification, and any potential red flags.

## Prerequisites

Before installing RESRAG, ensure you have the following installed on your system:

*   **Python 3.8+**
*   **Ollama:** You need Ollama installed and running locally to serve the LLM and embedding models. Download from [ollama.com](https://ollama.com/).

## Models Required

You must pull the following models via Ollama before running the application:

1.  **LLM Model:** The orchestrator currently uses `gemma4:e2b` for the agents.
    ```shell
    ollama run gemma4:e2b
    ```
    *(Note: If `gemma4:e2b` is not available, you may need to update `LLM_MODEL` in `orchestrator.py` to an available model like `llama3` or `gemma:2b`.)*

2.  **Embedding Model:** The vector database uses `nomic-embed-text` for generating embeddings.
    ```shell
    ollama pull nomic-embed-text
    ```

## Step-by-Step Installation

1.  **Clone the repository (if applicable) or navigate to the project directory:**
    ```shell
    cd <path-to-your-project>
    ```

2.  **Create a virtual environment (recommended):**
    ```shell
    python3 -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   On Windows:
        ```shell
        venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```shell
        source venv/bin/activate
        ```

4.  **Install the required dependencies:**
    ```shell
    pip install -r requirements.txt
    ```
    *(The requirements include: `streamlit`, `chromadb`, `PyMuPDF` (fitz), `ollama`, `pydantic`, and `python-docx`)*

## Execution Instructions

1.  **Start Ollama:** Ensure the Ollama service is running in the background.

2.  **Run the Streamlit Application:**
    Navigate to the project root directory in your terminal and execute:
    ```shell
    streamlit run app.py
    ```

3.  **Using the Interface:**
    *   **Step 1: Upload Technical Docs (Silo A):** Use the sidebar to upload one or more technical PDF documents that describe the environment, architecture, or tools the candidate will use. Click "Ingest to ChromaDB" to process and store them in the vector database.
    *   **Step 2: Upload Resume (Silo B):** In the main area, upload the candidate's resume (supports PDF, DOCX, TXT, MD). You can preview the extracted text.
    *   **Step 3: Paste Job Description (Silo C):** Paste the job description text into the provided text area.
    *   **Step 4: Run Evaluation:** Click the "Run Multi-Agent Evaluation" button.
    *   **Step 5: Review Results:** The system will process the data and display:
        *   The JSON extraction from the HR Agent.
        *   The retrieved context from the Retrieval Agent.
        *   The final JSON evaluation (score, justification, red flags) from the Evaluator Agent.
