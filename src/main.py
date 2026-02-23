from src.rag.github_codebase_loader import GitHubCodeBaseLoader
from src.rag.text_splitter import TextSplitter
from src.rag.embedding_manager import EmbeddingManager
from src.rag.vector_store import VectorStore
from src.rag.rag_retriever import RAGRetriever
from src.rag.groq_llm import GroqLLM
import os
import getpass
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

if __name__ == "__main__" :
    print(r"""/**
 *    __________                    __________    _____    ____________  ___
 *    \______   \ ____ ______   ____\______   \  /  _  \  /  _____/\   \/  /
 *     |       _// __ \\____ \ /  _ \|       _/ /  /_\  \/   \  ___ \     / 
 *     |    |   \  ___/|  |_> >  <_> )    |   \/    |    \    \_\  \/     \ 
 *     |____|_  /\___  >   __/ \____/|____|_  /\____|__  /\______  /___/\  \
 *            \/     \/|__|                 \/         \/        \/      \_/
 */""")
    
    print("\nChat with your github repository\n")

    github_token = getpass.getpass("GitHub Personal Access Token: ").strip()
    groq_key = getpass.getpass("Groq API Key: ").strip()
    os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"] = github_token
    os.environ["GROQ_API_KEY"] = groq_key
    model_name = input("Model Name (default: llama-3.3-70b-versatile, see Groq docs for supported models): ").strip() or "llama-3.3-70b-versatile"

    repo = input("Repo (owner/repo): ").strip()
    branch = input("Branch (default: main): ").strip() or "main"

    persist_directory = Path.home()/".RepoRAGX"/"vector_store"
    os.makedirs(persist_directory, exist_ok=True)
    
    docs = GitHubCodeBaseLoader(repo=repo,branch=branch,access_token=github_token).load()
    chunks = TextSplitter(docs).split_documents_into_chunks()
    embedding_manager = EmbeddingManager()

    vector_store = VectorStore(collection_name=repo.replace("/", "_"),persist_directory=persist_directory)
    texts=[doc.page_content for doc in chunks]
    embeddings=embedding_manager.generate_embeddings(texts)
    vector_store.add_documents(chunks,embeddings)

    rag_retriever = RAGRetriever(vector_store=vector_store,embedding_manager=embedding_manager)
    llm = GroqLLM(model_name=model_name)
   
    while True:
        query = input("\nAsk anything ('exit' to quit): ")
        if query.strip().lower() == "exit":
            break
        answer = llm.rag(query=query,retriever=rag_retriever)
        print(answer)   

