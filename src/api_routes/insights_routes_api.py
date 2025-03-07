from fastapi import APIRouter, Depends, FastAPI, HTTPException
from src.pipelines.insights_generation import InsightsGenerator
from config.config import GPT4O_MINI_CONFIG

insights_router = APIRouter()

openai_api_key = GPT4O_MINI_CONFIG['OPENAI_API_KEY_4o_MINI']

@insights_router.get("/insights/")
async def get_insights(app: FastAPI = Depends()):
    """
    Generate insights from stored document chunks.
    """
    try:
        chunks = getattr(app.state, "chunks", None)
        if not chunks:
            raise HTTPException(status_code=400, detail="No document chunks available.")

        insights = InsightsGenerator(model="gpt-4o-mini", api_key=openai_api_key)
        summary = insights.generate_insights(chunks, topic="Data Analytics Insights")

        return {"insights": summary}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating insights: {str(e)}")
