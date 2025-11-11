from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from chaplygin import simulate_model2
import numpy as np

app = FastAPI()

# Allow requests from your React dev server (5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Chaplygin Ball Simulation API"}

@app.get("/simulate/{case}")
def simulate(case: str = "tilted_roll", T: float = 6.0):
    """Run a Chaplygin ball simulation and return JSON results."""
    t, r, Q, w, g = simulate_model2(case, T=T, outdir="outputs")
    data = []
    for i in range(len(t)):
        data.append({
            "t": float(t[i]),
            "r": r[i].tolist(),
            "Q": Q[i].tolist(),
            "w": w[i].tolist(),
            "g": g[i].tolist(),
        })
    return {"case": case, "count": len(data), "data": data}
