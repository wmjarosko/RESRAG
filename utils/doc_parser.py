import fitz  # PyMuPDF
import docx  # python-docx

class DocumentParser:
    @staticmethod
    def parse(file_path, file_name):
        """Routes the file to the correct parser based on extension."""
        ext = file_name.split('.')[-1].lower()
        text = ""
        
        try:
            if ext == "pdf":
                doc = fitz.open(file_path)
                for page in doc:
                    text += page.get_text("text") + "\n"
            
            elif ext == "docx":
                doc = docx.Document(file_path)
                for para in doc.paragraphs:
                    text += para.text + "\n"
            
            elif ext in ["txt", "md"]:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
            else:
                text = f"Unsupported file extension: {ext}"
                
        except Exception as e:
            text = f"Error parsing {file_name}: {str(e)}"
            
        return text.strip()