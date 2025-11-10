import numpy as np
from numpy.linalg import inv

def skew(w):
    return np.array([[0, -w[2], w[1]],
                     [w[2], 0, -w[0]],
                     [-w[1], w[0], 0]], float)

def A_of_gamma(I_diag, m, R, g):
    I = np.diag(I_diag)
    ggT = np.outer(g, g)
    return I + m * R**2 * (np.eye(3) - ggT)

def rhs(t, y, m, R, I, drive=None):
    M = y[0:3]
    g = y[3:6]
    Q = y[6:15].reshape(3, 3)
    r = y[15:18]

    A = A_of_gamma(I, m, R, g)
    w = inv(A) @ M
    if drive is not None:
        w = w + drive(t)

    dM = np.cross(M, w)
    dg = np.cross(g, w)
    dQ = Q @ skew(w)              # Lie-group style
    dr = -R * (Q @ np.cross(g, w))  # no-slip

    return np.r_[dM, dg, dQ.reshape(-1), dr]

def drive_func(t):
    """Example time-varying modulation (UI parity)."""
    return np.array([0.2*np.sin(0.5*t), 0.2*np.cos(0.5*t), 0.0])

def initial_state(case, I=(0.4, 0.5, 0.6), m=1.0, R=1.0):
    if case == "pure_spin":
        Q0 = np.eye(3); w0 = np.array([0.0, 0.0, 8.0])
    elif case == "tilted_roll":
        th = np.deg2rad(15)
        Rx = np.array([[1,0,0],[0,np.cos(th),-np.sin(th)],[0,np.sin(th),np.cos(th)]])
        Q0 = Rx; w0 = np.array([0.0, 2.0, 6.0])
    elif case == "time_varying":
        Q0 = np.eye(3); w0 = np.array([0.0, 0.0, 5.0])
    else:
        raise ValueError("unknown case")

    g0 = Q0.T @ np.array([0, 0, 1.0])
    A0 = A_of_gamma(I, m, R, g0)
    M0 = A0 @ w0
    r0 = np.array([0.0, 0.0, R])
    return np.r_[M0, g0, Q0.reshape(-1), r0]
