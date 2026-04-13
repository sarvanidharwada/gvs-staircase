import pytest
from staircase.core import Staircase

def test_intensity_decreases_after_n_down():
    """(1) intensity decreases after n_down consecutive correct."""
    sc = Staircase(start=10.0, step=2.0, n_down=2, n_up=1)
    
    # 1st correct response: shouldn't step down yet (needs 2)
    sc.update(True)
    assert sc.intensity == 10.0
    
    # 2nd correct response: should step down by 2.0
    sc.update(True)
    assert sc.intensity == 8.0

def test_intensity_increases_after_n_up():
    """(2) intensity increases after n_up consecutive wrong."""
    sc = Staircase(start=10.0, step=2.0, n_down=2, n_up=1)
    
    # 1st wrong response: should step up immediately since n_up=1
    sc.update(False)
    assert sc.intensity == 12.0

def test_reversals_are_detected_correctly():
    """(3) reversals are detected correctly when direction flips."""
    sc = Staircase(start=10.0, step=2.0, n_down=1, n_up=1)
    
    sc.update(True)  # Steps down to 8.0 (Initial direction)
    sc.update(False) # Reverses! Ascends to 10.0. Old intensity 8.0 is a reversal.
    sc.update(True)  # Reverses! Descends to 8.0. Old intensity 10.0 is a reversal.
    
    assert sc.n_reversals == 2
    assert sc.reversal_values == [8.0, 10.0]

def test_step_size_halves():
    """(4) step size halves after step_shrink_after reversals."""
    sc = Staircase(start=10.0, step=2.0, n_down=1, n_up=1, step_shrink_after=2)
    
    sc.update(True)   # Step down -> 8.0
    sc.update(False)  # Reversal 1 -> 10.0
    sc.update(True)   # Reversal 2 (at 10.0). Step shrinks to 1.0. Descends by 1.0 -> 9.0
    
    assert sc.intensity == 9.0
    
    # Further check: subsequent steps use the new step size
    sc.update(True)   # No reversal, descends by 1.0 -> 8.0
    assert sc.intensity == 8.0

def test_finished_after_n_reversals_stop():
    """(5) finished becomes True after n_reversals_stop reversals."""
    sc = Staircase(start=10.0, step=2.0, n_down=1, n_up=1, n_reversals_stop=3)
    
    sc.update(True)    # 8.0
    assert not sc.finished
    sc.update(False)   # rev 1
    assert not sc.finished
    sc.update(True)    # rev 2
    assert not sc.finished
    sc.update(False)   # rev 3
    
    assert sc.finished
    
    # Updating while finished shouldn't change intensity or add to history
    old_length = len(sc.responses)
    sc.update(False)
    assert len(sc.responses) == old_length

def test_threshold_returns_mean_of_last_k():
    """(6) threshold() returns mean of last k reversals."""
    sc = Staircase(start=10.0, step=2.0, n_down=1, n_up=1)
    
    # Let's force a pattern of reversals: 8, 10, 8, 10
    sc.update(True)   # 8.0
    sc.update(False)  # Rev 1: 8.0
    sc.update(True)   # Rev 2: 10.0
    sc.update(False)  # Rev 3: 8.0
    sc.update(True)   # Rev 4: 10.0
    
    assert sc.reversal_values == [8.0, 10.0, 8.0, 10.0]
    
    # last k=2: mean of (8.0, 10.0) is 9.0
    assert sc.threshold(last_k=2) == 9.0
    # last k=3: mean of (10.0, 8.0, 10.0) is 28/3 = 9.333...
    assert sc.threshold(last_k=3) == pytest.approx(28.0 / 3.0)

def test_intensity_never_goes_below_min_val():
    """(7) intensity never goes below min_val."""
    sc = Staircase(start=2.0, step=2.0, n_down=1, n_up=1, min_val=1.0)
    
    # 2.0 - 2.0 = 0.0, which is below 1.0, so should clamp strictly to 1.0
    sc.update(True)
    assert sc.intensity == 1.0
    
    # Try pushing it further down
    sc.update(True)
    assert sc.intensity == 1.0
