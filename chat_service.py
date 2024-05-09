from flask import Flask, jsonify, request
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os

# Constants
EMBEDDING_SIZE = 768

def preprocess_text(text):
  return text.lower().strip()

def load_macros():
  # Read macros from JSON file
  with open("macros.json") as f:
    macros = json.load(f)
  return macros

def encode_macro(macro_text):
  macro_embedding = model.encode(preprocess_text(macro_text), convert_to_tensor=True)
  return macro_embedding.cpu().detach().numpy()

def update_faiss_index(macros, index):
  # Preprocess and encode all macros beforehand
  macro_embeddings = []
  for macro in macros:
    macro_texts = ' '.join([macro["Content"],
                           macro["Description"],
                           macro["Id"],
                           macro["Name"],
                           macro["Intent category"]])
    macro_embedding = encode_macro(macro_texts)
    macro_embeddings.append(macro_embedding)

  # Convert embeddings to a single numpy array
  macro_embeddings_np = np.stack(macro_embeddings)

  # Add embeddings and store corresponding macro data
  for i, macro in enumerate(macros):
    index.add(np.expand_dims(macro_embeddings_np[i], axis=0))

model_name = "sentence-transformers/sentence-t5-base"  # The model name from the warning
model = SentenceTransformer(model_name)

# Define Faiss index (outside function for persistence)
index = faiss.IndexFlatL2(EMBEDDING_SIZE)

# Load macros (replace with your actual data)
macros = load_macros()

# Update Faiss index with initial macros (do this once during startup)
update_faiss_index(macros, index)

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
  # Get request data
  data = request.get_json()
  question = data.get('Question')
  customer_details = data.get('Customer_details')

  # Preprocess question text and customer details
  preprocessed_text = preprocess_text(question)

  # Combine preprocessed text and encoded details
  input_text = preprocessed_text + customer_details.get("active_policies", "") + " " + customer_details.get("timezone", "")
  input_embedding = model.encode(input_text, convert_to_tensor=True).cpu().detach().numpy()

  # Search for nearest neighbors in Faiss index
  d, i = index.search(input_embedding.reshape(1, -1), 1)  # Search for 1 nearest neighbor

  # Retrieve macro name associated with the nearest neighbor
  macro_index = i.flatten()[0]


  # Return JSON response
  return jsonify({"answer": macros[macro_index]["Id"]})


if __name__ == '__main__':
  app.run(debug=True)
