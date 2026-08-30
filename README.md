# Unified Knowledge AI

A production-oriented **multi-source AI knowledge base and management system** that allows businesses to connect their existing document sources to an AI-powered knowledge base and use **Retrieval-Augmented Generation (RAG)** for semantic search, question answering, and source-grounded analysis.

The system is designed around a common problem in business AI deployments: organizations already store their knowledge across platforms such as **Google Drive, Notion, SharePoint, Slack, and other business systems**, but their existing storage and collaboration tools do not provide a unified way to search, analyze, and interact with that knowledge using AI.

Rather than replacing these systems, Unified Knowledge AI acts as an **AI knowledge layer** on top of them.

> **Existing business knowledge sources → synchronization → unified knowledge base → RAG → grounded AI answers**

The first implemented external knowledge source is **Google Drive**, with the architecture designed to support additional sources in the future.

---

# Project Purpose

Businesses accumulate large amounts of organizational knowledge in documents, spreadsheets, reports, policies, manuals, procedures, and other internal resources.

This information may already be stored in systems such as:

```text
Google Drive
Notion
SharePoint
Slack
Dropbox
Internal systems
```

The problem is that these systems primarily solve **storage, organization, collaboration, and document management**.

They do not necessarily provide an AI-native interface for questions such as:

> "What is our current procedure for handling this situation?"

> "Compare the information in these documents and identify the differences."

> "What does our documentation say about this product?"

> "Find the relevant information and explain it with supporting sources."

Unified Knowledge AI addresses this problem by creating an AI-accessible knowledge layer over existing business information.

---

# Core Concept

The system separates the responsibilities of **document storage** and **AI knowledge retrieval**.

```text
              Existing Business Sources
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
     Google Drive    Notion       SharePoint
     (implemented)   (future)       (future)
          │            │            │
          └────────────┼────────────┘
                       ▼
              Source / Sync Layer
                       │
                       ▼
              Document Processing
                       │
                       ▼
              Unified Knowledge Base
                       │
                       ▼
              Retrieval + Reranking
                       │
                       ▼
                Grounded LLM
                       │
                       ▼
                AI Knowledge UI
```

The original systems remain the **source of truth** for business documents.

The Unified Knowledge AI system maintains a derived, AI-optimized representation of that information.

---

# Key Objectives

The project focuses on building the infrastructure required to make an organizational RAG system usable in a realistic business environment.

The main objectives are:

* Connect AI knowledge bases to existing business document sources.
* Synchronize changes from external sources.
* Provide administrators with control over indexed knowledge.
* Process multiple business document types.
* Preserve document structure and metadata.
* Provide semantic and lexical retrieval.
* Generate source-grounded answers with citations.
* Prevent outdated or deleted information from remaining active in retrieval.
* Provide visibility into the state of the knowledge base.
* Design the architecture so additional knowledge sources can be added later.

---

# Knowledge Source Architecture

A key design principle is:

> **External systems remain the source of truth; Unified Knowledge AI maintains the AI-searchable representation.**

For example:

```text
Google Drive
     │
     │ Source of truth
     ▼
Change Detection
     │
     ▼
Synchronization
     │
     ▼
Document Processing
     │
     ▼
Chunking
     │
     ▼
Embeddings + Search Index
     │
     ▼
AI Knowledge Base
```

This avoids requiring businesses to migrate their existing document repositories into a new storage system.

The same architecture can later support additional sources:

```text
Knowledge Sources
│
├── Google Drive       ← Current
├── Notion             ← Future
├── SharePoint         ← Future
├── Slack               ← Future
└── Other sources       ← Future
```

All sources ultimately feed into the same knowledge-processing and retrieval pipeline.

---

# Knowledge Base Management

The system includes an administrative interface for managing the AI knowledge base.

The admin interface provides visibility into information such as:

```text
Documents
Indexed documents
Processing documents
Failed documents
Chunks
Connected sources
Last synchronization
Processing status
```

Administrators can perform actions such as:

* Add documents.
* Select multiple documents for ingestion.
* Remove documents from the AI knowledge base.
* Re-ingest documents.
* Inspect document metadata.
* Monitor ingestion status.
* Trigger synchronization.
* Manage connected knowledge sources.

The purpose of this interface is to allow **non-technical users to manage what the AI system knows without manually interacting with databases, vector stores, or ingestion scripts.**

---

# Document Lifecycle

Documents in the knowledge base follow a lifecycle rather than being treated as static files.

```text
Source
  │
  ▼
Discovered
  │
  ▼
Processing
  │
  ▼
Indexed
  │
  ├───────────────┐
  ▼               ▼
Modified        Deleted
  │               │
  ▼               ▼
Re-process      Deactivate
```

This allows the AI knowledge base to remain aligned with changes in the source system.

For example:

### New document

```text
New file
   ↓
Detect
   ↓
Process
   ↓
Chunk
   ↓
Embed
   ↓
Index
```

### Modified document

```text
File modified
   ↓
Detect
   ↓
Process latest version
   ↓
Replace previous representation
   ↓
Update index
```

### Deleted document

```text
File deleted
   ↓
Detect
   ↓
Deactivate indexed content
   ↓
Exclude from retrieval
```

---

# Google Drive Integration

Google Drive is the first implemented external knowledge source.

The integration is designed around the idea that businesses should be able to continue managing their documents normally in Google Drive while keeping their AI knowledge base synchronized.

The intended workflow is:

```text
Business user
     │
     ▼
Adds / edits document in Google Drive
     │
     ▼
Unified Knowledge AI detects change
     │
     ▼
Document is processed
     │
     ▼
Knowledge base is updated
```

The system should avoid rebuilding the entire knowledge base whenever a small change occurs.

Instead, synchronization is designed around **incremental updates**.

---

# Document Processing

The document processing pipeline builds upon the advanced document parsing and chunking work developed in the previous RAG projects.

The processing pipeline is designed to preserve useful document structure and metadata.

```text
Document
   │
   ▼
Parsing
   │
   ▼
Structure Extraction
   │
   ▼
Structure-Aware Chunking
   │
   ▼
Metadata
   │
   ▼
Embeddings
   │
   ▼
Knowledge Index
```

For PDF documents, **Docling** is used to preserve structures such as:

* Headings
* Paragraphs
* Lists
* Tables
* Page information
* Other document elements

Other supported document formats can be normalized into the same internal representation.

---

# Google Sheets and Structured Data

Business knowledge is not limited to unstructured documents.

Organizations frequently maintain important information in spreadsheets such as:

* Product information
* Pricing
* Inventory
* Specifications
* Operational data
* Maintenance schedules
* Customer information
* Business metrics

The system therefore treats spreadsheets as a distinct type of knowledge source rather than simply converting them into plain text.

A spreadsheet can be represented as:

```text
Workbook
   │
   ├── Sheet 1
   │     ├── Headers
   │     └── Rows
   │
   ├── Sheet 2
   │     ├── Headers
   │     └── Rows
   │
   └── Sheet 3
```

Relevant metadata such as:

```text
Workbook
Sheet
Row
Column
Cell / Range
```

can be retained for retrieval and citation.

The system can use both:

### Searchable representation

For questions such as:

> "What does the maintenance schedule say about Product X?"

and:

### Structured representation

For questions requiring operations over structured data, such as:

> "Which products have a maintenance interval below 500 hours?"

This allows structured business data to be handled more appropriately than treating every spreadsheet as ordinary document text.

---

# Unified Document Representation

Regardless of the source, documents are transformed into a common internal representation before entering the RAG pipeline.

Conceptually:

```text
Google Drive Document
        │
        ▼
       Parse
        │
        ▼
Normalized Document
        │
        ├── Content
        ├── Structure
        ├── Metadata
        └── Source information
                │
                ▼
             Chunking
                │
                ▼
             Indexing
```

This abstraction allows different source connectors to share the same downstream RAG infrastructure.

---

# Metadata and Provenance

Each document and chunk retains information about its origin.

Example document metadata:

```text
document_id
source
source_file_id
file_name
document_type
modified_time
version
status
source_url
```

Example chunk metadata:

```text
document_id
document_version_id
chunk_index
page
section
sheet_name
row_start
row_end
content
embedding
```

This metadata supports:

* Source filtering
* Retrieval
* Citations
* Document lifecycle management
* Version handling
* Source inspection
* Future access-control mechanisms

---

# Retrieval

The knowledge base uses multiple retrieval signals rather than relying exclusively on semantic vector search.

The retrieval pipeline is:

```text
User Query
     │
     ▼
Query Processing
     │
     ├───────────────┐
     ▼               ▼
Dense Search     Lexical Search
     │               │
     │          PostgreSQL
     │          Full-Text Search
     │               │
     └───────┬───────┘
             ▼
        Result Fusion
             │
             ▼
       Final Retrieval
             │
             ▼
          Reranking
             │
             ▼
       Relevant Evidence
```

### Dense Retrieval

Dense retrieval provides semantic matching between queries and document chunks.

It is useful when the query and source material express similar concepts using different wording.

### PostgreSQL Full-Text Search

PostgreSQL full-text search provides lexical matching.

This is particularly useful for:

* Technical terms
* Product names
* Error codes
* Part numbers
* Identifiers
* Exact terminology
* Domain-specific keywords

### Hybrid Retrieval

The two retrieval signals are combined to provide a more robust retrieval system.

The goal is to combine:

```text
Semantic understanding
        +
Exact term matching
        ↓
Better retrieval
```

The retrieval implementation builds upon the retrieval experiments developed in the Advanced RAG Lab.

---

# Grounded Generation

Retrieved evidence is provided to the LLM along with the user's question.

```text
User Question
      +
Retrieved Evidence
      +
Metadata
      ↓
     LLM
      ↓
Grounded Answer
      +
Citations
```

The model is instructed to rely on the retrieved evidence rather than generating unsupported information.

If sufficient evidence cannot be found, the system should be able to abstain rather than confidently fabricate an answer.

Example:

> I could not find sufficient supporting information in the current knowledge base.

This is particularly important for business and technical knowledge systems where incorrect information can be more harmful than an explicit lack of an answer.

---

# Citations and Source Provenance

Answers should expose the documents used to generate them.

Example:

```text
The recommended maintenance interval is 500 operating hours.

Sources:
• Maintenance_Manual.pdf — Page 42
• Maintenance_Schedule.xlsx — Sheet: Schedule, Rows 18–21
```

Citations are treated as part of the application's data model rather than only as formatting added by the LLM.

The system retains the relationship between:

```text
Answer
   ↓
Retrieved evidence
   ↓
Chunk
   ↓
Document
   ↓
Original source
```

This allows users to inspect where an answer originated.

---

# Admin Knowledge Base Overview

The management interface provides a high-level view of the AI knowledge base.

A conceptual dashboard might expose:

```text
Knowledge Base
────────────────────────────

Documents          247
Indexed             243
Processing            3
Failed                1

Chunks           18,432

Sources
────────────────────────────
Google Drive       Connected

Last Sync
────────────────────────────
Today, 10:42 AM
```

This allows administrators to understand the state of the AI system without interacting directly with the underlying infrastructure.

---

# System Architecture

The application is organized into several major layers.

```text
                         USERS
                           │
                ┌──────────┴──────────┐
                ▼                     ▼
           React UI              Admin UI
                │                     │
                └──────────┬──────────┘
                           ▼
                      FastAPI Backend
                           │
          ┌────────────────┼─────────────────┐
          ▼                ▼                 ▼
    Chat / RAG API    Knowledge API     Source API
          │                │                 │
          │                │                 ▼
          │                │          Google Drive
          │                │
          └────────────────┼─────────────────┐
                           ▼                 │
                    Knowledge Core           │
                           │                 │
                  ┌────────┴────────┐        │
                  ▼                 ▼        │
              Retrieval        Ingestion ◄───┘
                  │                 │
                  │          ┌──────┴──────┐
                  │          ▼             ▼
                  │       Parsing       Chunking
                  │          │             │
                  │          └──────┬──────┘
                  │                 ▼
                  │             Embeddings
                  │                 │
                  └──────────┬──────┘
                             ▼
                     PostgreSQL + pgvector
```

---

# Technology Stack

## Frontend

* React
* Vite
* TypeScript
* React Markdown

## Backend

* Python
* FastAPI
* Pydantic

## Database

* PostgreSQL
* pgvector
* PostgreSQL Full-Text Search

## Document Processing

* Docling
* OCR where required
* Python document-processing libraries
* pandas
* openpyxl

## AI

* OpenAI API
* Embedding models

## External Sources

* Google Drive API
* Google Docs API
* Google Sheets API

## Background Processing

The architecture is designed to support asynchronous document processing for larger ingestion workloads.

Potential components include:

* Redis
* Celery

## Deployment

* Docker
* Cloud-hosted PostgreSQL
* Cloud-hosted FastAPI backend
* Cloud-hosted React frontend

---

# Relationship to Previous Projects

Unified Knowledge AI builds upon the RAG capabilities developed in earlier projects.

```text
Project 1
Basic AI Knowledge Base
        │
        ▼
Project 2
Advanced Document Parsing
        │
        ▼
Project 3
Advanced Retrieval & Evaluation
        │
        ▼
Unified Knowledge AI
        │
        ├── Knowledge source integration
        ├── Synchronization
        ├── Knowledge base management
        ├── Document lifecycle
        ├── Structured data
        └── Business-facing AI interface
```

The objective is not to rebuild the underlying RAG techniques from scratch, but to apply them within a more realistic **business knowledge management environment**.

---

# Design Principles

## 1. External sources remain the source of truth

The system should not require businesses to abandon their existing document-management platforms.

```text
Business source
      ↓
Source of truth

AI Knowledge Base
      ↓
Derived searchable representation
```

---

## 2. Connectors should be separated from the RAG core

Source-specific logic should remain isolated from the core knowledge pipeline.

Conceptually:

```text
KnowledgeSource
      │
      ├── Google Drive
      ├── Notion
      ├── SharePoint
      └── Future sources
```

while all sources eventually feed:

```text
Normalize
   ↓
Parse
   ↓
Chunk
   ↓
Embed
   ↓
Index
```

This allows additional connectors to be introduced without redesigning the RAG system.

---

## 3. Synchronization should be incremental

A small change to one source document should not require rebuilding the entire knowledge base.

```text
Changed source
     ↓
Identify affected document
     ↓
Reprocess
     ↓
Update affected index entries
```

---

## 4. Knowledge management should be accessible to non-technical users

Administrators should be able to manage the AI knowledge base through the application rather than interacting with:

```text
Databases
Vector stores
CLI scripts
Python pipelines
```

The application should expose the important operations through a simple interface.

---

## 5. The AI should be grounded in organizational knowledge

The system should prioritize:

```text
Retrieved evidence
      ↓
Grounded answer
      ↓
Source citation
```

over unsupported model knowledge.

---

# Current Scope

The initial version focuses on:

### Knowledge Base

* Document ingestion
* Document management
* Metadata
* Processing status
* Deletion and re-ingestion

### Google Drive

* Authentication
* File discovery
* Document retrieval
* Change detection
* Incremental synchronization

### Documents

* PDF processing
* Google Docs
* Google Sheets
* Structured spreadsheet representation
* Structure-aware parsing and chunking

### RAG

* Dense retrieval
* PostgreSQL lexical retrieval
* Hybrid retrieval
* Reranking
* Source-grounded generation
* Citations
* Abstention

### Administration

* Knowledge base overview
* Document management
* Source management
* Ingestion controls
* Synchronization controls

---

# Future Extensions

The architecture is intended to support additional capabilities such as:

### Additional Knowledge Sources

* Notion
* Slack
* Microsoft SharePoint
* OneDrive
* Dropbox
* Confluence

### Advanced Synchronization

* Event-driven synchronization
* Periodic reconciliation
* Version-aware indexing
* Conflict handling
* Improved synchronization monitoring

### Retrieval

* Metadata filtering
* Query rewriting
* Query expansion
* Multi-query retrieval
* Advanced reranking

### Knowledge Management

* Fine-grained access control
* Folder/source selection
* Document version history
* Source-level permissions
* Knowledge-base analytics

### AI

* Advanced citation validation
* Answer quality evaluation
* Structured-data analysis
* Multi-document reasoning
* Knowledge-base evaluation and regression testing

---

# Project Objective

The long-term objective is to demonstrate how a basic RAG application can evolve into a system that can actually be integrated into a business environment.

The progression is:

```text
Documents
    ↓
RAG
    ↓
AI Knowledge Base
    ↓
Knowledge Base Management
    ↓
External Source Integration
    ↓
Synchronization
    ↓
Reliable Organizational AI
```

The project therefore focuses not only on **how to retrieve information**, but also on the infrastructure required to keep an AI knowledge base **current, manageable, traceable, and connected to the way businesses already store their information**.

---

# Final Project Definition

> **Unified Knowledge AI is a multi-source AI knowledge base and management system that connects businesses' existing information sources to a unified RAG layer, allowing employees to search, analyze, and interact with organizational knowledge using source-grounded AI while allowing administrators to manage and synchronize the knowledge base through a dedicated interface.**

The current implementation uses **Google Drive as the first external knowledge source**, while the underlying architecture is designed to support additional sources as the system evolves.
