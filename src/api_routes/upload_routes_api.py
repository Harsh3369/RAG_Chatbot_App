from fastapi import APIRouter, UploadFile, File, Depends
import os
import shutil
from fastapi import FastAPI, HTTPException
from src.pipelines.data_ingestion_pipeline import DocumentLoader
from src.pipelines.document_embedding_pipeline import DocumentProcessor

upload_router = APIRouter()

@upload_router.post("/upload/")
async def upload_document(file: UploadFile = File(...), app: FastAPI = Depends()):
    """
    Upload a document, process it, and store chunks in FastAPI state.
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

        # Process the document
        processor = DocumentProcessor(documents)
        vector_db = processor.store_in_chromadb()

        # Get document chunks
        chunks = processor.chunk_documents()
        if not chunks:
            raise HTTPException(status_code=500, detail="Failed to generate chunks.")

        # Store in app state
        app.state.vector_db = vector_db
        app.state.chunks = chunks

        return {"message": f"Document '{file.filename}' processed successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
