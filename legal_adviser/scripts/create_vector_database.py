"""
Vector Database Creation Module

This module creates a persistent vector database from legal case data stored in Excel format.
Each row in the Excel file represents a complete legal case and is stored as a separate chunk.
"""

import pandas as pd
from pathlib import Path
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()


def load_excel_as_documents(excel_path: Path) -> List[Document]:
    """
    Load Excel file and convert each row into a LangChain Document.

    Args:
        excel_path: Path to the Excel file containing legal cases

    Returns:
        List of Document objects, one per Excel row
    """
    df = pd.read_excel(excel_path)

    documents = []
    for idx, row in df.iterrows():
        # Combine all columns into a structured text representation
        content_parts = []

        for column in df.columns:
            value = row[column]
            if pd.notna(value):  # Only add non-null values
                content_parts.append(f"{column}: {value}")

        content = "\n".join(content_parts)
        documents.append(Document(page_content=content))

    return documents


def create_vector_database(
        documents: List[Document],
        persist_directory: Path,
        collection_name: str = "sentencias_pasadas",
        batch_size: int = 100
) -> Chroma:
    """
    Create and persist a Chroma vector database from documents.

    Args:
        documents: List of Document objects to embed and store
        persist_directory: Directory where the database will be persisted
        collection_name: Name for the Chroma collection
        batch_size: Number of documents to process per batch

    Returns:
        Chroma vectorstore instance
    """
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # Process first batch to create the vectorstore
    vectorstore = Chroma.from_documents(
        documents=documents[:batch_size],
        embedding=embeddings,
        persist_directory=str(persist_directory),
        collection_name=collection_name
    )

    # Add remaining documents in batches
    for i in range(batch_size, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        vectorstore.add_documents(batch)
        print(f"Processed {min(i + batch_size, len(documents))}/{len(documents)} documents")

    return vectorstore


def main() -> None:

    # Get project root (assuming script is in scripts/ folder)
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"
    excel_path = data_dir / "sentencias_pasadas.xlsx"
    persist_dir = data_dir / "chroma_db"

    # Ensure data directory exists
    persist_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading Excel file from: {excel_path}")
    documents = load_excel_as_documents(excel_path)
    print(f"Loaded {len(documents)} legal cases")

    print("Creating vector database...")
    vectorstore = create_vector_database(documents, persist_dir)
    print(f"Vector database created and persisted at: {persist_dir}")
    print(f"Total documents in collection: {vectorstore._collection.count()}")


if __name__ == "__main__":
    main()