from flask import Flask, jsonify
from scraper import get_rates

app = Flask(__name__)

@app.route("/api/rates", methods=["GET"])
def rates():
    return jsonify(get_rates())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
