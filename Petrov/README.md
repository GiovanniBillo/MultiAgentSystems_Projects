# Consensus in Robotic Swarms: Simulation Framework

This project simulates consensus formation in robotic swarms using a Gillespie algorithm-based stochastic model. The model incorporates cross-inhibition and zealotry behaviors to explore under what conditions consensus is reached.

---

## 📁 Project Structure

```
project_root/
├── notebooks/
│   └── consensus_analysis.ipynb     # Interactive notebook for running and visualizing experiments
│
├── experiments/                     # (Optional) Python scripts for batch simulations
│
├── src/
│   ├── model/
│   │   ├── state.py                # Defines the State representation (x, y, u)
│   │   ├── reactions.py            # Defines all reactions (as a function of input parameters)
│   │   └── gillespie.py            # Implements the Gillespie stochastic simulation algorithm
│   │
│   └── simulation/
│       └── cross_inhibition.py     # Main simulation function and trajectory plotting tools
│
├── tests/                           # (Optional) Unit tests
└── README.md
```

---

## 🔬 Core Functionality

The system models three agent types:
- `X`, `Y`, and `U` (undecided agents),
- including a fixed number of "zealots" (`Zx`, `Zy`) which never change state.

The dynamics evolve through stochastic reactions, and consensus is defined based on the dominance of one type under a set of criteria.

---

## 📓 Notebook Experiments

All experiments and result visualizations are performed within the notebook: 
**`notebooks/consensus_analysis.ipynb`**.

### Experiments Conducted:

1. **Baseline Probability of Consensus**
   > Parameters: `m = 50`, `d = 10`, `t = 35`, `h = 40`, `N = 100`, `Zx = Zy = 10`  
   Initial condition: `X = 40`, `Y = 40`

2. **Varying Number of Zealots**
   > Test how different values of `Zx = Zy` (as a percentage of N) affect consensus probability

3. **Varying Group Size**
   > Evaluate how changing `N` (group size) impacts the likelihood of reaching consensus

---

## 🧪 How to Extend
- Add new experiments in `experiments/` or directly in the notebook
- Modify `reactions.py` to explore different behavioral rules
- Swap out `State` structure if tracking additional features (e.g., location, memory)

---

## 🔧 Dependencies
Basic scientific Python stack:
- `numpy`
- `matplotlib`

You can install these with:
```bash
pip install numpy matplotlib
```

---


