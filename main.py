import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. Load the knowledge base from a file
with open('data/knowledge_base.txt', 'r') as f:
    knowledge_base_text = f.read()

# 2. Chunking
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=500,
    chunk_overlap=100,
    length_function=len,
)
chunks = text_splitter.split_text(knowledge_base_text)

# 3. Embeddings & Vector Store
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = FAISS.from_texts(texts=chunks, embedding=embeddings)

# 4. Retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 3}) # Retrieve top 3 chunks

# 5. Prompt Template
template = """
Answer the following question based only on the provided context.
If you don't know the answer, just say that you don't know.

Context:
{context}

Question:
{question}
"""
prompt = ChatPromptTemplate.from_template(template)

# 6. LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key="YOUR_API_KEY")

# The RAG Chain
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Ask a question
user_question = "What is the primary mitigation for a lost update race condition?"
response = rag_chain.invoke(user_question)

print("User Question:", user_question)
print("Generated Answer:", response)

