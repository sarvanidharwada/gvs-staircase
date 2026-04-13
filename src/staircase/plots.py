"""Plotting utilities for staircase simulation."""

import numpy as np
import matplotlib.pyplot as plt
from typing import List
from staircase.core import Staircase

def plot_trajectories(staircases: List[Staircase], true_threshold: float, out_path: str) -> None:
    """
    Plot the trial-by-trial intensity trajectories for up to the first 5 participants.
    
    Parameters
    ----------
    staircases : List[Staircase]
        A list of completed Staircase objects.
    true_threshold : float
        The underlying true threshold (for the horizontal reference line).
    out_path : str
        File path to save the generated plot.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    n_plot = min(5, len(staircases))
    for i in range(n_plot):
        sc = staircases[i]
        trials = np.arange(1, len(sc.intensities) + 1)
        
        # Plot the main trajectory
        ax.plot(trials, sc.intensities, marker='.', alpha=0.7, label=f'Participant {i+1}')
        
        # Plot markers at reversal points
        if sc.reversal_indices:
            # sc.reversal_indices correspond to the list index in sc.intensities
            rev_trials = [trials[idx] for idx in sc.reversal_indices]
            if i == 0:
                ax.plot(rev_trials, sc.reversal_values, 'ro', fillstyle='none', markersize=8, label='Reversal')
            else:
                ax.plot(rev_trials, sc.reversal_values, 'ro', fillstyle='none', markersize=8)

    # Plot true threshold reference
    ax.axhline(true_threshold, color='black', linestyle='--', alpha=0.8, label=f'True Threshold ({true_threshold})')
    
    ax.set_xlabel('Trial Number')
    ax.set_ylabel('Stimulus Intensity')
    ax.set_title(f'Staircase Trajectories (First {n_plot} Participants)')
    
    # Deduplicate legend
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='best')
    
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_recovery(estimates: np.ndarray, true_threshold: float, out_path: str) -> None:
    """
    Plot a histogram of recovered threshold estimates compared to the true value.
    
    Parameters
    ----------
    estimates : np.ndarray
        Array containing the final estimated thresholds for all participants.
    true_threshold : float
        The underlying true threshold used in the simulation.
    out_path : str
        File path to save the generated plot.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Histogram of estimates
    ax.hist(estimates, bins='auto', color='#4C72B0', edgecolor='white', alpha=0.8)
    
    # Vertical lines for true vs empirical mean
    mean_est = np.mean(estimates)
    ax.axvline(true_threshold, color='black', linestyle='--', linewidth=2, label=f'True Threshold: {true_threshold:.2f}')
    ax.axvline(mean_est, color='#C44E52', linestyle=':', linewidth=2, label=f'Mean Estimate: {mean_est:.2f}')
    
    ax.set_xlabel('Estimated Threshold')
    ax.set_ylabel('Frequency')
    ax.set_title('Recovery of Underlying Threshold Across Participants')
    ax.legend()
    
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
