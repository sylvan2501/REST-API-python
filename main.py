# API - application programming interface
# REST - REPRESENTATIONAL STATE TRANSFER
# -- it describes the way of communicating - in this case it is the internet
# GET - Retrieve data; POST - write NEW data to the server; PUT - update existing data
# POST vs. PUT - difference in idempotency & safe
# Being idempotent means the return value of an operation produces the same result each time the operation runs,
# and it can be repeated as many times as needed
# safe operations only read but never write.
# idempotent may mean both safe and not safe operations
# if an operation is idempotent it is not necessarily safe; yet a safe operation is always idempotent
# POST is not idempotent, and it is not safe
# PUT is idempotent, but it is not safe
# whereas GET is both idempotent and safe


import requests
import json

response = requests.get('https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow')
# print(response.json()['items'])

for data in response.json()['items']:
    if data['answer_count'] == 0:
        print(data['title'])
        print(data['link'])
    else:
        print('skipped')

