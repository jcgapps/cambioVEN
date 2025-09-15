from flask import Flask, jsonify, request
from scraper import get_rates, get_history

app = Flask(__name__)

@app.route("/api/rates", methods=["GET"])
def rates():
    return jsonify(get_rates())

@app.route("/api/history", methods=["GET"])
def history():
    days = request.args.get("days", default=30, type=int)
    if days > 90:
        days = 90
    return jsonify(get_history(days))

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "API de Tasas BCV",
        "endpoints": {
            "/api/rates": "Última tasa de cambio",
            "/api/history?days=N": "Histórico (N=7,30,90)"
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
