# Use official Python image as base
FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PORT=8501

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy only dependency files first (for caching)
COPY requirements.txt ./

# Install dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000 8501

# Start FastAPI and Streamlit together
CMD ["bash", "-c", "uvicorn api:app --host 0.0.0.0 --port 8000 & streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0"]