from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

EXTENSION_TO_LANGUAGE = {
    # Systems
    ".cpp": Language.CPP,
    ".cc": Language.CPP,
    ".cxx": Language.CPP,
    ".c": Language.C,
    ".h": Language.C,
    # JVM
    ".java": Language.JAVA,
    ".kt": Language.KOTLIN,
    ".scala": Language.SCALA,
    # Web
    ".js": Language.JS,
    ".jsx": Language.JS,
    ".ts": Language.TS,
    ".tsx": Language.TS,
    ".php": Language.PHP,
    ".html": Language.HTML,
    # Scripting
    ".py": Language.PYTHON,
    # ".rb": Language.RB,
    ".lua": Language.LUA,
    ".pl": Language.PERL,
    ".pm": Language.PERL,
    ".r": Language.R,
    # Systems/Low level
    ".rs": Language.RUST,
    ".swift": Language.SWIFT,
    ".go": Language.GO,
    # Functional
    ".hs": Language.HASKELL,
    ".ex": Language.ELIXIR,
    ".exs": Language.ELIXIR,
    # Docs/Config
    ".md": Language.MARKDOWN,
    ".rst": Language.RST,
    ".tex": Language.LATEX,
    # Other
    ".proto": Language.PROTO,
    ".sol": Language.SOL,
    ".cs": Language.CSHARP,
    ".cob": Language.COBOL,
    ".cbl": Language.COBOL,
    ".ps1": Language.POWERSHELL,
    ".psm1": Language.POWERSHELL,
    ".vb": Language.VISUALBASIC6,
    ".bas": Language.VISUALBASIC6,
}

class TextSplitter:
    def __init__(self,documents,chunk_size=1000,chunk_overlap=200):
        self.documents = documents
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split_documents_into_chunks(self):
        print("Splitting documents into chunks...")
        all_chunks = []
        for doc in self.documents:
            splitter = self._get_splitter(doc)
            chunks = splitter.split_documents([doc])
            all_chunks.extend(chunks)

        print("chunking completed")
        return all_chunks
    
    def _get_splitter(self,doc):
        file_path = doc.metadata.get("path", "")
        ext = "." + file_path.split(".")[-1] if "." in file_path else ""
        language = EXTENSION_TO_LANGUAGE.get(ext)
        if language:
            return RecursiveCharacterTextSplitter.from_language(
                language=language,
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
            )
        else : 
            return RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                length_function=len,
                separators=["\n\n", "\n", " ", ""]
            )