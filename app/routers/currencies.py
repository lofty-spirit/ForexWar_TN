from fastapi import status, HTTPException, Depends, APIRouter
from decimal import Decimal, getcontext
import requests #fastforex API documentation
from ..schemas import CurrencyRequest


router=APIRouter(
    tags=["Currencies"]
)

# Global variables to store exchange rates
TNDEUR_rate = None
EURUSD_rate = None
USDCAD_rate = None

def fetch_and_store_exchange_rates():
    global TNDEUR_rate, EURUSD_rate, USDCAD_rate
    
    url = "https://api.fastforex.io/fetch-multi"
    api_key = "76f07a3a59-eae93469e4-s7mu3c"
    currencies = ["TNDEUR", "EURUSD", "USDCAD"]
    
    for currency_pair in currencies:
        from_currency, to_currency = currency_pair[:3], currency_pair[3:]
        api_params = {
            "from": from_currency,
            "to": to_currency,
            "api_key": api_key
        }
        
        headers = {"accept": "application/json"}
        response = requests.get(url, params=api_params, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            exchange_rate = Decimal(result["results"][to_currency])
            store_exchange_rate(currency_pair, exchange_rate)
        else:
            print(f"Error fetching exchange rate for {currency_pair}. Status code: {response.status_code}")

def store_exchange_rate(currency_pair, exchange_rate):
    global TNDEUR_rate, EURUSD_rate, USDCAD_rate
    
    if currency_pair == "TNDEUR":
        TNDEUR_rate = exchange_rate
    elif currency_pair == "EURUSD":
        EURUSD_rate = exchange_rate
    elif currency_pair == "USDCAD":
        USDCAD_rate = exchange_rate
    
    print(f"Storing {currency_pair} exchange rate: {exchange_rate}")


# Endpoint to get exchange rates
@router.get("/get_current_exchange_rates")
def get_exchange_rates():
    fetch_and_store_exchange_rates()
    return {
        "TNDEUR": TNDEUR_rate,
        "EURUSD": EURUSD_rate,
        "USDCAD": USDCAD_rate
    }


@router.post("/get_time_series/")
async def get_time_series(request_body: CurrencyRequest):
    api_key = "76f07a3a59-eae93469e4-s7mu3c"
    base_url = "https://api.fastforex.io/time-series"

    # Calculate the start and end dates for the last 14 days
    # Assuming today's date is 2024-01-22
    import datetime
    end_date = datetime.date(2024, 1, 22)
    start_date = end_date - datetime.timedelta(days=13)

    url = f"{base_url}?from={request_body.from_currency}&to={request_body.to_currency}&start={start_date}&end={end_date}&api_key={api_key}"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch time series data")

