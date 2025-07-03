import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import random
from datetime import datetime

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

from simulation.cross_inhibition import run_cross_inhibition_simulation
from src.config import (
    ZEALOT_PERCENTAGES, GROUP_SIZES, SMALL_GROUP_SIZES,
    TMAX, CYCLES
)

log_file = "results.txt"
with open(log_file, "a") as f:
    f.write(f"\n===== Experiment Log Started: {datetime.now()} =====\n")
    f.write("All parameters are defined in the src.config file.\n")

def log_print(msg):
    print(msg)
    with open(log_file, "a") as f:
        f.write(msg + "\n")

def exp_single_run(plot, seeds):
    for seed in seeds:
        random.seed(seed)
        result = run_cross_inhibition_simulation(cycles=CYCLES, Tmax=TMAX, plot=plot)
        log_print(f"Seed {seed} - Single baseline run: {result}")

def exp_same_n_zealots(plot, seeds):
    for p in ZEALOT_PERCENTAGES:
        probs = []
        for seed in seeds:
            random.seed(seed)
            result = run_cross_inhibition_simulation(
                cycles=CYCLES, Tmax=TMAX, N=100, Nhalf=50, m=50, d=10, h=40,
                Zx=int(p * 100), Zy=int(p * 100),
                qx=1.05 / 100, qy=0.95 / 100,
                plot=plot, print_params=False
            )
            probs.append(result['robust_consensus_prob'])
        log_print(f"Zealot % {p:.2f} - mean: {np.mean(probs):.3f}, std: {np.std(probs):.3f}")

def exp_vary_x_zealots(plot, seeds):
    for p in ZEALOT_PERCENTAGES:
        probs = []
        for seed in seeds:
            random.seed(seed)
            result = run_cross_inhibition_simulation(
                N=100, cycles=CYCLES, Tmax=TMAX, Zx=int(p * 100), plot=plot, print_params=False
            )
            probs.append(result['robust_consensus_prob'])
        log_print(f"X Zealots % {p:.2f} - mean: {np.mean(probs):.3f}, std: {np.std(probs):.3f}")

def exp_vary_y_zealots(plot, seeds):
    for p in ZEALOT_PERCENTAGES:
        probs = []
        for seed in seeds:
            random.seed(seed)
            result = run_cross_inhibition_simulation(
                N=100, cycles=CYCLES, Tmax=TMAX, Zy=int(p * 100), plot=plot, print_params=False
            )
            probs.append(result['robust_consensus_prob'])
        log_print(f"Y Zealots % {p:.2f} - mean: {np.mean(probs):.3f}, std: {np.std(probs):.3f}")

def exp_vary_group_size(plot, seeds):
    for g in GROUP_SIZES:
        probs = []
        for seed in seeds:
            random.seed(seed)
            result = run_cross_inhibition_simulation(
                N=g, cycles=CYCLES, Tmax=TMAX, plot=plot, print_params=False
            )
            probs.append(result['robust_consensus_prob'])
        log_print(f"Group size {g} - mean: {np.mean(probs):.3f}, std: {np.std(probs):.3f}")

def exp_small_group_sizes(plot, seeds):
    for g in SMALL_GROUP_SIZES:
        probs = []
        for seed in seeds:
            random.seed(seed)
            result = run_cross_inhibition_simulation(
                N=g, cycles=CYCLES, Tmax=TMAX,
                Zx=int(0.1 * g), Zy=int(0.1 * g),
                plot=plot, print_params=False
            )
            probs.append(result['robust_consensus_prob'])
        log_print(f"Small group size {g} (10% zealots) - mean: {np.mean(probs):.3f}, std: {np.std(probs):.3f}")

def run_all_selected_experiments(selected, plot, seeds):
    exp_map = {
        "1": exp_single_run,
        "2": exp_same_n_zealots,
        "3": exp_vary_x_zealots,
        "4": exp_vary_y_zealots,
        "5": exp_vary_group_size,
        "6": exp_small_group_sizes
    }
    if "all" in selected:
        for name, func in exp_map.items():
            log_print(f"\n=== Running Experiment {name} ===")
            func(plot, seeds)
    else:
        for s in selected:
            if s in exp_map:
                log_print(f"\n=== Running Experiment {s} ===")
                exp_map[s](plot, seeds)
            else:
                log_print(f"Experiment {s} not recognized.")

if __name__ == "__main__":
    print("Select experiments to run:")
    print("1: Single baseline run")
    print("2: Same % of zealots for X and Y")
    print("3: Vary % of zealots for X")
    print("4: Vary % of zealots for Y")
    print("5: Vary group size")
    print("6: Small group sizes with 10% zealots")
    print("Type 'all' to run all experiments.\n")

    selected = input("Enter experiment numbers separated by space (e.g., 1 3 5): ").lower().split()
    plot_input = input("Plot results? (y/n): ").lower()
    plot = plot_input in ['y', 'yes']

    seed_input = input("Enter random seeds separated by space (default is '42 43 44'): ")
    if seed_input.strip():
        seeds = [int(s) for s in seed_input.split()]
    else:
        seeds = [42, 43, 44]

    run_all_selected_experiments(selected, plot, seeds)

    with open(log_file, "a") as f:
        f.write(f"===== Experiment Log Ended: {datetime.now()} =====\n\n")
