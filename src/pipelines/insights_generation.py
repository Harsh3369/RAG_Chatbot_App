from config.prompt import insights_generation_prompt_template
from langchain_openai import ChatOpenAI 
from langchain.prompts import PromptTemplate
# Load config parameters
from config.config import GPT4O_MINI_CONFIG

class InsightsGenerator:
    def __init__(self, model="gpt-4o-mini", temperature=0, api_key=GPT4O_MINI_CONFIG['OPENAI_API_KEY_4o_MINI']):
        """
        Initializes the InsightsGenerator class.

        Parameters:
        - model (str): OpenAI model to use.
        - temperature (float): Controls randomness of the response.
        - api_key (str): OpenAI API key.
        """
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            openai_api_key=api_key
        )

    def generate_insights(self, chunks, topic="Data Analytics Insights"):
        """
        Generates insights from document chunks.

        Parameters:
        - chunks (list): List of document chunks to process.
        - topic (str): The main topic for the insights.

        Returns:
        - str: Generated insights summary.
        """
        if not chunks:
            return "No content provided for insights generation."

        # Prepare context by joining the first 100 chunks
        insight_context = "\n".join([chunk.page_content for chunk in chunks[:100]])

        # Format the prompt with topic and context
        insights_prompt = insights_generation_prompt_template.format(
            topic=topic,
            context=insight_context
        )

        # Generate summary using LLM
        summary = self.llm.invoke(insights_prompt)

        return summary.content
