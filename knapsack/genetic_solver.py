import sys
import time
import cupy as cp

# Genetik algoritma parametreleri
POPULATION_SIZE = 200
NUM_GENERATIONS = 500
MUTATION_RATE = 0.02
ELITISM_RATE = 0.1
TOURNAMENT_SIZE = 5


def read_dataset(file_path):
    """Veri setini dosyadan okur ve CuPy dizileri olarak döndürür."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
        num_items, capacity = map(int, lines[0].strip().split())
        # Not: Dosyadaki format (değer, ağırlık) ise bu sıra doğrudur.
        # Eğer (ağırlık, değer) ise [int(p[0]), int(p[1])] olmalıdır.
        # Genellikle format (değer, ağırlık) şeklindedir.
        items = cp.array([[int(p[1]), int(p[0])] for p in (line.strip().split() for line in lines[1:] if line.strip())], dtype=cp.int32)
    return num_items, capacity, items


def create_population(num_items):
    """Başlangıç popülasyonunu GPU üzerinde oluşturur."""
    return cp.random.randint(0, 2, size=(POPULATION_SIZE, num_items), dtype=cp.int8)


def calculate_fitness_gpu(population, items, capacity):
    """Popülasyonun uygunluk değerlerini GPU'da paralel olarak hesaplar."""
    weights = items[:, 0]
    values = items[:, 1]
    
    # Matris çarpımı ile her bireyin toplam ağırlığını ve değerini hesapla
    total_weights = population @ weights
    total_values = population @ values
    
    # Kapasiteyi aşan bireylere büyük bir ceza vererek "öldür"
    penalty = -1_000_000_000
    fitness = cp.where(total_weights <= capacity, total_values, penalty)
    return fitness


def selection_gpu(population, fitness):
    """Turnuva seçimi yöntemini GPU üzerinde uygular."""
    # Turnuva için rastgele birey indeksleri seç
    indices = cp.random.randint(0, POPULATION_SIZE, size=(TOURNAMENT_SIZE,))
    
    # Seçilen bireylerin uygunluk değerlerini al
    selected_fitness = fitness[indices]
    
    # Turnuvanın galibinin popülasyondaki orijinal indeksini bul
    winner_index_in_tournament = cp.argmax(selected_fitness)
    best_idx = indices[winner_index_in_tournament]
    
    return population[best_idx]


def crossover_gpu(parent1, parent2):
    """İki ebeveyn arasında tek noktalı çaprazlama uygular."""
    # 0 ve uzunluk arasında değil, 1 ve uzunluk-1 arasında bir nokta seç
    if len(parent1) < 2:
        return parent1.copy(), parent2.copy()
    point = cp.random.randint(1, len(parent1))
    child1 = cp.concatenate((parent1[:point], parent2[point:]))
    child2 = cp.concatenate((parent2[:point], parent1[point:]))
    return child1, child2


def mutate_gpu(individual, mutation_rate):
    """Bir bireyin genlerini belirli bir olasılıkla mutasyona uğratır."""
    mutation_mask = cp.random.rand(len(individual)) < mutation_rate
    # Maskenin True olduğu yerlerde biti tersine çevir (0->1, 1->0)
    individual = cp.where(mutation_mask, 1 - individual, individual)
    return individual


def solve_with_genetic_gpu(file_path):
    """Knapsack problemini GPU destekli genetik algoritma ile çözer ve ilerlemeyi gösterir."""
    # ... fonksiyonun başındaki kodlar aynı kalacak ...
    print("=" * 60)
    print(f"İşleniyor: '{file_path}' (GPU Destekli Genetik Algoritma)")
    print("=" * 60)

    num_items, capacity, items = read_dataset(file_path)
    
    # --- Diagnostik Bilgi ---
    # print(f"Kapasite: {capacity}, Toplam Item: {num_items}")
    # print("Okunan ilk 5 item (Ağırlık, Değer):\n", items[:5].get())
    # -----------------------

    population = create_population(num_items)
    best_solution = None
    best_fitness = -1.0

    start_time = time.time()

    for gen in range(NUM_GENERATIONS):
        # İlk nesli de onararak başlayalım ki en başta geçerli çözüm olsun
        if gen == 0:
            for i in range(POPULATION_SIZE):
                population[i] = repair_gpu(population[i], items, capacity)

        fitness = calculate_fitness_gpu(population, items, capacity)
        gen_best_idx = cp.argmax(fitness)
        gen_best_fit = fitness[gen_best_idx].item()

        status_text = (
            f"Nesil {gen + 1}/{NUM_GENERATIONS} | "
            f"Mevcut Nesil En İyisi: {int(gen_best_fit):<10} | "
            f"Global En İyi: {int(best_fitness):<10}"
        )
        print(status_text, end='\r', flush=True)

        if gen_best_fit > best_fitness:
            print(" " * len(status_text), end='\r')
            best_fitness = gen_best_fit
            best_solution = population[gen_best_idx].copy()
            print(f"✅ Nesil {gen+1:03d}: Yeni en iyi çözüm! Değer: {int(best_fitness)}")

        next_population = cp.empty_like(population)
        
        elite_count = int(POPULATION_SIZE * ELITISM_RATE)
        if elite_count > 0:
            elite_indices = cp.argsort(fitness)[-elite_count:]
            next_population[:elite_count] = population[elite_indices]

        offspring_count = POPULATION_SIZE - elite_count
        current_offspring = 0
        while current_offspring < offspring_count:
            p1 = selection_gpu(population, fitness)
            p2 = selection_gpu(population, fitness)
            c1, c2 = crossover_gpu(p1, p2)
            
            # Mutasyondan sonra ONARIM işlemini uygula
            c1 = mutate_gpu(c1, MUTATION_RATE)
            c1 = repair_gpu(c1, items, capacity)
            next_population[elite_count + current_offspring] = c1
            current_offspring += 1

            if current_offspring < offspring_count:
                c2 = mutate_gpu(c2, MUTATION_RATE)
                c2 = repair_gpu(c2, items, capacity)
                next_population[elite_count + current_offspring] = c2
                current_offspring += 1
                
        population = next_population

    # ... fonksiyonun sonundaki kodlar aynı kalacak ...
    end_time = time.time()
    print() 

    if best_solution is None:
        print("\n❌ Onarım mekanizmasına rağmen geçerli çözüm bulunamadı. Veri setini kontrol edin.")
        return

    selected_indices = (cp.where(best_solution == 1)[0] + 1).get()

    print("\n✅ Evrim Tamamlandı!")
    print("-" * 30)
    print(f"Çalışma Süresi: {end_time - start_time:.4f} saniye")
    print(f"Bulunan En İyi Değer: {int(best_fitness)}")
    print(f"Toplam {len(selected_indices)} item seçildi.")
    print(f"Dahil edilen item'ler: {','.join(map(str, selected_indices))}")
    print("=" * 60)

def repair_gpu(individual, items, capacity):
    """
    Kapasiteyi aşan bir bireyi, ağırlık limite inene kadar
    içinden rastgele item'lar çıkararak onarır.
    """
    weights = items[:, 0]
    total_weight = individual @ weights
    
    # Birey zaten geçerliyse dokunma
    if total_weight <= capacity:
        return individual
        
    # Birey geçersizse, geçerli olana kadar onar
    item_indices = cp.where(individual == 1)[0]
    
    while total_weight > capacity:
        # Çantadaki item'lardan rastgele birini seç
        random_index_to_remove = cp.random.choice(item_indices)
        
        # Eğer bu item hala çantadaysa (döngünün önceki adımlarında çıkarılmadıysa)
        if individual[random_index_to_remove] == 1:
            # Item'ı çantadan çıkar
            individual[random_index_to_remove] = 0
            # Ağırlığı güncelle
            total_weight -= weights[random_index_to_remove]
            # Çıkarılan item'ı tekrar seçmemek için listeden kaldır
            item_indices = item_indices[item_indices != random_index_to_remove]
            
        # Eğer çıkarılacak item kalmadıysa döngüden çık
        if len(item_indices) == 0:
            break
            
    return individual


if __name__ == "__main__":
    if len(sys.argv) > 1:
        solve_with_genetic_gpu(sys.argv[1])
    else:
        print("Kullanım: python genetic_solver.py <dosya_yolu>")