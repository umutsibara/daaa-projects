import sys
import time

# Item sınıfı öncekiyle aynı
class Item:
    def __init__(self, weight, value, index):
        self.weight, self.value, self.index = weight, value, index
        self.ratio = value / weight if weight > 0 else 0

def solve_with_greedy(file_path):
    print("=" * 60)
    print(f"İşleniyor: '{file_path}' (Algoritma: Basit Açgözlü Yaklaşım)")
    print("=" * 60)

    try:
        print("[1/3] 讀 Dosya okunuyor...")
        with open(file_path, 'r') as f:
            lines = f.readlines()
            num_items, capacity = map(int, lines[0].strip().split())
            items = [Item(int(p[1]), int(p[0]), i+1) for i, p in enumerate(line.strip().split() for line in lines[1:] if line.strip())]
    except Exception as e:
        print(f"HATA: Dosya işlenirken bir sorun oluştu! Detay: {e}")
        return

    print("\n[2/3] 🏎️  Açgözlü seçim yapılıyor...")
    start_time = time.time()
    items.sort(key=lambda x: x.ratio, reverse=True)

    total_value = 0
    total_weight = 0
    selected_items = []

    for item in items:
        if total_weight + item.weight <= capacity:
            total_weight += item.weight
            total_value += item.value
            selected_items.append(item.index)
    
    end_time = time.time()
    
    binary_solution = ['0'] * num_items
    for item_index in selected_items:
        binary_solution[item_index - 1] = '1'
    
    print("\n[3/3] ✅ Yaklaşık Çözüm Raporu:")
    print("-" * 30)
    print(f"Çalışma Süresi: {end_time - start_time:.6f} saniye")
    print(f"Bulunan Değer (Optimal Değil): {total_value}")
    print(f"Bulunan çözüm: {','.join(binary_solution)}")
    print(f"Dahil edilen itemler: {','.join(map(str, sorted(selected_items)))}")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        solve_with_greedy(sys.argv[1])
    else:
        print("Kullanım: python greedy_solver_revised.py <dosya_adı>")