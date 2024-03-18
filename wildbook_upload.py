import requests

url = "http://localhost:84/api/upload/image/"
files = {'image': open('sample_seals/DSC_0021.jpg', 'rb')}
response = requests.post(url, files=files)

print(response.text)  # This should print the gid of the uploaded image