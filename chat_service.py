from flask import Flask, jsonify, request
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os

# Constants
EMBEDDING_SIZE = 512

def preprocess_text(text):
  return text.lower().strip()

def load_macros():
  # Read macros from JSON file
  with open("macros.json") as f:
    macros = json.load(f)
  return macros

def encode_macro(macro_text):
  model = SentenceTransformer('google-t5/t5-small')  # Load model (outside function for efficiency)
  macro_embedding = model.encode(preprocess_text(macro_text), convert_to_tensor=True)
  return macro_embedding.cpu().detach().numpy()

def update_faiss_index(macros, index):
  # Preprocess and encode all macros beforehand
  macro_embeddings = [encode_macro(macro["Content"]) for macro in macros]

  # Convert embeddings to a single numpy array
  macro_embeddings_np = np.stack(macro_embeddings)

  # Create a dictionary to map macros to their index in the Faiss index
  macro_to_index_map = {}

  # Add embeddings and store corresponding macro data
  for i, macro in enumerate(macros):
    index.add(np.expand_dims(macro_embeddings_np[i], axis=0))
    macro_to_index_map[i] = macro["Name"]  # Use macro name for identification

  # Update distances after adding all data points (using search)
  d, i = index.search(macro_embeddings_np, len(macro_embeddings_np))

  return macro_to_index_map


# Define Faiss index (outside function for persistence)
index = faiss.IndexFlatL2(EMBEDDING_SIZE)

# Load macros (replace with your actual data)
macros = load_macros()

# Update Faiss index with initial macros (do this once during startup)
macro_to_index_map = update_faiss_index(macros, index)

model_name = "google-t5/t5-small"
if not os.path.exists(f"{model_name}.h5"):  # Check if model file exists
  print(f"Downloading model {model_name}")
  model = SentenceTransformer(model_name)
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
  selected_macro = macro_index


  # Return JSON response
  return jsonify({"answer": macros[macro_index]["Id"]})


if __name__ == '__main__':
  app.run(debug=True)
