import random
from itertools import combinations, product
from functools import lru_cache

import argparse

parser = argparse.ArgumentParser(description="Automated Mechanism Design")
parser.add_argument('--num_goods', type=int, default=4, help='Number of goods')
parser.add_argument('--num_theta', type=int, default=15, help='Number of Agent 2 types')
parser.add_argument('--debug', action='store_true', help='Enable debug output')
args = parser.parse_args()

NUM_GOODS = args.num_goods
NUM_THETA = args.num_theta

goods = [f"g{i}" for i in range(NUM_GOODS)]


def powerset(lst):
    return [set(comb) for i in range(len(lst)+1) for comb in combinations(lst, i)]

all_subsets = powerset(goods)





even_split = (NUM_GOODS//2)
if args.debug: print(even_split)

initial_endowment_1 = frozenset(goods[:even_split])  
initial_endowment_2 = frozenset(goods[even_split:])  
initial_endowment = (initial_endowment_1, initial_endowment_2)

print(f"INITIAL GOOD ENDOWMENTS: Agent 1 has {initial_endowment_1}, Agent 2 has {initial_endowment_2}")



preference_1 = {frozenset({g}): random.randint(1, 5) for g in goods}


theta_1 = {}
for subset in all_subsets:
    subset_utility = sum(preference_1.get(frozenset({good}), 0) for good in subset)
    theta_1[frozenset(subset)] = subset_utility


theta_2_list = []
for _ in range(NUM_THETA):
    
    preference_2 = {frozenset({g}): random.randint(1, 5) for g in goods}

    
    profile = {}
    for subset in all_subsets:
        
        subset_utility = sum(preference_2.get(frozenset({good}), 0) for good in subset)
        profile[frozenset(subset)] = subset_utility
    theta_2_list.append(profile)


if args.debug: print("theta_1:", theta_1)
if args.debug: print("theta_2_list (first profile):", theta_2_list[0])
if args.debug: print("theta_2_list (second profile):", theta_2_list[1]) 


outcomes = []
for bits in product([0, 1], repeat=NUM_GOODS):
    agent1_goods = {goods[i] for i in range(NUM_GOODS) if bits[i] == 0}
    agent2_goods = {goods[i] for i in range(NUM_GOODS) if bits[i] == 1}
    outcomes.append((frozenset(agent1_goods), frozenset(agent2_goods)))

assert len(outcomes) == 2 ** NUM_GOODS


def g(outcome):
    agent1_bundle, _ = outcome
    return theta_1.get(agent1_bundle, 0) - theta_1.get(initial_endowment_1, 0)


outcomes.sort(key=g, reverse=True)


def u(theta, outcome):
    _, agent2_bundle = outcome
    return theta.get(agent2_bundle, 0) - theta.get(initial_endowment_2, 0)

@lru_cache(maxsize=None)
def v_cached(X_tuple, Y_tuple):
    X = set(X_tuple)
    Y = set(Y_tuple)
    remaining_outcomes = [o for o in outcomes if o not in Y]
    total = 0
    for theta in theta_2_list:
        best_value = -float("inf")
        for o in remaining_outcomes:
            if all(u(theta, o) >= u(theta, x) for x in X):
                best_value = max(best_value, g(o))
        if best_value != -float("inf"):
            total += best_value
    return total / len(theta_2_list)

CB = None
L = -float("inf")

def SEARCH1(X, Y, w, d):
    global CB, L

    if d > len(outcomes):
        CB = X.copy()
        L = w
        return

    
        

    od = outcomes[d - 1]
    X_with_od = X | {od}
    v1 = v_cached(tuple(X_with_od), tuple(Y))
    if v1 > L:
        SEARCH1(X_with_od, Y, v1, d + 1)

    new_Y = Y | {od}
    remaining_outcomes = [o for o in outcomes if o not in new_Y]
    condition1 = all(any(u(theta, o) >= 0 for o in remaining_outcomes) for theta in theta_2_list)
    v2 = v_cached(tuple(X), tuple(new_Y))

    if condition1 and v2 > L:
        SEARCH1(X, new_Y, v2, d + 1)

def BnB_DFS():
    global CB, L
    CB = set()
    L = -float("inf")
    SEARCH1(set(), set(), 0, 1)
    return CB

def MCB(theta, CB):
    if not CB:
        return None
    
    # Find the outcome that agent 2 prefers most among all outcomes in CB
    best_outcome = max(CB, key=lambda o: u(theta, o))
    
    # Check if the best outcome gives non-negative utility to agent 2
    if u(theta, best_outcome) >= 0:
        return best_outcome
    else:
        return None

CB_result = BnB_DFS()
if args.debug: print("CB_result:", CB_result)


from itertools import product

def generate_misreports(theta, goods, value_range=(1, 5), max_misreports=1000):
    misreports = []
    
    # Calculate total possible misreports
    total_possible = (value_range[1] - value_range[0] + 1) ** len(goods)
    
    if total_possible > max_misreports:
        print(f"Warning: {total_possible} possible misreports would be generated. Limiting to {max_misreports} for performance.")
        # Generate a subset of misreports instead of all
        for _ in range(max_misreports):
            values = [random.randint(value_range[0], value_range[1]) for _ in range(len(goods))]
            misreported_preference = {frozenset({goods[i]}): values[i] for i in range(len(goods))}
            
            misreported_theta = {}
            for subset in all_subsets:
                subset_utility = sum(misreported_preference.get(frozenset({good}), 0) for good in subset)
                misreported_theta[frozenset(subset)] = subset_utility
            
            misreports.append(misreported_theta)
    else:
        # Generate all possible value combinations for individual goods
        value_combinations = product(range(value_range[0], value_range[1] + 1), repeat=len(goods))

        for values in value_combinations:
            # Create misreported preference for individual goods
            misreported_preference = {frozenset({goods[i]}): values[i] for i in range(len(goods))}

            # Create misreported theta by summing individual good preferences
            misreported_theta = {}
            for subset in all_subsets:
                subset_utility = sum(misreported_preference.get(frozenset({good}), 0) for good in subset)
                misreported_theta[frozenset(subset)] = subset_utility

            misreports.append(misreported_theta)
    
    return misreports

def verify_truthfulness(true_theta, chosen_outcome, goods, CB_result):

    true_utility = u(true_theta, chosen_outcome)
    misreports = generate_misreports(true_theta, goods)

    print(f"Verifying truthfulness for a true theta with utility {true_utility} for the chosen outcome.")
    print(f"Generated {len(misreports)} possible misreports.")

    for i, misreported_theta in enumerate(misreports):
        misreported_chosen_outcome = MCB(misreported_theta, CB_result)

        if misreported_chosen_outcome:
            misreported_utility = u(true_theta, misreported_chosen_outcome)
            assert misreported_utility <= true_utility, f"Truthfulness violated! Misreport {i} with outcome {misreported_chosen_outcome} yielded utility {misreported_utility} which is better than true utility {true_utility} with chosen outcome {chosen_outcome}."
    print("Truthfulness verified for this theta: All misreports resulted in utility less than or equal to the true utility.")



if args.debug:
    theta_to_test = theta_2_list[0]


    chosen_outcome_for_test_theta = MCB(theta_to_test, CB_result)


    if chosen_outcome_for_test_theta:
        verify_truthfulness(theta_to_test, chosen_outcome_for_test_theta, goods, CB_result)


for i, theta in enumerate(theta_2_list):
    chosen_outcome = MCB(theta, CB_result)
    print(f"\nChosen outcome for θ[{i}]:")
    if chosen_outcome:
        print("  Agent 1 gets:", set(chosen_outcome[0]))
        print("  Agent 2 gets:", set(chosen_outcome[1]))
        if args.debug:
            print("  Agent 1 utility (g):", g(chosen_outcome))
            print("  Agent 2 utility (u):", u(theta, chosen_outcome))
            print(f"  Agent 1 had {initial_endowment_1} with utility {g(initial_endowment)} initially (actual initial goods valuation: {theta_1.get(initial_endowment[0])}),  \n Agent 2 had {initial_endowment_2} with utility {u(theta, initial_endowment)} (actual initial goods valuation: {theta.get(initial_endowment[1])})")
        verify_truthfulness(theta, chosen_outcome, goods, CB_result)
    else:
        print("  No valid outcome found for this theta type.")
