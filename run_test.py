import os
import sys

# Ensure we use the correct directory
os.chdir(r"c:\Users\vinay\Desktop\rag chat bot\rag-chatbot")

try:
    from dotenv import load_dotenv
    from rag_chain import get_rag_chain

    load_dotenv()
    
    # Initialize chain
    print("Initializing RAG chain...")
    chain = get_rag_chain()
    
    # Test query
    prompt = "What is the difference between a stack and a queue?"
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
