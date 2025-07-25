# grid_bot.py

from binance.client import Client
from config import API_KEY, API_SECRET, SYMBOL, GRID_LEVELS, GRID_RANGE, BASE_ORDER_SIZE, USE_TESTNET

client = Client(API_KEY, API_SECRET)

if USE_TESTNET:
    client.API_URL = 'https://testnet.binance.vision/api'

def get_price(symbol):
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker['price'])

def place_grid_orders():
    price = get_price(SYMBOL)
    lower = price - GRID_RANGE / 2
    upper = price + GRID_RANGE / 2
    step = GRID_RANGE / GRID_LEVELS

    print(f"📉 Mevcut Fiyat: {price}")
    print(f"📈 Grid Aralığı: {lower:.2f} - {upper:.2f}")
    print(f"📊 Grid Adımı: {step:.2f}")

    for i in range(GRID_LEVELS + 1):
        grid_price = lower + i * step

        if grid_price < price:
            # Alım emri (buy limit)
            order = client.order_limit_buy(
                symbol=SYMBOL,
                quantity=BASE_ORDER_SIZE,
                price=f"{grid_price:.2f}"
            )
            print(f"🟢 Alım emri yerleştirildi: {grid_price:.2f}")

        else:
            # Satış emri (sell limit)
            order = client.order_limit_sell(
                symbol=SYMBOL,
                quantity=BASE_ORDER_SIZE,
                price=f"{grid_price:.2f}"
            )
            print(f"🔴 Satış emri yerleştirildi: {grid_price:.2f}")

if __name__ == "__main__":
    place_grid_orders()
