from langchain_community.document_loaders import GithubFileLoader

EXCLUDE_EXTENSIONS = (
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".bmp", ".webp",
    ".zip", ".tar", ".gz", ".rar", ".7z",
    ".exe", ".dll", ".so", ".o", ".a", ".dylib",
    ".mp3", ".mp4", ".wav", ".avi", ".mov",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".lock", ".DS_Store", ".bin", ".ipynb",
    ".woff", ".woff2", ".ttf", ".eot", ".otf",
    ".pyc", ".class", ".jar",
    ".db", ".sqlite", ".sqlite3",
    ".min.js", ".min.css",
)

EXCLUDE_FOLDERS = (
    "node_modules/",
    ".git/",
    "dist/",
    "build/",
    "__pycache__/",
    "venv/",
    ".venv/",
)


class GitHubCodeBaseLoader :
    def __init__(self,repo,branch,access_token=None):
        self.repo = repo
        self.branch = branch
        self.access_token = access_token
        self.loader = None
        self._init_loader()
    
    def _init_loader(self):
        print("Initilizing github loader.....")
        self.loader = GithubFileLoader(
            repo = self.repo,
            branch = self.branch,
            access_token = self.access_token,
            file_filter = GitHubCodeBaseLoader.file_filter
        )

    def load(self):
        print("Fetching files from github....")
        # docs = self.loader.load() #load all at once
        docs = []
        for doc in self.loader.lazy_load(): #lazy -> one by one
            try:
                docs.append(doc)
            except Exception:
                print(f"Skipping file: {doc.metadata.get('path','unknown')}")
        print(f"Loaded {len(docs)} files from github!")
        return docs
    
    @staticmethod
    def file_filter(path):
        for folder in EXCLUDE_FOLDERS:
            if folder in path:
                return False

        for ext in EXCLUDE_EXTENSIONS:
            if path.endswith(ext):
                return False

        return True