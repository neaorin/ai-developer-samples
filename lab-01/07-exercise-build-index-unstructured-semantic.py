# Exercitiu 07: Indexarea unor documente în Azure AI Search folosind Unstructured.io si Semantic Chunking
# Resurse utile:
# https://unstructured.io/
# https://python.langchain.com/docs/integrations/document_loaders/unstructured_file/
# https://python.langchain.com/docs/how_to/semantic-chunker/
# https://github.com/FullStackRetrieval-com/RetrievalTutorials/blob/main/tutorials/LevelsOfTextSplitting/5_Levels_Of_Text_Splitting.ipynb

pdf_folder_path = 'docs/'
index_name: str = 'langchain-vector-demo'


import os
from dotenv import load_dotenv
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings

# Configuration

load_dotenv(override=True)  # take environment variables from .env file
AZURE_OPENAI_API_ENDPOINT = os.getenv("AZURE_OPENAI_API_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME")
AZURE_SEARCH_API_ENDPOINT = os.getenv("AZURE_SEARCH_API_ENDPOINT")
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")

# Delete the index if it already exists
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient

client = SearchIndexClient(endpoint=AZURE_SEARCH_API_ENDPOINT, credential=AzureKeyCredential(AZURE_SEARCH_API_KEY))
index_list = client.list_index_names()

if index_name in index_list:
    # Delete the index if it exists
    client.delete_index(index_name)
    print(f"Index '{index_name}' deleted successfully.")
else:
    print(f"Index '{index_name}' does not exist.")

# Create embeddings and vector store instances
embeddings: AzureOpenAIEmbeddings = AzureOpenAIEmbeddings(
    azure_deployment=AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME,
    openai_api_version="2024-06-01",
    azure_endpoint=AZURE_OPENAI_API_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
)

vector_store: AzureSearch = AzureSearch(
    azure_search_endpoint=AZURE_SEARCH_API_ENDPOINT,
    azure_search_key=AZURE_SEARCH_API_KEY,
    index_name=index_name,
    embedding_function=embeddings.embed_query,
    additional_search_client_options={"retry_total": 4},
)

# Insert text and embeddings into vector store

# iterate over all PDF files in the folder, create embeddings and add them to the vector store
for pdf_file in os.listdir(pdf_folder_path):
    if not pdf_file.endswith('.pdf'):
        continue
    pdf_document_path = os.path.join(pdf_folder_path, pdf_file)
    print(f"Processing document: {pdf_document_path}")

    ### Inserati aici codul dvs
    ### / Inserati aici codul dvs
    break

print(f"Done adding documents to index {index_name}.")


