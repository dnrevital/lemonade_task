import requests

url = "http://localhost:5000/ask"

data = {
  "Question": "I moved to a new state and need to update my address.",
  "Customer_details": {"active_policies": "Car", "timezone": "America/LA"}
}

response = requests.post(url, json=data)

if response.status_code == 200:
  output_data = response.json()
  answer = output_data.get("answer")
  print(f"Selected Answer (Macro): {answer}")
else:
  print("Error: Request failed")
