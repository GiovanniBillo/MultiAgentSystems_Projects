import random

def gillespie_simulation(state, reactions, Tmax=100):
    time = 0
    trajectory = [(time, state)]
    while time < Tmax:
        propensities = [r['rate'](state) if r['guard'](state) else 0 for r in reactions]
        total_rate = sum(propensities)
        if total_rate == 0:
            break
        time += random.expovariate(total_rate)
        chosen = random.choices(reactions, weights=propensities)[0]
        state = chosen['delta'](state)
        trajectory.append((time, state))
    return trajectory

