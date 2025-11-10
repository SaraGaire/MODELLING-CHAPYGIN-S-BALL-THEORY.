from chaplygin import simulate_model1, simulate_model2, animate_tilted_roll
t, r = simulate_model1("tilted_roll")
t, r, Q, w, g = simulate_model2("time_varying", T=6.0)
animate_tilted_roll(T=6.0)
