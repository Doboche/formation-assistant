from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File,HTTPException,Form
from fastapi.middleware.cors import CORSMiddleware
import os
from models import Quiz
from extraction import extract_text
from generation import generate_content
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # l'origine de ton frontend Vite
    allow_credentials=True,
    allow_methods=["*"],   # autorise toutes les méthodes (GET, POST...)
    allow_headers=["*"],   # autorise tous les headers
)
# Le modèle qui décrit les données entrantes
class CourseInput(BaseModel):
    content: str

@app.get("/")
def read_root():
    return {"message": "API formation assistant opérationnelle"}

@app.post("/generate-content")
async def generate_content_endpoint(file : UploadFile = File(...), content_type: str = Form(...)):
    content = await file.read()
    try:
        filename,file_extension = os.path.splitext(file.filename)
        text = extract_text(content,file_extension)   
        return generate_content(text, content_type)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur dans le génération du quiz : {e}")
 