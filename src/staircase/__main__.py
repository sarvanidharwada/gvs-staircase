"""Main entry point for running the GVS staircase simulation."""

import numpy as np
from pathlib import Path

from staircase.simulate import run_experiment
from staircase.plots import plot_trajectories, plot_recovery

def main() -> None:
    # ── Simulation Defaults ──────────────────────────────────────────
    true_threshold = 1.5  # mA
    slope = 4.0
    n_participants = 50
    seed = 0
    
    # Staircase kwargs for a 2-down, 1-up task
    sc_kwargs = {
        'start': 3.0,              # Initial intensity (mA)
        'step': 0.5,               # Initial step size
        'n_down': 2,
        'n_up': 1,
        'min_val': 0.0,
        'step_shrink_after': 2,
        'n_reversals_stop': 8
    }

    # ── Run Experiment ───────────────────────────────────────────────
    print(f"Running simulation with {n_participants} participants...")
    print(f"Underlying true threshold: {true_threshold} mA, slope={slope}")
    print("-" * 50)
    
    staircases, estimates = run_experiment(
        n_participants=n_participants,
        true_threshold=true_threshold,
        slope=slope,
        seed=seed,
        **sc_kwargs
    )
    
    # ── Compute Summary ──────────────────────────────────────────────
    mean_est = np.mean(estimates)
    sd_est = np.std(estimates, ddof=1)
    bias = mean_est - true_threshold
    
    print("Simulation Summary:")
    print(f"True Threshold : {true_threshold:.3f} mA")
    print(f"Mean Estimate  : {mean_est:.3f} mA")
    print(f"Standard Dev.  : {sd_est:.3f} mA")
    print(f"Bias           : {bias:+.3f} mA")
    print("-" * 50)
    
    # ── Generate Plots ───────────────────────────────────────────────
    # Dynamically find the project root (gvs-staircase/) based on this file's location
    project_root = Path(__file__).resolve().parent.parent.parent
    figures_dir = project_root / 'figures'
    figures_dir.mkdir(exist_ok=True)
    
    traj_path = figures_dir / 'trajectories.png'
    rec_path = figures_dir / 'recovery.png'
    
    print("Generating plots...")
    plot_trajectories(staircases, true_threshold, str(traj_path))
    plot_recovery(estimates, true_threshold, str(rec_path))
    print(f"Saved: {traj_path}")
    print(f"Saved: {rec_path}")

if __name__ == "__main__":
    main()
