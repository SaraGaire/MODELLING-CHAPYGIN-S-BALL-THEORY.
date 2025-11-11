from chaplygin import simulate_model2, animate_tilted_roll

if __name__ == "__main__":
    # Run all three scenarios (creates CSVs in outputs/)
    for case in ["pure_spin", "tilted_roll", "time_varying"]:
        simulate_model2(case, T=6.0)
    # Make a GIF for tilted_roll
    animate_tilted_roll(T=6.0)
