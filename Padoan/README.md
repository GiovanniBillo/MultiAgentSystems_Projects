# Automated Mechanism Design for Bartering (One-on-One Setting)

This project implements a solution to the **Automated Mechanism Design (AMD)** problem in a bartering context, as introduced by:

> **[CS04] Vincent Conitzer and Tuomas Sandholm (2004)**  
> *An Algorithm for Automatically Designing Deterministic Mechanisms Without Payments*.  
> Proceedings of AAMAS’04.

---

## 🧩 Problem Overview
Two agents each start with an initial endowment of 3 goods (configurable) and have **valuation functions over every subset** of the total good set. No monetary transfers are allowed — only goods can be traded.

- **Agent 1** acts as the **mechanism designer**, proposing a bartering rule (mechanism).
- **Agent 2** can accept or reject the mechanism and may **misreport** preferences.
- The mechanism must be:
  - **Truthful** (Agent 2 gains nothing from lying)
  - **Individually Rational** (Agent 2 never ends up worse than initial endowment)

The goal is to **maximize Agent 1's expected utility** by selecting a subset of outcomes using a **Branch-and-Bound Depth-First Search (BnB-DFS)** over possible allocations.

---

## 📁 File Description

- `automatedmechanismdesign_finalfixed.py` — main implementation file.
  - Generates the set of goods and all possible allocations (outcomes).
  - Samples preference types for Agent 2 and one fixed profile for Agent 1.
  - Implements:
    - Utility functions `g`, `u`
    - Objective function `v(X,Y)` with caching
    - Core BnB-DFS algorithm (`SEARCH1`, `BnB_DFS`)
    - Mechanism extraction `MCB()`
    - Truthfulness verification utilities

---

## 🧪 Experiments

This script supports running experiments to:
- Generate truthful and individually rational deterministic mechanisms
- Validate output mechanisms across a variety of preference types
- Verify **truthfulness** by simulating misreports and comparing outcomes

---

## 🛠️ Configurable Parameters
You can change:
- `NUM_GOODS` (default: 2 or 6)
- `NUM_THETA` (default: 15 or 50)
- Value assignment ranges for goods (default: 1–5)

For larger values (e.g., 6 goods and 50 thetas), computation may be expensive.

