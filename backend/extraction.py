from pypdf import PdfReader
import io
from fastapi import HTTPException

def extract_text(content,file_extension):
    if(file_extension == '.txt'):
        text = content.decode("utf-8")
    elif (file_extension == '.pdf'):
        reader = PdfReader(io.BytesIO(content))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
    else:
        raise HTTPException(status_code=400, detail="Format non supporté. Utilisez .txt ou .pdf")
    return text