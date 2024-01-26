import os
import sys 

class Config:
    # We need to include the root directory in sys.path to ensure that we can
    # find everything we need when running in the standalone runtime.
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    if sys.path[0] != BASE_DIR:
        sys.path.insert(0, BASE_DIR)

    MAX_NEW_TOKENS = 8192
    MODEL_ID = "Qwen/Qwen-1_8B-Chat-Int8"

    EMBEDDINGS_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

    VECTOR_DATABASE_PATH = BASE_DIR + "/faiss_index"
    DATA_FOLDER = BASE_DIR + "/data"
    CLEAN_DATA_FOLDER = BASE_DIR + "/clean_data"
    FILES_FOR_INDEXING = ["travail.md", "education.md", "electoral.md"]
    DO_INDEXING = True
    """
    Set this to True to force indexing docs to database
    """