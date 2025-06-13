import sys
import time
import random

# Item sınıfı öncekiyle aynı
class Item:
    def __init__(self, weight, value, index):
        self.weight, self.value, self.index = weight, value, index
        self.ratio = value / weight if weight > 0 else 0

def solve_with_local_search(file_path, search_iterations=1000000):
    print("=" * 60)
    print(f"İşleniyor: '{file_path}' (Algoritma: Yerel Aramalı Açgözlü)")
    print("=" * 60)

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            num_items, capacity = map(int, lines[0].strip().split())
            all_items = [Item(int(p[1]), int(p[0]), i+1) for i, p in enumerate(line.strip().split() for line in lines[1:] if line.strip())]
    except Exception as e:
        print(f"HATA: Dosya işlenirken bir sorun oluştu! Detay: {e}")
        return

    start_time = time.time()

    # --- 1. Adım: Geliştirilmiş Açgözlü ile iyi bir başlangıç çözümü bul ---
    # Strateji A (Oran)
    all_items.sort(key=lambda x: x.ratio, reverse=True)
    val_A, w_A, path_A = 0, 0, []
    for item in all_items:
        if w_A + item.weight <= capacity: w_A, val_A, path_A = w_A + item.weight, val_A + item.value, path_A + [item]
    
    # Strateji B (En Değerli Tek Eşya)
    val_B, path_B = 0, []
    fittable = [item for item in all_items if item.weight <= capacity]
    if fittable:
        best_single = max(fittable, key=lambda x: x.value)
        val_B, path_B = best_single.value, [best_single]
    
    # Başlangıç çözümünü seç
    if val_A > val_B: current_path = path_A
    else: current_path = path_B
    
    current_value = sum(item.value for item in current_path)
    current_weight = sum(item.weight for item in current_path)
    
    print(f" -> Başlangıç çözümü bulundu. Değer: {current_value}")

    # --- 2. Adım: Yerel Arama ile çözümü iyileştir ---
    print(f"\n -> {search_iterations} denemelik Yerel Arama başlatılıyor...")
    
    # Çantadaki ve dışarıdaki eşyaları ayır
    in_knapsack = set(current_path)
    out_of_knapsack = [item for item in all_items if item not in in_knapsack]
    
    for i in range(search_iterations):
        if not in_knapsack or not out_of_knapsack: break # Takas yapacak eşya kalmadıysa dur

        # Rastgele birer eşya seç
        item_to_remove = random.choice(list(in_knapsack))
        item_to_add = random.choice(out_of_knapsack)
        
        # Takas geçerli ve karlı mı?
        new_weight = current_weight - item_to_remove.weight + item_to_add.weight
        if new_weight <= capacity:
            new_value = current_value - item_to_remove.value + item_to_add.value
            if new_value > current_value:
                # Takası yap ve setleri güncelle
                current_value, current_weight = new_value, new_weight
                in_knapsack.remove(item_to_remove)
                in_knapsack.add(item_to_add)
                out_of_knapsack.remove(item_to_add)
                out_of_knapsack.append(item_to_remove)
                print(f"  -> İyileştirme bulundu! Yeni Değer: {current_value} (Deneme: {i})")
    
    end_time = time.time()
    final_path_indices = sorted([item.index for item in in_knapsack])
    binary_solution = ['0'] * num_items
    for item_index in final_path_indices:
        binary_solution[item_index - 1] = '1'

    print("\n✅ Yaklaşık Çözüm Raporu:")
    print("-" * 30)
    print(f"Çalışma Süresi: {end_time - start_time:.4f} saniye")
    print(f"Bulunan Değer: {current_value}")
    print(f"Bulunan çözüm: {','.join(binary_solution)}")
    print(f"Dahil edilen itemler: {','.join(map(str, final_path_indices))}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        solve_with_local_search(sys.argv[1])
    else:
        print("Kullanım: python local_search_solver.py <dosya_adı>")