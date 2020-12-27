import requests

uri = "http://127.0.0.1:5000/"

data = {
    'from_currency_list': ['EUR', 'USD', 'JPY'],
    'to_currency_list': ['USD', 'EUR'],
    'from_date': '2020-12-01',
    'to_date': '2020-12-07'
}

res = requests.post(uri, None, data)

print('Got results from server ' + res.text)