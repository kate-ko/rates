The task was to write an app which gets POST requests with data:
For example:
{
    'from_currency_list': ['EUR', 'USD', 'JPY'],
    'to_currency_list': ['USD', 'EUR'],
    'from_date': '2020-12-01',
    'to_date': '2020-12-07'
}

Using API of EU Central Bank https://sdw-wsrest.ecb.europa.eu/help/ it return data in format:
For example:
 {"2020-12-01":{"EUR-USD":"1.1968","JPY-EUR":0.008,"JPY-USD":104.3783,"USD-EUR":0.8356}, "2020-12-02":{"EUR-USD":"1.2066"...

API only returns rates in relation to Euro.

I used Flask for a server.

