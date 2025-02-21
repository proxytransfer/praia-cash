from flask import Flask, jsonify
import pandas as pd
from dash_app import run_dash

# Iniciar Dash em uma thread separada
dash_thread = threading.Thread(target=run_dash, daemon=True)
dash_thread.start()

app = Flask(__name__)

def load_market_data():
    """Carrega os dados de mercado do arquivo CSV."""
    try:
        df = pd.read_csv("../data/market_data.csv")
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["timestamp", "price"])

def load_processed_data():
    """Carrega os dados processados pelo bot."""
    try:
        df = pd.read_csv("../data/processed_data.csv")
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["timestamp", "profit"])

@app.route("/api/market_data")
def get_market_data():
    df = load_market_data()
    return jsonify(df.to_dict(orient="records"))

@app.route("/api/processed_data")
def get_processed_data():
    df = load_processed_data()
    return jsonify(df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True, port=65432)
