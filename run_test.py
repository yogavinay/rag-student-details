import os
import sys

# Avoid Windows console encoding issues (e.g., ₹)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Ensure we run relative to this repo (works on any machine/path)
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(REPO_ROOT)

try:
    from dotenv import load_dotenv
    from rag_chain import get_rag_chain

    load_dotenv()
    
    # Initialize chain
    print("Initializing RAG chain...")
    chain = get_rag_chain()
    
    # Test query (should be answerable from your indexed data)
    prompt = "Summarize the key information in the uploaded document."
    print(f"\nAsking: {prompt}")
    
    # Run the query
    result = chain.invoke(prompt)
    print("\n--- Answer ---")
    print(result)
    print("--------------\nSuccess!!!")
except Exception as e:
    import traceback
    print("\n--- Error ---")
    traceback.print_exc()
