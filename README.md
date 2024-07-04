# RagPanel
## Usage
install [cardinal](https://github.com/the-seeds/cardinal.git)

install [redis](https://github.com/redis/redis.git) and start

create a .env
```
# imitater or openai
OPENAI_BASE_URL=http://localhost:8000/v1
OPENAI_API_KEY=0

# models
DEFAULT_EMBED_MODEL=text-embedding-ada-002
DEFAULT_CHAT_MODEL=gpt-3.5-turbo
HF_TOKENIZER_PATH=01-ai/Yi-6B-Chat

# text splitter
DEFAULT_CHUNK_SIZE=300
DEFAULT_CHUNK_OVERLAP=100

# storages
STORAGE=redis
SEARCH_TARGET=content
REDIS_URI=redis://localhost:6379
ELASTICSEARCH_URI=http://localhost:9001

# vectorstore
VECTORSTORE=chroma
CHROMA_PATH=./chroma
MILVUS_URI=http://localhost:19530
MILVUS_TOKEN=0
```

Run `python launch.py`

## Note
当前demo只能选择某一操作进行，优先级insert > search > delete > replace，高优先级内容为空时才会进行低优先级操作，后续会进行调整
