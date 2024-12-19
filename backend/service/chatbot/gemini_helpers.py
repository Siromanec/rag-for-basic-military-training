import google.generativeai as genai
from langchain.vectorstores.base import VectorStoreRetriever


def get_RAG_prompt(query: str, context: str):
    prompt = (
        f"You are a helpful and informative assistant that answers questions using the reference passage provided. "
        f"Respond in a complete sentence and ensure the response is easy to understand and concise. Answer in Ukrainian."
        f"If the context does not contain relevant information, ignore it and answer to the best of your ability.\n\n"
        f"QUESTION: {query}\n"
        f"CONTEXT: {context}\n\n"
        f"ANSWER:"
    )
    return prompt


def generate_RAG_response(query: str, retriever: VectorStoreRetriever, llm: genai.GenerativeModel):
    retrieved_docs = retriever.invoke(query)
    context = " ".join([doc.page_content for doc in retrieved_docs])

    prompt = get_RAG_prompt(query, context)

    response = llm.generate_content(prompt)

    return {
        "response": response.candidates[0].content.parts[0].text,
        "retrieved_docs": retrieved_docs
    }
