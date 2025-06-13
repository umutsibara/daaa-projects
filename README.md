# Optimizasyon Algoritmaları: WLP, TSP ve Knapsack Çözücüleri

Bu repository, üç önemli optimizasyon probleminin çözümü için geliştirilmiş algoritmaları içermektedir. Tüm problemler NP-zor (NP-hard) kategorisinde olup, farklı metasezgisel (metaheuristic) ve kesin (exact) algoritmalar kullanılarak çözülmüştür.

## 🎯 Projenin Amacı

Bu proje, üç önemli optimizasyon probleminin çözümü için farklı algoritmaların uygulanmasını ve performans karşılaştırmasını amaçlamaktadır:

1. **Depo Yerleşim Problemi (Warehouse Location Problem - WLP)**: Tedarik zinciri ve lojistik alanlarında önemli bir optimizasyon problemi
2. **Gezgin Satıcı Problemi (Traveling Salesman Problem - TSP)**: Klasik bir kombinatoriyel optimizasyon problemi
3. **Sırt Çantası Problemi (Knapsack Problem)**: Kaynak tahsisi ve optimizasyon problemlerinin temel yapı taşı

## 📚 Proje Bileşenleri

### 1. Depo Yerleşim Problemi (WLP) Çözücü (`wlp/main.py`)

#### Kullanılan Algoritmalar
- Açgözlü (Greedy) algoritma (başlangıç çözümü için)
- Değişken Komşuluk Araması (Variable Neighborhood Search - VNS)

#### Özellikler
- 25, 50, 200, 300 ve 500 müşteriden oluşan veri setleri desteği
- Depo kurulum ve taşıma maliyetlerinin optimizasyonu
- Yapılandırılmış giriş/çıkış dosya formatları
- Detaylı performans raporlama

### 2. Gezgin Satıcı Problemi (TSP) Çözücü (`tsp/tsp_ga_solver.py`)

#### Kullanılan Algoritma
- Genetik Algoritma (Genetic Algorithm - GA) implementasyonu

#### Özellikler
- Turnuva Seçimi (Tournament Selection)
- Sıralı Çaprazlama (Order Crossover - OX)
- Takas Mutasyonu (Swap Mutation)
- Elitizm (Elitism) stratejisi
- Büyük ölçekli problemler için optimize edilmiş bellek kullanımı

### 3. Sırt Çantası Problemi (Knapsack) Çözücüleri (`knapsack/`)

#### Kullanılan Algoritmalar
1. **Branch and Bound (`branch_and_bound_knapsack.py`)**
   - Kesin çözüm garantisi
   - Checkpoint sistemi ile ilerleme kaydı
   - Öncelik kuyruğu kullanımı
   - Sınır hesaplama optimizasyonu

2. **Genetik Algoritma (`genetic_solver.py`)**
   - GPU destekli paralel hesaplama
   - Turnuva seçimi
   - Tek noktalı çaprazlama
   - Onarım mekanizması
   - Elitizm stratejisi

3. **Dinamik Programlama (`dynamic_programming_knapsack.py`)**
   - Kesin çözüm garantisi
   - Bellek optimizasyonu
   - Alt problem çözümlerinin önbelleklenmesi

4. **Yerel Arama (`local_search_solver.py`)**
   - Komşuluk yapısı optimizasyonu
   - Tabu listesi kullanımı
   - Çözüm kalitesi iyileştirme

5. **Geliştirilmiş Açgözlü Algoritma (`enhanced_greedy_solver.py`)**
   - Değer/ağırlık oranı optimizasyonu
   - Yerel iyileştirme adımları
   - Hızlı çözüm üretimi

#### Özellikler
- Farklı problem boyutları için optimize edilmiş çözücüler
- Detaylı performans analizi ve karşılaştırma
- Görselleştirme araçları (`create_graph.py`)
- Excel tabanlı sonuç analizi

## 💻 Teknik Detaylar

### Genel Özellikler
- **Programlama Dili**: Python
- **Kullanılan Kütüphaneler**: 
  - NumPy (TSP çözücü)
  - CuPy (Knapsack GPU çözücü)
  - Matplotlib (Görselleştirme)
  - Pandas (Veri analizi)

### Performans Metrikleri

#### WLP Çözücü
- 25 müşteri: ~0.5 saniye
- 500 müşteri: ~30 saniye

#### TSP Çözücü
- 51 şehir: ~1 saniye
- 1000 şehir: ~5 dakika
- 85.900 şehir: ~15 dakika

#### Knapsack Çözücüler
- Branch and Bound: Kesin çözüm, değişken süre
- Genetik Algoritma (GPU): Hızlı yaklaşık çözüm
- Dinamik Programlama: Orta boyutlu problemler için optimal
- Yerel Arama: Hızlı yaklaşık çözüm
- Geliştirilmiş Açgözlü: En hızlı yaklaşık çözüm

## 🛠️ Kurulum ve Kullanım

### Gereksinimler
```bash
pip install numpy cupy-cuda11x matplotlib pandas
```

### WLP Çözücü
```bash
cd wlp
python main.py
```

### TSP Çözücü
```bash
cd tsp
python tsp_ga_solver.py
```

### Knapsack Çözücüler
```bash
cd knapsack
# Branch and Bound
python branch_and_bound_knapsack.py <dosya_yolu>

# Genetik Algoritma (GPU)
python genetic_solver.py <dosya_yolu>

# Diğer çözücüler
python dynamic_programming_knapsack.py <dosya_yolu>
python local_search_solver.py <dosya_yolu>
python enhanced_greedy_solver.py <dosya_yolu>
```

## 📊 Sonuç Analizi

- `knapsack/BestOptimalValue.xlsx`: En iyi çözüm değerleri
- `knapsack/OptimalValue_Cozum_Itemler.xlsx`: Detaylı çözüm analizi
- `knapsack/zaman_grafigi.png`: Performans karşılaştırma grafiği

## 📝 Notlar
- Tüm çözücüler eğitim amaçlı geliştirilmiştir
- Gerçek dünya uygulamaları için ek optimizasyonlar gerekebilir
- Performans sonuçları donanıma göre değişiklik gösterebilir
- GPU çözücü için CUDA destekli NVIDIA GPU gereklidir

## 📄 Lisans
Bu proje MIT lisansı altında lisanslanmıştır. 