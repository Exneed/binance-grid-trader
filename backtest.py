import pandas as pd

dosya_yolu = r"Dosya_yolu(users desktop smthg"
df = pd.read_csv(dosya_yolu)

baslangic_fiyati = df.iloc[0]['close']
grid_sayisi = 5
grid_araligi = 50  # Daha küçük aralık

alis_seviyeleri = [baslangic_fiyati - grid_araligi * i for i in range(grid_sayisi, 0, -1)]
satim_seviyeleri = [baslangic_fiyati + grid_araligi * i for i in range(1, grid_sayisi + 1)]

print("Alış Seviyeleri:", alis_seviyeleri)
print("Satış Seviyeleri:", satim_seviyeleri)
print(f"Fiyat aralığı: {min(df['close'])} - {max(df['close'])}")

pozisyon = 0.0
nakit = 10000.0
miktar_per_islem = nakit / grid_sayisi / baslangic_fiyati

for i, row in df.iterrows():
    fiyat = row['close']
    islem_yapildi = False

    # Her adımda güncel miktar_per_islem hesapla
    miktar_per_islem = nakit / grid_sayisi / fiyat if nakit > 0 else 0

    # Alım işlemi
    for alis_fiyat in alis_seviyeleri.copy():
        if fiyat <= alis_fiyat + (grid_araligi * 0.1) and nakit >= alis_fiyat * miktar_per_islem and miktar_per_islem > 0:
            pozisyon += miktar_per_islem
            nakit -= alis_fiyat * miktar_per_islem
            alis_seviyeleri.remove(alis_fiyat)
            yeni_alis = alis_seviyeleri[0] - grid_araligi if alis_seviyeleri else alis_fiyat - grid_araligi
            alis_seviyeleri.insert(0, yeni_alis)
            print(f"🟢 ALIM: Gün {i} - Fiyat: {fiyat:.2f} (Alış seviyesi: {alis_fiyat:.2f})")
            islem_yapildi = True
            break

    # Satım işlemi
    if not islem_yapildi:
        # Güncel miktar_per_islem pozisyona göre sınırla
        miktar_per_islem_satim = min(miktar_per_islem, pozisyon)

        for sat_fiyat in satim_seviyeleri.copy():
            if fiyat >= sat_fiyat - (grid_araligi * 0.1) and pozisyon >= miktar_per_islem_satim and miktar_per_islem_satim > 0:
                pozisyon -= miktar_per_islem_satim
                nakit += sat_fiyat * miktar_per_islem_satim
                satim_seviyeleri.remove(sat_fiyat)
                yeni_sat = satim_seviyeleri[-1] + grid_araligi if satim_seviyeleri else sat_fiyat + grid_araligi
                satim_seviyeleri.append(yeni_sat)
                print(f"🔴 SATIM: Gün {i} - Fiyat: {fiyat:.2f} (Satış seviyesi: {sat_fiyat:.2f})")
                islem_yapildi = True
                break

    if not islem_yapildi:
        print(f"İşlem Yok - Gün {i} - Fiyat: {fiyat:.2f} | Pozisyon: {pozisyon:.4f} BTC | Nakit: {nakit:.2f} USDT")
