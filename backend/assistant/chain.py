import os
import re
from typing import List, Tuple

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage



MAX_NEW_TOKENS = 8192
MODEL_ID = "Qwen/Qwen-1_8B-Chat-Int8"

EMBEDDINGS_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

VECTOR_DATABASE_PATH = "./faiss_index"
DATA_FOLDER = "data"
CLEAN_DATA_FOLDER = "clean_data"
FILES_FOR_INDEXING = ["travail.md", "education.md", "electoral.md"]
DO_INDEXING = False
"""
Set this to True to force indexing docs to database
"""


class LLMPipelineFactory:
    def __init__(self, model_id: str, max_new_tokens: int):
        self.model_id = model_id
        self.max_new_tokens = max_new_tokens
        
    def create(self) -> HuggingFacePipeline:
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id, 
                                                       trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_id,
                                                          device_map="auto",
                                                          trust_remote_code=True)
        pipe = pipeline("text-generation", 
                        model=self.model, 
                        tokenizer=self.tokenizer, 
                        max_new_tokens=self.max_new_tokens)
        return HuggingFacePipeline(pipeline=pipe)

class EmbeddingsFactory:
    def __init__(self, model_name: str):
        self.model_name = model_name
        
    def create(self) -> HuggingFaceEmbeddings:
        return HuggingFaceEmbeddings(model_name=self.model_name)
    
class VectorDatabase:
    def __init__(self, embeddings: HuggingFaceEmbeddings, 
                 storage_path: str, 
                 data_folder: str, 
                 clean_data_folder: str, 
                 files_for_indexing: List[str]):
        self.embeddings = embeddings
        self.storage_path = storage_path
        self.data_folder = data_folder
        self.clean_data_folder = clean_data_folder
        self.files_for_indexing = files_for_indexing
        self.db = None
        self.docs = []
        

    def create_or_load(self):
        if os.path.exists(self.storage_path) and os.path.isdir(self.storage_path) and not DO_INDEXING:
            self.db = FAISS.load_local(self.storage_path, self.embeddings)
        else:
            self.clean_data()
            self.add_docs()
            self.db = FAISS.from_documents(self.docs, self.embeddings)
            self.db.save_local(self.storage_path)
    
    
    def clean_data(self):
        if not os.path.exists(self.clean_data_folder):
                os.makedirs(self.clean_data_folder)

        for file in os.listdir(self.data_folder):
            if file in self.files_for_indexing:
                file_path = self.data_folder + "/" + file 
                clean_file_path = self.clean_data_folder + "/clean_" + file
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()

                    # Transform textdata with re here
                    pattern1 = re.compile(r'---.*?---', re.DOTALL) # remove title and date 
                    text = re.sub(pattern1, '', text)
                    
                    pattern2 = re.compile(r'#+.*\n') # remove Markdown titles
                    text = re.sub(pattern2, '', text)

                    pattern2 = re.compile(r'\*\*.*\*\*') # remove Article titles
                    text = re.sub(pattern2, '', text)

                    pattern3 = re.compile(r'<div.*</div>') # remove html content (simple approach, usually tables)
                    text = re.sub(pattern3, '', text)

                    pattern4 = re.compile(r'([:;])\n+') # form paragraphs
                    text = re.sub(pattern4,lambda x: x.group(1) + ' ', text)

                    with open(clean_file_path, "w", encoding="utf-8") as f:
                        f.write(text)


    def add_docs(self):
        documents : List[Document] = []
        for file in os.listdir(self.clean_data_folder):
            filename = os.fsdecode(self.clean_data_folder + "/" + file)
            loader = TextLoader(filename)
            documents += loader.load()

        docs = []
        for doc in documents:
            texts = re.split('\n+', doc.page_content)
            texts = [text for text in texts if text]
            for text in texts:
                docs.append(Document(page_content = text, metadata=doc.metadata))
        self.docs = docs

class droitGPT:
    def __init__(
            self, 
            llm_pipe: HuggingFacePipeline, 
            vector_database: VectorDatabase):
        self.llm_pipe = llm_pipe
        self.retriever = vector_database.db.as_retriever()
        self.retrieval_chain = None
    
    def get_prompt_context(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            # MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
        ])
    
    def get_prompt_answer(self):
        return ChatPromptTemplate.from_messages([
            ("system", "Vous êtes un assistant spécialisé en codes juridiques français."),
            # ("system", "Voici la conversation entre vous et l'utilisateur:\n"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("system", "Information pour répondre au question de l'utilisateur:\n{context}"),
            ("user", "{input}"),
            ("system", "Réponse en français:"),
        ])
    
    def create(self):
        prompt_context = self.get_prompt_context()
        retriever_chain = create_history_aware_retriever(self.llm_pipe, self.retriever, prompt_context)

        prompt_answer = self.get_prompt_answer()
        document_chain = create_stuff_documents_chain(self.llm_pipe, prompt_answer)
        
        retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)
        self.retrieval_chain = retrieval_chain

    @staticmethod
    def build_chat_history(conversation: List[Tuple[str,str]]) -> List[HumanMessage|AIMessage]:
        return [HumanMessage(content=speaker_text["text"]) if speaker_text["speaker"] == "user" else AIMessage(content=speaker_text["text"]) for speaker_text in conversation]

    def answer(self, input: str, conversation: List[Tuple[str,str]], is_multiple: bool = False) -> List[str]:
        assert self.retrieval_chain, f"Chain has not been created yet!"
        
        chat_history = self.build_chat_history(conversation)
        n = 3 if is_multiple else 1
        outputs = [self.retrieval_chain.invoke({"chat_history": chat_history,"input": input}) for _ in range(n)]
        answers = [o["answer"] for o in outputs]
        return answers


def droitGPT_init() -> droitGPT:
    llm_pipe_factory = LLMPipelineFactory(model_id = MODEL_ID, max_new_tokens = MAX_NEW_TOKENS)
    llm_pipe = llm_pipe_factory.create()

    embeddings_factory = EmbeddingsFactory(model_name = EMBEDDINGS_MODEL_NAME)
    embeddings = embeddings_factory.create()

    vector_database = VectorDatabase(embeddings=embeddings, 
                                     storage_path=VECTOR_DATABASE_PATH, 
                                     data_folder=DATA_FOLDER, 
                                     clean_data_folder=CLEAN_DATA_FOLDER, 
                                     files_for_indexing=FILES_FOR_INDEXING)
    vector_database.create_or_load()

    conversational_retrieval_chain = droitGPT(llm_pipe=llm_pipe, vector_database=vector_database)
    conversational_retrieval_chain.create()

    return conversational_retrieval_chain


if __name__ == "__main__":
    droitGPT_init()