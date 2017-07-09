import json
import requests
from datetime import date,datetime,timedelta
from urlparse import urljoin
from decimal import Decimal, ROUND_HALF_UP

class Currency:
    def __init__(self,base_url):
        self.base_url = base_url
        self.currencies = []
        self.max_rates = {}
        self.min_rates = {}
        self.avg_rates = {}
     
    def get_currency(self,url):
        req=requests.get(urljoin(self.base_url,url))
        return req.json()["rates"]

    def currencies_for_duration(self,start,end,base):
        self.currencies = []
        start_date = datetime.strptime(start,'%Y-%m-%d').date()
        end_date = datetime.strptime(end,'%Y-%m-%d').date() 
        delta = end_date - start_date         # timedelta
        for i in range(delta.days + 1):
            d = (start_date + timedelta(days=i)).isoformat()
            payload = {'base':base} 
            req = requests.get(urljoin(self.base_url,d),params=payload)
            self.currencies.append(req.json())

    def get_max_rates(self):
        self.max_rates = {}
        if self.currencies:
            rates1 = self.currencies[0]["rates"] # get the first exchage values
            for key in rates1.keys():
                self.max_rates[key] = rates1[key] # initialize the max_rates dictionary
            for c in self.currencies:
                rates2 = c["rates"]
                for k in rates2.keys():
                    if rates2[k] > self.max_rates[k]:
                        self.max_rates[k] = rates2[k]
        return self.max_rates 

    def get_min_rates(self):
        self.min_rates = {}
        if self.currencies:
            rates1 = self.currencies[0]["rates"] # get the first exchage values
            for key in rates1.keys():
                self.min_rates[key] = rates1[key] # initialize the min_rates dictionary
            for c in self.currencies:
                rates2 = c["rates"]
                for k in rates2.keys():
                    if rates2[k] < self.min_rates[k]:
                        self.min_rates[k] = rates2[k]
        return self.min_rates     

    def get_avg_rates(self):
        self.avg_rates = {}
        if self.currencies:
            rates1 = self.currencies[0]["rates"] # get the first exchage values
            cents = Decimal('.01') # for rounding currency
            for key in rates1.keys():
                self.avg_rates[key] = 0 # initialize the avg_rates dictionary
            for c in self.currencies:
                rates2 = c["rates"]
                for k in rates2.keys():
                    self.avg_rates[k] += rates2[k] # compute total rate during the start and end time
            for ky in self.avg_rates.keys():
                avg_rate = Decimal(str(self.avg_rates[ky]/len(self.currencies))) # compute the average rate
                self.avg_rates[ky]=float(avg_rate.quantize(cents,ROUND_HALF_UP)) # rounding currency vlaue
        return self.avg_rates 
