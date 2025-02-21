import time
import threading
import logging
import schedule
from dash import dash_table
from flask import Flask
from trading_bot.risk_management import calculate_trailing_stop, calculate_atr
from indicators.wr import williams_r


# Configuração de Logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Parâmetros de negociação
SYMBOLS = ["EURUSDz", "BTCUSDz"]
LOT_SIZE = 0.1
ATR_MULTIPLIER = 1.5
WR_OVERBOUGHT = -20
WR_OVERSOLD = -80
CHECK_INTERVAL = 60  # Segundos

# Iniciar Flask
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Flask e Dash rodando no Render!"

# Integrar Flask com Dash
dash_app.server = flask_app

# Função para análise de mercado
def analyze_market():
    for symbol in SYMBOLS:
        df = get_mt5_data(symbol)
        if df is None or df.empty:
            logger.error(f"❌ Erro ao obter dados para {symbol}. Verifique a conexão!")
            continue

        df["WR"] = williams_r(df)
        last_wr = df["WR"].iloc[-1]
        logger.info(f"📊 {symbol} - Último Williams %R: {last_wr:.2f}")

        if last_wr < WR_OVERSOLD:
            logger.info(f"🟢 {symbol} está sobrevendido! Entrada em COMPRA.")
            execute_trade_with_trailing_stop(symbol, "buy", LOT_SIZE, ATR_MULTIPLIER)
        elif last_wr > WR_OVERBOUGHT:
            logger.info(f"🔴 {symbol} está sobrecomprado! Entrada em VENDA.")
            execute_trade_with_trailing_stop(symbol, "sell", LOT_SIZE, ATR_MULTIPLIER)
        else:
            logger.info(f"⚪ Nenhuma condição forte identificada para {symbol}. Aguardando próximo sinal...")

# Agendar análise de mercado
schedule.every(CHECK_INTERVAL).seconds.do(analyze_market)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    logger.info("🚀 Iniciando Flask, Dash e Bot de Trading...")

    # Iniciar análise de mercado em uma thread separada
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    # Rodar Flask (Dash já integrado)
    flask_app.run(debug=False, host="0.0.0.0", port=65432)

if __name__ == '__main__':
    from waitress import serve
    print("Iniciando o servidor com Waitress...")
    serve(server, host='0.0.0.0', port=8050)