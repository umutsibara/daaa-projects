import sys
import time

def solve_with_dp(file_path):
    print("=" * 60)
    print(f"İşleniyor: '{file_path}' (Algoritma: Dinamik Programlama)")
    print("=" * 60)

    try:
        print("[1/4] 讀 Dosya okunuyor...")
        with open(file_path, 'r') as f:
            lines = f.readlines()
            num_items, capacity = map(int, lines[0].strip().split())
            values = [int(line.strip().split()[0]) for line in lines[1:] if line.strip()]
            weights = [int(line.strip().split()[1]) for line in lines[1:] if line.strip()]
    except Exception as e:
        print(f"HATA: Dosya işlenirken bir sorun oluştu! Detay: {e}")
        return

    print("\n[2/4] ⏳ DP tablosu dolduruluyor...")
    start_time = time.time()
    dp = [[0 for _ in range(capacity + 1)] for _ in range(num_items + 1)]

    for i in range(1, num_items + 1):
        val, wt = values[i-1], weights[i-1]
        for w in range(capacity + 1):
            if wt <= w:
                dp[i][w] = max(dp[i-1][w], val + dp[i-1][w - wt])
            else:
                dp[i][w] = dp[i-1][w]
        if i % (num_items // 10 or 1) == 0:
            print(f" -> İlerleme: %{(i / num_items) * 100:.0f} tamamlandı...")

    print("\n[3/4] 🔍 Geri izleme (backtracking) yapılıyor...")
    optimal_value = dp[num_items][capacity]
    selected_items = []
    w = capacity
    for i in range(num_items, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected_items.append(i)
            w -= weights[i-1]
    selected_items.reverse()
    end_time = time.time()

    # --- YENİ FORMAT İÇİN ÇIKTI OLUŞTURMA ---
    binary_solution = ['0'] * num_items
    for item_index in selected_items:
        binary_solution[item_index - 1] = '1'
    
    # İstenen formatlar: "0,0,1,1" ve "3,4"
    binary_output_str = ','.join(binary_solution)
    item_list_output_str = ','.join(map(str, selected_items))

    print("\n[4/4] ✅ Çözüm Raporu:")
    print("-" * 30)
    print(f"Çalışma Süresi: {end_time - start_time:.4f} saniye")
    print("\n--- Excel İçin Çıktılar ---")
    print(f"Optimal Value Değeri: {optimal_value}")
    print(f"Optimal çözüm: {binary_output_str}")
    print(f"Optimal çözüme dahil edilen itemler: {item_list_output_str}")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for file_name in sys.argv[1:]:
            solve_with_dp(file_name)
    else:
        print("Kullanım: python dp_solver.py <dosya_adı>")