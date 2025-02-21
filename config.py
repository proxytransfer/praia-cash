# config.py

MT5_CONFIG = {
    "server": "Exness-MT5Trial12",
    "login": "83041233",
    "password": "@#$eFRLK(*&hgf8"
}

TRADE_SETTINGS = {
    "lot_size": 1,  # Tamanho do lote padrão
    "max_risk": 0.02,  # Risco máximo por operação (2%)
    "symbols": ["EURUSDz", "GBPUSDz", "USDJPYz", "EBTCUSDz", "GBPUSDz", "USTECz"]  # Ativos negociados
}

REPORT_CONFIG = {
    "weekly_summary": True,  # Ativar relatórios semanais
    "save_path": "data/reports/"
}
