import sqlite3
import pandas as pd
from sentence_transformers import SentenceTransformer
import pickle

# Load FAQ data
df = pd.read_csv('data/faqs.csv')

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Connect to DB
conn = sqlite3.connect('supportbot.db')
cursor = conn.cursor()

# Generate and store embeddings
for index, row in df.iterrows():
    question = row['question']
    answer = row['answer']
    embedding = model.encode([question])[0]
    embedding_blob = pickle.dumps(embedding)
    cursor.execute("INSERT INTO faqs (question, answer, embedding) VALUES (?, ?, ?)", (question, answer, embedding_blob))

conn.commit()
conn.close()

print("✅ FAQ data seeded successfully.")
