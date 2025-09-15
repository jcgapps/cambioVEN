from flask import Flask, jsonify, request
from scraper import get_rates, get_usd_history

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

@app.route("/api/rates", methods=["GET"])
def rates():
    return jsonify(get_rates())

@app.route("/api/history", methods=["GET"])
def history():
    days = request.args.get("days", default=30, type=int)
    if days > 90:
        days = 90
    return jsonify(get_usd_history(days))

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "API de Tasas BCV",
        "endpoints": {
            "/api/rates": "Última tasa de cambio (todas las divisas + USD previo)",
            "/api/history?days=N": "Histórico del USD (N=7,30,90)"
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
