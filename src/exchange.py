import requests
import json
import logging
from datetime import datetime, date
import os

from config import LOGS_DIR, CURRENCY_JSON, CURRENCY_EXCHANGE_RATES_DIR, NOT_FOUND, CURRENCY_HRK, CURRENCY_EXCHANGE_RATES_DIR
from logger import logger_setup


logger = logger_setup()

logging.basicConfig(filename=LOGS_DIR/'currency_exchange.log', filemode='w', 
                    format='%(name)s - %(levelname)s - %(message)s')

def update_exchange_rates() -> bool:
    apikey = os.getenv('CURRENCY_API_KEY')
    url = 'https://api.currencyapi.com/v3/latest'
    pars = {'apikey': apikey, 'base_currency': 'EUR'}
       
    try:
        r = requests.get(url, params=pars)
    
        CURRENCY_EXCHANGE_RATES_DIR.mkdir(parents=True, exist_ok=True)
        with open(CURRENCY_JSON, mode='w') as f:
            json.dump(r.json(), f)
        
        return True
    
    except Exception as err:
        print(err)
        logging.error(f'{datetime.today()} an exception occurred', exc_info=True)
        return False

    
def get_exchange_rates() -> tuple:
    
    try:
        with open(CURRENCY_JSON, mode='r') as f:
            currencies = json.load(f)
            
        with open(CURRENCY_HRK, mode='r') as f_2:
            hrk = json.load(f_2)
        
        last_update_date = currencies['meta']['last_updated_at']
        ago_days = date.today() - datetime.strptime(last_update_date, '%Y-%m-%dT%H:%M:%SZ').date()
        
        currencies['data']['HRK'] = hrk['data']['HRK']
        exchange_rates = currencies['data']

        return (ago_days.days, exchange_rates)
            
    except FileNotFoundError as err:
        logger.critical(f'File not found: {err.filename}')
        return NOT_FOUND, NOT_FOUND


if __name__ == '__main__':
    update_exchange_rates()    
    pass