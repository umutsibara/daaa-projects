import numpy as np
import random
import time
import os

def read_tsp_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    n = int(lines[0].strip())
    coords = []
    for line in lines[1:]:
        parts = line.strip().split()
        if len(parts) != 2:
            continue
        coords.append((float(parts[0]), float(parts[1])))
    coords = np.array(coords)
    return coords

def calc_distance_matrix(coords):
    n = len(coords)
    # Büyük dosya için mesafe matrisi oluşturma!
    if n > 10000:
        return None
    dist = np.sqrt(((coords.reshape((n, 1, 2)) - coords.reshape((1, n, 2))) ** 2).sum(axis=2))
    return dist

def path_cost(path, dist_matrix, coords=None):
    if dist_matrix is not None:
        return sum(dist_matrix[path[i], path[(i+1)%len(path)]] for i in range(len(path)))
    # RAM dostu: mesafe matrisini kullanmadan anlık hesapla
    total = 0.0
    for i in range(len(path)):
        a = coords[path[i]]
        b = coords[path[(i+1)%len(path)]]
        total += np.linalg.norm(a - b)
    return total

def tournament_selection(pop, costs, k=5):
    selected = random.sample(range(len(pop)), k)
    best = min(selected, key=lambda idx: costs[idx])
    return pop[best]

def ordered_crossover(parent1, parent2):
    size = len(parent1)
    a, b = sorted(random.sample(range(size), 2))
    child = [-1]*size
    child[a:b] = parent1[a:b]
    fill = [x for x in parent2 if x not in child]
    idx = 0
    for i in range(size):
        if child[i] == -1:
            child[i] = fill[idx]
            idx += 1
    return child

def swap_mutation(path):
    a, b = random.sample(range(len(path)), 2)
    path[a], path[b] = path[b], path[a]
    return path

def genetic_algorithm(dist_matrix, coords, n_generations=1000, pop_size=100, elite_size=5, mutation_rate=0.2, time_limit=600):
    n = len(coords)
    pop = [random.sample(range(n), n) for _ in range(pop_size)]
    best_cost = float('inf')
    best_path = None
    start_time = time.time()
    for gen in range(n_generations):
        costs = [path_cost(ind, dist_matrix, coords) for ind in pop]
        zipped = list(zip(costs, pop))
        zipped.sort()
        costs, pop = zip(*zipped)
        pop = list(pop)
        if costs[0] < best_cost:
            best_cost = costs[0]
            best_path = pop[0][:]
        # İlerleme çıktısı: her 50 nesilde bir ekrana yazdır
        if gen % 50 == 0 or gen == n_generations - 1:
            print(f'Nesil {gen}: En iyi maliyet = {costs[0]:.2f}')
        new_pop = list(pop[:elite_size])
        while len(new_pop) < pop_size:
            p1 = tournament_selection(pop, costs)
            p2 = tournament_selection(pop, costs)
            child = ordered_crossover(p1, p2)
            if random.random() < mutation_rate:
                child = swap_mutation(child)
            new_pop.append(child)
        pop = new_pop
        if time.time() - start_time > time_limit:
            break
    return best_cost, best_path

def solve_tsp_file(filepath, time_limit=600):
    coords = read_tsp_file(filepath)
    dist_matrix = calc_distance_matrix(coords)
    n = len(coords)
    if n > 10000:
        pop_size = 20
        n_generations = 300
        time_limit = min(time_limit, 900)
    elif n > 3000:
        pop_size = 40
        n_generations = 500
        time_limit = min(time_limit, 900)
    else:
        pop_size = 100
        n_generations = 1000
        time_limit = min(time_limit, 600)
    cost, path = genetic_algorithm(dist_matrix, coords, n_generations=n_generations, pop_size=pop_size, time_limit=time_limit)
    return cost, path

def write_result_for_file(output_path, student_no, name, size, cost, path, error=None):
    mode = 'a' if os.path.exists(output_path) else 'w'
    with open(output_path, mode, encoding='utf-8') as f:
        if os.path.getsize(output_path) == 0:
            f.write(f'{student_no}, {name}\n')
        f.write(f'Dosya Boyutu {size}:\n')
        if error:
            f.write(f'HATA: {error}\n')
        else:
            f.write(f'Optimal maliyet değeri: {cost}\n')
            f.write('Optimal maliyeti sağlayan path: ')
            f.write(' –> '.join(map(str, path)))
            f.write('\n')

def main():
    base_dir = os.path.join(os.path.dirname(__file__), 'Dataset', 'Dataset')
    files = [
        ('tsp_14051_1', 14051),
        ('tsp_85900_1', 85900),
    ]
    output_path = 'sonuclar.txt'
    student_no = '222804007'
    name = 'Muhammed Umut Şıbara'
    for fname, size in files:
        print(f'Çözülüyor: {fname} ({size})')
        fpath = os.path.join(base_dir, fname)
        if not os.path.exists(fpath):
            print(f'Bulunamadı: {fpath}')
            write_result_for_file(output_path, student_no, name, size, None, None, error='Dosya bulunamadı')
            continue
        try:
            cost, path = solve_tsp_file(fpath, time_limit=900)
            write_result_for_file(output_path, student_no, name, size, cost, path)
            print(f'{fname}: maliyet={cost} -- Tamamlandı')
        except Exception as e:
            print(f'{fname}: HATA -- {str(e)}')
            write_result_for_file(output_path, student_no, name, size, None, None, error=str(e))
    print('Tüm sonuçlar sonuclar.txt dosyasına yazıldı.')

if __name__ == '__main__':
    main()
