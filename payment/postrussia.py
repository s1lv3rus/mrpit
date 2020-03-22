import requests
import json

token = '5SHr_TxD2ZtxgxrlN6HI7Da_Jn4ajc5Y'
key = 'am9obl9rQGluYm94LnJ1OkdnNTU1NTU2'

host = "https://otpravka-api.pochta.ru"

request_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json;charset=UTF-8",
    "Authorization": "AccessToken " + token,
    "X-User-Authorization": "Basic " + key
}

path = "/1.0/tariff"

destination = {
    "index-from": "614000",
    "index-to": "555555",
    "mail-category": "ORDINARY",
    "mail-type": "POSTAL_PARCEL",
    "mass": 19000,
    "fragile": "false"
}
url = host + path

response = requests.post(url, headers=request_headers, data=json.dumps(destination))
decoder_json = json.loads(response.text)
value = str(decoder_json['total-rate']+decoder_json['total-vat'])
value = value[0:-2] + ' р.'
print("Status code: ", response.status_code)
print(decoder_json)
