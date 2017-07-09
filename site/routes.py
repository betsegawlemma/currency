import json
import requests
from flask import request, url_for, render_template, redirect
from flask_bootstrap import Bootstrap
from urlparse import urljoin
from flask_api import FlaskAPI

modsite = FlaskAPI(__name__)
Bootstrap(modsite)

api_url="http://127.0.0.1:8081"

@modsite.route('/')
def index():
    return render_template('index.html')

@modsite.route('/range',methods=['POST'])
def result():
    
    base=request.form.get('base')
    start_date=request.form.get('start_date')
    end_date=request.form.get('end_date')
    req=requests.get(urljoin(api_url,url_for('result',start_date=start_date,end_date=end_date,base=base)))
    data = req.json()
    return render_template('result.html',data=data)

if __name__ == "__main__":
    modsite.run(debug=True)
