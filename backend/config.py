import os
import sys

from dotenv import load_dotenv

load_dotenv()


class Config:
    # We need to include the root directory in sys.path to ensure that we can
    # find everything we need when running in the standalone runtime.
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    if sys.path[0] != BASE_DIR:
        sys.path.insert(0, BASE_DIR)

    ENV = os.getenv("ENV")
    DEBUG = True if os.getenv("DEBUG") == "True" else False
    PORT = int(os.getenv("PORT"))
    PORT_FRONTEND = int(os.getenv("PORT_FRONTEND"))
    HOST = os.getenv("HOST")
    WORKERS_NUMBER = int(os.getenv("WORKERS_NUMBER"))

    # Set this to True once for downloading the models. Then switch to false
    DOWNLOAD_MODELS = True if os.getenv("DOWNLOAD_MODELS") == "True" else False
    EMBEDDINGS_MODEL_PATH = BASE_DIR + os.getenv("EMBEDDINGS_MODEL_PATH")
    LLM_PATH = BASE_DIR + os.getenv("LLM_PATH")
    TOKENIZER_PATH = BASE_DIR + os.getenv("TOKENIZER_PATH")

    LLM_MODEL_ID = os.getenv("LLM_MODEL_ID")

    EMBEDDINGS_MODEL_NAME = os.getenv("EMBEDDINGS_MODEL_NAME")

    VECTOR_DATABASE_PATH = BASE_DIR + os.getenv("VECTOR_DATABASE_PATH")
    DATA_FOLDER = BASE_DIR + os.getenv("DATA_FOLDER")
    CLEAN_DATA_FOLDER = BASE_DIR + os.getenv("CLEAN_DATA_FOLDER")
    FILES_FOR_INDEXING = os.getenv("FILES_FOR_INDEXING").split(",")
    DO_INDEXING = True if os.getenv("DO_INDEXING") == "True" else False
