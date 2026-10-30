import os
import time
from network_tools import NetworkToolsAPI, EmbedModels

api_key = "API_KEY"  # замените на ваш API ключ
client = NetworkToolsAPI(api_key=api_key)

test_texts = [
    "Hello from NetworkTools Embed!",
    "Тестирование семантического поиска и эмбеддингов",
    "FastAPI and Python RAG architecture"
]

print("=== 1. Тест всех моделей из EmbedModels через client.embed_api ===")
for embed_mode in EmbedModels:
    start_ts = time.time()
    try:
        res = client.embed_api(
            texts=test_texts,
            model=embed_mode,
            input_type="search_document"
        )
        elapsed_ms = int((time.time() - start_ts) * 1000)
        dim = len(res[0]) if len(res) > 0 else 0
        print(
            f"[{embed_mode}] Успех: векторов={len(res)}, dim={dim}, "
            f"cost={res.cost:.6f} Credit, время={elapsed_ms} ms"
        )
    except Exception as e:
        print(f"[{embed_mode}] Ошибка: {e}")

print("\n=== 2. Тест совместимости с LangChain OpenAIEmbeddings ===")
try:
    from langchain_openai import OpenAIEmbeddings

    judge_embeddings = OpenAIEmbeddings(
        model=EmbedModels.embed_v5_0_fast,
        base_url=f"{client.api_url}/v1",
        api_key=api_key,
    )
    query_vec = judge_embeddings.embed_query("Как работает векторный поиск?")
    doc_vecs = judge_embeddings.embed_documents(test_texts)
    print(f"[OpenAIEmbeddings] Query vector dim: {len(query_vec)}, Docs count: {len(doc_vecs)}")
except ImportError:
    print("Пакет langchain_openai не установлен (pip install langchain-openai), пропуск теста LangChain.")
except Exception as e:
    print(f"[OpenAIEmbeddings] Ошибка: {e}")
