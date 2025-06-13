import numpy as np
import matplotlib.pyplot as plt
from src.model.state import State
from src.model.reactions import get_reactions
from src.model.gillespie import gillespie_simulation

def consensus(s, Zx, Zy, m, d):
    x_win = (s.x + Zx >= m) and (s.x >= s.y + d)
    y_win = (s.y + Zy >= m) and (s.y >= s.x + d)
    return x_win or y_win

def plot_trajectories(trajectories, T_ave, X_ave, Y_ave, U_ave):
    fig, axs = plt.subplots(3, 1, figsize=(10, 18))
    axs[0].plot(T_ave, X_ave, color='red', linewidth=3, label='Average X')
    axs[1].plot(T_ave, Y_ave, color='green', linewidth=3, label='Average Y')
    axs[2].plot(T_ave, U_ave, color='blue', linewidth=3, label='Average U')

    for traj in trajectories:
        times = [t for t, s in traj]
        xs = [s.x for t, s in traj]
        ys = [s.y for t, s in traj]
        us = [s.u for t, s in traj]
        axs[0].plot(times, xs, color='grey', alpha=0.3)
        axs[1].plot(times, ys, color='grey', alpha=0.3)
        axs[2].plot(times, us, color='grey', alpha=0.3)

    for ax in axs:
        ax.grid(True)
        ax.legend()

    axs[0].set_title('Average Number of X')
    axs[1].set_title('Average Number of Y')
    axs[2].set_title('Average Number of U')
    axs[2].set_xlabel('Time')
    axs[0].set_ylabel('Number of X')
    axs[1].set_ylabel('Number of Y')
    axs[2].set_ylabel('Number of U')

    plt.tight_layout()
    plt.show()

def run_cross_inhibition_simulation(
    cycles=100, Tmax=50, N=100, Nhalf=None, m=50, d=10, h=40,
    Zx=0.1*N, Zy=, qx=None, qy=None, initial_state=None,
    ave_steps=200, plot=False, print_params=True):

    if Nhalf is None:
        Nhalf = N // 2
    if qx is None:
        qx = 1.05 / N
    if qy is None:
        qy = 0.95 / N
    if initial_state is None:
        initial_state = State(Nhalf - Zx, Nhalf - Zy, 0)

    if print_params:
        print("Running Cross-Inhibition Simulation with the following parameters:")
        print(f"  cycles      = {cycles}")
        print(f"  Tmax        = {Tmax}")
        print(f"  N           = {N}")
        print(f"  Nhalf       = {Nhalf}")
        print(f"  m           = {m}")
        print(f"  d           = {d}")
        print(f"  h           = {h}")
        print(f"  Zx          = {Zx}")
        print(f"  Zy          = {Zy}")
        print(f"  qx          = {qx:.5f}")
        print(f"  qy          = {qy:.5f}")
        print(f"  ave_steps   = {ave_steps}")
        print(f"  InitialState= (x={initial_state.x}, y={initial_state.y}, u={initial_state.u})")
        print("="*50)
    
    assert (Zx + Zy + (Nhalf - Zx) + (Nhalf - Zy)) == N, f"Something is wrong: the sum of Zealots, X, Y and undecided is not equal to the number of agents in the system"
    reactions = get_reactions(N, qx, qy, Zx, Zy)
    trajectories = [gillespie_simulation(initial_state, reactions, Tmax) for _ in range(cycles)]

    T_ave = np.linspace(0, Tmax, ave_steps+1)
    X_ave, Y_ave, U_ave = np.zeros(ave_steps+1), np.zeros(ave_steps+1), np.zeros(ave_steps+1)

    robust_consensus_count = 0
    for traj in trajectories:
        holding = False
        hold_start = None
        for i in range(len(traj)-1):
            t0, s0 = traj[i]
            t1, s1 = traj[i+1]
            if consensus(s0, Zx, Zy, m, d):
                if not holding:
                    hold_start = t0
                    holding = True
                elif t1 - hold_start >= h:
                    robust_consensus_count += 1
                    break
            else:
                holding = False
                hold_start = None

    for i, t_point in enumerate(T_ave):
        X_sum, Y_sum, U_sum, count = 0, 0, 0, 0
        for traj in trajectories:
            for j in range(len(traj)-1):
                t0, s0 = traj[j]
                t1, s1 = traj[j+1]
                if t0 <= t_point < t1:
                    X_sum += s0.x
                    Y_sum += s0.y
                    U_sum += s0.u
                    count += 1
                    break
        if count > 0:
            X_ave[i] = X_sum / count
            Y_ave[i] = Y_sum / count
            U_ave[i] = U_sum / count
        else:
            if i > 0:
                X_ave[i], Y_ave[i], U_ave[i] = X_ave[i-1], Y_ave[i-1], U_ave[i-1]
            else:
                X_ave[i], Y_ave[i], U_ave[i] = initial_state.x, initial_state.y, initial_state.u

    print(f"Robust consensus reached {robust_consensus_count} times.")

    if plot:
        plot_trajectories(trajectories, T_ave, X_ave, Y_ave, U_ave)
    
    result = {
        'robust_consensus_count': robust_consensus_count,
        'robust_consensus_prob': robust_consensus_count / len(trajectories)
    }
    print(result)
    return result 

