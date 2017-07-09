import json
import requests
from flask import request, url_for
from currency import Currency
from flask_api import FlaskAPI

modapi = FlaskAPI(__name__)

base_url="http://api.fixer.io"
curr = Currency(base_url)

@modapi.route('/latest')
def current():
    base=request.args.get('base')
    return curr.get_currency(url_for('current',base=base)) 

@modapi.route('/<date>')
def any_date(date):
    base=request.args.get('base')
    return curr.get_currency(url_for('any_date',date=date,base=base))

@modapi.route('/range')
def for_duration():
    
    base=request.args.get('base')
    start_date=request.args.get('start_date')
    end_date=request.args.get('end_date')
    data = get_statistics(start_date,end_date,base) 
    return data

def get_statistics(start_date,end_date,base):
    curr.currencies_for_duration(start_date,end_date,base)
    avg_rate = curr.get_avg_rates()
    min_rate = curr.get_min_rates()
    max_rate = curr.get_max_rates()
    latest_rate = curr.get_currency(url_for('current',base=base)) 
    data = {"base":base,"start_date":start_date,"end_date":end_date,"latest":latest_rate,"min":min_rate,"max":max_rate,"avg":avg_rate} 
    return data

if __name__ == "__main__":
    modapi.run(debug=True)
