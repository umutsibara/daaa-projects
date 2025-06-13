import os
import random
import time

# ========================
# Warehouse Location Problem Solver using VNS
# Works on dataset sizes: 200, 300, 500
# Reads input files from Dataset/wl_<size>
# Writes output to Res/R_wl_<size>.txt
# ========================

def read_input(file_path):
    """
    Reads input format:
      Line 1: num_depots num_customers
      Next num_depots lines: capacity setup_cost
      Then for each customer (2 lines):
        Line: demand
        Line: transport_costs for each depot
    """
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    # First line: counts
    num_depots, num_customers = map(int, lines[0].split())

    # Depots data
    capacities = []
    setup_costs = []
    for i in range(1, 1 + num_depots):
        cap, cost = lines[i].split()
        capacities.append(int(cap))
        setup_costs.append(float(cost))

    # Customers data
    demands = []
    transport_costs = []
    idx = 1 + num_depots
    while idx < len(lines):
        demand = int(lines[idx])
        costs = list(map(float, lines[idx + 1].split()))
        demands.append(demand)
        transport_costs.append(costs)
        idx += 2

    return num_depots, num_customers, capacities, setup_costs, demands, transport_costs


def greedy_initial_solution(num_depots, num_customers, capacities, setup_costs, demands, transport_costs):
    """
    Greedy: assign each customer in order to the feasible depot with minimum (transport + setup if needed).
    """
    assigned = [-1] * num_customers
    remaining_cap = capacities[:]  # copy
    open_depots = set()

    for c in range(num_customers):
        best_dep = None
        best_cost = float('inf')
        for d in range(num_depots):
            if remaining_cap[d] < demands[c]:
                continue
            cost = transport_costs[c][d]
            if d not in open_depots:
                cost += setup_costs[d]
            if cost < best_cost:
                best_cost = cost
                best_dep = d
        if best_dep is None:
            raise RuntimeError(f"No feasible depot for customer {c}")
        assigned[c] = best_dep
        remaining_cap[best_dep] -= demands[c]
        open_depots.add(best_dep)

    return assigned


def calculate_cost(assigned, setup_costs, transport_costs):
    total = 0.0
    used = set(assigned)
    for d in used:
        total += setup_costs[d]
    for c, d in enumerate(assigned):
        total += transport_costs[c][d]
    return total


def is_feasible(assigned, capacities, demands):
    load = [0] * len(capacities)
    for c, d in enumerate(assigned):
        load[d] += demands[c]
    return all(load[i] <= capacities[i] for i in range(len(capacities)))


def shake(solution, num_depots):
    """Randomly reassign one customer to a random depot"""
    neighbor = solution.copy()
    c = random.randrange(len(neighbor))
    new_d = random.randrange(num_depots)
    neighbor[c] = new_d
    return neighbor


def local_search(sol, num_depots, capacities, demands, setup_costs, transport_costs):
    """Try relocating each customer to any other depot if cost improves"""
    best = sol.copy()
    best_cost = calculate_cost(best, setup_costs, transport_costs)
    for c in range(len(sol)):
        current_d = best[c]
        for d in range(num_depots):
            if d == current_d:
                continue
            cand = best.copy()
            cand[c] = d
            if not is_feasible(cand, capacities, demands):
                continue
            cand_cost = calculate_cost(cand, setup_costs, transport_costs)
            if cand_cost < best_cost:
                best = cand
                best_cost = cand_cost
    return best


def vns(num_depots, num_customers, capacities, setup_costs, demands, transport_costs, max_iter=30):
    random.seed(0)
    # Initial solution
    current = greedy_initial_solution(num_depots, num_customers, capacities, setup_costs, demands, transport_costs)
    best = current.copy()
    best_cost = calculate_cost(best, setup_costs, transport_costs)

    print(f"  Başlangıç maliyeti: {best_cost:.3f}")
    start_time = time.time()

    for it in range(1, max_iter + 1):
        # Shake
        nei = shake(best, num_depots)
        if not is_feasible(nei, capacities, demands):
            continue
        # Local search
        nei_ls = local_search(nei, num_depots, capacities, demands, setup_costs, transport_costs)
        nei_cost = calculate_cost(nei_ls, setup_costs, transport_costs)
        if nei_cost < best_cost:
            best = nei_ls.copy()
            best_cost = nei_cost
        # Progress
        elapsed = time.time() - start_time
        print(f"  Iterasyon {it}/{max_iter}, En iyi maliyet: {best_cost:.3f}, Süre: {elapsed:.1f}s")

    return best, best_cost


def solve_and_save(size, base_path="."):
    in_path = os.path.join(base_path, f"Dataset/wl_{size}")
    out_path = os.path.join(base_path, f"Res/R_wl_{size}.txt")
    print(f"Çözülüyor: wl_{size} -> {in_path}")
    data = read_input(in_path)
    best_assign, best_cost = vns(*data)
    # Write output: cost then assignments
    with open(out_path, 'w') as f:
        f.write(f"{best_cost:.3f}\n")
        f.write(' '.join(map(str, best_assign)))
    print(f"Çıktı kaydedildi: {out_path}\n")

if __name__ == "__main__":
    base = os.getcwd()  # WLP_odev klasörü
    for sz in [25,50, 200, 300, 500]:
        solve_and_save(sz, base)
