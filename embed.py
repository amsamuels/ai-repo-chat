import os
from dotenv import load_dotenv
from supabase.client import Client, create_client
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import SupabaseVectorStore
from langchain.document_loaders import TextLoader
from langchain.docstore.document import Document



load_dotenv()

superbase_url = os.getenv("SUPERBASE_URL")
superbase_key = os.getenv("SUPABASE_SERVICE_KEY")
superbase:Client = create_client(superbase_url, superbase_key)


# configure these to your liking
exclude_dir = ['.git', 'node_modules', 'public', 'assets']
exclude_files = ['package-lock.json', '.DS_Store']
exclude_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.ico', '.svg', '.webp',
                      '.mp3', '.wav']
exclude_filenames = ['LICENSE', 'README.md', 'README', 'CHANGELOG.md', 'CHANGELOG', 'CONTRIBUTING.md', 'CONTRIBUTING', 
                        'CODE_OF_CONDUCT.md', 'CODE_OF_CONDUCT', 'SECURITY.md', 'SECURITY', 'PULL_REQUEST_TEMPLATE.md', 'PULL_REQUEST_TEMPLATE',]

documents = []


for rootPath, dirnames, filenames in os.walk('repo'):
    # skip directories in exclude_dir
    dirnames[:] = [d for d in dirnames if d not in exclude_dir]
    
    for file in filenames:
        _, file_extension = os.path.splitext(file)
        # skip files in exclude_files
        
        if file not in exclude_files and file_extension not in exclude_extensions and file not in exclude_filenames:
            file_path = os.path.join(rootPath, file)
            __loader__ = TextLoader(file_path,encoding='ISO-8859-1')
            documents.extend(__loader__.load())
            
print(f'Loaded {len(documents)} documents')
text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
docs = text_splitter.split_documents(documents)
            
            
for doc in docs:
    print(f'Embedding {doc.metadata["source"]}')
    source = doc.metadata['source']
    cleaned_source = '/'.join(source.split('/')[1:])
    doc.page_content = "FILE NAME: " + cleaned_source + \
        "\n###\n" + doc.page_content.replace('\u0000', '')

embeddings = OpenAIEmbeddings()

vector_store = SupabaseVectorStore.from_documents(
    docs,
    embeddings,
    client=superbase,
    table_name=os.environ.get("TABLE_NAME"),
    
)