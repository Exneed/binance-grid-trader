import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Grid Trading Backtest Görselleştirme")

# CSV oku
dosya_yolu = st.text_input("CSV Dosya Yolu", "historical_data.csv")
df = pd.read_csv(dosya_yolu)
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Parametreler
GRID_LEVELS = st.slider("Grid Sayısı", 5, 50, 10)
GRID_RANGE = st.slider("Grid Aralığı (USDT)", 100, 5000, 1000)
INITIAL_CASH = st.number_input("Başlangıç Nakit (USDT)", value=10000.0, step=1000.0)
ORDER_SIZE = st.number_input("Başlangıç İşlem Miktarı (BTC)", value=0.001, format="%.6f")

prices = df["close"]
timestamps = df["timestamp"]
start_price = prices.iloc[0]

# Alış ve Satış Seviyeleri (ikinci koddaki mantık)
alis_seviyeleri = [start_price - GRID_RANGE * i for i in range(GRID_LEVELS, 0, -1)]
satim_seviyeleri = [start_price + GRID_RANGE * i for i in range(1, GRID_LEVELS + 1)]

pozisyon = 0.0
nakit = INITIAL_CASH
alis_log = []
satim_log = []
islem_log = []

for i, row in df.iterrows():
    fiyat = row['close']
    islem_yapildi = False

    # Her adımda güncel miktar_per_islem hesapla (nakit / grid_sayısı / güncel fiyat)
    miktar_per_islem = nakit / GRID_LEVELS / fiyat if nakit > 0 else 0

    # ALIM işlemi
    for alis_fiyat in alis_seviyeleri.copy():
        if fiyat <= alis_fiyat + (GRID_RANGE * 0.1) and nakit >= alis_fiyat * miktar_per_islem and miktar_per_islem > 0:
            pozisyon += miktar_per_islem
            nakit -= alis_fiyat * miktar_per_islem
            alis_seviyeleri.remove(alis_fiyat)
            yeni_alis = alis_seviyeleri[0] - GRID_RANGE if alis_seviyeleri else alis_fiyat - GRID_RANGE
            alis_seviyeleri.insert(0, yeni_alis)
            alis_log.append((timestamps[i], fiyat))
            islem_log.append(f"🟢 ALIM: Gün {i} - Fiyat: {fiyat:.2f} (Alış seviyesi: {alis_fiyat:.2f})")
            islem_yapildi = True
            break

    # SATIM işlemi
    if not islem_yapildi:
        miktar_per_islem_satim = min(miktar_per_islem, pozisyon)
        for sat_fiyat in satim_seviyeleri.copy():
            if fiyat >= sat_fiyat - (GRID_RANGE * 0.1) and pozisyon >= miktar_per_islem_satim and miktar_per_islem_satim > 0:
                pozisyon -= miktar_per_islem_satim
                nakit += sat_fiyat * miktar_per_islem_satim
                satim_seviyeleri.remove(sat_fiyat)
                yeni_sat = satim_seviyeleri[-1] + GRID_RANGE if satim_seviyeleri else sat_fiyat + GRID_RANGE
                satim_seviyeleri.append(yeni_sat)
                satim_log.append((timestamps[i], fiyat))
                islem_log.append(f"🔴 SATIM: Gün {i} - Fiyat: {fiyat:.2f} (Satış seviyesi: {sat_fiyat:.2f})")
                islem_yapildi = True
                break

    if not islem_yapildi:
        islem_log.append(f"İşlem Yok - Gün {i} - Fiyat: {fiyat:.2f} | Pozisyon: {pozisyon:.6f} BTC | Nakit: {nakit:.2f} USDT")

# Son değerler
final_price = prices.iloc[-1]
unrealized = pozisyon * final_price
total = nakit + unrealized

# Grafik çizimi
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(timestamps, prices, label="Fiyat", color="gray")

# Grid çizgileri
for g in alis_seviyeleri + satim_seviyeleri:
    ax.axhline(y=g, color='lightblue', linestyle='--', linewidth=0.7)

# Alım/satım noktaları
if alis_log:
    bx, by = zip(*alis_log)
    ax.scatter(bx, by, color="green", label="Alım", s=20)
if satim_log:
    sx, sy = zip(*satim_log)
    ax.scatter(sx, sy, color="red", label="Satım", s=20)

ax.legend()
ax.set_title("Grid Trading Backtest")
ax.set_xlabel("Zaman")
ax.set_ylabel("Fiyat (USDT)")
st.pyplot(fig)

# Performans Özeti
st.subheader("📈 Performans Özeti")
st.markdown(f"**Toplam Nakit:** {nakit:.2f} USDT")
st.markdown(f"**Pozisyon:** {pozisyon:.6f} BTC")
st.markdown(f"**Son Fiyat:** {final_price:.2f} USDT")
st.markdown(f"**Toplam Değer:** {total:.2f} USDT")

# İşlem Günlüğü (isteğe bağlı göster)
if st.checkbox("İşlem Günlüğünü Göster"):
    for log in islem_log[-50:]:  # Son 50 işlem
        st.write(log)
