import traceback
import emoji
import requests
import pdfplumber
from pydantic import BaseModel
from bs4 import BeautifulSoup
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from chat import fetch_query_response
from database import get_extraction_by_id, insert_extraction, init_db


app = FastAPI()
init_db()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    id: str
    question: str

class URLRequest(BaseModel):
    url: str


def url_data_extractor(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        content = []

        body = soup.find('body')
        if body:
            content.append(body.get_text(separator='\n', strip=True))

        # Extract text from <p> tags
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            content.append(p.get_text(separator='\n', strip=True))
        headings = soup.find_all(['h1', 'h2', 'h3'])
        for heading in headings:
            content.append(heading.get_text(separator='\n', strip=True))
        extracted_text = emoji.replace_emoji("\n".join(content), replace='')

        return extracted_text

    except requests.RequestException as e:
        return f"An error occurred: {e}"
    

@app.get("/")
def hello():
    return {"Success": "Successfully called GET API"}

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
    content = emoji.replace_emoji("\n".join(pdf_content), replace='')
    
    chat_id = insert_extraction(content, "pdf")
    return {"chat_id": chat_id, "message": "PDF content processed and saved to DB."}

@app.post("/chat/")
async def chat_with_extracted_data(data: ChatRequest):
    try:
        corpus = get_extraction_by_id(str(data.id))
        response = fetch_query_response(corpus[1], data.question)
        return {"response": response}
    except Exception as e:
        error_trace = traceback.format_exc()
        return {"error": "Something went wrong", "details": str(e), "traceback": error_trace}