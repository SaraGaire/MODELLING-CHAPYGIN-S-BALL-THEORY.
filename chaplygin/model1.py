import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from .core import rhs, initial_state

def simulate_model1(case="tilted_roll", T=6.0, I=(0.4,0.5,0.6), m=1.0, R=1.0):
    """Minimal mathematical model; returns (t, r)."""
    y0 = initial_state(case, I, m, R)
    sol = solve_ivp(rhs, (0, T), y0, args=(m, R, I, None), rtol=1e-8, atol=1e-10)
    t = sol.t
    Y = sol.y.T
    r = Y[:, 15:18]
    return t, r

def plot_trajectory(case="tilted_roll", T=6.0):
    t, r = simulate_model1(case, T)
    plt.figure(figsize=(5, 5))
    plt.plot(r[:, 0], r[:, 1], label=case)
    plt.gca().set_aspect("equal")
    plt.xlabel("x"); plt.ylabel("y")
    plt.title("Model 1: Center trajectory")
    plt.grid(True); plt.legend(); plt.show()
