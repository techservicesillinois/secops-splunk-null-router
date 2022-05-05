#!/usr/bin/env python

import json
import base64
import requests
import os

file_contents = open('soar_null_router.tgz', 'rb').read()
encoded_contents = base64.b64encode(file_contents)
payload = {'app': encoded_contents.decode('ascii')}
headers = {'ph-auth-token': os.environ['SOAR_TOKEN']}
result = requests.post('https://automate-illinois.soar.splunkcloud.com/rest/app',
                headers=headers,
                data=json.dumps(payload))

print(result.text)

# curl 'https://automate-illinois.soar.splunkcloud.com/apps/' \
#   -H 'Accept: application/json, text/plain, */*' \
#   -H 'Accept-Language: en-US,en;q=0.9' \
#   -H 'Cache-Control: no-cache, no-store, must-revalidate' \
#   -H 'Connection: keep-alive' \
#   -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
#   -H 'Cookie: telemetry_data=1; apt.uid=AP-7SBC7L5BZ8ML-2-1649357679214-92129465.0.2.8220eb14-1881-43da-96f4-5d2bf2070975; csrftoken=FOO; sessionid=sgchjtlls9wimtdy3sd29s9xe46oy6t5; token_key=FOO; experience_id=7c043ff9-f6da-65c0-82dd-f0b1781f5def' \
#   -H 'DNT: 1' \
#   -H 'Origin: https://automate-illinois.soar.splunkcloud.com' \
#   -H 'Pragma: no-cache' \
#   -H 'Referer: https://automate-illinois.soar.splunkcloud.com/apps?search=null' \
#   -H 'Sec-Fetch-Dest: empty' \
#   -H 'Sec-Fetch-Mode: cors' \
#   -H 'Sec-Fetch-Site: same-origin' \
#   -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36' \
#   -H 'X-CSRFToken: FOO' \
#   -H 'sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'sec-ch-ua-platform: "Windows"' \
#   -H 'sec-gpc: 1' \
#   --data-raw 'update=204&version=2.0.3&forced_installation=false' \
#   --compressed

# Form Data: update=204&version=2.0.3&forced_installation=false