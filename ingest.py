import os
import json
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Configuration
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db")
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
    Loads JSON documents from the data directory, splits them into chunks,
    generates embeddings, and stores them in a local Chroma database.
    """
    if not os.path.exists(DATA_DIR):
        print(f"Directory '{DATA_DIR}' does not exist. Creating one...")
        os.makedirs(DATA_DIR)
        print(f"Please place your JSON files in the '{DATA_DIR}' directory and run again.")
        return

    json_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.json')]
    if not json_files:
        print(f"No JSON files found in '{DATA_DIR}'. Please add some JSON files.")
        return

    documents = []
    print("Loading JSON documents...")
    for file in json_files:
        file_path = os.path.join(DATA_DIR, file)
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
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

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
