# assignment-namekart

# Notes App & RAG Pipeline

This repository contains a **Notes Application** built with **FastAPI** and **React**, along with a **Retrieval-Augmented Generation (RAG) pipeline** to enhance Large Language Models (LLMs) using external knowledge.

---

## 1. Backend API: FastAPI for Notes

I've chosen **FastAPI** for its modern features, high performance, and automatic documentation, which makes it excellent for rapid development.

### Database Schema (PostgreSQL)

We use two tables:

- **users** – Stores user credentials.
- **notes** – Stores note content and links to a user via a foreign key. Includes a `version` column for optimistic locking.

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL
);

CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    content TEXT,
    owner_id INTEGER NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    CONSTRAINT fk_owner
        FOREIGN KEY(owner_id) 
        REFERENCES users(id)
        ON DELETE CASCADE
);

Authentication
We use JWT (JSON Web Tokens). This is a stateless, token-based standard that's perfect for decoupled applications like a React frontend talking to a FastAPI backend. After login, users receive a short-lived access token, which they must include in the Authorization header for all protected requests.

Login Example (POST /token)

Request (form data):

ini
Copy
Edit
username=user&password=pass
Response (200 OK):

json
Copy
Edit
{
  "access_token": "your_jwt_token_here",
  "token_type": "bearer"
}
Notes CRUD API
Create Note (POST /notes)

Request Body:

json
Copy
Edit
{
  "title": "My First Note",
  "content": "This is the content of the note."
}
Response (200 OK):

json
Copy
Edit
{
  "id": 1,
  "title": "My First Note",
  "content": "This is the content of the note.",
  "owner_id": 101,
  "version": 1
}
Update Note (PUT /notes/{note_id})

Request Body:

json
Copy
Edit
{
  "title": "Updated Note Title",
  "content": "Updated content.",
  "version": 1
}
Response (200 OK):

json
Copy
Edit
{
  "id": 1,
  "title": "Updated Note Title",
  "content": "Updated content.",
  "owner_id": 101,
  "version": 2
}
Delete Note (DELETE /notes/{note_id})

Response (200 OK):

json
Copy
Edit
{
  "detail": "Note deleted successfully"
}
Failure Mode & Mitigation
Lost Update (Race Condition):

Happens when two clients edit the same note simultaneously.

Mitigated using Optimistic Locking with the version column.

Server checks the version before updating. If it doesn't match, returns 409 Conflict.

2. Notes App Design (React + FastAPI)
Directory Structure:

pgsql
Copy
Edit
notes-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── crud.py
│   │   ├── schema.py
│   │   └── auth.py
│   ├── requirements.txt
│   └── .env
└── frontend/
    ├── public/
    ├── src/
    │   ├── components/
    │   ├── services/
    │   ├── pages/
    │   ├── App.js
    │   └── index.js
    └── package.json
Frontend: React, Tailwind CSS.

Backend: FastAPI, PostgreSQL.

Authentication: JWT.

Version Control: Optimistic locking for notes.

3. RAG Pipeline (Retrieval-Augmented Generation)
A RAG pipeline enhances an LLM by providing it with relevant external information before generating a response.

Directory Structure:

css
Copy
Edit
rag-pipeline/
├── data/
│   └── knowledge_base.txt
├── main.py
└── requirements.txt
Python Implementation (main.py)

python
Copy
Edit
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

with open('data/knowledge_base.txt', 'r') as f:
    knowledge_base_text = f.read()

text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=500,
    chunk_overlap=100,
    length_function=len,
)
chunks = text_splitter.split_text(knowledge_base_text)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = FAISS.from_texts(texts=chunks, embedding=embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

template = """
Answer the following question based only on the provided context.
If you don't know the answer, just say that you don't know.

Context:
{context}

Question:
{question}
"""
prompt = ChatPromptTemplate.from_template(template)
llm = ChatOpenAI(model_name="gpt-3.5-turbo")

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

user_question = "What is the primary mitigation for a lost update race condition?"
response = rag_chain.invoke(user_question)

print("User Question:", user_question)
print("Generated Answer:", response)
Evaluation Metric: Context Precision
Definition: Measures how many retrieved documents are relevant.

Formula: (Relevant Chunks) / (Total Retrieved Chunks)

Purpose: Ensures the RAG pipeline retrieves useful context for the LLM.

4. Tech Stack
Frontend: React, Tailwind CSS

Backend: FastAPI, PostgreSQL

Authentication: JWT (Supabase optional)

RAG Pipeline: LangChain, FAISS, HuggingFace embeddings, OpenAI LLM
