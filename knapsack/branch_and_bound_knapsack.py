# -*- coding: utf-8 -*-
# Dosya Adı: bnb_solver_with_checkpoint.py
# AÇIKLAMA: Branch and Bound çözer ve bulduğu her daha iyi çözümü
#           anında 'bnb_checkpoint.txt' dosyasına kaydederek ilerlemeyi güvence altına alır.

import sys
import time
from queue import PriorityQueue

# (Item, Node sınıfları ve calculate_bound fonksiyonu öncekiyle aynı)
class Item:
    def __init__(self, weight, value, index):
        self.weight, self.value, self.index = weight, value, index
        self.ratio = value / weight if weight > 0 else 0

class Node:
    def __init__(self, level, profit, weight, path):
        self.level, self.profit, self.weight, self.path = level, profit, weight, path
        self.bound = 0
    def __lt__(self, other):
        return self.bound < other.bound

def calculate_bound(node, num_items, capacity, items):
    if node.weight >= capacity: return 0
    profit_bound, current_weight, j = node.profit, node.weight, node.level + 1
    while j < num_items and current_weight + items[j].weight <= capacity:
        current_weight += items[j].weight
        profit_bound += items[j].value
        j += 1
    if j < num_items:
        profit_bound += (capacity - current_weight) * items[j].ratio
    return profit_bound

def solve_with_bnb_safe(file_path):
    # ... (Dosya okuma kısmı öncekiyle aynı) ...
    print("=" * 60)
    print(f"İşleniyor: '{file_path}' (Güvenli Mod: Checkpoint Aktif)")
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
    items.sort(key=lambda x: x.ratio, reverse=True)
    
    pq, max_profit, best_path = PriorityQueue(), 0, []
    root = Node(level=-1, profit=0, weight=0, path=[])
    root.bound = calculate_bound(root, num_items, capacity, items)
    pq.put(root)
    
    node_counter = 0
    checkpoint_file = "bnb_checkpoint.txt"
    print(f"Bilgi: Bulunan en iyi sonuçlar anlık olarak '{checkpoint_file}' dosyasına kaydedilecektir.")
    print("\n[!] Çözüm ağacı taranıyor... (İstediğiniz zaman Ctrl+C ile durdurabilirsiniz)\n")

    try:
        while not pq.empty():
            u_node = pq.get()
            node_counter += 1
            if node_counter % 250000 == 0:
                print(f" -> {node_counter} düğüm işlendi. Mevcut en iyi değer: {max_profit}")

            if u_node.bound > max_profit:
                level = u_node.level + 1
                if level < num_items:
                    item = items[level]
                    # Dal 1: Ekle
                    incl_weight = u_node.weight + item.weight
                    if incl_weight <= capacity:
                        incl_profit = u_node.profit + item.value
                        if incl_profit > max_profit:
                            print(f"  -> ✨ YENİ EN İYİ ÇÖZÜM BULUNDU! Değer: {max_profit} -> {incl_profit}")
                            max_profit = incl_profit
                            best_path = u_node.path + [item.index]
                            
                            # --- YENİ KISIM: Çözümü Dosyaya Yaz ---
                            print(f"     -> Çözüm '{checkpoint_file}' dosyasına kaydediliyor...")
                            binary_solution = ['0'] * num_items
                            for item_index in best_path:
                                binary_solution[item_index - 1] = '1'
                            
                            with open(checkpoint_file, 'w') as f_out:
                                f_out.write(f"{max_profit}\n")
                                f_out.write(f"{','.join(binary_solution)}\n")
                                f_out.write(f"{','.join(map(str, sorted(best_path)))}\n")
                            # ------------------------------------

                        v_incl = Node(level, incl_profit, incl_weight, u_node.path + [item.index])
                        v_incl.bound = calculate_bound(v_incl, num_items, capacity, items)
                        if v_incl.bound > max_profit: pq.put(v_incl)
                    # Dal 2: Ekleme
                    v_excl = Node(level, u_node.profit, u_node.weight, u_node.path)
                    v_excl.bound = calculate_bound(v_excl, num_items, capacity, items)
                    if v_excl.bound > max_profit: pq.put(v_excl)
    except KeyboardInterrupt:
        print("\n\n[!] İşlem kullanıcı tarafından durduruldu.")
        print(f"O ana kadar bulunan en iyi sonuç '{checkpoint_file}' dosyasında saklandı.")
        return

    print("\n[!] İşlem tamamlandı (Optimal sonuca ulaşıldı).")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        solve_with_bnb_safe(sys.argv[1])
    else:
        print("Kullanım: python bnb_solver_with_checkpoint.py <dosya_adı>")