from binance.client import Client
import config  # config.py dosyasını import ediyoruz

# Client'ı oluştur
client = Client(config.API_KEY, config.API_SECRET)

# Testnet kullanıyorsan API URL'ini değiştir
if config.USE_TESTNET:
    client.API_URL = 'https://testnet.binance.vision/api'

# Bakiyeyi çek
balance = client.get_asset_balance(asset='USDT')
print("USDT Bakiyesi:", balance)

# Testnette örnek alım emri ver
order = client.create_order(
    symbol=config.SYMBOL,
    side=Client.SIDE_BUY,
    type=Client.ORDER_TYPE_MARKET,
    quantity=config.BASE_ORDER_SIZE
)
print("Alım Emri Detayları:", order)
