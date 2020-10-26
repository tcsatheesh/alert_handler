import os
alert_dict = {"id": "123456", "message": "something went wrong"}

import json
app_json = json.dumps(alert_dict)
print(app_json)

import requests
# see local.settings.json for end point details.
url = os.environ["ALERT_END_POINT"]
# url = "http://localhost:7071/api/AlertHandler"
x = requests.post(url, data=app_json)
print(x)