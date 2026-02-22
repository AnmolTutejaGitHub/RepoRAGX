from langchain_community.document_loaders import GithubFileLoader

EXCLUDE_EXTENSIONS = (
    ".png", ".jpg", ".jpeg", ".gif", ".svg",
    ".zip", ".tar", ".gz", ".rar",
    ".exe", ".dll", ".so",
    ".mp3", ".mp4", ".wav",
    ".pdf", ".doc", ".docx",
    ".lock"
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
        docs = self.loader.load()
        print(f"Loaded all the files from github!!")
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