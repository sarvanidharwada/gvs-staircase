"""Observer simulation for the staircase procedure."""

import numpy as np
from staircase.core import Staircase

def logistic_pc(intensity: float, threshold: float, slope: float, lapse: float = 0.02) -> float:
    """
    Evaluate a logistic psychometric function to get the probability of a 
    correct response.
    
    Parameters
    ----------
    intensity : float
        Current stimulus intensity.
    threshold : float
        The true threshold of the simulated observer.
    slope : float
        Slope of the psychometric function.
    lapse : float, optional
        Lapse rate (probability of an incorrect response despite high intensity), 
        by default 0.02.
        
    Returns
    -------
    float
        Probability of a correct response, bounded at 1 - lapse.
    """
    # Base logistic function going from 0 to 1
    p = 1.0 / (1.0 + np.exp(-slope * (intensity - threshold)))
    # Scale to upper bound (1 - lapse)
    return p * (1.0 - lapse)

def simulate_observer(true_threshold: float, slope: float, rng: np.random.Generator, **sc_kwargs) -> Staircase:
    """
    Simulate an observer completing a staircase procedure.
    
    Parameters
    ----------
    true_threshold : float
        The underlying actual threshold for the observer.
    slope : float
        The slope of the observer's psychometric function.
    rng : np.random.Generator
        A numpy random number generator instance.
    **sc_kwargs : dict
        Keyword arguments to pass to the Staircase constructor.
        
    Returns
    -------
    Staircase
        The completed staircase object.
    """
    sc = Staircase(**sc_kwargs)
    max_trials = 300
    trials = 0
    
    while not sc.finished and trials < max_trials:
        # Get current probability of being correct
        p_correct = logistic_pc(sc.intensity, true_threshold, slope)
        
        # Draw a random outcome based on p_correct
        correct = rng.random() < p_correct
        
        # Advance the staircase
        sc.update(correct)
        
        trials += 1
        
    return sc
