
---

# ⚖️ LexAI — Judicial Intelligence System

**LexAI** is a Retrieval-Augmented Generation (RAG) powered legal intelligence assistant built to analyze and answer queries based strictly on statutory data from the Indian Motor Vehicles Act.

It leverages **LangChain, ChromaDB, Ollama (Gemma), and Streamlit** to provide grounded, citation-based legal responses without hallucination.

---

## 🚀 Features

* 🔎 **RAG-based Architecture** (Retrieval + LLM grounding)
* 📚 Vector database powered by **Chroma**
* 🧠 Local LLM via **Ollama (Gemma)**
* 📄 Excel-based statutory ingestion pipeline
* ⚖️ Strict document-bound answering (no hallucinations)
* 🔒 Fully local and private
* 🎨 Premium Streamlit UI (Judicial-themed interface)

---

## 🏗️ Architecture Overview

```
User Query
     ↓
Chroma Vector Store (Embeddings: mxbai-embed-large)
     ↓
Top-K Relevant Legal Sections
     ↓
Prompt Injection (Strict Grounded Template)
     ↓
Gemma LLM (via Ollama)
     ↓
Final Answer (No Assumptions Allowed)
```

---

## 🛠️ Tech Stack

* **Frontend**: Streamlit
* **LLM Runtime**: Ollama
* **Model Used**: gemma3:latest
* **Embeddings**: mxbai-embed-large
* **Vector Store**: ChromaDB
* **Framework**: LangChain
* **Data Source**: Structured Excel (Motor Vehicles Act provisions)

---

## 📂 Project Structure

```
LexAI/
│
├── main.py              # Streamlit App
├── vector.py            # Vector DB ingestion + retriever
├── converted_data.xlsx  # Legal dataset
├── chroma_docs_db2/     # Persisted embeddings
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/lexai.git
cd lexai
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Install Ollama & Models

Install Ollama from:
[https://ollama.com](https://ollama.com)

Pull required models:

```bash
ollama pull gemma3
ollama pull mxbai-embed-large
```

---

## ▶️ Running the Application

```bash
streamlit run main.py
```

The application will launch locally in your browser.

---

## 📊 Accuracy Evaluation

LexAI was tested using structured legal queries based on:

* Statutory definitions
* Penal provisions
* Amendment references
* Rule-making powers
* Insurance & liability provisions

The system demonstrates:

* High grounding reliability
* Strong statutory quotation accuracy
* Correct fallback behavior when information is unavailable

(See `LexAI_Accuracy_Report.txt` for detailed evaluation.)

---

## 🧠 How It Prevents Hallucinations

The prompt template enforces:

* Use ONLY retrieved records
* No external knowledge injection
* Explicit fallback:

  > "The data does not contain this information."

Additionally:

* Context trimming prevents overflow
* Retrieval uses Max Marginal Relevance
* Embedding model optimized for semantic legal search

---

## 🔐 Privacy

* 100% Local Inference
* No API calls
* No external data transmission
* Fully offline capable

---

## 📈 Future Enhancements

* Multi-Act support (IPC, CPC, CrPC)
* Section-wise citation formatting
* PDF ingestion pipeline
* Legal citation scoring
* Confidence estimation output
* Hybrid search (BM25 + Embeddings)

---

## ⚠️ Disclaimer

LexAI is an AI-powered legal research assistant.
It does not constitute legal advice.
For legal matters, consult a qualified legal professional.

---

## 👨‍💻 Author

Built as a Retrieval-Augmented Generation system for statutory law accuracy benchmarking.

---


.
# LexRag-india
