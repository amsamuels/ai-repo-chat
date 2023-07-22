import os
from dotenv import load_dotenv
from langchain.document_loaders import GitLoader


load_dotenv()

loader = GitLoader(
    clone_url=os.getenv("REPO_URL"),
    repo_path='repo',
    branch=os.getenv("REPO_BRANCH"),
)

loader.load()