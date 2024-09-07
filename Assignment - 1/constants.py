MARKDOWN_DOC_STRING = """
## API Documentation

This documentation provides detailed information on the API endpoints, their request structures, functionalities, and the expected responses. These APIs allow users to process web URLs, extract content from PDF documents, and interact with a chat system using stored content.

---

## 1. Process Web URL API

### **Endpoint**: `POST /process_url`

### **Description**:
This API allows you to scrape content from a specified web URL. Once the content is scraped, it is cleaned and stored in the system. Each request generates a unique `chat_id`, which is used to reference the stored content in future interactions.

### **Request**:
The request body should contain the following:

#### **Request Body**:
```json
{
    "url": "https://example.com"
}
```
- url: The URL of the website whose content you want to process (string, required).
### **Functionality**:
- Scrapes the web page content from the provided URL.
- Cleans the content by removing unnecessary characters like line breaks, extra spaces, etc.
- Stores the cleaned content and associates it with a unique `chat_id`.


##### When using on local system : 
```copy
http://localhost:8000/process_url/
```

### **Response**:
Upon successful processing, the API returns a response with a unique chat_id and a confirmation message.

```json
{
    "chat_id": "unique_chat_id_for_url",
    "message": "URL content processed and stored successfully."
}
```
- `chat_id`: A unique identifier for the stored content (string).
- `message`: A confirmation message indicating the success of the content processing (string).

                
## 2. Process PDF Document API
### **Endpoint**: `POST /process_pdf`

#### When using on local system : 
```copy
http://localhost:8000/process_pdf/
```
### **Description**:
This API allows you to upload a PDF document for text extraction. Once the text is extracted, it is cleaned and stored in the system. Each request generates a unique chat_id, which can be used for future queries related to the processed content.

### **Request**:
The request should include a PDF file uploaded using multipart/form-data.

#### **Request Body**:
- `file`: The PDF document uploaded in multipart/form-data format.

#### **Functionality**:
1. Extracts text content from the uploaded PDF document.
2. Cleans the extracted text by removing unnecessary characters (extra spaces, line breaks, etc.).
3. Stores the cleaned text and associates it with a unique `chat_id`.


##### When using on local system : 
```copy
http://localhost:8000/process_url/
```

#### **Response**:
After the PDF content is successfully processed, the API returns a unique `chat_id` and a confirmation message.

```json
{
    "chat_id": "unique_chat_id_for_pdf",
    "message": "PDF content processed and stored successfully."
}
```
- `chat_id`: A unique identifier for the content extracted from the PDF (string).
- `message`: A confirmation message indicating that the PDF content was processed successfully (string).


## 3. Chat API
### **Endpoint**: `POST /chat`

### **Description**:
This API allows users to query stored content (either from a processed URL or a PDF document) using a chat_id. The API returns the most relevant response based on the user's question and the content stored.

### **Request**:
The request should contain a `chat_id` referencing the stored content and the user's question.

#### **Request Body**:
```json
{
    "chat_id": "unique_chat_id",
    "question": "What is the main idea of the document?"
}
```
- `chat_id`: The unique identifier for the stored content (string, required).
- `question`: The user's question related to the stored content (string, required).

### **Functionality**:
- Retrieves the stored content using the provided `chat_id`.
- Converts both the content and the user’s query into vector representations using embeddings.
- Compares the query’s embeddings with the stored content’s embeddings using cosine similarity.
- Returns the most relevant section of the content in response to the user’s query.


##### When using on local system : 
```copy
http://localhost:8000/chat/
```

### **Response**:
The API returns the most relevant response based on the query and the stored content.

```json
{
    "response": "The main idea of the document is..."
}
```
- `response`: The system-generated answer to the user's question based on the stored content (string).

## **Summary**
The APIs described in this documentation facilitate the following functionalities:

1. `Process Web URL API`: Scrapes, cleans, and stores content from a specified web URL. Returns a unique chat_id for future reference.

2. `Process PDF Document API`: Extracts, cleans, and stores text from a PDF document. Provides a unique chat_id for future queries.

3. `Chat API`: Allows querying of stored content using a chat_id, providing relevant responses based on the user's questions.

"""