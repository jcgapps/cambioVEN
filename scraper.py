import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import urllib3

CACHE_FILE = "cache.json"
HISTORY_FILE = "history.json"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_bcv_rates():
    url = "https://www.bcv.org.ve/politica-cambiaria/intervencion-cambiaria"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers, timeout=10, verify=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    data = {}
    mapping = {
        "dolar": "USD",
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
                value = value.replace(".", "").replace(",", ".")
                data[code] = float(value)
            else:
                data[code] = None
        except Exception:
            data[code] = None

    return data


def load_json(file):
    if not os.path.exists(file):
        return None
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_rates():
    cache = load_json(CACHE_FILE)
    history = load_json(HISTORY_FILE) or []

    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Si ya tenemos datos de hoy → devolver caché
    if cache and cache["date"].startswith(today):
        return cache

    # Obtener valores nuevos
    rates = get_bcv_rates()

    # Valor previo del USD
    prev_usd = history[-1]["usd"] if history else None

    # Registrar en histórico solo USD
    history.append({
        "date": now,
        "usd": rates.get("USD")
    })

    # Mantener solo 90 días
    if len(history) > 90:
        history = history[-90:]

    save_json(HISTORY_FILE, history)

    cache = {
        "date": now,
        "rates": rates,
        "prev_usd": prev_usd
    }
    save_json(CACHE_FILE, cache)

    return cache


def get_usd_history(days=90):
    history = load_json(HISTORY_FILE) or []
    return history[-days:]
