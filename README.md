# Notes App & RAG Pipeline

This repository contains two main components:
1.  A full-stack **Notes Application** built with a **React** frontend and a **FastAPI** backend.
2.  A **Retrieval-Augmented Generation (RAG) pipeline** that demonstrates how to enhance a Large Language Model (LLM) with external knowledge.

---

## 1. Notes Application (React + FastAPI)

This is a modern, full-stack web application that allows users to sign up, log in, and perform CRUD (Create, Read, Update, Delete) operations on their notes securely.

### **Features**

*   **User Authentication:** Secure user registration and login using JWT (JSON Web Tokens).
*   **CRUD for Notes:** Authenticated users can create, view, update, and delete their own notes.
*   **Optimistic Locking:** Prevents race conditions and lost updates when multiple clients try to edit the same note simultaneously.

### **Tech Stack**

*   **Backend:** FastAPI, Python, PostgreSQL
*   **Frontend:** React, Tailwind CSS
*   ... (and other libraries listed in `requirements.txt` and `package.json`)

### **Setup & Running the Backend (FastAPI)**

1.  **Navigate to the Backend Directory:**
    ```
    cd backend
    ```

2.  **Create and Activate a Virtual Environment:**
    ```
    # Create the environment
    python -m venv venv

    # Activate on macOS/Linux
    source venv/bin/activate

    # Activate on Windows
    source venv/Scripts/activate
    ```

3.  **Install Dependencies:**
    ```
    pip install -r requirements.txt
    ```

4.  **Run the Server:**
    ```
    uvicorn app.main:app --reload
    ```
    The backend server is now running. You can view the interactive API documentation at `http://127.0.0.1:8000/docs`.

---

## 2. RAG Pipeline

This script demonstrates how to build a simple RAG pipeline using LangChain. It uses a local text file as a knowledge base to answer questions, making the LLM's responses more accurate and context-aware.

### **How It Works**

1.  **Load:** A local text file (`data/knowledge_base.txt`) is loaded.
2.  **Chunk:** The text is split into smaller, manageable chunks.
3.  **Embed & Store:** Each chunk is converted into a numerical vector (embedding) and stored in a FAISS vector store for efficient searching.
4.  **Retrieve:** When a question is asked, the pipeline retrieves the most relevant chunks from the vector store.
5.  **Generate:** The question and the retrieved context are passed to an LLM (GPT-3.5 Turbo) to generate a final answer.

### **Setup & Running the RAG Pipeline**

1.  **Navigate to the Project Directory:**
    ```
    cd rag-pipeline # Or your main project folder
    ```

2.  **Create and Activate a Virtual Environment:**
    Follow the same steps as for the backend to create and activate a `venv`.

3.  **Install Dependencies:**
    ```
    pip install -r requirements.txt
    ```

4.  **Set Your OpenAI API Key:**
    *   Create a file named `.env` in the project root.
    *   Add your API key to this file:
        ```
        OPENAI_API_KEY="your_sk_key_here"
        ```

5.  **Create the Knowledge Base:**
    The script requires a knowledge base file to read from.
    ```
    # Create the directory
    mkdir data

    # Create the file with some content
    echo "The primary mitigation for a lost update race condition is optimistic locking." > data/knowledge_base.txt
    ```

6.  **Run the Script:**
    ```
    python main.py
    ```
    The script will execute the pipeline and print the user's question and the LLM's generated answer to the terminal.
