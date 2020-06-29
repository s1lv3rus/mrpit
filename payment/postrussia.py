import datetime

import requests
import json

# properties
protocol = "https://"
host = "otpravka-api.pochta.ru"
token = "5SHr_TxD2ZtxgxrlN6HI7Da_Jn4ajc5Y"
key = "am9obl9rQGluYm94LnJ1OkdnNTU1NTU2"

request_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json;charset=UTF-8",
    "Authorization": "AccessToken " + token,
    "X-User-Authorization": "Basic " + key
}

path = "/1.0/user/backlog"

new_orders = [{
    "postoffice-code": "614961",
    "tel-address": 89678300518,
    "surname": "Васильев",
    "given-name": "Олег",
    "mail-direct": 643,
    "address-type-to": "DEFAULT",
    "index-to": 416368,
    "region-to": "Астраханская",
    "place-to": "Посёлок Товарный",
    "street-to": "Набережная",
    "house-to": "82",
    "mass": 2500,
    "mail-category": "ORDINARY",
    "mail-type": "ONLINE_PARCEL",
    "order-num": ""
}]

url = protocol + host + path

response = requests.put(
    url, headers=request_headers, data=json.dumps(new_orders)
)
with open('russian_post_delivery_log.txt', 'a') as outFile:
    outFile.write('\nВремя отправки:{}, Код: {} Текст: {}'
                  .format(datetime.datetime.now(), response.status_code, response.text))
