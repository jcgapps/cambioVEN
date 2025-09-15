import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

CACHE_FILE = "cache.json"

def get_bcv_rates():
    """Scrapea la página del BCV y obtiene las tasas."""
    url = "https://www.bcv.org.ve/"
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    divisas = ["USD", "EUR", "CNY", "TRY", "RUB"]
    data = {}

    for divisa in divisas:
        try:
            value = soup.find("div", {"id": divisa.lower()}).text.strip()
            data[divisa] = float(value.replace(",", "."))
        except Exception:
            data[divisa] = None

    return data


def load_cache():
    """Carga el archivo de caché si existe y es válido para hoy."""
    if not os.path.exists(CACHE_FILE):
        return None

    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        cache = json.load(f)

    today = datetime.now().strftime("%Y-%m-%d")
    if cache.get("date") == today:
        return cache["rates"]

    return None


def save_cache(rates):
    """Guarda los datos en el archivo de caché."""
    today = datetime.now().strftime("%Y-%m-%d")
    cache = {"date": today, "rates": rates}
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def get_rates():
    """Obtiene las tasas desde caché o desde scraping."""
    rates = load_cache()
    if rates is not None:
        return rates

    rates = get_bcv_rates()
    save_cache(rates)
    return rates
