from sentence_transformers import SentenceTransformer
import torch
import os
base_path = "./services/embedding_model/models--hiieu--halong_embedding/snapshots"
snapshots = os.listdir(base_path)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")
if not snapshots:
    model_embed = SentenceTransformer("hiieu/halong_embedding", cache_folder = "./", device=device) 
else:
    model_path = os.path.join(base_path, snapshots[0])
    model_embed = SentenceTransformer(model_path, device=device)
    
def embedding_text(texts):
    """
    Dịch văn bản thành các vector nhúng sử dụng mô hình GPT4All.

    Parameters:
        texts (list): Danh sách các văn bản cần dịch.

    Returns:
        list: Danh sách các vector nhúng tương ứng với các văn bản đầu vào.
    """
    if not texts:
        return []

    # Dịch văn bản thành vector nhúng
    embeddings = model_embed.encode(texts)
    
    return embeddings.tolist()
