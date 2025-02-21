import MetaTrader5 as mt5

# Caminho manual do terminal (ajuste se necessário)
mt5.initialize(path="C:\Program Files\MetaTrader 5 EXNESS\terminal64.exe")

if not mt5.initialize():
    print(f"initialize() failed, error code = {mt5.last_error()}")
else:
    print("Conectado ao MetaTrader 5!")
    mt5.shutdown()
