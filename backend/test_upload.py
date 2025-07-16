import requests

url = "http://localhost:8000/analyze"
file_path = "sample_logs/test_log.txt"

with open(file_path, "rb") as file:
    files = {"file": (file_path, file)}
    response = requests.post(url, files=files)

print("Status Code:", response.status_code)
print("Response:", response.json())
