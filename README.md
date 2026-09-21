# 🤖 CodeAtlas

> **AI-powered GitHub Repository Assistant for intelligent repository understanding, analysis, explainable retrieval, and evidence-based documentation.**

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![LangChain](https://img.shields.io/badge/LangChain-RAG-success)
![FAISS](https://img.shields.io/badge/FAISS-VectorDB-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![Groq](https://img.shields.io/badge/Groq-LLM-purple)
![FastEmbed](https://img.shields.io/badge/FastEmbed-Embeddings-blueviolet)

---

## 📌 Overview

**CodeAtlas** is an AI-powered GitHub Repository Assistant that helps developers understand unfamiliar codebases through natural-language interaction and automated repository analysis.

Users provide a **public GitHub repository URL**, and CodeAtlas:

- Clones and indexes the repository
- Analyzes its source-code structure
- Detects languages, files, functions, classes, and entry points
- Reconstructs internal dependencies
- Performs change-impact analysis
- Creates a semantic knowledge base using **Retrieval-Augmented Generation (RAG)**
- Answers repository questions using retrieved source-code evidence
- Shows retrieval evidence and relevance scores
- Reconstructs an **evidence-based Software Requirements Specification (SRS)** from the repository

The system combines **static repository analysis** with **LLM-powered conversational retrieval**, providing both structural understanding and natural-language interaction.

---

 ## 🎥 Demo

A complete walkthrough of CodeAtlas covering repository ingestion, repository intelligence, dependency analysis, change-impact analysis, explainable RAG, and evidence-based SRS generation.


![](https://github.com/user-attachments/assets/c8dbd78c-2e9c-43c0-8236-fd66eadda242)



## ✨ Key Features

### 1. 🧠 Repository Intelligence

CodeAtlas automatically analyzes the repository source code and builds a structured repository profile.

It detects:

- Programming languages
- Source files
- Functions
- Classes
- Entry points
- Directory structure
- Largest files
- Internal dependencies

**Analysis approach:** For Python repositories, CodeAtlas uses **Python AST parsing** to inspect classes, functions, and imports. For other supported languages, it uses language-specific file and pattern analysis to extract structural information.

### 2. 🕸️ Dependency Graph

CodeAtlas reconstructs internal relationships between repository files/modules based on source-code dependencies.

```text
simulation/generate_dataset.py
            │
            ▼
simulation/queue_simulator.py
```

The dependency analysis identifies source files, dependent files, internal dependency edges, and repository-level relationships. This information is also used by the change-impact analysis module.

### 3. 🔍 Change Impact Analysis

CodeAtlas analyzes the potential effect of modifying a repository file.

Given a changed file, the system identifies:

- Direct dependents
- Indirect dependents
- Total affected files
- Change-sensitive repository hotspots

The analysis uses the reconstructed dependency graph and reverse dependency traversal to determine which components may be affected by a change.

### 4. 📚 Explainable Retrieval

CodeAtlas does not only return an LLM-generated answer. For every repository question, the system retrieves relevant source-code chunks from the FAISS vector database and exposes the evidence used by the retrieval pipeline.

The interface displays:

- Retrieved source files
- Retrieval rank
- Relevance score
- Evidence preview

This makes repository answers easier to inspect and verify.

> **Important:** Retrieval relevance scores indicate the relevance of retrieved evidence, not the probability that the final answer is correct.

### 5. 📄 Evidence-Based SRS Generation

CodeAtlas can automatically reconstruct a Software Requirements Specification from repository evidence.

```text
Repository Analysis
        ↓
Capability Detection
        ↓
Requirement Construction
        ↓
Evidence Mapping
        ↓
SRS Section Generation
        ↓
Formatted SRS
```

The generated SRS can include:

- Introduction
- Overall Description
- External Interface Requirements
- System Features
- Nonfunctional Requirements (when supported)
- Other Requirements (when supported)
- Glossary
- Analysis Models
- Evidence Traceability
- Change-Sensitivity Snapshot

**Evidence-first approach:** CodeAtlas deliberately avoids inventing unsupported requirements. Requirements are mapped back to repository evidence such as source files, functions, classes, dependencies, and detected capabilities. The SRS reconstruction itself is performed using **deterministic application logic**, rather than sending the entire repository to an external LLM for document generation.

### 6. 💬 Repository Chatbot

Users can ask natural-language questions about the indexed repository:

```text
What does this project do?
Explain the repository architecture.
Which files implement the UI?
Where is the machine-learning logic?
Which files depend on this module?
How does the application execute?
What technologies are used?
Explain this repository for a beginner.
```

The chatbot uses the repository as its primary knowledge source and returns answers together with supporting evidence.

---

## 🏗️ System Architecture

```text
                            User
                              │
                              ▼
                     Streamlit Frontend
                              │
                              ▼
                       FastAPI Backend
                              │
             ┌────────────────┴────────────────┐
             │                                 │
             ▼                                 ▼
    Repository Ingestion              Repository Intelligence
             │                                 │
             ▼                                 ├── Language Detection
       Clone Repository                        ├── Structure Analysis
             │                                 ├── Dependency Analysis
             ▼                                 ├── Entry Point Detection
      Load Source Files                        ├── File Analysis
             │                                 └── Architecture Profile
             ▼
        Text Chunking
             │
             ▼
     FastEmbed Embeddings
             │
             ▼
         FAISS Index
             │
             ▼
       Retrieval Service
             │
             ▼
      Relevant Evidence
             │
             ▼
       Chat / RAG Service
             │
             ▼
        Groq LLM
             │
             ▼
      Answer + Sources
             │
             ▼
       Streamlit UI
```

### Repository Intelligence Flow

```text
Repository
    │
    ▼
Repository Analyzer
    │
    ├── Language Detection
    ├── Code Structure Analysis
    ├── Dependency Analysis
    ├── Entry Point Detection
    ├── Largest File Detection
    └── Directory Structure
    │
    ▼
Repository Profile
    │
    ├── Repository Intelligence
    ├── Dependency Graph
    ├── Change Impact Analysis
    └── Evidence-Based SRS
```

---

## 🧠 How CodeAtlas Works

### Step 1 — Repository Ingestion

The user provides a public GitHub repository URL:

```text
https://github.com/username/project
```

CodeAtlas validates the repository URL and clones the repository locally using **GitPython**.

### Step 2 — Document Loading

The repository is recursively scanned for supported source and documentation files, including Python, Java, C/C++, JavaScript, TypeScript, HTML, CSS, JSON, YAML, Markdown, and plain text files.

Excluded directories such as `.git`, `node_modules`, virtual environments, and generated build directories are skipped during indexing.

Each loaded file is converted into a document with metadata such as its source path and file type.

### Step 3 — Text Chunking

Large files are divided into smaller chunks using LangChain's **Recursive Character Text Splitter**.

```text
Chunk size: 1000
Chunk overlap: 200
```

Chunking allows the retrieval system to work with relevant portions of large files instead of retrieving entire files unnecessarily.

### Step 4 — Embedding Generation

Each chunk is converted into a vector representation using `BAAI/bge-small-en-v1.5` through **FastEmbed**, enabling semantic similarity search over repository content.

### Step 5 — Vector Storage

The generated embeddings are stored in a **FAISS vector database**, enabling efficient similarity search over indexed repository chunks.

### Step 6 — Repository Intelligence

In parallel with semantic indexing, CodeAtlas analyzes the repository structurally, extracting languages, files, functions, classes, imports, dependencies, entry points, and directory structure. The resulting repository profile is persisted for later use by the architecture, dependency, impact, and SRS modules.

### Step 7 — Retrieval-Augmented Generation

```text
Question
   ↓
Similarity Retrieval
   ↓
Top Relevant Chunks
   ↓
Evidence Ranking
   ↓
Prompt Construction
   ↓
Groq LLM
   ↓
Answer + Sources + Evidence
```

The current retrieval layer ranks candidate chunks and returns the most relevant evidence to the chat service.

### Step 8 — Evidence-Based SRS Reconstruction

```text
Capability Detection
        ↓
Requirement Builder
        ↓
Evidence Mapper
        ↓
SRS Sections
        ↓
SRS Formatter
```

Only capabilities and requirements supported by repository evidence are represented.

---

## ⚙️ Technology Stack

| Category              | Technology                           |
| ---------------------- | ------------------------------------ |
| Programming Language   | Python 3.11                          |
| Frontend                | Streamlit                            |
| Backend                 | FastAPI                              |
| LLM                     | Groq — `openai/gpt-oss-120b`         |
| Framework                | LangChain                            |
| Embeddings              | FastEmbed — `BAAI/bge-small-en-v1.5` |
| Vector Database         | FAISS                                |
| Repository Cloning      | GitPython                            |
| Repository Analysis     | Python AST + static analysis         |
| Data Validation         | Pydantic                             |
| API Communication       | REST / HTTP                          |

---

## 📂 Project Structure

```text
CodeAtlas/
│
├── backend/
│   ├── api/
│   │   ├── routes.py
│   │   └── schemas.py
│   │
│   ├── loaders/
│   │   ├── github_loader.py
│   │   └── document_loader.py
│   │
│   ├── services/
│   │   ├── chunking_service.py
│   │   ├── embedding_service.py
│   │   ├── vectorstore_service.py
│   │   ├── github_service.py
│   │   ├── chat_service.py
│   │   └── retrieval_service.py
│   │
│   ├── repository_intelligence/
│   │   ├── analysis_store.py
│   │   ├── code_structure_analyzer.py
│   │   ├── dependency_analyzer.py
│   │   ├── impact_analyzer.py
│   │   ├── language_detector.py
│   │   ├── repository_analyzer.py
│   │   └── srs/
│   │       ├── capability_detector.py
│   │       ├── requirement_builder.py
│   │       ├── evidence_mapper.py
│   │       ├── srs_generator.py
│   │       ├── srs_sections.py
│   │       └── srs_formatter.py
│   │
│   ├── config.py
│   └── main.py
│
├── frontend/
│   ├── components/
│   │   ├── repository_card.py
│   │   ├── stats_dashboard.py
│   │   ├── repository_intelligence.py
│   │   ├── architecture_view.py
│   │   ├── srs_generator.py
│   │   └── chat_interface.py
│   │
│   ├── api_client.py
│   ├── config.py
│   ├── session_state.py
│   └── app.py
│
├── data/
│   ├── repos/
│   ├── vectorstore/
│   └── repository_analysis/
│
├── requirements.txt
├── README.md
└── .env
```

---

## 🏛️ Software Engineering Principles

### Separation of Concerns

CodeAtlas separates responsibilities across independent layers:

- **Frontend Layer** — Streamlit interface and user interactions
- **API Layer** — FastAPI endpoints and request/response handling
- **Service Layer** — ingestion, indexing, retrieval, and chat orchestration
- **Repository Intelligence Layer** — static repository analysis and dependency reasoning
- **SRS Layer** — capability detection, requirement construction, evidence mapping, and formatting
- **Data Layer** — repositories, analysis artifacts, and FAISS vector stores

This structure keeps individual responsibilities isolated and makes the application easier to maintain and extend.

### Modular Architecture

The application is divided into focused modules for GitHub repository cloning, document loading, text chunking, embedding generation, vector storage, retrieval, chat orchestration, repository analysis, dependency analysis, change-impact analysis, SRS generation, frontend components, API communication, and session management.

This avoids placing the complete application inside a single file and supports independent modification of major components.

---

## 🔍 Explainable RAG

A major part of CodeAtlas is making retrieval visible to the user.

For every question, the system exposes:

```text
Retrieved Source
      ↓
Rank
      ↓
Relevance Score
      ↓
Evidence Preview
```


The retrieved evidence is then supplied to the conversational generation layer, allowing users to inspect the repository sources contributing to an answer.

---

## 📄 Evidence Traceability

The SRS module connects reconstructed requirements to implementation evidence.

Example:

```text
REQ-ML-001
    │
    ├── Capability: Machine Learning
    ├── Evidence: ai_models/train_model.py
    ├── Evidence: dashboard/arrival_prediction_model.py
    └── Implementation Unit: predict_arrival_next_hour
```

This creates a direct relationship between:

```text
Requirement
    ↓
Capability
    ↓
Repository Evidence
    ↓
Implementation
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd CodeAtlas
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file:

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

> ⚠️ Never commit `.env` or API keys to GitHub.

---

## ▶️ Running the Application

### Start the FastAPI backend

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

The backend will be available at:

```text
http://localhost:8000
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

### Start the Streamlit frontend

Open another terminal:

```bash
python -m streamlit run frontend/app.py
```

The frontend will normally be available at:

```text
http://localhost:8501
```

---



## 🎯 What CodeAtlas Provides

```text
              CODEATLAS
                  │
      ┌───────────┼───────────┐
      │           │           │
      ▼           ▼           ▼
 Repository   Repository   Repository
 Intelligence  Analysis     Chat
      │           │           │
      │           ├── Dependency Graph
      │           ├── Impact Analysis
      │           └── Architecture
      │
      ├── Languages
      ├── Files
      ├── Functions
      ├── Classes
      └── Entry Points
                  │
                  ▼
          Evidence-Based SRS
                  │
                  ▼
          Requirement Traceability
```

CodeAtlas combines **repository structure analysis, semantic retrieval, conversational interaction, dependency reasoning, change analysis, and evidence-based documentation** in a single application.

---

## 🎓 Key Learning Outcomes

This project demonstrates practical implementation of:

- Retrieval-Augmented Generation
- Semantic Search
- Vector Databases
- Embeddings
- LLM Integration
- Prompt Engineering
- Static Code Analysis
- Python AST Parsing
- Dependency Analysis
- Change Impact Analysis
- Evidence Traceability
- Software Requirements Reconstruction
- FastAPI Development
- Streamlit Development
- REST API Integration
- Modular Software Architecture
- Separation of Concerns

---

## 🔮 Future Improvements

- Multi-repository support
- Repository caching
- GitHub Issues integration
- Pull Request analysis
- Commit history analysis
- Branch selection
- Function-level explanations
- Line-level citations
- Private repository support
- Authentication
- Docker support
- Persistent conversation memory
- Advanced cross-file and cross-language analysis

---

## 👨‍💻 Author

**Hareesha Nellakara**

Developed as an end-to-end AI application exploring repository intelligence, Retrieval-Augmented Generation, software architecture, static code analysis, and explainable AI-assisted development tools.

---

## 📄 License

This project is intended for **educational and portfolio purposes**.