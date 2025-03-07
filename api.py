import os
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import uvicorn
from pydantic import BaseModel
from src.pipelines.data_ingestion_pipeline import DocumentLoader
from src.pipelines.document_embedding_pipeline import DocumentProcessor
from src.pipelines.insights_generation import InsightsGenerator
from src.pipelines.document_rag_chatbot import RAGPipeline
from langchain_openai import ChatOpenAI

from config.config import GPT4O_MINI_CONFIG

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Global variables
vector_db = None
chunks = None  # Store chunks globally after processing
openai_api_key = GPT4O_MINI_CONFIG['OPENAI_API_KEY_4o_MINI']  # Get from environment

if not openai_api_key:
    raise Exception("OPENAI_API_KEY is not set in the environment.")


# **Upload & Process Document**
@app.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    """
    Uploads a document, processes it, chunks it, and stores it in vector_db.
    """
    try:
        file_path = f"uploaded_files/{file.filename}"
        os.makedirs("uploaded_files", exist_ok=True)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Load document content
        loader = DocumentLoader(file_path)
        documents = loader.load()

        if not documents:
            raise HTTPException(status_code=500, detail="Failed to load document.")

        # Process the document and store in vector DB
        processor = DocumentProcessor(documents)
        global vector_db, chunks
        vector_db = processor.store_in_chromadb()

        # Get document chunks
        chunks = processor.chunk_documents()
        if not chunks:
            raise HTTPException(status_code=500, detail="Failed to generate chunks.")

        return {"message": f"Document '{file.filename}' processed successfully."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# **Generate Insights**
@app.get("/insights/")
async def get_insights():
    """
    Generates insights from stored document chunks.
    """
    try:
        if not chunks:
            raise HTTPException(status_code=400, detail="No document chunks available.")

        # Generate insights
        insights = InsightsGenerator(model="gpt-4o-mini", api_key=openai_api_key)
        summary = insights.generate_insights(chunks, topic="Data Analytics Insights")

        return {"insights": summary}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating insights: {str(e)}")


# **Chat with RAG**
class ChatRequest(BaseModel):
    query: str

@app.post("/chat/")
async def chat_with_bot(request: ChatRequest):
    """
    Handles chat queries using the retriever.
    """
    try:
        if vector_db is None:
            raise HTTPException(status_code=400, detail="No documents uploaded yet.")

        retriever = vector_db.as_retriever()
        rag_pipeline = RAGPipeline(retriever)
        response = rag_pipeline.generate_response(request.query)

        return {"query": request.query, "response": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chat response: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)