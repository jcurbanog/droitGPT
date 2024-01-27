import os
import re
from typing import List, Tuple

from config import Config
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_core.documents import Document
from transformers import AutoModelForCausalLM, AutoTokenizer


class AIAssistant:
    def __init__(self, model_id: str):
        self.model_id = model_id
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id, device_map="auto", trust_remote_code=True
        ).eval()


class Embeddings:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs={"device": "cuda"},
        )


class VectorDatabase:
    def __init__(
        self,
        embeddings: Embeddings,
        vector_db_path: str,
        data_folder: str,
        clean_data_folder: str,
        files_for_indexing: List[str],
    ):
        self.embeddings_model = embeddings.model
        self.vector_db_path = vector_db_path
        self.data_folder = data_folder
        self.clean_data_folder = clean_data_folder
        self.files_for_indexing = files_for_indexing
        self.searcher = None
        self.docs = []
        self.create_or_load()

    def create_or_load(self):
        if (
            os.path.exists(self.vector_db_path)
            and os.path.isdir(self.vector_db_path)
            and not Config.DO_INDEXING
        ):
            self.searcher = FAISS.load_local(
                self.vector_db_path,
                self.embeddings_model,
                distance_strategy=DistanceStrategy.COSINE,
                normalize_L2=True,
            )
        else:
            self.clean_data()
            self.add_docs()
            self.searcher = FAISS.from_documents(
                self.docs,
                self.embeddings_model,
                distance_strategy=DistanceStrategy.COSINE,
                normalize_L2=True,
            )
            self.searcher.save_local(self.vector_db_path)
        return self

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
                    pattern1 = re.compile(r"---.*?---", re.DOTALL)  # remove title and date
                    text = re.sub(pattern1, "", text)

                    pattern2 = re.compile(r"#+.*\n")  # remove Markdown titles
                    text = re.sub(pattern2, "", text)

                    pattern2 = re.compile(r"\*\*.*\*\*")  # remove Article titles
                    text = re.sub(pattern2, "", text)

                    pattern3 = re.compile(
                        r"<div.*</div>"
                    )  # remove html content (simple approach, usually tables)
                    text = re.sub(pattern3, "", text)

                    pattern4 = re.compile(r"([:;])\n+")  # form paragraphs
                    text = re.sub(pattern4, lambda x: x.group(1) + " ", text)

                    with open(clean_file_path, "w", encoding="utf-8") as f:
                        f.write(text)

    def add_docs(self):
        documents: List[Document] = []
        for file in os.listdir(self.clean_data_folder):
            filename = os.fsdecode(self.clean_data_folder + "/" + file)
            loader = TextLoader(filename)
            documents += loader.load()

        for doc in documents:
            texts = re.split("\n+", doc.page_content)
            texts = [text for text in texts if text]
            for text in texts:
                if self.is_text_relevant(text):
                    self.docs.append(Document(page_content=text, metadata=doc.metadata))

    @staticmethod
    def is_text_relevant(text: str):
        """Simple way to filter out noise"""
        return len(text) >= 100


class droitGPT:
    def __init__(self, ai_assistant: AIAssistant, vector_database: VectorDatabase):
        self.ai_assistant = ai_assistant
        self.searcher = vector_database.searcher
        self.system_prompt = (
            "Vous êtes un assistant spécialisé dans les codes juridiques français."
        )

    def get_additional_info(self, query: str, sim_threshold: float = 1.0) -> str:
        results = self.searcher.similarity_search_with_score(query)
        relevant_docs = [doc for doc, score in results if score <= sim_threshold]
        if not relevant_docs:
            return ""
        return "\n".join([doc.page_content for doc in relevant_docs])

    def enrich_input(self, input: str):
        additional_info = self.get_additional_info(query=input)
        if not additional_info:
            return input
        return input + "\nÉtant donné que:\n" + additional_info + "\n"

    def format_history(self, history):
        new_history = []
        for qa in history:
            new_history.append((qa["user"], qa["assistant"]))
        return new_history

    def answer(
        self, input: str, conversation: List[Tuple[str, str]], is_multiple: bool = False
    ) -> List[str]:

        input_enriched = self.enrich_input(input)

        n = 3 if is_multiple else 1
        answers = []
        for _ in range(n):
            answer, _ = self.ai_assistant.model.chat(
                self.ai_assistant.tokenizer,
                input_enriched,
                history=self.format_history(conversation),
                system=self.system_prompt,
            )
            answers.append(answer)
        return answers


def droitGPT_init() -> droitGPT:
    ai_assistant = AIAssistant(model_id=Config.LLM_MODEL_ID)
    embeddings = Embeddings(model_name=Config.EMBEDDINGS_MODEL_NAME)
    vector_database = VectorDatabase(
        embeddings=embeddings,
        vector_db_path=Config.VECTOR_DATABASE_PATH,
        data_folder=Config.DATA_FOLDER,
        clean_data_folder=Config.CLEAN_DATA_FOLDER,
        files_for_indexing=Config.FILES_FOR_INDEXING,
    )
    assistant = droitGPT(
        ai_assistant=ai_assistant,
        vector_database=vector_database,
    )
    return assistant


if __name__ == "__main__":
    droitGPT_init()
