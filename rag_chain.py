"""
rag_chain.py — RAG Pipeline for DSA Mentor AI
-----------------------------------------------
Provides two main functions:
  - get_rag_chain()        : returns the LCEL chain (kept for backward compat)
  - get_rag_response(query, topic_filter) : returns answer + source docs
"""

import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Load environment variables from .env file
load_dotenv()

# Configuration — use absolute paths
DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db")


def format_docs(docs):
    """Helper function to format retrieved documents into a single string."""
    return "\n\n".join(doc.page_content for doc in docs)


def _build_components():
    """
    Internal: initialise embeddings, vectorstore, retriever, and LLM once.
    Returns (retriever, llm).
    """
    # 1. Embeddings (same model used in ingest.py)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 2. Load Chroma vector DB
    if not os.path.exists(DB_DIR):
        raise FileNotFoundError(
            f"Database directory '{DB_DIR}' not found. Please run ingest.py first."
        )
    vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)

    # 3. Retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # 4. Gemini LLM
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Please add it to the .env file.")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.3,
    )

    return vectorstore, retriever, llm


def get_rag_chain():
    """
    Legacy helper — returns a simple LCEL chain (str in → str out).
    """
    _, retriever, llm = _build_components()

    prompt = ChatPromptTemplate.from_template(
        """You are **DSA Mentor AI**, an expert tutor for Data Structures and Algorithms.

Use the following retrieved context to answer the question.
If the answer is not found in the context, use your own knowledge to provide a helpful, accurate answer about DSA.
Always include code examples in Python when relevant, and mention time/space complexity.

Context:
{context}

Question: {question}

Answer (use markdown formatting, code blocks, and bullet points):"""
    )

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain


def get_rag_response(query: str, topic_filter: str = "All Topics"):
    """
    High-level API used by the Streamlit UI.

    Parameters
    ----------
    query : str
        The user's question.
    topic_filter : str
        Optional topic filter (e.g. "Arrays", "Trees"). "All Topics" = no filter.

    Returns
    -------
    dict  {"answer": str, "sources": list[dict]}
        answer  — the LLM-generated response (markdown string)
        sources — list of {"content": str, "source": str} for retrieved chunks
    """
    vectorstore, _, llm = _build_components()

    # ----- Build search query with optional topic hint -------------------
    search_query = query
    if topic_filter and topic_filter != "All Topics":
        search_query = f"{topic_filter}: {query}"

    # Retrieve relevant docs
    docs = vectorstore.similarity_search(search_query, k=5)

    context = format_docs(docs)

    # ----- Prompt --------------------------------------------------------
    prompt = ChatPromptTemplate.from_template(
        """You are **DSA Mentor AI** 🧠, an expert tutor for Data Structures and Algorithms.

You must answer the student's question using the retrieved context below AND your own expert knowledge.
Follow these rules:
1. Always provide **clear explanations** with real-world analogies when possible.
2. Include **Python code examples** with proper syntax highlighting when relevant.
3. Always state the **Time Complexity** and **Space Complexity** of any algorithm or solution you discuss.
   Format them as: `Time: O(...)` | `Space: O(...)`.
4. Use **markdown** formatting: headers, bullet points, numbered lists, bold text, and code blocks.
5. If the topic is about a specific data structure, briefly describe it before diving into the solution.
6. Be encouraging and supportive — you are a mentor!

Context from knowledge base:
{context}

Student's question: {question}

Your detailed answer:"""
    )

    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({"context": context, "question": query})

    # ----- Collect source metadata ---------------------------------------
    sources = []
    for doc in docs:
        sources.append(
            {
                "content": doc.page_content[:300] + ("…" if len(doc.page_content) > 300 else ""),
                "source": doc.metadata.get("source", "Unknown"),
            }
        )

    return {"answer": answer, "sources": sources}
