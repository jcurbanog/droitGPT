from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document

import os
import re


def clean_data(data_folder, relevant_files, clean_data_folder_name):
    if not os.path.exists(clean_data_folder_name):
            os.makedirs(clean_data_folder_name)

    for file in os.listdir(data_folder):
        if file in relevant_files:
            file_path = data_folder + "/" + file 
            clean_file_path = clean_data_folder_name + "/clean_" + file
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


def create_docs(clean_data_folder_name):
    documents = []
    for file in os.listdir(clean_data_folder_name):
        filename = os.fsdecode(clean_data_folder_name + "/" + file)
        loader = TextLoader(filename)
        documents += loader.load()

    docs = []
    for doc in documents:
        texts = re.split('\n+', doc.page_content)
        texts = [text for text in texts if text]
        for text in texts:
            docs.append(Document(page_content = text, metadata=doc.metadata))
    return docs


