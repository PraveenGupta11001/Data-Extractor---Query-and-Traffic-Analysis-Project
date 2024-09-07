## **Data Extractor & Query and Traffic Analysis Project**

### **Overview**
This repository contains two assignments:

1. `Assignment 1`: A project using FastAPI and Streamlit for content extraction from web URLs and PDF documents, with chat functionality for querying stored content. The assignment is fully dockerized.

2. `Assignment 2`: A data analysis project involving web traffic analysis to gain insights on events like clicks and pageviews.


### **Assignment 1: FastAPI & Streamlit Project**
#### **Features:**
- **Process Web URL API**: Scrapes and stores content from URLs.
- **Process PDF API**: Extracts and stores text from uploaded PDFs.
- **Chat API**: Allows users to query stored content.
- **Streamlit Interface**: A front-end page that interacts with the APIs, with functionalities like viewing data, filtering, and searching.

### **API Documentation:**
The full API documentation is available in the Streamlit app under the API Documentation tab.

1. Build the Docker image:
```copy
docker build -t fastapi-streamlit-app .
```
2. Run the container:

```copy
docker run -p 8000:8000 -p 8501:8501 fastapi-streamlit-app
```

3. **Stopping/Removing Containers**: If you stop the container (using Ctrl+C), remove the container with:

```copy
docker ps  # To check running containers
docker stop <container_id> # To stop running container
docker rm <container_id> # To remove docker container
```

### **Assignment 2: Web Traffic Data Analysis**
- **Dataset**: Contains 226,278 rows and 9 columns, capturing events such as clicks and pageviews.
- **Tools Used**: Pandas, SciPy, and Pandas `groupby` for analysis.

Example of data:

| event | date       | country      | city   | artist | album       | track       | isrc          | linkid                                   |
|-------|------------|--------------|--------|--------|-------------|-------------|---------------|------------------------------------------|
| click | 2021-08-21 | Saudi Arabia | Jeddah | Tesher | Jalebi Baby | Jalebi Baby | QZNWQ2070741  | 2d896d31-97b6-4869-967b-1c5fb9cd4bb8    |



### **Installation**
1. Install the required packages :
```copy
pip install -r requirements.txt
```

### **Conclusion**
This project showcases content extraction using FastAPI and Streamlit, with Docker for deployment, as well as web traffic data analysis using Python libraries.
