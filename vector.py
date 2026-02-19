import os
import pandas as pd
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# =========================
# CONFIG (UNCHANGED)
# =========================
XLSX_FILE = r"C:\Users\kavin\Desktop\LLM Project\converted_data.xlsx"
DB_LOCATION = "./chroma_docs_db2"
COLLECTION_NAME = "document_store"

# =========================
# LOAD DATA
# =========================
df = pd.read_excel(XLSX_FILE)
df = df.fillna("")  # Prevent NoneType embedding errors

# =========================
# EMBEDDING MODEL (UNCHANGED)
# =========================
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# =========================
# VECTOR STORE (UNCHANGED LOCATION)
# =========================
vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    persist_directory=DB_LOCATION,
    embedding_function=embeddings
)

# Safer count method
try:
    existing_count = vector_store._collection.count()
except Exception:
    existing_count = 0

print("Existing documents in DB:", existing_count)

# =========================
# PREPARE DOCUMENTS (ENHANCED)
# =========================
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,          # Kept within mxbai-embed-large's 512-token limit
    chunk_overlap=50,        # Overlap for section continuity
    separators=["\n\n", "\n", ".", " ", ""]
)

documents = []
ids = []

for i, row in df.iterrows():
    content = (
        f"Title: {row['title']}\n\n"
        f"Section Content:\n{row['description']}"
    )

    chunks = splitter.split_text(content)

    for j, chunk in enumerate(chunks):
        doc_id = f"{i}_{j}"

        doc = Document(
            page_content=chunk.strip(),
            metadata={
                "title": row["title"],
                "row_index": i,
                "source": "motor_vehicles_act"
            },
            id=doc_id
        )

        documents.append(doc)
        ids.append(doc_id)

# =========================
# INGEST (ONLY IF EMPTY)
# =========================
if existing_count == 0:
    print("Ingesting documents into Chroma...")
    for idx, doc in enumerate(documents):
        try:
            vector_store.add_documents(
                documents=[doc],
                ids=[ids[idx]]
            )
            if idx % 100 == 0:
                print(f"Inserted {idx}/{len(documents)} documents...")
        except Exception as e:
            print(f"Skipping document {ids[idx]} due to error: {e}")
            continue

    print("Final document count:", vector_store._collection.count())
else:
    print("Using existing embeddings. No re-ingestion needed.")

# =========================
# RETRIEVER (ACCURACY BOOSTED)
# =========================
retriever = vector_store.as_retriever(
    search_type="mmr",   # Improves relevance diversity
    search_kwargs={
        "k": 8,          # Final returned docs
        "fetch_k": 25,   # Retrieve more before filtering
        "lambda_mult": 0.7
    }
)
