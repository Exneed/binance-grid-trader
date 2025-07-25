import pandas as pd
from binance.client import Client
from config import API_KEY, API_SECRET

client = Client(API_KEY, API_SECRET)

symbol = "BTCUSDT"
interval = Client.KLINE_INTERVAL_1MINUTE
limit = 1000  # max 1000 satır

# Veriyi çek
klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)

# DataFrame'e dönüştür
df = pd.DataFrame(klines, columns=[
    "timestamp", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "number_of_trades",
    "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
])

# İlgili kolonları seç ve dönüştür
df = df[["timestamp", "open", "high", "low", "close", "volume"]]
df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)

# CSV'ye yaz
df.to_csv("historical_data.csv", index=False)
print("✅ CSV dosyası oluşturuldu: historical_data.csv")
