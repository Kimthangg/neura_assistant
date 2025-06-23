import time
from langchain_community.embeddings import GPT4AllEmbeddings

# Đo thời gian bắt đầu
start_time = time.time()

# Khởi tạo embedder
embedder = GPT4AllEmbeddings(
    model_file="./all-MiniLM-L6-v2-Q8_0.gguf",
    n_threads=8,
)

# Chạy embed
vector = embedder.embed_query("Xin chào Cậu chủ")

# Đo thời gian kết thúc
end_time = time.time()

print(f"Số chiều vector: {len(vector)}")
print(f"Thời gian chạy: {end_time - start_time:.4f} giây")

start = time.time()
vector = embedder.embed_query("Tóm tắt email ngày 08/05 đến 10/05")
end = time.time()

print(f"Embedding mất: {end - start:.4f} giây")

