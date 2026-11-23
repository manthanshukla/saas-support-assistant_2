
from app.services.retrieval import retrieve_documents

questions = [
    "How do I reset my password?",
    "Does CloudDesk support two-factor authentication?",
    "How can I cancel my subscription?",
    "How do I manage team members?"
]

for question in questions:

    print("\nQuestion:", question)

    results = retrieve_documents(question)

    if results:
        for result in results:
            print("Relevant information:", result["content"])
            print("Score:", result["score"])
    else:
        print("No relevant information found.")
