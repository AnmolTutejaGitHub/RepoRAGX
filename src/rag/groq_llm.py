from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()


class GroqLLM:
    def __init__(
        self,
        model_name="llama-3.3-70b-versatile",
        temperature=0.1,
        max_tokens=1024
    ):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment")

        print("Initializing Groq LLM...")

        self.llm = ChatGroq(
            groq_api_key=api_key,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )

    def rag(self,query,retriever,top_k=5):
        print(f"Running RAG for query: {query}")

        results = retriever.retrieve(query,top_k=top_k)

        if not results:
            return "No relevant context found to answer the question."

        context_parts = []
        for doc in results:
            meta = doc.get("metadata",{})
            header = f"File: {meta.get('path','unknown')}"
            context_parts.append(f"--- {header} ---\n{doc['content']}")
        
        context = "\n\n".join(context_parts)

        prompt = f"""
            Use the following context to answer the question concisely.

            Context:
            {context}

            Question: {query}

            Answer:
            """

        response = self.llm.invoke(prompt)
        return response.content