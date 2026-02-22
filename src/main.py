from src.rag.github_codebase_loader import GitHubCodeBaseLoader
from src.rag.text_splitter import TextSplitter
from src.rag.embedding_manager import EmbeddingManager
import os
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__" :
    print("Chat with your github repo")
    docs = GitHubCodeBaseLoader(repo="AnmolTutejaGitHub/portfolio",branch="main",access_token=os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")).load()
    chunks = TextSplitter(docs).split_documents_into_chunks()
    print(chunks)
    embedding_manager = EmbeddingManager()
