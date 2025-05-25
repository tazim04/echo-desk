import requests

API_URL = "http://localhost:8000/chat"
session_id = "test-session-1"

def send_message(message):
    response = requests.post(API_URL, json={
        "session_id": session_id,
        "message": message
    })

    print(f"> Client: {message}")
    try:
        print(f"Echo: {response.json().get('response')}")
    except Exception:
        print("Server returned an invalid response:")
        print(f"Status code: {response.status_code}")
        print("Raw response:")
        print(response.text)
    print("-" * 40)


# Simulate a conversation
send_message("Hi, my name is John Doe, and I would like to book an appointment for May 24th, at 9:10am")
send_message("Yes sorry aobut that, my phone number is 613-111-1111, and sure, the reason for my appointment is that I have a tummy ache.")
send_message("Thats correct, thank you.")
