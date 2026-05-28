import os
import json
from dotenv import load_dotenv

load_dotenv()
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings

# Configuration
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db_nvidia")
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def flatten_json(obj, prefix=""):
    """Recursively flatten a JSON object into readable text lines."""
    lines = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_key = f"{prefix}.{key}" if prefix else key
            lines.extend(flatten_json(value, new_key))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            lines.extend(flatten_json(item, f"{prefix}[{i}]"))
    else:
        lines.append(f"{prefix}: {obj}")
    return lines


def ingest_documents():
    """
    Loads documents from the data directory (PDF/TXT/JSON), splits them into
    chunks, generates embeddings, and stores them in a local Chroma database.
    """
    if not os.path.exists(DATA_DIR):
        print(f"Directory '{DATA_DIR}' does not exist. Creating one...")
        os.makedirs(DATA_DIR)
        print(f"Please place your PDF/TXT/JSON files in the '{DATA_DIR}' directory and run again.")
        return

    supported_exts = (".pdf", ".txt", ".json")
    data_files = [f for f in os.listdir(DATA_DIR) if f.lower().endswith(supported_exts)]
    if not data_files:
        print(
            f"No supported files found in '{DATA_DIR}'. "
            f"Add one of: {', '.join(supported_exts)}"
        )
        return

    documents = []
    print("Loading documents...")
    for file in data_files:
        file_path = os.path.join(DATA_DIR, file)
        ext = os.path.splitext(file)[1].lower()

        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            for d in docs:
                d.metadata["source"] = file
            documents.extend(docs)
            print(f"Loaded: {file} ({len(docs)} pages)")

        elif ext == ".txt":
            loader = TextLoader(file_path, encoding="utf-8")
            docs = loader.load()
            for d in docs:
                d.metadata["source"] = file
            documents.extend(docs)
            print(f"Loaded: {file} ({sum(len(d.page_content) for d in docs)} characters)")

        elif ext == ".json":
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Flatten the JSON into readable text
            text_lines = flatten_json(data)
            text_content = "\n".join(text_lines)

            doc = Document(page_content=text_content, metadata={"source": file})
            documents.append(doc)
            print(f"Loaded: {file} ({len(text_content)} characters)")

    if not documents:
        print("No documents were loaded. Please check your JSON files.")
        return

    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Total chunks created: {len(chunks)}")

    print("Initializing embedding model (sentence-transformers)...")
    embeddings = None
    try:
        # Prefer local HF embeddings if already cached (works offline).
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={"local_files_only": True},
        )
        print("Using local HuggingFace embeddings: all-MiniLM-L6-v2")
    except Exception as e:
        # Fallback: use NVIDIA embeddings (requires NVIDIA_API_KEY)
        api_key = os.environ.get("NVIDIA_API_KEY")
        if not api_key:
            raise RuntimeError(
                "Could not load local HuggingFace embeddings (offline) and NVIDIA_API_KEY is missing. "
                "Either connect to the internet once to cache 'all-MiniLM-L6-v2', or set NVIDIA_API_KEY "
                "to use NVIDIA embeddings."
            ) from e

        print("Falling back to NVIDIA embeddings.")
        embeddings = NVIDIAEmbeddings(
            api_key=api_key,
        )

    # Remove old DB if it exists to avoid duplicates
    if os.path.exists(DB_DIR):
        import shutil
        shutil.rmtree(DB_DIR)
        print("Cleared old database.")

    print(f"Creating Chroma vector database in '{DB_DIR}'...")
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR
    )

    print("Ingestion complete! Database saved successfully.")


if __name__ == "__main__":
    ingest_documents()
