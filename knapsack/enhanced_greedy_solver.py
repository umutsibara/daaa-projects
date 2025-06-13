# Dosya Adı: enhanced_greedy_solver.py

import sys
import time

# Item sınıfı öncekiyle aynı
class Item:
    def __init__(self, weight, value, index):
        self.weight, self.value, self.index = weight, value, index
        self.ratio = value / weight if weight > 0 else 0

def solve_with_enhanced_greedy(file_path):
    print("=" * 60)
    print(f"İşleniyor: '{file_path}' (Algoritma: Geliştirilmiş Açgözlü Yaklaşım)")
    print("=" * 60)

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            num_items, capacity = map(int, lines[0].strip().split())
            items = [Item(int(p[1]), int(p[0]), i+1) for i, p in enumerate(line.strip().split() for line in lines[1:] if line.strip())]
    except Exception as e:
        print(f"HATA: Dosya işlenirken bir sorun oluştu! Detay: {e}")
        return

    start_time = time.time()

    # --- Strateji A: Oran Odaklı Açgözlü ---
    items.sort(key=lambda x: x.ratio, reverse=True)
    value_A, weight_A, path_A = 0, 0, []
    for item in items:
        if weight_A + item.weight <= capacity:
            weight_A += item.weight
            value_A += item.value
            path_A.append(item.index)

    # --- Strateji B: En Değerli Tek Eşya ---
    value_B, path_B = 0, []
    # Sadece çantaya sığanlar arasından en değerli olanı bul
    fittable_items = [item for item in items if item.weight <= capacity]
    if fittable_items:
        best_single_item = max(fittable_items, key=lambda x: x.value)
        value_B = best_single_item.value
        path_B = [best_single_item.index]
    
    # --- Final Kararı: Hangi strateji daha iyi? ---
    if value_A > value_B:
        final_value = value_A
        final_path = path_A
        print(" -> Karar: Oran-odaklı strateji daha iyi sonuç verdi.")
    else:
        final_value = value_B
        final_path = path_B
        print(" -> Karar: En-değerli-tek-eşya stratejisi daha iyi sonuç verdi.")

    end_time = time.time()
    
    binary_solution = ['0'] * num_items
    for item_index in final_path:
        binary_solution[item_index - 1] = '1'
    
    print("\n✅ Yaklaşık Çözüm Raporu:")
    print("-" * 30)
    print(f"Çalışma Süresi: {end_time - start_time:.6f} saniye")
    print(f"Bulunan Değer (Optimal Değil): {final_value}")
    print(f"Bulunan çözüm: {','.join(binary_solution)}")
    print(f"Dahil edilen itemler: {','.join(map(str, sorted(final_path)))}")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        solve_with_enhanced_greedy(sys.argv[1])
    else:
        print("Kullanım: python enhanced_greedy_solver.py <dosya_adı>")