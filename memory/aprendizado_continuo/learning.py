import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

modelo = SentenceTransformer("all-MiniLM-L6-v2")  # Modelo leve e eficiente
dim = 384  # Dimensão do embedding
index = faiss.IndexFlatL2(dim)  # Índice FAISS para buscas eficientes

def adicionar_memoria(texto):
    embedding = modelo.encode([texto])
    index.add(np.array(embedding, dtype=np.float32))

def buscar_memoria(query):
    embedding = modelo.encode([query])
    D, I = index.search(np.array(embedding, dtype=np.float32), k=5)  # Retorna os 5 mais similares
    return I
