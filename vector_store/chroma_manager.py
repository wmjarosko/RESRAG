import os
import fitz  # PyMuPDF
import chromadb
from utils.security import ROOT_DIR
from chromadb import Documents, EmbeddingFunction, Embeddings
import ollama


class OllamaEmbeddingFunction(EmbeddingFunction):
    """Custom embedding function to use Ollama natively with ChromaDB."""
    def __init__(self, model_name="nomic-embed-text"):
        self.model_name = model_name

    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for doc in input:
            # We explicitly set num_ctx to 8192 to unlock nomic's full capacity
            # and prevent token overflow from dense technical chunks.
            response = ollama.embeddings(
                model=self.model_name, 
                prompt=doc,
                options={'num_ctx': 8192} 
            )
            embeddings.append(response["embedding"])
        return embeddings

class VectorStoreManager:
    def __init__(self, db_path=str(ROOT_DIR / "vector_store" / "chroma_db")):
        self.client = chromadb.PersistentClient(path=db_path)
        self.embedding_fn = OllamaEmbeddingFunction()
        
        # Silo A: Technical Documentation
        self.tech_collection = self.client.get_or_create_collection(
            name="tech_software_docs",
            embedding_function=self.embedding_fn
        )

    def extract_text_from_pdf(self, pdf_path):
        from utils.security import enforce_safe_path
        """Extracts text from a PDF using PyMuPDF."""
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"
        return text

    #def chunk_text(self, text, chunk_size=800, overlap=200):
    #    """Chunks text by words based on your parameters."""
    #    words = text.split()
    #    chunks = []
    #    for i in range(0, len(words), chunk_size - overlap):
    #        chunk = " ".join(words[i:i + chunk_size])
    #        chunks.append(chunk)
    #        if i + chunk_size >= len(words):
    #            break
    #    return chunks
    def chunk_text(self, text, chunk_size=300, overlap=50):
        """
        Chunks text by words, specifically optimized for dense XML, 
        system paths, and tabular data found in technical documentation.
        """
        # Force spaces around XML brackets and common delimiters so 
        # text.split() doesn't treat giant code blocks as single words.
        safe_text = text.replace("<", " <").replace(">", "> ").replace("/", " / ")
        
        words = safe_text.split()
        chunks = []
        
        # Calculate step size, ensuring it's always at least 1 to prevent infinite loops
        step = max(1, chunk_size - overlap) 
        
        for i in range(0, len(words), step):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
            if i + chunk_size >= len(words):
                break
                
        return chunks

    def ingest_technical_pdf(self, pdf_path, doc_name):
        """Processes a PDF and stores it in Silo A."""
        raw_text = self.extract_text_from_pdf(pdf_path)
        chunks = self.chunk_text(raw_text)
        
        ids = [f"{doc_name}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"source": doc_name, "chunk_index": i} for i in range(len(chunks))]
        
        self.tech_collection.add(
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
        return len(chunks)

    def query_technical_docs(self, query_text, n_results=3):
        """Retrieves relevant technical context from Silo A."""
        results = self.tech_collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results["documents"][0] if results["documents"] else []