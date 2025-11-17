import os

import requests

HTML_PATH = "./delme.html"
URL = os.getenv("FUNCTION_URL", "http://localhost:7071/api/html_to_docx/convert")

# 1. Read HTML file as string
with open(HTML_PATH, encoding="utf-8") as f:
    html_string = f.read()

# 2. Build payload
payload = {"html": html_string}

# 3. POST to your Function
response = requests.post(
    URL,
    headers={"Content-Type": "application/json"},
    json=payload,  # requests will json.dumps for you
)

print("Status:", response.status_code)
print("Response:", response.text)
