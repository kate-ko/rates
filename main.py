import requests
from datetime import datetime, timedelta
from xml.dom.minidom import parse, parseString

# returs dictionary with all the currencies and dates in comparison to EUR
def getBasicRates(currencies, from_date, to_date):
    curr = "+".join(currencies)
    #'https://sdw-wsrest.ecb.europa.eu/service/data/EXR/D.USD+GBP+JPY.EUR.SP00.A?startPeriod=2020-12-02&endPeriod=2020-12-05'
    uri = 'https://sdw-wsrest.ecb.europa.eu/service/data/EXR/D.' + curr + '.EUR.SP00.A?startPeriod=' + from_date + '&endPeriod=' + to_date
    x = requests.get(uri)
    xmldoc = parseString(x.text)
    
    datasets = xmldoc.getElementsByTagName('generic:Series')
    rates = {}

    for dataset in datasets:
        #dataset.getElementsByTagName("generic:SeriesKey")[0].attributes['id'].value 

        curr_node = dataset.getElementsByTagName("generic:SeriesKey")[0].childNodes
        curr = find_value_element_by_id(curr_node, 'CURRENCY')

        dates = dataset.getElementsByTagName("generic:Obs")

        prev_date = ""
        prev_rate = ""

        for d in dates: 
            date = d.getElementsByTagName("generic:ObsDimension")[0].attributes['value'].value
            rate = d.getElementsByTagName("generic:ObsValue")[0].attributes['value'].value

            if (prev_date != ''):
                next_date = get_next_day(prev_date)
                
                #filling missing dates with previous available date
                while (next_date != date):
                    if (rates.get(date) is None) :
                        rates[next_date] = {curr : prev_rate}
                    else :
                        rates[next_date][curr] = prev_rate
                    next_date = get_next_day(next_date)    
                
            if (rates.get(date) is None) :
                rates[date] = {curr : rate}
            else :
                rates[date][curr] = rate

            prev_date = date    
            prev_rate = rate

    return rates  

def find_value_element_by_id(childnodes, id):
    i=0
    for i in range(len(childnodes)):
        if hasattr(childnodes[i],'getAttribute') and childnodes[i].getAttribute("id") == id:
            return childnodes[i].attributes['value'].value

def get_next_day(start_date):
    date_1 = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = date_1 + timedelta(days=1)
    end_date = end_date.strftime("%Y-%m-%d")
    return end_date            

'''
Receives data object from server with the structure: 
data = {
    'from_currency_list': ['EUR', 'USD', 'JPY'],
    'to_currency_list': ['XXX'],
    'from_date': '2020-12-01',
    'to_date': '2020-12-07'
}
'''

def processData(data):
    from_date = data['from_date']
    to_date = data['to_date']

    from_currency_list = data['from_currency_list']
    to_currency_list = data['to_currency_list']

    # bringing all the currencies except for EUR to make api request and build base dictionary with rates
    req_curr = from_currency_list + to_currency_list
    req_curr = list(dict.fromkeys(req_curr))
    if ('EUR' in req_curr): 
        req_curr.remove('EUR')

    if (len(req_curr) == 0):
         return {}

    rates = getBasicRates(req_curr, from_date, to_date)       

    # get all the possible conversion rates pairs liek USD-UER etc
    pairs = []

    for fr in from_currency_list:
        for to in to_currency_list:
            if (fr == 'EUR' and to == 'EUR') or (fr == to):
                continue
            name = fr + '-' + to   
            pairs.append([fr, to, name])

    # building results dictionary looking like {'2020-12-01: {'EUR-JPY' : 0.3, ...}...}
    results = {}
   
    for date in rates.keys():
        for pair in pairs:
            name = pair[2]

            if (pair[0] == 'EUR'):
                rate = rates[date][pair[1]]

            elif (pair[1] == 'EUR'):
                rate = round(1/float(rates[date][pair[0]]),4)

            else:
                rate = round(float(rates[date][pair[0]])/float(rates[date][pair[1]]),4)

            if (results.get(date) is None) :
                results[date] = {name : rate}
            else :
                results[date][name] = rate

    return results            

            



    
