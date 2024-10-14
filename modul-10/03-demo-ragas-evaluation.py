# Demo 03: Evaluarea performanței unui RAG chain folosind RAGAS 
# https://github.com/explodinggradients/ragas

index_name: str = 'langchain-vector-demo'

import os
from pprint import pprint
from dotenv import load_dotenv
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings
from ragas import evaluate
from datasets import Dataset


# Configuration

load_dotenv(override=True)  # take environment variables from .env file
AZURE_OPENAI_API_ENDPOINT = os.getenv("AZURE_OPENAI_API_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME")
AZURE_SEARCH_API_ENDPOINT = os.getenv("AZURE_SEARCH_API_ENDPOINT")
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")

AZURE_OPENAI_API_VERSION = "2024-06-01"

# Create embeddings and vector store instances
embeddings: AzureOpenAIEmbeddings = AzureOpenAIEmbeddings(
    azure_deployment=AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME,
    openai_api_version=AZURE_OPENAI_API_VERSION,
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

# Create a Langchain LLM using Azure Open AI
# https://python.langchain.com/docs/integrations/chat/azure_chat_openai/

from langchain_openai import AzureChatOpenAI

llm = AzureChatOpenAI(
    azure_endpoint=AZURE_OPENAI_API_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    azure_deployment=AZURE_OPENAI_CHAT_DEPLOYMENT_NAME, 
    api_version=AZURE_OPENAI_API_VERSION,
    temperature=0,
    max_tokens=150,
    timeout=None,
    max_retries=2
)


# Creating a Langchain RAG chain for answering questions
# https://python.langchain.com/docs/tutorials/rag

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
retriever = vector_store.as_retriever(search_type="similarity", k=3, score_threshold=0.80)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


# Evaluate the RAG chain using RAGAS
from ragas.metrics import (
    answer_relevancy,
    faithfulness,
    context_recall,
    context_precision
)

# evaluate on a single question
question = "Ce profit consolidat a avut banca în 2024 S1?"
ground_truth = "2146 milioane lei"

response = rag_chain.invoke({"input": question})
print(response)

data_samples = {
    'question': [question],
    'ground_truth': [ground_truth],
    'answer': [response['answer']],
    'contexts': [[c.page_content for c in response['context']]],
}
dataset = Dataset.from_dict(data_samples)

eval_results = evaluate(
    dataset,
    llm=llm,
    embeddings=embeddings,
    metrics=[
        context_precision,
        faithfulness,
        answer_relevancy,
        context_recall,
    ]
)

print(eval_results)

