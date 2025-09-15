import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import urllib3

CACHE_FILE = "cache.json"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_bcv_rates():
    url = "https://www.bcv.org.ve/politica-cambiaria/intervencion-cambiaria"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers, timeout=10, verify=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    data = {}
    mapping = {
        "usd": "USD",
        "euro": "EUR",
        "yuan": "CNY",
        "lira": "TRY",
        "rublo": "RUB"
    }

    for html_id, code in mapping.items():
        try:
            div = soup.find("div", {"id": html_id})
            if div:
                value = div.find("strong").text.strip()
                # Convertir a float con formato decimal correcto
                value = value.replace(".", "").replace(",", ".")
                data[code] = float(value)
            else:
                data[code] = None
        except Exception:
            data[code] = None

    return data


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return None

    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        cache = json.load(f)

    today = datetime.now().strftime("%Y-%m-%d")
    if cache.get("date") == today:
        return cache["rates"]

    return None


def save_cache(rates):
    today = datetime.now().strftime("%Y-%m-%d")
    cache = {"date": today, "rates": rates}
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def get_rates():
    rates = load_cache()
    if rates is not None:
        return rates

    rates = get_bcv_rates()
    save_cache(rates)
    return rates
