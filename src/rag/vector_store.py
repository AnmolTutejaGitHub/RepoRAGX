import chromadb
import uuid
import os
from sklearn.metrics.pairwise import cosine_similarity

class VectorStore:
    def __init__(self,collection_name,persist_directory):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.client = None
        self.collection = None
        self._initialize_store()

    def _initialize_store(self):
        print("Initilizing vector database....")
        try:
            os.makedirs(self.persist_directory,exist_ok=True)
            self.client = chromadb.PersistentClient(path=self.persist_directory)
            
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={
                    "repo": self.collection_name,
                    "type": "github_codebase",
                    "embedding_model": "all-MiniLM-L6-v2",
                }
            )

            print(f"Vector store initialized. Collection: {self.collection_name}")
            print(f"Existing documents in collection: {self.collection.count()}")
            
        except Exception as e:
            print(f"Error initializing vector store: {e}")
            raise
    
    def add_documents(self,documents,embeddings):
        """
            types : documents : List[Any]
            embeddings : numpy.ndarray
        """
        if len(documents) != len(embeddings):
            raise ValueError("Number of documents must match number of embeddings")
        
        print(f"Adding {len(documents)} documents to vector store...")
        ids = []
        metadatas = []
        documents_text = []
        embeddings_list = []

        for i,(doc,embedding) in enumerate(zip(documents,embeddings)):
            doc_id = f"doc_{uuid.uuid4().hex[:8]}_{i}"
            ids.append(doc_id)
            
            metadata = dict(doc.metadata)
            metadata['doc_index'] = i
            metadata['content_length'] = len(doc.page_content)
            metadatas.append(metadata)
            
            documents_text.append(doc.page_content)
            
            embeddings_list.append(embedding.tolist())

            try:
                self.collection.add(
                    ids=ids,
                    embeddings=embeddings_list,
                    metadatas=metadatas,
                    documents=documents_text
                )
                print(f"Successfully added {len(documents)} documents to vector store")
                print(f"Total documents in collection: {self.collection.count()}")
            
            except Exception as e:
                print(f"Error adding documents to vector store: {e}")
                raise
