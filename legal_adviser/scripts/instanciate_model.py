"""
Model Instantiation Module

This module loads the vector database and sets up a RAG pipeline for answering
questions about legal cases in colloquial Spanish.
"""

from pathlib import Path
from typing import Optional, Dict, Any
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def load_vector_database(
    persist_directory: Path, collection_name: str = "sentencias_pasadas"
) -> Chroma:
    """
    Load the persisted Chroma vector database.

    Args:
        persist_directory: Directory where the database is stored
        collection_name: Name of the Chroma collection

    Returns:
        Chroma vectorstore instance
    """
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vectorstore = Chroma(
        persist_directory=str(persist_directory),
        embedding_function=embeddings,
        collection_name=collection_name,
    )

    return vectorstore


def create_rag_chain(vectorstore: Chroma, k: int = 3):
    """
    Create a RAG chain for question answering.

    Args:
        vectorstore: Chroma vectorstore with legal cases
        k: Number of relevant documents to retrieve

    Returns:
        Retrieval chain ready for queries
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

    # Custom prompt for colloquial Spanish responses
    system_prompt = """Eres un asistente legal que explica casos de demandas de forma clara y sencilla, como si hablaras con alguien sin conocimientos de derecho.

Usa la siguiente información de casos legales para responder la pregunta:

{context}

Instrucciones:
- Responde en español de forma coloquial y fácil de entender
- Evita términos legales complicados, o explícalos si es necesario
- Sé preciso con la información de los casos
- Si no encuentras la información, dilo claramente"""

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    # Create chains
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    return rag_chain


def ask_question(question: str, rag_chain: Optional[Any] = None) -> Dict[str, Any]:
    """
    Ask a question to the RAG system.

    Args:
        question: Question in natural language
        rag_chain: Pre-initialized RAG chain (if None, creates a new one)

    Returns:
        Dictionary with 'answer' and 'context' (source documents)
    """
    if rag_chain is None:
        persist_dir = DATA_DIR / "chroma_db"
        vectorstore = load_vector_database(persist_dir)
        rag_chain = create_rag_chain(vectorstore)

    response = rag_chain.invoke({"input": question})
    return response


def initialize_qa_system():
    """
    Initialize the complete QA system.

    Returns:
        Ready-to-use RAG chain
    """
    persist_dir = DATA_DIR / "chroma_db"

    print("Loading vector database...")
    vectorstore = load_vector_database(persist_dir)
    print(f"Loaded {vectorstore._collection.count()} documents")

    print("Creating RAG chain...")
    rag_chain = create_rag_chain(vectorstore)
    print("QA system ready!")

    return rag_chain


if __name__ == "__main__":
    # Test the system
    rag_chain = initialize_qa_system()

    test_question = "¿Cuál fue la sentencia del caso de acoso escolar?"
    print(f"\nTest question: {test_question}")
    response = ask_question(test_question, rag_chain)
    print(f"\nAnswer: {response['answer']}")
