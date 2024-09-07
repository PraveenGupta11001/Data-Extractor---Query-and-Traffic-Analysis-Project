# Use an official Python image as the base
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Expose the necessary ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000 8501

# Command to run both FastAPI and Streamlit concurrently
CMD ["sh", "-c", "fastapi dev apis.py --reload --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 8501"]