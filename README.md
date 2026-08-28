# NEXORA

## AI-Powered Academic Knowledge Assistant for College Students

---

# 1. Project Overview

NEXORA is an AI-powered academic knowledge assistant designed to help college students quickly find information from academic study materials.

Students usually have access to large amounts of academic information, including:

- Syllabus documents
- Subject PDFs
- Study materials
- Academic regulations
- Previous study resources
- Department information
- Course-related documents

However, this information is usually distributed across multiple websites and PDF documents.

Students often spend significant time searching for the correct document or manually reading large PDF files to find a specific piece of information.

NEXORA solves this problem by creating an intelligent chatbot based on academic documents.

The system uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from the available academic knowledge base and generate answers based on that information.

---

# 2. Business Context

Educational institutions and students generate and consume large amounts of academic information.

This information is usually stored in:

- Websites
- PDF documents
- Syllabus documents
- Study materials
- Department resources

The information may be available online, but availability does not automatically mean that it is easy to search.

A student may need to answer questions such as:

> What is the syllabus for a particular subject?

> Which units are included in this course?

> Where can I find study material for this subject?

> What topics should I prepare for an examination?

Currently, students may need to manually:

1. Search through websites.
2. Download PDF documents.
3. Open multiple documents.
4. Search through hundreds of pages.
5. Identify the correct information.

This process is inefficient and time-consuming.

---

# 3. Business Problem

## The Core Problem

Students face difficulty finding accurate academic information quickly because study materials are distributed across multiple documents and online sources.

The major problems are:

### 3.1 Information Fragmentation

Academic information is distributed across multiple locations.

For example:

- Syllabus websites
- Academic resource websites
- PDF documents
- Study material repositories

Students must know where to search before they can find information.

---

### 3.2 Large Number of PDF Documents

Academic documents may contain hundreds of pages.

Students may know that the information exists but may not know:

- Which document contains it.
- Which page contains it.
- Which section is relevant.

Manual searching consumes significant time.

---

### 3.3 Traditional Search Limitations

Traditional search systems usually depend heavily on keywords.

For example:

A student may ask:

> What topics should I study for Unit 3?

However, the document may contain:

> Module III contains the following topics...

A traditional keyword-based search may not understand that these questions are semantically related.

---

### 3.4 Lack of Centralized Knowledge Access

Students need to visit multiple websites and download multiple files.

There is no single conversational interface where a student can ask an academic question and receive information from the available study materials.

---

### 3.5 Large Language Model Hallucination

A normal AI chatbot may answer academic questions using its general training knowledge.

This creates a risk.

The answer may sound correct but may not match the actual syllabus or study material.

For academic applications, incorrect information can negatively affect students.

Therefore, the chatbot should answer using verified documents rather than relying only on general model knowledge.

---

# 4. Problem Statement

How can we build an intelligent academic assistant that allows students to ask questions about their study materials and retrieve accurate answers from academic documents?

The system should:

1. Collect academic source documents.
2. Securely store the original documents.
3. Process text-based PDF documents.
4. Process scanned or image-based PDF documents.
5. Convert academic documents into searchable knowledge.
6. Understand the meaning of student questions.
7. Retrieve relevant academic information.
8. Generate answers based on retrieved documents.
9. Display the sources used for the answer.
10. Reduce hallucination by grounding answers in available academic documents.

---

# 5. Proposed Solution

NEXORA uses Retrieval-Augmented Generation (RAG).

Instead of directly asking an AI model to answer a student's question, the system first searches the academic knowledge base.

The workflow is:

Student Question

↓

Convert Question into an Embedding

↓

Search Relevant Academic Documents

↓

Retrieve Relevant Document Chunks

↓

Provide Context to the LLM

↓

Generate Grounded Answer

↓

Display Answer with Source Information

The AI model does not rely only on its general knowledge.

Instead, it receives relevant information from the academic documents before generating an answer.

---

# 6. What is Retrieval-Augmented Generation?

Retrieval-Augmented Generation is a technique that combines:

1. Information Retrieval
2. Large Language Models

The retrieval system searches the knowledge base.

The Large Language Model generates an understandable answer using the retrieved information.

The process is:

Documents

↓

Text Extraction

↓

Chunking

↓

Embeddings

↓

Vector Database

↓

User Question

↓

Semantic Search

↓

Relevant Context

↓

Large Language Model

↓

Final Answer

---

# 7. Data Sources

The initial academic data for the project is collected from publicly available academic resource websites.

The sources currently considered include:

- https://manaclg.com/
- https://www.jntufastupdates.com/jntuk-syllabus-books/

These sources are used to identify relevant syllabus information and academic PDF resources.

The collected documents may include:

- Syllabus PDFs
- Subject-related academic materials
- Course information
- Study resources

The documents are processed and converted into a searchable knowledge base.

Important:

The project should store information about the original source of each document.

Example metadata:

{
    document_name,
    original_source,
    subject,
    regulation,
    branch,
    document_type
}

This improves traceability and allows answers to reference the original academic source.

---

# 8. Data Collection Architecture

The high-level data flow is:

Academic Source Websites

↓

Identify Relevant Documents

↓

Collect Document URLs

↓

Download or Ingest Documents

↓

Store Original Files

↓

Supabase Private Storage

↓

Document Processing Pipeline

↓

Vector Database

The original source documents are separated from the processed vector data.

This is an important architectural decision.

---

# 9. Why Supabase Storage?

Supabase Storage is used to store the original academic documents.

Examples:

- Syllabus PDFs
- Study material PDFs
- Academic documents

The bucket is private.

The private bucket provides better control over document access.

The architecture is:

Original Documents

↓

Supabase Private Bucket

↓

Document Processing Service

↓

Extracted Text

↓

Embeddings

↓

Vector Database

Supabase Storage acts as the document storage layer.

The vector database acts as the semantic search layer.

These two components have different responsibilities.

---

## 9.1 Storage Bucket Structure & Sources

The private Supabase Storage bucket contains the source documents organized into 2 main folders:

1. **`SYLLABUS/`**: Contains syllabus documentation (contains 1 file).
2. **`SUBJECTS/`**: Contains subject-related reference documents.

---

# 10. Document Processing Challenge

PDF documents are not always structured in the same way.

There are two major categories.

---

## 10.1 Text-Based PDFs

Text-based PDFs contain machine-readable text.

Example:

A syllabus document created using Microsoft Word and exported as a PDF.

The system can extract text directly.

Workflow:

PDF

↓

PDF Text Extraction

↓

Machine-Readable Text

↓

Text Processing

---

## 10.2 Image-Based or Scanned PDFs

Some documents are scanned copies.

The PDF may contain images of text instead of actual machine-readable text.

For example:

Physical Document

↓

Scanner

↓

Image-Based PDF

A normal PDF extraction tool may return:

- Empty text
- Incomplete text
- Very little text

Therefore, an additional process called Optical Character Recognition (OCR) is required.

---

# 11. Solution for Mixed PDF Types

NEXORA uses an adaptive document processing pipeline.

The system first attempts normal text extraction.

The extracted text is evaluated.

If sufficient text is found:

Use the normal text extraction pipeline.

If little or no text is found:

Use OCR.

The workflow is:

PDF Document

↓

Try Text Extraction

↓

Is Sufficient Text Available?

↓

YES ----------------→ Text Processing

↓

NO

↓

OCR Processing

↓

Extract Text from Images

↓

Text Processing

This approach avoids running OCR unnecessarily.

OCR can require more computational resources than normal text extraction.

---

# 12. Text Processing Pipeline

After text is extracted, the document is processed.

The pipeline is:

Raw Document Text

↓

Text Cleaning

↓

Text Normalization

↓

Chunking

↓

Embedding Generation

↓

Vector Database Storage

---

# 13. Why Chunking is Required

Academic documents can be very large.

Sending an entire document to an AI model for every student question is inefficient.

Therefore, the document is divided into smaller sections called chunks.

Example:

Original Document

[Page 1]

[Page 2]

[Page 3]

↓

Chunking

↓

Chunk 1

Chunk 2

Chunk 3

Chunk 4

Each chunk contains a meaningful section of the academic content.

When a student asks a question, the system retrieves only the most relevant chunks.

---

# 14. Chunk Overlap

Chunks may share a small amount of information with neighboring chunks.

This is called overlap.

Example:

Chunk 1:

Topic A

Topic B

Topic C

Chunk 2:

Topic C

Topic D

Topic E

Topic C is shared.

This prevents important contextual information from being lost at chunk boundaries.

---

# 15. Why Embeddings are Required

Computers do not understand semantic meaning in the same way humans do.

Therefore, the text is converted into numerical representations called embeddings.

Example:

"What topics are included in Unit 3?"

↓

Embedding Vector

[0.123, -0.542, 0.876, ...]

A semantically similar sentence may be:

"What should I study in Module 3?"

Even though the exact words are different, the meaning is similar.

Embeddings allow the system to perform semantic search.

---

# 16. Vector Database

The embeddings are stored inside a vector database.

Each stored record contains:

- Text chunk
- Vector embedding
- Document name
- Source information
- Subject information
- Page number
- Other metadata

Example:

{
    chunk_text,
    embedding,
    document_name,
    source_url,
    subject,
    page_number
}

When a student asks a question, the system searches for vectors that are semantically similar to the question.

---

# 17. Chatbot Query Architecture

The question-answering pipeline is:

Student

↓

Question

↓

Question Embedding

↓

Vector Similarity Search

↓

Retrieve Relevant Chunks

↓

Build Context

↓

Large Language Model

↓

Generate Answer

↓

Display Sources

---

# 18. Preventing Hallucination

The system uses a grounded generation strategy.

The LLM receives instructions to answer only using the retrieved academic context.

The expected behavior is:

If the answer exists in the documents:

Generate an answer based on the retrieved information.

If the answer does not exist:

Respond that sufficient information was not found in the available academic knowledge base.

The chatbot should not invent academic information.

---

# 19. Answer Sources

Each answer should provide source information.

Example:

Answer:

The subject contains five units.

Sources:

Document:
Computer Networks Syllabus

Page:
4

Original Source:
Academic Resource Website

Source information improves:

- Trust
- Transparency
- Verification
- Debugging

Students can verify where the answer came from.

---

# 20. End Users

The primary users of NEXORA are students.

## 20.1 College Students

Students are the primary users.

They can ask questions about:

- Syllabus
- Subjects
- Units
- Study materials
- Academic topics

The chatbot reduces the time required to search through multiple documents.

---

## 20.2 Final Year Students

Final year students can use the system to quickly search academic materials and subject information.

They may use the system for:

- Exam preparation
- Subject revision
- Finding syllabus information
- Locating relevant study resources

---

## 20.3 New Students

New students may not know:

- Which documents are important.
- Where the syllabus is located.
- Where study resources can be found.

The chatbot provides a simpler conversational interface.

---

# 21. Stakeholders

Stakeholders are individuals or organizations that are affected by or interested in the system.

---

## 21.1 Students

Students are the primary beneficiaries.

Benefits:

- Faster information access
- Reduced manual searching
- Conversational academic search
- Easier access to study materials

---

## 21.2 College or Academic Institution

Educational institutions may benefit from a centralized knowledge access system.

Potential benefits:

- Better access to academic information
- Reduced repetitive information requests
- Improved student support

---

## 21.3 Faculty Members

Faculty members may use the platform to help students locate relevant academic resources.

The system may reduce repetitive questions about:

- Syllabus
- Course topics
- Study resources

---

## 21.4 Project Development Team

The development team is responsible for:

- System architecture
- Data ingestion
- AI integration
- Testing
- Deployment
- Maintenance

---

## 21.5 System Administrators

Administrators may manage:

- Documents
- Knowledge base updates
- User access
- System configuration

---

# 22. Technology Stack

The system uses the following technology stack.

---

## 22.1 Frontend

Technology:

Streamlit

Purpose:

Provides a simple chat interface for students.

The user can:

- Ask questions
- View answers
- View source documents

---

## 22.2 Backend

Technology:

FastAPI

Purpose:

FastAPI provides the backend API.

Responsibilities include:

- Receiving user questions
- Managing API requests
- Calling the RAG pipeline
- Returning responses

---

## 22.3 Object Storage

Technology:

Supabase Storage

Purpose:

Stores original academic PDF documents.

The project uses a private bucket.

---

## 22.4 PDF Processing

Technology:

PyMuPDF

Purpose:

Extracts text from normal text-based PDFs.

---

## 22.5 OCR Processing

Technology:

OCR Engine

Examples include:

- Tesseract OCR
- Cloud OCR services

Purpose:

Extract text from scanned and image-based PDF documents.

---

## 22.6 Embedding Model

Technology:

Sentence Transformer

Example model:

all-MiniLM-L6-v2

Purpose:

Converts text into vector embeddings.

---

## 22.7 Vector Database

Initial Technology:

ChromaDB

Purpose:

Stores vector embeddings and performs semantic similarity searches.

Future versions can use:

- pgvector
- Managed vector databases

---

## 22.8 Large Language Model

An LLM is used to generate the final answer.

The LLM receives:

1. Student question
2. Retrieved academic context

The LLM generates an understandable answer based on the retrieved context.

---

# 23. Complete Technology Architecture

Student

↓

Streamlit Frontend

↓

FastAPI Backend

↓

RAG Service

↓

Vector Database

↓

Relevant Academic Chunks

↓

Large Language Model

↓

Answer + Sources


Document Pipeline:

Academic Source

↓

PDF Documents

↓

Supabase Private Storage

↓

Document Ingestion

↓

Text Extraction / OCR

↓

Chunking

↓

Embeddings

↓

Vector Database

---

# 24. Major Technical Problems and Solutions

## Problem 1: Documents are Distributed

Problem:

Academic information is available across different websites and documents.

Solution:

Collect relevant documents and create a centralized knowledge base.

---

## Problem 2: Large PDF Files

Problem:

Students cannot efficiently read large documents for every question.

Solution:

Split documents into smaller chunks and retrieve only relevant sections.

---

## Problem 3: Scanned PDFs

Problem:

Some PDF documents contain images rather than machine-readable text.

Solution:

Detect insufficient extracted text and use OCR.

---

## Problem 4: Semantic Search

Problem:

Traditional keyword search may fail when students use different wording.

Solution:

Use embeddings and vector similarity search.

---

## Problem 5: AI Hallucination

Problem:

A general AI model may generate incorrect academic information.

Solution:

Use Retrieval-Augmented Generation and instruct the LLM to answer using retrieved context.

---

## Problem 6: Source Verification

Problem:

Students need to verify AI-generated answers.

Solution:

Store metadata and display the document source and page information.

---

## Problem 7: Document Security

Problem:

Academic documents may need controlled access.

Solution:

Use a private Supabase Storage bucket and control access through the application.

---

# 25. Current System Scope

The initial version of NEXORA focuses on:

- Academic document collection
- PDF storage
- Text extraction
- OCR support
- Document chunking
- Embedding generation
- Vector search
- RAG-based answers
- Source information
- Student chatbot interface

---

# 26. Future Improvements

The future system can include:

- User authentication
- Student-specific access
- Conversation history
- Hybrid search
- Reranking
- Multilingual support
- Voice-based interaction
- Document upload by administrators
- Automatic document processing
- Background workers
- Monitoring
- Docker
- Kubernetes
- CI/CD pipelines

---

# 27. Production-Oriented Architecture

The current implementation is a production-oriented MVP.

The architecture separates:

- Document storage
- Document processing
- OCR
- Embedding generation
- Vector search
- Answer generation

This separation allows the system to evolve into a scalable architecture.

A future production pipeline can be:

Document Upload

↓

Supabase Storage

↓

Message Queue

↓

Background Processing Worker

↓

Text Extraction / OCR

↓

Chunking

↓

Embedding Generation

↓

Vector Database

This prevents students from waiting while large documents are being processed.

---

# 28. Business Value

NEXORA provides value by:

- Reducing time spent searching academic documents.
- Providing conversational access to study materials.
- Centralizing distributed academic knowledge.
- Supporting semantic search.
- Providing source-based answers.
- Reducing the risk of unsupported AI responses.

---

# 29. Success Criteria

The project is successful if:

1. Academic documents can be collected.
2. Original documents can be securely stored.
3. Text can be extracted from normal PDFs.
4. Image-based PDFs can be processed using OCR.
5. Documents can be converted into chunks.
6. Chunks can be converted into embeddings.
7. Relevant chunks can be retrieved.
8. Students can ask academic questions.
9. The system generates answers using retrieved information.
10. Sources are displayed with answers.

---

# 30. Conclusion

NEXORA is an AI-powered academic knowledge assistant designed to improve access to college study materials.

The system transforms static academic documents into an intelligent searchable knowledge base.

By combining:

- Academic document collection
- Secure document storage
- PDF processing
- OCR
- Semantic embeddings
- Vector databases
- Retrieval-Augmented Generation

NEXORA provides students with a conversational way to access academic information.

The system is designed as a production-oriented foundation that can be extended with authentication, scalable document processing, monitoring, and cloud deployment in future versions.
