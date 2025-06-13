# Dosya Adı: create_graph.py
# Açıklama: Optimal çözüm üreten Dinamik Programlama algoritmasının, 
#           farklı veri setlerindeki çalışma zamanlarını görselleştiren
#           bir grafik oluşturur ve dosyaya kaydeder.

import matplotlib.pyplot as plt
import numpy as np

print("Deneysel sonuçlar için grafik oluşturuluyor...")

# --- DENEY VERİLERİ ---
# Bu veriler, senin sağladığın çıktılardan alınmıştır.
veri_boyutlari = [40, 300, 1000]
calisma_sureleri = [
    0.5364,      # ks_40_0 için süre
    250.0422,    # ks_300_0 için süre
    19.6553      # ks_1000_0 için süre
]

# --- GRAFİK OLUŞTURMA ---
# Grafik ve eksenleri oluştur
fig, ax = plt.subplots(figsize=(10, 7))

# Veri noktalarını çiz
ax.plot(veri_boyutlari, calisma_sureleri, marker='o', linestyle='--', color='b', label='Dinamik Programlama Çalışma Süresi')

# Eksenleri isimlendir ve başlık ekle
ax.set_xlabel('Veri Setindeki Eşya Sayısı (n)', fontsize=12)
ax.set_ylabel('Çalışma Süresi (Saniye)', fontsize=12)
ax.set_title('Veri Boyutuna Göre Algoritma Performansı', fontsize=16, pad=20)

# Daha iyi okunabilirlik için grid ekle
ax.grid(True, which='both', linestyle='--', linewidth=0.5)

# Y eksenini logaritmik ölçeğe alarak büyük değer farklarını daha iyi göster
# Bu, 250 saniye ile 0.5 saniye arasındaki devasa farkı grafikte anlamlı kılar.
ax.set_yscale('log')

# Her noktanın üzerine kendi değerini yaz
for i, txt in enumerate(calisma_sureleri):
    ax.annotate(f'{txt:.2f} s', (veri_boyutlari[i], calisma_sureleri[i]), textcoords="offset points", xytext=(0,10), ha='center')

# Grafiği daha şık hale getir
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend()

# Grafiği 'zaman_grafigi.png' olarak kaydet
# dpi=300, resmin kalitesini artırır.
dosya_adi = 'zaman_grafigi.png'
plt.savefig(dosya_adi, dpi=300, bbox_inches='tight')

print(f"\nGrafik başarıyla '{dosya_adi}' olarak kaydedildi.")
print("Bu dosyayı LaTeX projenin olduğu klasöre koyman yeterli.")

# Grafiği ekranda göster
plt.show()