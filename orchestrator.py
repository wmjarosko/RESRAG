import json
import ollama
from vector_store.chroma_manager import VectorStoreManager

LLM_MODEL = "llama3.1:8b"

class RAGOrchestrator:
    def __init__(self):
        self.db_manager = VectorStoreManager()

    def _call_agent(self, system_prompt, user_content):
        """Generic method to call an Ollama model and force JSON output."""
        response = ollama.chat(
            model=LLM_MODEL,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_content}
            ],
            format='json',
            options={
                'num_ctx': 8192,       # Expand context to comfortably fit RAG chunks
                'temperature': 0.1,    # Make the agent highly analytical and deterministic
                'num_predict': 1024    # Cap output to prevent runaway generation
            }
        )
        try:
            return json.loads(response['message']['content'])
        except json.JSONDecodeError:
            return {"error": "Agent failed to return valid JSON."}

    def hr_agent(self, resume_text, job_description_text):
        """Extracts skills from Resume and JD."""
        system_prompt = """You are an expert HR Analyst. Extract the core technical skills, software experience, and infrastructure knowledge from the provided Resume and Job Description. 
        Respond ONLY in valid JSON format:
        {
            "candidate_skills": ["skill1", "skill2"],
            "job_requirements": ["req1", "req2"],
            "identified_gaps": ["gap1"]
        }"""
        
        user_content = f"RESUME:\n{resume_text}\n\nJOB DESCRIPTION:\n{job_description_text}"
        return self._call_agent(system_prompt, user_content)

    def retrieval_agent(self, hr_analysis):
        """Formulates queries based on HR analysis and fetches technical realities from Vector DB."""
        # Convert the job requirements into a search query string
        search_query = " ".join(hr_analysis.get("job_requirements", []))
        
        # Query Silo A (ChromaDB)
        retrieved_docs = self.db_manager.query_technical_docs(search_query, n_results=4)
        technical_context = "\n---\n".join(retrieved_docs)
        
        return technical_context

    def evaluator_agent(self, hr_analysis, technical_context):
        """Compares the candidate's skills against the actual technical documentation."""
        system_prompt = """You are a Senior Technical Evaluator. Compare the Candidate's Skills against the Job Requirements, heavily factoring in the provided Technical Documentation realities.
        Determine if the candidate is truly technically capable of operating in this specific environment.
        Respond ONLY in valid JSON format:
        {
            "technical_match_score_1_to_10": 8,
            "justification": "Detailed explanation...",
            "red_flags": ["flag1", "flag2"]
        }"""
        
        user_content = (
            f"HR ANALYSIS:\n{json.dumps(hr_analysis)}\n\n"
            f"TECHNICAL DOCUMENTATION REALITIES:\n{technical_context}"
        )
        return self._call_agent(system_prompt, user_content)

    def run_evaluation_pipeline(self, resume_text, job_description_text):
        """The Orchestrator logic tying the agents together."""
        
        # Step 1: HR Agent parses silos B and C
        hr_data = self.hr_agent(resume_text, job_description_text)
        
        # Step 2: Retrieval Agent queries Silo A
        tech_context = self.retrieval_agent(hr_data)
        
        # Step 3: Evaluator Agent makes final determination
        final_evaluation = self.evaluator_agent(hr_data, tech_context)
        
        return {
            "hr_extraction": hr_data,
            "retrieved_context": tech_context,
            "final_evaluation": final_evaluation
        }