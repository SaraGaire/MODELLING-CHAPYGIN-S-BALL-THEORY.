import numpy as np
import os
import matplotlib.pyplot as plt
from numpy.linalg import inv
from scipy.integrate import solve_ivp
from matplotlib import animation
from .core import rhs, drive_func, initial_state, A_of_gamma

def simulate_model2(case="tilted_roll", T=8.0, outdir="outputs", rtol=1e-8, atol=1e-10):
    """Full numerics; returns (t, r, Q, w, g) and writes CSV."""
    os.makedirs(outdir, exist_ok=True)
    I = (0.4, 0.5, 0.6); m = 1.0; R = 1.0
    y0 = initial_state(case, I, m, R)
    drive = drive_func if case == "time_varying" else None

    sol = solve_ivp(rhs, (0, T), y0, args=(m, R, I, drive), rtol=rtol, atol=atol)
    Y = sol.y.T
    t = sol.t
    r = Y[:, 15:18]
    Q = Y[:, 6:15].reshape(-1, 3, 3)
    g = Y[:, 3:6]

    # angular velocity over time
    w = np.empty_like(r)
    for k in range(len(t)):
        A = A_of_gamma(I, m, R, g[k])
        w[k] = inv(A) @ Y[k, 0:3]
        if drive is not None:
            w[k] += drive(t[k])

    # CSV export
    header = "t,x,y,z," + ",".join([f"Q{i}{j}" for i in [1,2,3] for j in [1,2,3]]) + ",wx,wy,wz,gx,gy,gz"
    data = np.column_stack([t, r, Q.reshape(-1, 9), w, g])
    np.savetxt(os.path.join(outdir, f"chaplygin_{case}.csv"), data, delimiter=",", header=header, comments="")

    return t, r, Q, w, g

def animate_tilted_roll(T=6.0, out="outputs/model2_tilted_roll.gif"):
    """Create a lightweight 3D attitude GIF for the tilted-roll scenario."""
    t, r, Q, _, _ = simulate_model2("tilted_roll", T)
    # subsample to keep GIF small
    idx = np.linspace(0, len(t) - 1, min(160, len(t))).astype(int)
    r = r[idx]; Q = Q[idx]

    # unit sphere mesh
    phi = np.linspace(0, np.pi, 16)
    th  = np.linspace(0, 2*np.pi, 32)
    xs = np.outer(np.sin(phi), np.cos(th))
    ys = np.outer(np.sin(phi), np.sin(th))
    zs = np.outer(np.cos(phi), np.ones_like(th))

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title("Model 2: 3D Attitude (tilted_roll)")
    ax.set_xlim(-2, 2); ax.set_ylim(-2, 2); ax.set_zlim(0, 2.5)
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")

    traj, = ax.plot([], [], [], 'b-', lw=1)
    ax_x, = ax.plot([], [], [], 'r-', lw=2)
    ax_y, = ax.plot([], [], [], 'g-', lw=2)
    ax_z, = ax.plot([], [], [], 'b-', lw=2)
    sphere = [None]

    def init():
        traj.set_data([], []); traj.set_3d_properties([])
        return (traj, ax_x, ax_y, ax_z)

    def update(i):
        traj.set_data(r[:i, 0], r[:i, 1]); traj.set_3d_properties(r[:i, 2])
        Qi = Q[i]; ci = r[i]; L = 0.6
        ends = [ci + L*Qi[:, 0], ci + L*Qi[:, 1], ci + L*Qi[:, 2]]
        ax_x.set_data([ci[0], ends[0][0]], [ci[1], ends[0][1]]); ax_x.set_3d_properties([ci[2], ends[0][2]])
        ax_y.set_data([ci[0], ends[1][0]], [ci[1], ends[1][1]]); ax_y.set_3d_properties([ci[2], ends[1][2]])
        ax_z.set_data([ci[0], ends[2][0]], [ci[1], ends[2][1]]); ax_z.set_3d_properties([ci[2], ends[2][2]])
        if sphere[0] is not None:
            try: sphere[0].remove()
            except Exception: pass
        sphere[0] = ax.plot_surface(xs+ci[0], ys+ci[1], zs+ci[2],
                                    color='lightsteelblue', alpha=0.6, edgecolor='none')
        return (traj, ax_x, ax_y, ax_z, sphere[0])

    ani = animation.FuncAnimation(fig, update, frames=len(r), init_func=init, interval=50, blit=False)
    ani.save(out, writer=animation.PillowWriter(fps=20))
    print("Saved:", out)
