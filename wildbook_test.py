import requests

response = requests.get("http://localhost:84/api/test/helloworld/")
print(response.content)