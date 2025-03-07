from fastapi import APIRouter, HTTPException, Form
from src.pipelines.document_rag_chatbot import RAGPipeline
from config.config import GPT4O_MINI_CONFIG

openai_api_key = GPT4O_MINI_CONFIG['OPENAI_API_KEY_4o_MINI']
chat_router = APIRouter()

# Global variable for storing vector database
vector_db = None

@chat_router.post("/chat/")
async def chat_with_bot(query: str = Form(...)):
    """
    Handles chat queries using the retriever.
    """
    try:
        if vector_db is None:
            raise HTTPException(status_code=400, detail="No documents uploaded yet.")

        retriever = vector_db.as_retriever()
        rag_pipeline = RAGPipeline(retriever)
        response = rag_pipeline.generate_response(query)

        return {"query": query, "response": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chat response: {str(e)}")
