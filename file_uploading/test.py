import knime.scripting.io as knio
import os
import requests
import pandas as pd # Used for data frame

file_path = knio.flow_variables['File-Path']
file_size = os.path.getsize(file_path)

print("File size:", file_size, "bytes")


############PHASE 1 - GET REQUEST############
url_get = knio.flow_variables['Phase1-URL']

payload = {}
headers = {
  'Authorization': 'Basic tokenXXXX'
}

response_get = requests.request("GET", url_get, headers=headers, data=payload)



############PHASE 2 - PUT REQUEST############
url_put =  response_get.json()['url']
filename = knio.flow_variables['Filename']
filepath = knio.flow_variables['File-Path']


session = requests.Session()

payload = {}
files=[
  ('',(filename,open(filepath,'rb'),'image/png'))
]

file_size_payload = os.path.getsize(file_path)

headers_put = {
  'X-Amz-Acl': 'public-read',
  'Content-Length': str(file_size),
  'Host': 'tw-eu-bucket.s3-accelerate.amazonaws.com'
}

request = requests.Request('PUT', url_put, headers=headers_put, data=payload, files=files)

prepared_request = request.prepare()

prepared_request.headers['Content-Length'] = str(file_size)


#response = requests.put(url_put, headers=headers_put, data=payload, files=files)
response = session.send(prepared_request)


data_table = pd.DataFrame({'HTTP Status': [response.status_code], 'PH2-PUT-URL': [url_put]})

knio.output_tables[0] = knio.Table.from_pandas(data_table)


print('Put Request', request.headers)
print('Headers variable', headers)
print(str(file_size))
#print(prepared_request.body)
#print(url_get)
#print(url_put)
#print(response_get.text)
print(response.status_code)