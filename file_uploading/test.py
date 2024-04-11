#import knime.scripting.io as knio

# This example script creates an output table containing randomly drawn integers using numpy and pandas.
import requests
import os

file_path = r'C:\Users\filipe.pedro\Downloads\File_0.png'
file_size = os.path.getsize(file_path)

print("File size:", file_size, "bytes")

url_get = f"https://ops.exsyn.com/projects/api/v1/pendingfiles/presignedurl.json?fileName=File_0.png&fileSize={file_size}"

payload = {}
headers = {
'Authorization': 'Basic teamwork_token'
}

response_get = requests.request("GET", url_get, headers=headers, data=payload)

url_put = response_get.json()['url']
print(url_put)
filename = 'File_0.png'
filepath = file_path

payload = {}
files=[
('',(filename,open(filepath,'rb'),'image/png'))
]
headers = {
'X-Amz-Acl': 'public-read',
'Content-Length': str(file_size)
}

response = requests.request("PUT", url_put, headers=headers, data=payload, files=files)

print(response.status_code)

#print(response_get.text)
print(response.text)