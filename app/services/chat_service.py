
from app.services.retrieval import retrieve_documents
from app.services.llm_service import generate_response


def process_chat(message, conversation=None):

    # Step 1: Retrieve relevant documents
    documents = retrieve_documents(message)

    # Step 2: Check whether documents were found
    if not documents:
        return {
            "answer": "I could not find this information in the available product documentation.",
            "status": "not_found",
            "sources": [],
            "confidence": 0.15
        }

    # Step 3: Prepare context
    context = "\n".join(
        [doc["content"] for doc in documents]
    )

    # Step 4: Call LLM
    answer = generate_response(
        question=message,
        context=context,
        conversation=conversation
    )

    # Step 5: Prepare response
    return {
        "answer": answer,
        "status": "answered",
        "sources": ["CloudDesk Knowledge Base"],
        "confidence": 0.90
    }
