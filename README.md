# Unified Knowledge AI

**Unified Knowledge AI is a multi-source organizational knowledge system that combines connected business information, agentic retrieval, and AI-powered tools to help people find evidence, reason across it, and complete knowledge-intensive tasks.**

Instead of asking businesses to move their information into another repository, the system connects to the sources they already use and builds an AI-ready knowledge layer on top of them. Users can ask questions across that knowledge, investigate information through iterative retrieval, and use tools to analyze or act on the results.

The first external source being integrated is **Google Drive**. The architecture is intended to support additional sources over time.

> **Connected sources → synchronized knowledge → agentic retrieval → tool-assisted work → evidence-backed results**

---

## Table of Contents

- [The Problem](#the-problem)
- [Product Direction](#product-direction)
- [System Architecture](#system-architecture)
- [1. Knowledge Source and Synchronization Layer](#1-knowledge-source-and-synchronization-layer)
- [2. Document Processing and Knowledge Layer](#2-document-processing-and-knowledge-layer)
- [3. Agentic Retrieval Layer](#3-agentic-retrieval-layer)
- [4. Tool-Use Layer](#4-tool-use-layer)
- [5. Answer Generation and Evidence](#5-answer-generation-and-evidence)
- [Evaluation and Observability](#evaluation-and-observability)
- [Administration and Knowledge Management](#administration-and-knowledge-management)
- [Technology Stack](#technology-stack)
- [Current Scope and Development Status](#current-scope-and-development-status)
- [Design Principles](#design-principles)
- [Relationship to Previous Projects](#relationship-to-previous-projects)
- [Future Extensions](#future-extensions)

---

## The Problem

Organizations store important knowledge across documents, spreadsheets, policies, manuals, reports, and collaboration platforms. That information may be distributed across systems such as:

- Google Drive
- Notion
- Microsoft SharePoint and OneDrive
- Slack
- Dropbox
- Internal business applications

These systems are useful for storing and managing information, but answering a business question often requires a person to locate several files, identify the relevant sections, compare versions, interpret tables, and combine the findings.

A conventional document-chat interface helps with basic question answering, but more involved work requires more than retrieving a few similar text passages. For example:

- What is the current procedure, and are there exceptions in another policy?
- Compare the specifications in these documents and identify conflicting values.
- Find the maintenance requirements for a product and calculate which items are overdue.
- Identify the evidence behind a recommendation and show where it came from.
- Use the relevant internal information to prepare the next step in a workflow.

Unified Knowledge AI aims to provide a common AI interface for this work while preserving the original systems as the source of truth.

## Product Direction

The project is evolving from a conventional RAG application into a **knowledge and tool-use system** with four connected capabilities:

1. **Connected knowledge:** bring information from existing business sources into a unified, synchronized representation.
2. **Agentic retrieval:** let the system plan and refine how it searches, rather than relying on a single retrieval attempt for every question.
3. **Tool-assisted work:** let the model select from controlled tools for retrieval, structured-data analysis, and eventually approved business actions.
4. **Evidence and verification:** preserve the provenance of information and evaluate whether retrieval, tool execution, and final responses are reliable.

These capabilities are separate but complementary. Agentic retrieval determines **what information to find and whether more evidence is needed**. The tool-use layer provides **the operations the system can execute**. Some tools support retrieval; others perform analysis or, in later versions, interact with external business systems.

The intention is not to make every question an autonomous multi-step task. Straightforward questions should still use a simple retrieval path. The system should use additional planning and tools when the request actually requires them.

---

## System Architecture

```text
                         USER
                           │
                           ▼
                    React Application
                           │
                           ▼
                     FastAPI Backend
                           │
                 Request / Agent Controller
                           │
             ┌─────────────┴──────────────┐
             │                           │
             ▼                           ▼
       Agentic Retrieval             Tool-Use Layer
             │                           │
             │                    ┌──────┴────────┐
             │                    │               │
             ▼                    ▼               ▼
      Retrieval Tools       Analysis Tools    Action Tools
             │                    │               │
             └─────────────┬───────┴───────────────┘
                           │
                           ▼
                 Evidence / Tool Results
                           │
                           ▼
                Grounded Response Generation
                           │
                           ▼
              Answer, Citations, and Results


       CONNECTED KNOWLEDGE AND INGESTION PIPELINE

 Google Drive (current)       Other sources (future)
          │                           │
          └─────────────┬─────────────┘
                        ▼
              Source and Sync Layer
                        │
                        ▼
              Document / Data Processing
                        │
                        ▼
              Normalized Knowledge Records
                        │
                        ▼
          PostgreSQL + pgvector + Full-Text Search
                        │
                        └────── used by retrieval tools
```

The main application is organized around the following responsibilities:

| Layer | Responsibility |
|---|---|
| Source and synchronization | Connect to external systems, discover changes, and keep the local knowledge representation current. |
| Processing and knowledge | Parse content, preserve structure and metadata, create chunks or structured records, and maintain search indexes. |
| Agentic retrieval | Interpret a question, select retrieval strategies, gather evidence, assess coverage, and refine the search when necessary. |
| Tool use | Expose validated operations that the model can call, execute them under application policies, and return structured results. |
| Generation and evidence | Produce a response grounded in retrieved evidence and tool outputs, with inspectable citations. |
| Evaluation and observability | Record and assess retrieval, tool execution, response quality, latency, and failures. |

---

## 1. Knowledge Source and Synchronization Layer

### External sources remain the source of truth

A central design decision is that Unified Knowledge AI does not replace the organization's existing document repository. It maintains a derived representation optimized for retrieval and AI-assisted work.

```text
External source
      │
      ▼
Change detection
      │
      ▼
Synchronization job
      │
      ▼
Fetch changed content
      │
      ▼
Processing and indexing
      │
      ▼
Updated knowledge representation
```

### Google Drive

Google Drive is the first external knowledge source. The integration is intended to let an administrator connect a Drive account, select the information that should be available to the AI system, and synchronize changes without manually uploading every revision.

The synchronization workflow covers the main document lifecycle:

- **Added:** discover the file, retrieve its content, process it, and index it.
- **Updated:** retrieve the latest version and replace the previous indexed representation.
- **Removed:** remove or deactivate the corresponding content so it is no longer returned by retrieval.

Synchronization is designed to be incremental. A change to one file should not require rebuilding the entire knowledge base.

### Background synchronization

Synchronization can involve network requests, document parsing, embedding generation, and database writes. These operations should run as background jobs rather than keeping an ordinary API request open for the entire process.

The current design uses persistent sync-job records and a Redis Streams-based queue for dispatching work. Job status and per-file outcomes can be used by the admin interface to show progress and errors. Workers must handle retries and duplicate delivery safely because queue processing is expected to provide at-least-once delivery rather than exactly-once execution.

### Additional sources

The connector boundary is intended to support additional providers without coupling their APIs to the core retrieval implementation.

Potential future connectors include:

- Notion
- Microsoft SharePoint and OneDrive
- Slack
- Dropbox
- Confluence
- Internal business APIs

These are architectural extensions, not claims that all connectors are currently implemented.

---

## 2. Document Processing and Knowledge Layer

The processing layer transforms source content into a common representation that can be indexed and retrieved consistently.

```text
Source file or data
        │
        ▼
Fetch / normalize
        │
        ▼
Parse and extract structure
        │
        ▼
Normalized document representation
        │
        ├── Content
        ├── Headings and sections
        ├── Page or sheet information
        ├── Source metadata
        └── Version information
        │
        ▼
Structure-aware chunking / record extraction
        │
        ▼
Embeddings + lexical search index
        │
        ▼
Unified knowledge base
```

### Structure-aware document processing

For PDF processing, **Docling** is used to extract document content and useful structure, including headings, paragraphs, lists, tables, and page information. Other supported formats can be normalized into a compatible internal representation.

Preserving structure matters because a passage's meaning can depend on its heading, table, page, or surrounding content. The system should retain enough metadata to trace retrieved information back to its source.

### Structured data and spreadsheets

Spreadsheets should not always be flattened into one long text document. Depending on the task, the system may need both:

- A searchable textual representation for semantic questions about a workbook.
- A structured representation of sheets, columns, rows, and values for filtering, comparisons, and calculations.

For example, a question about what a maintenance schedule says can use text retrieval. A question asking which products have an interval below a given threshold is better handled by a structured-data operation.

Google Sheets is an important part of the intended knowledge model. The precise ingestion and structured-query capabilities can be expanded independently of the document retrieval pipeline.

### Searchable knowledge store

The current database direction uses PostgreSQL as the main relational store, with:

- **pgvector** for dense vector similarity search.
- **PostgreSQL Full-Text Search** for lexical matching.
- Relational metadata for documents, sources, users, chunks, sync jobs, and citations.

This keeps operational data and retrieval indexes in a common database while allowing semantic and exact-term retrieval to work together.

---

## 3. Agentic Retrieval Layer

The agentic retrieval layer is a central part of the project's direction. It extends ordinary RAG by allowing the system to decide **how to retrieve information, inspect what it found, and make another retrieval attempt when the evidence is incomplete**.

A fixed RAG pipeline often looks like this:

```text
Question → Retrieve once → Generate answer
```

That is sufficient for many direct questions, but can be weak for requests involving several entities, multiple documents, comparisons, or ambiguous terminology. Agentic retrieval introduces a bounded reasoning and retrieval loop:

```text
User request
     │
     ▼
Understand the information need
     │
     ▼
Create a retrieval plan
     │
     ▼
Choose retrieval strategy and filters
     │
     ▼
Execute retrieval tools
     │
     ▼
Inspect evidence and identify gaps
     │
     ├──── Evidence sufficient ────► Build answer context
     │
     └──── Evidence incomplete
                    │
                    ▼
           Refine query / plan
                    │
                    └──────────────► Retrieve again
```

### Responsibilities

The retrieval controller may perform the following steps, depending on the request:

1. **Understand the query:** identify the subject, entities, requested output, time/version constraints, and likely knowledge scope.
2. **Decompose complex questions:** turn a multi-part request into smaller information needs that can be searched separately.
3. **Choose retrieval strategies:** select dense search, lexical search, metadata filtering, source-specific retrieval, or structured-data lookup.
4. **Gather candidate evidence:** run the selected retrieval operations, potentially in parallel when they are independent.
5. **Combine and rank results:** merge retrieval results, remove duplicates, and apply reranking where appropriate.
6. **Inspect coverage:** determine whether the retrieved material answers each part of the request or whether important evidence is missing or contradictory.
7. **Refine retrieval:** rewrite a query, use a more specific filter, retrieve a different source, or fetch additional context when useful.
8. **Stop or abstain:** stop when the evidence is sufficient or the retrieval budget is reached. If the knowledge base does not contain adequate evidence, communicate that limitation instead of inventing an answer.

### Retrieval methods

The retrieval layer combines complementary signals:

| Method | Purpose |
|---|---|
| Dense retrieval | Find conceptually related passages even when the query uses different wording. |
| PostgreSQL full-text search | Match exact terminology, identifiers, product names, error codes, and domain-specific terms. |
| Metadata filtering | Restrict results by source, document, ownership, date, type, or other available metadata. |
| Hybrid retrieval | Combine semantic and lexical results to improve candidate coverage. |
| Reranking | Reorder candidates based on their relevance to the complete query. |
| Structured-data lookup | Retrieve or compute over tabular data when a question requires rows, columns, filters, or calculations. |

### Example: multi-document comparison

For a request such as *"Compare the warranty conditions for Product A across the current product guide and the service policy"*, the retrieval controller could:

1. Identify the product and the two requested source types.
2. Search for Product A in both source groups.
3. Retrieve the matching sections and surrounding context.
4. Check whether the evidence covers the relevant warranty terms in both documents.
5. Search again with a more specific query if one document's evidence is incomplete.
6. Compare the supported terms and cite each source separately.

The important difference is that retrieval is guided by the information need and the evidence found so far, rather than treating the first set of search results as automatically sufficient.

### Bounded and controlled retrieval

Agentic retrieval should not become an unconstrained loop. The controller should enforce limits such as maximum retrieval iterations, tool-call budgets, timeouts, and an evidence-based stopping condition. Retrieval must also respect the user's authorization and knowledge scope on every call.

---

## 4. Tool-Use Layer

The tool-use layer allows the AI system to interact with well-defined application capabilities instead of relying only on text generation. The model can select a tool when a task requires an operation, provide arguments, receive a structured result, and use that result in the next step.

The tool layer is separate from the model. The model may decide **which tool to request**, but the application remains responsible for validating and executing that request.

### Tool execution flow

```text
User request
     │
     ▼
Agent / request controller
     │
     ▼
Select a tool
     │
     ▼
Validate tool name, arguments, and permissions
     │
     ▼
Execute tool
     │
     ▼
Return structured result or error
     │
     ▼
Controller observes result
     │
     ├── More work required ───► Select next tool
     │
     └── Task complete ────────► Compose final response
```

### Tool categories

The tool registry can expose capabilities in several categories.

#### A. Knowledge retrieval tools

These tools give the retrieval controller access to the knowledge base. Examples include:

- Search documents using dense retrieval.
- Search documents using PostgreSQL full-text search.
- Run hybrid retrieval and reranking.
- Filter documents by metadata or source.
- Retrieve a document section or additional surrounding context.
- Search a selected knowledge source.

These are the tools used by the agentic retrieval process described above.

#### B. Knowledge analysis tools

These tools operate on retrieved content or structured business data. Examples include:

- Compare information extracted from multiple documents.
- Summarize selected evidence or a document section.
- Query spreadsheet rows using filters.
- Calculate values or aggregate structured records.
- Extract specified fields into a structured result.

The purpose is to use deterministic code for operations that should not be left to free-form language generation alone. For example, arithmetic and filtering should be performed by an appropriate computation tool, with the result then explained by the model.

#### C. Application and business action tools

A later extension can expose tools that interact with other applications or initiate workflow actions. Examples could include creating a task, preparing a ticket, or updating a business record through an authorized integration.

These tools introduce side effects, so they require stricter controls than read-only retrieval tools. The application should enforce user permissions, validate arguments, record the action, and require explicit confirmation for consequential operations where appropriate.

### Tool design principles

Each tool should have:

- A narrow, clearly defined responsibility.
- A validated input schema and predictable output structure.
- Explicit authorization and knowledge-scope checks.
- Timeouts and controlled error handling.
- Logging or tracing of the request and execution result.
- Idempotency protections for operations that may be retried.

Read-only tools are the safer starting point. Tools that modify external data should be introduced only with appropriate authorization, confirmation, and auditability.

### Why keep retrieval and tools as distinct layers?

Agentic retrieval is a specialized process focused on finding sufficient and relevant evidence. The tool-use layer is the broader execution interface through which the AI can access retrieval functions, analysis operations, and eventually external actions.

Keeping these concepts separate makes it possible to improve retrieval without redesigning every business tool, and to add new tools without turning the retrieval pipeline into a collection of provider-specific integrations.

---

## 5. Answer Generation and Evidence

After retrieval and any required tool operations, the system assembles the relevant evidence and results for the language model.

```text
User request
     +
Retrieved passages and metadata
     +
Structured tool results
     +
Execution context
     │
     ▼
Grounded response generation
     │
     ▼
Answer + citations + relevant results
```

The model should distinguish between information supported by the connected knowledge base, results returned by tools, and information that is unavailable. When evidence is insufficient, it should say so rather than fill gaps with unsupported claims.

### Citations and provenance

Citations are part of the application's data model, not merely text generated by the model. The application should retain the relationship between an answer, the retrieved chunk, the document, and the original source.

Depending on the source type, a citation may identify:

- File name and page number for a PDF.
- Document title and section for a text document.
- Workbook, sheet, and row or range for spreadsheet data.
- Original source URL or external file identifier.

This allows users to inspect the evidence behind an answer. If a source document is later removed or updated, citation history should be handled deliberately so that older answers do not silently point to unrelated or newly indexed content.

---

## Evaluation and Observability

Evaluation and tracing are cross-cutting requirements for a system that performs multi-step retrieval and tool execution. A final answer alone does not reveal whether the system searched the right sources, selected useful evidence, or executed a tool correctly.

### What should be evaluated?

| Area | Example questions |
|---|---|
| Retrieval quality | Did the system retrieve the relevant document and passages? Were important sources missed? |
| Evidence quality | Does the context support each important claim? Are there contradictions? |
| Citation quality | Do citations point to the correct document, page, section, or data range? |
| Tool execution | Was the correct tool selected? Were its arguments valid? Did it return the expected result? |
| Answer quality | Is the response complete, accurate, appropriately qualified, and grounded? |
| System performance | What were the latency, failure rate, retry count, and model/tool usage? |

### Tracing a request

A trace should make it possible to inspect the main stages of a request, for example:

```text
Request received
  └── Query understood
      └── Retrieval plan created
          ├── Dense search
          ├── Full-text search
          ├── Results fused / reranked
          └── Evidence coverage checked
              └── Additional retrieval (if needed)
                  └── Context assembled
                      └── Response generated
```

For tool-assisted tasks, the trace should also record the selected tool, validated arguments, execution status, duration, and result metadata. Sensitive document content and credentials should not be indiscriminately written to logs.

Evaluation datasets and regression tests can be used to compare changes to chunking, retrieval, reranking, prompts, and tool behavior over time.

---

## Administration and Knowledge Management

The admin interface provides a way to manage connected sources and understand the state of the knowledge base without directly interacting with databases, vector indexes, or background workers.

The management experience is intended to cover:

- Connecting and managing knowledge sources.
- Selecting which files or folders should be indexed.
- Triggering synchronization and viewing sync status.
- Inspecting added, updated, removed, and failed files.
- Viewing document and indexing status.
- Re-ingesting or removing indexed documents.
- Viewing high-level document, chunk, and source statistics.

This is important because a reliable knowledge assistant depends on administrators being able to understand and control what information is available to the AI.

---

## Technology Stack

The project is being developed with the following stack:

| Area | Technologies |
|---|---|
| Frontend | React, Vite, JavaScript, Axios, React Markdown |
| Backend | Python, FastAPI, Pydantic |
| Database and ORM | PostgreSQL, pgvector, SQLAlchemy, Alembic |
| Retrieval | Dense vector search, PostgreSQL Full-Text Search |
| Document processing | Docling, Python document-processing libraries |
| AI models | Google Gemini API for language-model and embedding capabilities |
| External integration | Google Drive API; Google Docs and Sheets integration as the source model evolves |
| Background jobs | Redis Streams / Upstash Redis |
| Deployment | Vercel frontend, Render backend, Supabase-hosted PostgreSQL |

The stack may evolve as retrieval, tool execution, and evaluation requirements become clearer.

---

## Current Scope and Development Status

The project is being developed incrementally. The following distinction is intentional: the architecture describes the target system, while individual capabilities are implemented and hardened in stages.

| Capability | Direction / status |
|---|---|
| React application and FastAPI backend | Core application foundation |
| Authentication and chat APIs | Application foundation being developed |
| PostgreSQL data model and migrations | Core persistence foundation |
| Google Drive integration | First external knowledge source; integration and synchronization workflow are the initial focus |
| Background synchronization | Sync-job and Redis Streams-based processing design |
| Document parsing and chunking | Builds on the Docling and structure-aware processing work from the earlier RAG projects |
| Dense and lexical retrieval | Core retrieval foundation using pgvector and PostgreSQL Full-Text Search |
| Hybrid retrieval and reranking | Retrieval capabilities to integrate and refine in the application |
| Agentic retrieval planning and iteration | Next architectural layer to develop on top of the retrieval foundation |
| Tool registry and controlled execution | Next application layer, beginning with read-only retrieval and analysis tools |
| Evaluation and tracing | Cross-cutting capability to add as the retrieval and tool workflows are implemented |
| Additional connectors and external actions | Future extensions |

### Initial development sequence

A practical implementation sequence is:

1. Complete the Google Drive connection, file selection, and synchronization workflow.
2. Stabilize document processing, metadata, and the shared knowledge representation.
3. Implement and evaluate the core retrieval methods: dense, lexical, hybrid, and reranking.
4. Add an agentic retrieval controller that can plan, refine, and stop retrieval based on evidence.
5. Introduce a tool registry and execution layer, starting with retrieval and structured-data analysis tools.
6. Add tracing and evaluation across retrieval, tool calls, and final answers.
7. Expand to additional sources and carefully permissioned business actions.

---

## Design Principles

### 1. External sources remain the source of truth

The knowledge base is a synchronized, AI-optimized representation of source information, not a replacement for the systems in which the organization manages its records.

### 2. Connectors are separate from the knowledge core

Source-specific authentication, APIs, and change detection should remain behind connector interfaces. The downstream processing and retrieval pipeline should work with normalized content and metadata.

### 3. Synchronization is incremental and recoverable

Changes should affect only the relevant files. Background jobs should expose status, support retries, and be safe against duplicate processing.

### 4. Retrieval is evidence-driven

The system should use retrieval strategies suited to the question, inspect the evidence it receives, and request more information only when needed. It should stop or abstain when it cannot establish sufficient support.

### 5. Tools are explicit and controlled

The model can request tools, but application code validates permissions, schemas, and execution. Side-effecting operations require stronger controls than read-only operations.

### 6. Results must be inspectable

Users should be able to see the sources and tool-derived results behind an answer. Internal traces should make failures and quality issues diagnosable.

### 7. Use agents where they add value

A multi-step agentic workflow is useful for complex information needs and tasks. It should not add unnecessary latency or complexity to simple questions that can be answered with a direct retrieval call.

---

## Future Extensions

Potential extensions include:

### Knowledge sources

- Notion, SharePoint, OneDrive, Slack, Dropbox, and Confluence.
- Source-level and document-level access-control enforcement.
- More robust version history and event-driven synchronization.

### Agentic retrieval

- Query decomposition and query rewriting.
- Multi-query and source-aware retrieval.
- Adaptive selection of retrieval strategies.
- Better evidence coverage and contradiction detection.
- Retrieval evaluation and regression testing.

### Tool use and workflows

- Structured spreadsheet querying and analysis.
- Cross-document comparison and extraction tools.
- Tools for interacting with approved business applications.
- Human approval for consequential or irreversible actions.
- Tool-call policies, audit logs, retries, and idempotency.

### Reliability and evaluation

- Retrieval and answer evaluation datasets.
- Citation and claim-support checks.
- Tool-selection and tool-execution evaluation.
- End-to-end traces, latency monitoring, and cost tracking.
- Access-control and data-isolation testing.

---

## Project Objective

The long-term objective is to build a business-oriented AI system that does more than retrieve a few passages and generate a response. It should connect to organizational knowledge, determine what evidence is needed, retrieve and verify that evidence through controlled iterative search, and use tools to perform useful analysis or approved actions.

> **Unified Knowledge AI is a multi-source organizational knowledge system that connects to existing business information, uses agentic retrieval to gather and verify relevant evidence, and provides a controlled tool-use layer for AI-assisted analysis and workflows—with traceable, source-grounded results.**

The first integration target is Google Drive. The broader architecture is designed to evolve toward additional knowledge sources, more capable retrieval, and a governed set of tools for business work.