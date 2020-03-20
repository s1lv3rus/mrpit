import requests
import json

host = ""
response = requests.post(
    host,
    json={
        "version": "1.0",
        "dateExecute": "2019-04-01",
        "senderCityPostCode": "614000",

        "receiverCityPostCode": "443000",
        "currency": "RUB",
        "tariffList":
            [
                {
                    "id": 1
                },
                {
                    "id": 8
                },
            ],
        "goods":
            [
                {
                    "weight": "1",
                    "length": "30",
                    "width": "30",
                    "height": "30"
                }
            ],
        "services":
            [
                {
                    "id": 2,
                    "param": 1000
                }
            ]
    })

decoder_json = json.loads(response.text)
print(decoder_json['result'][0]['result']['price'])
