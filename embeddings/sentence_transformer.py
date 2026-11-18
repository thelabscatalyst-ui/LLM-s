
from sentence_transformers import SentenceTransformer

# Load pretrained embedding model
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

sentences = [
    "How do I learn Python programming?",
    "What is the best way to study Python?",
    "What is the capital of India?"
]

# Generate embeddings
embeddings = model.encode(sentences)

print("Embedding shape:", embeddings.shape)

# Calculate similarity
similarities = model.similarity(
    embeddings,
    embeddings
)

print("\nSimilarity Matrix:")
print(similarities)
