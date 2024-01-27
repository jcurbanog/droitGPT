# droitGPT

AI assistant awared of French Legal Codes

# Corpus

French Legal Codes in markdown format

- https://www.cri.ensmp.fr/people/silber/nlp/codes.tar.gz

# Methodology

- Research for open-source LLM/GPT models taking into account the following limitations:

  - 4GB GPU (GeForce RTX 3050 Ti Mobile)
  - Pre-trained in French corpus

- Research for open-source Vector Databases technologies that allow efficient similarity search

- Research for open-source Sentence Transformer models

  - 4GB GPU (GeForce RTX 3050 Ti Mobile)
  - Pre-trained in French corpus

- Research for tools that allow create prototypes for context-aware applications

# Technologies

- LLM: [Qwen/Qwen-1_8B-Chat-Int8](https://huggingface.co/Qwen/Qwen-1_8B-Chat-Int8)

  - model proposed by Alibaba Cloud
  - AI assistant trained with alignment techniques
  - Int4 quantized version (low-cost deployment)
  - 8192 context length
  - Friendly to multiple languages

- Vector Database: [FAISS](https://github.com/facebookresearch/faiss)

  - Efficient similarity search
  - Supported by CUDA

- Sentence Transformer: [paraphrase-multilingual-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2#sentence-transformersparaphrase-multilingual-minilm-l12-v2)

  - Best performance in the context of multilingual models given the constrain of GPU RAM memory

- Prototype Framework: [Langchain](https://python.langchain.com/docs/get_started/introduction)
  - Allows development of applications powered by language models

# Limitations

- LLM and Sentence Transformer model: The hardware limitations do not allow the use of much 'larger' language models
  - The model may not properly reply in French (as requested).
  - The quality of the requested context may not be good.

# TODO

- Prompt Engineering for improving further more the performance
- Use a much larger language model pre-trained in a much larger French corpus
- Use Ollama embeddings model for FAISS

# Set up

- Python 3.10 or higher required
- [Install Node.JS](https://learn.microsoft.com/en-us/windows/dev-environment/javascript/nodejs-overview) 18.13 or higher
- Set up a python virtual environment `python -m venv venv && source venv/bin/activate`
- Do `cat backend/requirements.txt | xargs -n 1 pip install`. if some packages could not be installed due to the version, do it manually
- Finally, after leaving the `venv` using `deactivate`, you can run the app at the root directory through `make run`

# Other Resources

- [LangChain Quickstart](https://python.langchain.com/docs/get_started/quickstart)

- [LangChain - FAISS Integration](https://python.langchain.com/docs/integrations/vectorstores/faiss)

- [LangChain - HuggingFace LLM Integration](https://python.langchain.com/docs/integrations/llms/huggingface_pipelines)

- [LangChain - Sentence Transformers Integration](https://python.langchain.com/docs/integrations/text_embeddingsentence_transformers)
