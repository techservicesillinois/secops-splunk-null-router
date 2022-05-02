#!/usr/bin/env python

import json
import base64
import requests
import os

file_contents = open('soar_null_router.tgz', 'rb').read()
encoded_contents = base64.b64encode(file_contents)
payload = {'app': encoded_contents.decode('utf-8')}
headers = {'ph-auth-token': os.environ['SOAR_TOKEN']}
result = requests.post('https://automate-illinois.soar.splunkcloud.com/rest/app',
                headers=headers,
                data=json.dumps(payload))

print(result.text)
