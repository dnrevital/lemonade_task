from flask import Flask, jsonify, request
from sentence_transformers import SentenceTransformer

def preprocess_text(text):
  return text.lower().strip()

def encode_customer_details(details):
  encoding = {"Car": 1, "Other": 0}
  return encoding.get(details.get("active_policies"), 0)


model_name = 'google-t5/t5-small'
model = SentenceTransformer(model_name)
app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
  # Get request data
  data = request.get_json()
  question = data.get('Question')
  customer_details = data.get('Customer_details')

  # Preprocess question text
  preprocessed_text = preprocess_text(question)

  # Encode customer details
  encoded_details = encode_customer_details(customer_details)

  # Combine preprocessed text and encoded details
  combined_data = f"{preprocessed_text} {encoded_details}"

  # Generate embedding for combined data
  embedding = model.encode(combined_data, convert_to_tensor=True)

  # Mock retrieval process (replace with actual retrieval logic using kNN)
  # This example assumes macro_1 is relevant to car insurance updates
  if encoded_details == 1:
    response = {"answer": "macro_1"}  # Macro specific to car insurance updates
  else:
    response = {"answer": "generic_update_macro"}  # Generic update macro

  # Return JSON response
  return jsonify(response)

if __name__ == '__main__':
  app.run(debug=True)
