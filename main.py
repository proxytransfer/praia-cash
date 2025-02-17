import time
from broker import get_mt5_data, execute_trade_with_trailing_stop
from indicators.wr import williams_r
from account.account_manager import create_account, deposit

# Criar uma conta para testes
create_account("user123", 1000)
deposit("user123", 500)

# Parâmetros de negociação
SYMBOLS = ["EURUSDz", "BTCUSDz"]
LOT_SIZE = 0.1
ATR_MULTIPLIER = 1.5
WR_OVERBOUGHT = -20  # Nível de sobrecompra do Williams %R
WR_OVERSOLD = -80    # Nível de sobrevenda do Williams %R
CHECK_INTERVAL = 60  # Tempo entre verificações (segundos)

def analyze_market(symbol):
    """Analisa o mercado para um ativo e decide se deve abrir uma ordem."""
    df = get_mt5_data(symbol)
    if df is None or df.empty:
        print(f"❌ Erro ao obter dados para {symbol}.")
        return

    df["WR"] = williams_r(df)
    last_wr = df["WR"].iloc[-1]

    print(f"📊 {symbol} - Último Williams %R: {last_wr:.2f}")

    if last_wr < WR_OVERSOLD:
        print(f"🟢 {symbol} está sobrevendido! Entrada em COMPRA.")
        execute_trade_with_trailing_stop(symbol, "buy", LOT_SIZE, ATR_MULTIPLIER)
    elif last_wr > WR_OVERBOUGHT:
        print(f"🔴 {symbol} está sobrecomprado! Entrada em VENDA.")
        execute_trade_with_trailing_stop(symbol, "sell", LOT_SIZE, ATR_MULTIPLIER)
    else:
        print(f"⚪ Nenhuma condição forte identificada para {symbol}. Aguardando próximo sinal...")

if __name__ == "__main__":
    print("🚀 Iniciando bot de trading...")
    while True:
        for symbol in SYMBOLS:
            analyze_market(symbol)
        time.sleep(CHECK_INTERVAL)
