import os
import re
from typing import List, Optional, Tuple

from config import Config
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_core.documents import Document
from transformers import AutoModelForCausalLM, AutoTokenizer


class AIAssistant:
    def __init__(self, model_id: Optional[str] = None):
        self.model_id = model_id
        self.tokenizer = None
        self.model = None

        if not self.model_id:
            self.tokenizer = AutoTokenizer.from_pretrained(
                Config.TOKENIZER_PATH,
                trust_remote_code=True,
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                Config.LLM_PATH,
                device_map="auto",
                trust_remote_code=True,
            ).eval()

        else:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_id, trust_remote_code=True)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                device_map="auto",
                trust_remote_code=True,
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
        self.docs: List[Document] = []
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

    def add_context_to_article(
        self,
        text: str,
        file: str,
        init_level=2,
        header_name: str = None,
    ):
        level = init_level
        pattern = "#{level} (.*?)\n(.*?)(?=\n#{level} )"
        formatted_pattern = pattern.format(level="{" + str(level) + "}")
        parts = re.findall(formatted_pattern, text.strip(), re.DOTALL)
        if not parts:
            if ":" not in header_name:
                header_name = ""
            else:
                header_name = header_name.split(":")[-1].strip()

            articles = re.findall(r"\*\*(Art\. .*?)\*\*\n(.*?)(?=\*\*)", text, re.DOTALL)
            articles_context = [
                (article_name, "Contexte: " + header_name + "\n" + article_text)
                for article_name, article_text in articles
            ]
            for article_name, text in articles_context:
                text = text.strip()
                if not text:
                    continue
                clean_file_path = self.clean_data_folder + "/" + article_name + "_" + file
                with open(clean_file_path, "w", encoding="utf-8") as f:
                    f.write(text)

        for part_name, part_text in parts:
            self.add_context_to_article(
                text=part_text,
                header_name=part_name,
                init_level=level + 1,
                file=file,
            )

    def clean_data(self):
        if not os.path.exists(self.clean_data_folder):
            os.makedirs(self.clean_data_folder)

        for file in os.listdir(self.data_folder):
            if file in self.files_for_indexing:
                file_path = self.data_folder + "/" + file

                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()

                    pattern1 = re.compile(r"---.*?---", re.DOTALL)  # remove title and date
                    text = re.sub(pattern1, "", text)

                    # remove html content (simple approach, usually tables)
                    pattern3 = re.compile(r"<div.*</div>")
                    text = re.sub(pattern3, "", text)

                    pattern4 = re.compile(r"([:;])\n+")  # form paragraphs
                    text = re.sub(pattern4, lambda x: x.group(1) + " ", text)

                    self.add_context_to_article(text=text, file=file)

    def add_docs(self):
        for file in os.listdir(self.clean_data_folder):
            filename = os.fsdecode(self.clean_data_folder + "/" + file)
            self.docs.extend(TextLoader(filename).load())


class droitGPT:
    def __init__(self, ai_assistant: AIAssistant, vector_database: VectorDatabase):
        self.ai_assistant = ai_assistant
        self.searcher = vector_database.searcher
        self.system_prompt = (
            "Vous êtes un assistant spécialisé dans les codes juridiques français."
        )

    @staticmethod
    def parse_doc_metadata(doc: Document) -> str:
        source = doc.metadata["source"].split("/")[-1][:-3].split("_")
        name = source[0]
        code = source[1]
        return f"Code {code} - {name}"

    def get_relevant_docs(self, query: str, sim_threshold: float = 1.0) -> List[Document]:
        results = self.searcher.similarity_search_with_score(query)
        relevant_docs = [doc for doc, score in results if score <= sim_threshold]

        clean_relevant_docs = [
            Document(
                page_content=doc.page_content.split("\n", 1)[-1].strip(), metadata=doc.metadata
            )
            for doc in relevant_docs
        ]

        return clean_relevant_docs

    @staticmethod
    def parse_doc_content(text: str) -> str:
        text = text.replace("\n\n", "\n")
        return text[:550] + "..." if len(text) > 550 else text

    def parse_relevant_docs(self, relevant_docs: List[Document]) -> str:
        if not relevant_docs:
            return ""
        parsed = "".join(
            [
                f"{self.parse_doc_metadata(doc)} : {self.parse_doc_content(doc.page_content)}\n\n\n"
                for doc in relevant_docs
            ]
        )
        return "Vous pouvez également vérifier :\n\n" + parsed

    def enrich_input(self, input: str, relevant_docs: List[Document]) -> str:
        if not relevant_docs:
            return input

        contents = "\n".join([doc.page_content for doc in relevant_docs])
        return "\nÉtant donné que:\n" + contents + "\n" + input

    def format_history(self, history):
        new_history = []
        assert len(history) % 2 == 0, f"Answer to last question missing!"
        for i in range(0, len(history), 2):
            assert history[i]["speaker"] == "user"
            assert history[i + 1]["speaker"] == "bot"
            new_history.append((history[i]["text"], history[i + 1]["text"]))
        return new_history

    def answer(self, input: str, conversation: List[Tuple[str, str]]) -> Tuple[List[str], str]:

        relevant_docs = self.get_relevant_docs(input)
        input_enriched = self.enrich_input(input, relevant_docs)
        retrieved_docs_info = self.parse_relevant_docs(relevant_docs)

        answer, _ = self.ai_assistant.model.chat(
            self.ai_assistant.tokenizer,
            input_enriched,
            history=self.format_history(conversation),
            system=self.system_prompt,
        )
        return [answer], retrieved_docs_info


def droitGPT_init() -> droitGPT:
    ai_assistant = AIAssistant(model_id=Config.LLM_MODEL_ID if Config.DOWNLOAD_MODELS else None)
    embeddings = Embeddings(
        model_name=(
            Config.EMBEDDINGS_MODEL_NAME
            if Config.DOWNLOAD_MODELS
            else Config.EMBEDDINGS_MODEL_PATH
        )
    )
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
