# Optimizasyon Algoritmaları: WLP ve TSP Çözücüleri

Bu repository, Depo Yerleşim Problemi (Warehouse Location Problem - WLP) ve Gezgin Satıcı Problemi (Traveling Salesman Problem - TSP) için geliştirilmiş optimizasyon algoritmalarını içermektedir. Her iki problem de NP-zor (NP-hard) kategorisinde olup, metasezgisel (metaheuristic) algoritmalar kullanılarak çözülmüştür.

## 🎯 Projenin Amacı

Bu proje, iki önemli optimizasyon probleminin çözümü için farklı metasezgisel (metaheuristic) algoritmaların uygulanmasını ve performans karşılaştırmasını amaçlamaktadır:

1. **Depo Yerleşim Problemi (Warehouse Location Problem - WLP)**: Tedarik zinciri (supply chain) ve lojistik alanlarında önemli bir optimizasyon problemi
2. **Gezgin Satıcı Problemi (Traveling Salesman Problem - TSP)**: Klasik bir kombinatoriyel (combinatorial) optimizasyon problemi

## 📚 Proje Bileşenleri

### 1. Depo Yerleşim Problemi (WLP) Çözücü

#### Kullanılan Algoritmalar
- Açgözlü (Greedy) algoritma (başlangıç çözümü için)
- Değişken Komşuluk Araması (Variable Neighborhood Search - VNS)
- Simüle Edilmiş Tavlama (Simulated Annealing - SA)
- Kuantum Tavlama (Quantum Annealing - QA)
- Tabu Arama (Tabu Search - TS)

#### Özellikler
- 25, 50, 200, 300 ve 500 müşteriden oluşan veri setleri desteği
- Depo kurulum (setup) ve taşıma (transportation) maliyetlerinin optimizasyonu
- Yapılandırılmış giriş/çıkış dosya formatları
- Detaylı performans raporlama

#### Dosya Yapısı
- `main.py`: Ana program ve VNS implementasyonu
- `Dataset/`: Test veri setleri
- `Res/`: Sonuç dosyaları

### 2. Gezgin Satıcı Problemi (TSP) Çözücü

#### Kullanılan Algoritma
- Genetik Algoritma (Genetic Algorithm - GA) implementasyonu

#### Özellikler
- Turnuva Seçimi (Tournament Selection)
- Sıralı Çaprazlama (Order Crossover - OX)
- Takas Mutasyonu (Swap Mutation)
- Elitizm (Elitism) stratejisi
- Büyük ölçekli problemler için optimize edilmiş bellek kullanımı

#### Dosya Yapısı
- `tsp_ga_solver.py`: GA implementasyonu
- Test veri setleri (51'den 85.900 şehre kadar)

## 💻 Teknik Detaylar

### WLP Çözücü
- **Programlama Dili**: Python
- **Kullanılan Kütüphaneler**: os, random, time
- **Giriş Formatı**:
  ```
  num_depots num_customers
  capacity_1 setup_cost_1
  capacity_2 setup_cost_2
  ...
  demand_1
  transport_costs_1
  demand_2
  transport_costs_2
  ...
  ```

### TSP Çözücü
- **Programlama Dili**: Python
- **Kullanılan Kütüphaneler**: NumPy
- **Özellikler**:
  - Anlık mesafe hesaplaması (On-the-fly distance calculation)
  - Dinamik parametre ayarlama (Dynamic parameter adjustment)
  - Büyük ölçekli problem desteği (Large-scale problem support)

## 📊 Performans ve Sonuçlar

### WLP Çözücü
- VNS algoritması, test edilen diğer metasezgisel algoritmalara göre daha kararlı ve iyi sonuçlar üretmiştir
- Özellikle büyük veri setlerinde (300+ müşteri) üstün performans göstermiştir
- Örnek performans metrikleri:
  - 25 müşteri: ~0.5 saniye çözüm süresi
  - 500 müşteri: ~30 saniye çözüm süresi

### TSP Çözücü
- 10.000+ şehirli problemlerde optimize edilmiş bellek kullanımı
- Farklı problem boyutları için adaptif parametre ayarları
- Elitizm stratejisi ile çözüm kalitesinin korunması
- Örnek performans metrikleri:
  - 51 şehir: ~1 saniye çözüm süresi
  - 1000 şehir: ~5 dakika çözüm süresi

## 🛠️ Kurulum ve Kullanım

### Gereksinimler
```bash
# Gerekli kütüphanelerin kurulumu
pip install numpy
```

### WLP Çözücü Kullanımı
```bash
# Proje dizinine git
cd WLP_222804007_MuhammedUmut_Şıbara

# Programı çalıştır
python main.py

# Belirli bir veri seti için çalıştırma
python main.py --dataset wl_200
```

### TSP Çözücü Kullanımı
```bash
# Programı çalıştır
python tsp_ga_solver.py

# Parametrelerle çalıştırma
python tsp_ga_solver.py --population 100 --generations 1000 --mutation_rate 0.1
```

## 📝 Notlar
- Her iki çözücü de eğitim amaçlı geliştirilmiştir
- Gerçek dünya uygulamaları için ek optimizasyonlar gerekebilir
- Performans sonuçları, kullanılan donanım ve veri setine göre değişiklik gösterebilir
- Önerilen minimum sistem gereksinimleri:
  - Python 3.8+
  - 4GB RAM
  - 2 çekirdekli işlemci

## 📄 Lisans
Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakınız.