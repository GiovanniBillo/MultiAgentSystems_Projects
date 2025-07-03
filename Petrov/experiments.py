#!/usr/bin/env python
# coding: utf-8

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import random

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

from simulation.cross_inhibition import run_cross_inhibition_simulation
from src.config import ZEALOT_PERCENTAGES, GROUP_SIZES, SMALL_GROUP_SIZES, TMAX, CYCLES


def exp_robust_consensus(plot):
    result = run_cross_inhibition_simulation(cycles=100, plot=plot)
    print("Single baseline run:", result)

def exp_same_n_zealots(plot):
    same_n_zealots_exp = {}
    for p in ZEALOT_PERCENTAGES:
        result = run_cross_inhibition_simulation(
            cycles=CYCLES, Tmax=TMAX, N=100, Nhalf=50, m=50, d=10, h=40,
            Zx=int(p*100), Zy=int(p*100),
            qx=1.05/100, qy=0.95/100,
            plot=plot, print_params=False
        )
        same_n_zealots_exp[p] = result
    print("Same % of zealots (X & Y):", same_n_zealots_exp)

def exp_vary_x_zealots(plot):
    vary_x_zealots_exp = {}
    for p in ZEALOT_PERCENTAGES:
        result = run_cross_inhibition_simulation(
            N=100, cycles=100, Zx=int(p*100), plot=plot, print_params=False
        )
        vary_x_zealots_exp[p] = result
    print("Varying X zealots:", vary_x_zealots_exp)

def exp_vary_y_zealots(plot):
    vary_y_zealots_exp = {}
    for p in ZEALOT_PERCENTAGES:
        result = run_cross_inhibition_simulation(
            N=100, cycles=100, Zy=int(p*100), plot=plot, print_params=False
        )
        vary_y_zealots_exp[p] = result
    print("Varying Y zealots:", vary_y_zealots_exp)

def exp_vary_group_size(plot):
    vary_group_size_exp = {}
    for g in GROUP_SIZES:
        result = run_cross_inhibition_simulation(
            N=g, cycles=100, Tmax=50, plot=plot, print_params=False
        )
        vary_group_size_exp[g] = result
    print("Varying group size:", vary_group_size_exp)

def exp_small_group_sizes(plot):
    small_group_size_exp = {}
    for g in SMALL_GROUP_SIZES:
        result = run_cross_inhibition_simulation(
            N=g, cycles=100, Tmax=50, Zx=int(0.1 * g), Zy=int(0.1 * g),
            plot=plot, print_params=False
        )
        small_group_size_exp[g] = result
    print("Small group sizes (10% zealots):", small_group_size_exp)


def run_all_selected_experiments(selected, plot):
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
            print(f"\n=== Running Experiment {name} ===")
            func(plot)
    else:
        for s in selected:
            if s in exp_map:
                print(f"\n=== Running Experiment {s} ===")
                exp_map[s](plot)
            else:
                print(f"Experiment {s} not recognized.")


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

    run_all_selected_experiments(selected, plot)

