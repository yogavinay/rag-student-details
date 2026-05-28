"""
rag_chain.py — RAG Pipeline
---------------------------
Provides two main functions:
  - get_rag_chain()        : returns the LCEL chain (kept for backward compat)
  - get_rag_response(query, topic_filter) : returns answer + source docs
"""

import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Load environment variables from .env file
load_dotenv()

# Configuration — use absolute paths
DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db_nvidia")


def format_docs(docs):
    """Helper function to format retrieved documents into a single string."""
    return "\n\n".join(doc.page_content for doc in docs)


def _build_components():
    """
    Internal: initialise embeddings, vectorstore, retriever, and LLM once.
    Returns (retriever, llm).
    """
    # 1. Embeddings (must match ingest.py)
    embeddings = None
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={"local_files_only": True},
        )
    except Exception:
        api_key = os.environ.get("NVIDIA_API_KEY")
        if not api_key:
            raise ValueError("NVIDIA_API_KEY not found. Please add it to the .env file.")
        embeddings = NVIDIAEmbeddings(
            api_key=api_key,
        )

    # 2. Load Chroma vector DB
    if not os.path.exists(DB_DIR):
        raise FileNotFoundError(
            f"Database directory '{DB_DIR}' not found. Please run ingest.py first."
        )
    vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)

    # 3. Retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # 4. Gemini LLM
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("NVIDIA_API_KEY not found. Please add it to the .env file.")

    llm = ChatNVIDIA(
        model="meta/llama3-70b-instruct",
        api_key=api_key,
        temperature=0.3,
    )

    return vectorstore, retriever, llm


def get_rag_chain():
    """
    Legacy helper — returns a simple LCEL chain (str in → str out).
    """
    _, retriever, llm = _build_components()

    prompt = ChatPromptTemplate.from_template(
        """You are a helpful assistant with access to a retrieved knowledge base.

Use the context below to answer the question as accurately as possible.
If the answer is not in the context, say you don't have it in the provided documents (do not guess).

Context:
{context}

Question: {question}

Answer (use markdown formatting when helpful):"""
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
        """You are a helpful assistant with access to a retrieved knowledge base.

Answer the user's question using the context below.
If the answer is not contained in the context, say you don't have enough information in the provided documents.

Context from knowledge base:
{context}

User's question: {question}

Your answer:"""
    )

    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({"context": context, "question": query})

    # ----- Collect source metadata ---------------------------------------
    sources = []
    for doc in docs:
        page = doc.metadata.get("page")
        page_str = f" (page {page + 1})" if isinstance(page, int) else ""
        sources.append(
            {
                "content": doc.page_content[:300] + ("…" if len(doc.page_content) > 300 else ""),
                "source": f"{doc.metadata.get('source', 'Unknown')}{page_str}",
            }
        )

    return {"answer": answer, "sources": sources}
