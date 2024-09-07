from bs4 import BeautifulSoup
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import requests
from chat import fetch_query_response
from database import get_extraction_by_id, insert_extraction, init_db
import pdfplumber

app = FastAPI()
init_db()

class ChatRequest(BaseModel):
    id: str
    question: str

class URLRequest(BaseModel):
    url: str

def url_data_extractor(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text()
    return text

@app.post("/process_url/")
async def process_url(data: URLRequest):
    content = url_data_extractor(data.url)
    chat_id = insert_extraction(content, "url")
    return {"chat_id": chat_id, "message": "URL content processed and saved to DB."}

@app.post("/process_pdf/")
async def process_pdf(file: UploadFile = File(...)):
    pdf_content = []
    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            pdf_content.append(page.extract_text())
    content = "\n".join(pdf_content)
    chat_id = insert_extraction(content, "pdf")
    return {"chat_id": chat_id, "message": "PDF content processed and saved to DB."}

@app.post("/chat/")
async def chat_with_extracted_data(data: ChatRequest):
    try:
        corpus = get_extraction_by_id(str(data.id))
        print(f"{type(corpus)=}\n{corpus=}")
        response = fetch_query_response(corpus[1], data.question)
        return {"response": response}
    except Exception:
        return {"error": "Something went wrong"}