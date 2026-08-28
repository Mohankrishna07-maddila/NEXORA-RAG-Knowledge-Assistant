# NEXORA

## Production-Oriented Multimodal RAG Knowledge Assistant

---

# 1. Business Problem

Organizations store important information in different documents such as:

- PDF files
- Scanned documents
- Image-based PDFs
- Reports
- Policies
- Technical manuals
- Academic documents
- Internal knowledge documents

Finding information from these documents manually is time-consuming.

Traditional keyword search also has limitations because it searches for exact words rather than understanding the meaning of a user's question.

For example, a user may ask:

> "What happens when a server fails?"

The relevant document may contain:

> "The system automatically performs failover and restores services."

A traditional keyword search may not understand that these two statements are related.

Another major problem is that Large Language Models can generate answers that sound correct but are not actually supported by the organization's documents.

This creates a problem of:

- Hallucination
- Lack of source verification
- Difficulty finding information
- Knowledge scattered across multiple documents
- Manual document searching

---

# 2. Problem Statement

How can we build an intelligent knowledge assistant that can:

1. Securely store organization documents.
2. Process both text-based and image-based PDFs.
3. Convert documents into searchable knowledge.
4. Understand the semantic meaning of user questions.
5. Retrieve relevant information.
6. Generate answers based only on available documents.
7. Provide the source document used for the answer.
8. Scale from a prototype to a production-ready architecture.

---

# 3. Proposed Solution

NEXORA is a Retrieval-Augmented Generation (RAG) platform.

Instead of asking an LLM to answer directly from its training knowledge, the system first searches the organization's documents.

The retrieved document content is then provided to the Large Language Model as context.

The LLM generates an answer using the retrieved information.

This process is called Retrieval-Augmented Generation.

---

# 4. System Architecture

                    DOCUMENT UPLOAD
                           |
                           v
              SUPABASE PRIVATE STORAGE
                           |
                           v
                   INGESTION SERVICE
                           |
             +-------------+-------------+
             |                           |
             v                           v
       TEXT PDF                    IMAGE/SCANNED PDF
             |                           |
             v                           v
      TEXT EXTRACTION                  OCR ENGINE
             |                           |
             +-------------+-------------+
                           |
                           v
                    TEXT NORMALIZATION
                           |
                           v
                       CHUNKING
                           |
                           v
                      EMBEDDINGS
                           |
                           v
                      VECTOR DATABASE
                           |
                           v
                        USER QUERY
                           |
                           v
                    QUERY EMBEDDING
                           |
                           v
                   SIMILARITY SEARCH
                           |
                           v
                    RELEVANT CHUNKS
                           |
                           v
                           LLM
                           |
                           v
                GROUNDED ANSWER + SOURCES

---

# 5. Why Supabase Storage?

Supabase Storage is used to store the original source documents.

The documents are stored in a private bucket.

A private bucket is important because:

- Documents may contain confidential information.
- Users should not access files directly without authorization.
- The application can control access.
- Signed URLs can be generated when temporary file access is required.

The original document is stored separately from its processed representation.

This allows the system to preserve the original source of information.

## 5.1 Storage Bucket Structure & Sources

The private Supabase Storage bucket contains the source documents organized into 2 main folders:

1. **`SYLLABUS/`**: Contains syllabus documentation (contains 1 file).
2. **`SUBJECTS/`**: Contains subject-related reference documents.


---

# 6. Document Processing Problem

PDF files are not all the same.

There are two important categories.

## 6.1 Text-Based PDFs

A text-based PDF contains actual machine-readable text.

Example:

A PDF generated from Microsoft Word.

The text can be extracted directly using a PDF parser.

Pipeline:

PDF
↓
PDF Text Extractor
↓
Raw Text
↓
Chunking

---

## 6.2 Image-Based or Scanned PDFs

A scanned PDF contains images of text.

The text is visible to humans but may not exist as machine-readable text.

A normal PDF text extraction library may return:

- Empty text
- Very little text
- Incorrect text

Therefore the system must use Optical Character Recognition.

Pipeline:

Scanned PDF
↓
Convert PDF Pages to Images
↓
OCR
↓
Extracted Text
↓
Chunking

---

# 7. Multimodal Document Processing Strategy

The ingestion pipeline first attempts normal text extraction.

The system measures how much useful text was extracted.

If enough text is available:

Use normal PDF text extraction.

If little or no text is available:

Use OCR processing.

This creates an adaptive document processing pipeline.

Pseudo workflow:

IF extracted_text_length > threshold:

    use_text_extraction()

ELSE:

    use_OCR()

This avoids unnecessarily running OCR on normal text PDFs.

OCR is more computationally expensive than normal text extraction.

---

# 8. Why Chunking Is Required

Large Language Models cannot efficiently process an unlimited number of complete documents.

Therefore documents are divided into smaller sections called chunks.

Example:

Original Document:

[Page 1]
[Page 2]
[Page 3]
[Page 4]

After Chunking:

Chunk 1
Chunk 2
Chunk 3
Chunk 4
Chunk 5

Each chunk represents a small meaningful section of the document.

Chunk overlap is used so that important context is not lost between two chunks.

Example:

Chunk 1:
Sentence A
Sentence B
Sentence C

Chunk 2:
Sentence C
Sentence D
Sentence E

Sentence C provides contextual overlap.

---

# 9. Why Embeddings Are Required

Computers cannot directly perform semantic search using raw text efficiently.

Therefore each text chunk is converted into a numerical representation called an embedding.

Example:

"What is machine learning?"

↓

[0.123, -0.456, 0.891, ...]

Text with similar meanings produces vectors that are mathematically closer together.

For example:

"How does the system recover?"

and

"What happens after a server failure?"

may have similar semantic representations.

---

# 10. Vector Database

The generated embeddings are stored in a vector database.

Each vector is stored with metadata.

Example:

{
    chunk_text,
    embedding,
    document_name,
    document_id,
    page_number,
    storage_path
}

When a user asks a question:

1. The question is converted into an embedding.
2. The system searches for similar vectors.
3. The most relevant document chunks are retrieved.
4. These chunks are provided to the LLM.

---

# 11. Retrieval-Augmented Generation

The RAG process consists of two major phases.

## Ingestion Phase

Documents
↓
Extraction
↓
OCR if required
↓
Chunking
↓
Embedding
↓
Vector Database

## Query Phase

User Question
↓
Question Embedding
↓
Vector Search
↓
Relevant Chunks
↓
LLM
↓
Answer with Sources

---

# 12. Preventing Hallucination

The LLM is instructed to answer only from the retrieved context.

System behavior:

If relevant information exists:

Generate an answer using the retrieved context.

If relevant information does not exist:

Respond:

"I could not find sufficient information in the available documents."

This prevents the model from pretending to know information that does not exist in the knowledge base.

---

# 13. Source Citations

Every answer should contain source information.

Example:

Answer:

The system automatically creates a backup before deployment.

Sources:

deployment_policy.pdf
Page: 12

Source information improves:

- Trust
- Transparency
- Verification
- Debugging

---

# 14. Security Architecture

The system uses a private Supabase Storage bucket.

Documents are not publicly accessible.

The application accesses files using authorized credentials.

Security layers include:

1. Private document storage
2. Authentication
3. Authorization
4. Signed URLs
5. Environment variables for secrets
6. Secure API communication

API keys are never stored directly in source code.

---

# 15. Production-Oriented Architecture

The prototype architecture is designed so components can later scale independently.

Components:

Frontend
↓
API Gateway
↓
FastAPI Backend
↓
RAG Service
↓
Vector Database
↓
LLM Provider

Document processing is separated from the chat system.

This is important because document processing can be slow.

A production architecture can later use:

Document Upload
↓
Message Queue
↓
Background Worker
↓
Document Processing
↓
Embedding
↓
Vector Database

This prevents users from waiting while large documents are processed.

---

# 16. Technology Stack

## Frontend

Streamlit

Purpose:

Provides a fast interface for demonstrating the chatbot.

---

## Backend

FastAPI

Purpose:

Provides API endpoints and separates application logic from the frontend.

---

## Object Storage

Supabase Storage

Purpose:

Secure storage of original documents.

---

## PDF Processing

PyMuPDF / pypdf

Purpose:

Extract text from machine-readable PDF files.

---

## OCR

Tesseract or another OCR service

Purpose:

Extract text from scanned and image-based PDF documents.

---

## Embedding Model

Sentence Transformer

Example:

all-MiniLM-L6-v2

Purpose:

Converts document chunks and user questions into numerical vectors.

---

## Vector Database

ChromaDB for the initial prototype.

Future architecture can migrate to a managed vector database or Supabase pgvector.

Purpose:

Stores embeddings and performs similarity search.

---

## LLM

Open-source model accessed through an API provider.

Purpose:

Generates the final grounded answer.

---

# 17. Current MVP Scope

The first working version focuses on:

- Uploading or reading documents from Supabase Storage
- Processing text PDFs
- Detecting scanned PDFs
- OCR support architecture
- Chunking
- Embedding
- Vector storage
- Semantic retrieval
- Question answering
- Source display

The architecture is designed to support production improvements later.

---

# 18. Future Improvements

Future versions can include:

- User authentication
- Role-based access control
- Background document processing
- Redis caching
- Hybrid search
- Reranking
- Conversation memory
- Monitoring
- Logging
- Docker
- Kubernetes
- CI/CD
- Automated evaluation
- Document versioning

---

# 19. Success Criteria

The system is successful when:

1. A document can be stored securely.
2. Text can be extracted from the document.
3. Image-based PDFs can be identified.
4. OCR can be applied when required.
5. Text can be converted into chunks.
6. Chunks can be embedded.
7. Embeddings can be searched semantically.
8. Relevant context can be retrieved.
9. The LLM generates grounded answers.
10. Sources are displayed to the user.

---

# 20. Conclusion

NEXORA transforms static documents into an intelligent searchable knowledge system.

The system combines:

- Secure document storage
- Text extraction
- OCR
- Semantic search
- Vector databases
- Retrieval-Augmented Generation
- Source-based answers

The architecture separates document storage, document processing, retrieval, and answer generation.

This separation provides a foundation for building a scalable and production-oriented AI knowledge platform.
