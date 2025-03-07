from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain import hub
from config.config import GPT4O_MINI_CONFIG

class RAGPipeline:
    def __init__(self, retriever):
        """
        Initializes the RAG pipeline with a retriever.

        Parameters:
        - retriever: The retrieval mechanism for fetching relevant document chunks.
        """
        self.retriever = retriever
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            openai_api_key=GPT4O_MINI_CONFIG['OPENAI_API_KEY_4o_MINI']
        )
        self.prompt = hub.pull("rlm/rag-prompt")
        print("RAG pipeline initialized")

    @staticmethod
    def format_docs(docs):
        """Formats retrieved documents into a structured text format."""
        return "\n\n".join(doc.page_content for doc in docs)

    def generate_response(self, question):
        """
        Generates a response using the RAG pipeline.

        Parameters:
        - question (str): The input query for which a response is needed.

        Returns:
        - str: The generated response.
        """
        rag_chain = (
            {"context": self.retriever | self.format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        response = rag_chain.invoke(question)
        return response
