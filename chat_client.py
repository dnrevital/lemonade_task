import requests

def get_user_input():
  question = input("Enter your question: ")
  active_policies = input("Enter your active policies (e.g., Car, Other): ")
  timezone = input("Enter your timezone (e.g., America/LA): ")
  return question, active_policies, timezone

if __name__ == '__main__':
  url = "http://localhost:5000/ask"

  # Get user input
  question, active_policies, timezone = get_user_input()

  # Prepare request data
  data = {
    "Question": question,
    "Customer_details": {"active_policies": active_policies, "timezone": timezone}
  }

  response = requests.post(url, json=data)

  if response.status_code == 200:
    output_data = response.json()
    answer = output_data.get("answer")
    print(f"Selected Answer (Macro): {answer}")
  else:
    print("Error: Request failed")
