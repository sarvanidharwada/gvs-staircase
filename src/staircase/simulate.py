"""Experiment simulation for multiple participants."""

import numpy as np
from typing import Tuple, List
from staircase.core import Staircase
from staircase.observer import simulate_observer

def run_experiment(
    n_participants: int,
    true_threshold: float,
    slope: float,
    seed: int,
    **sc_kwargs
) -> Tuple[List[Staircase], np.ndarray]:
    """
    Run a simulated experiment across multiple participants.

    Parameters
    ----------
    n_participants : int
        Number of simulated observers.
    true_threshold : float
        The underlying actual threshold used for all simulated observers.
    slope : float
        The slope of the psychometric function used for all observers.
    seed : int
        Random seed for reproducibility.
    **sc_kwargs : dict
        Keyword arguments passed to the Staircase constructor for each participant.

    Returns
    -------
    Tuple[List[Staircase], np.ndarray]
        A tuple containing:
        - List of completed Staircase objects
        - A 1D numpy array of the final threshold estimates for each participant
    """
    rng = np.random.default_rng(seed)
    staircases = []
    estimates = []
    
    for _ in range(n_participants):
        sc = simulate_observer(
            true_threshold=true_threshold,
            slope=slope,
            rng=rng,
            **sc_kwargs
        )
        staircases.append(sc)
        estimates.append(sc.threshold())
        
    return staircases, np.array(estimates)
