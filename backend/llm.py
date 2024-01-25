from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain.prompts import PromptTemplate
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
import os

from preprocess import create_docs, clean_data

DO_INDEXING = False
MAX_NEW_TOKENS = 8192
MODEL_ID = "Qwen/Qwen-1_8B-Chat-Int4"
TEMPLATE = """
Vous êtes un assistant spécialisé en codes juridiques français.

Utilisez les informations suivantes pour répondre à la question:
{context}

Question: {input}

Réponse: En utilisant le contexte, répondre à la question.
"""

def llm_init():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID,device_map="auto",trust_remote_code=True)
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=MAX_NEW_TOKENS)
    hf = HuggingFacePipeline(pipeline=pipe)

    prompt = PromptTemplate.from_template(TEMPLATE)
    document_chain = create_stuff_documents_chain(hf, prompt)

    embeddings_model_id = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_id)

    faiss_index_path = "./faiss_index"
    if os.path.exists(faiss_index_path) and os.path.isdir(faiss_index_path) and not DO_INDEXING:
        vector = FAISS.load_local(faiss_index_path, embeddings)
    else:
        data_folder = "data"
        relevant_files = ["travail.md", "education.md", "electoral.md"]
        clean_data_folder_name = "clean_data"
        clean_data(data_folder, relevant_files, clean_data_folder_name)

        docs = create_docs(clean_data_folder_name)
        vector = FAISS.from_documents(docs, embeddings)
        vector.save_local("faiss_index")

    retrieval_chain = create_retrieval_chain(vector.as_retriever(), document_chain)
    return retrieval_chain

def get_answer_from_response(response):
    return response["answer"]

if __name__ == "__main__":
    llm_init()