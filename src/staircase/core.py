"""Transformed up-down adaptive staircase procedure."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Staircase:
    """N-down / M-up adaptive staircase.

    Parameters
    ----------
    start : float
        Initial stimulus intensity.
    step : float
        Initial step size (always positive; direction is handled internally).
    n_down : int
        Number of consecutive correct responses before stepping down
        (i.e. making the stimulus harder).
    n_up : int
        Number of consecutive incorrect responses before stepping up
        (i.e. making the stimulus easier).
    min_val : float
        Floor value for intensity (intensity is clamped to this minimum).
    step_shrink_after : int
        Halve the step size once this many reversals have occurred.
    n_reversals_stop : int
        Terminate the staircase after this many reversals.
    """

    # ── configurable parameters ──────────────────────────────────────
    start: float
    step: float
    n_down: int = 2
    n_up: int = 1
    min_val: float = 0.0
    step_shrink_after: int = 2
    n_reversals_stop: int = 8

    # ── internal bookkeeping (not set by caller) ─────────────────────
    _intensity: float = field(init=False, repr=False)
    _step_size: float = field(init=False, repr=False)
    _consecutive_correct: int = field(init=False, default=0, repr=False)
    _consecutive_incorrect: int = field(init=False, default=0, repr=False)
    _last_direction: int = field(init=False, default=0, repr=False)

    # ── public history ───────────────────────────────────────────────
    intensities: list[float] = field(init=False, default_factory=list)
    responses: list[bool] = field(init=False, default_factory=list)
    reversal_indices: list[int] = field(init=False, default_factory=list)
    reversal_values: list[float] = field(init=False, default_factory=list)

    # ── initialisation ───────────────────────────────────────────────
    def __post_init__(self) -> None:
        self._intensity = self.start
        self._step_size = self.step
        # Record the starting intensity as trial-0 level.
        self.intensities = [self.start]

    # ── public properties ────────────────────────────────────────────
    @property
    def intensity(self) -> float:
        """Current stimulus intensity (i.e. the level for the next trial)."""
        return self._intensity

    @property
    def n_reversals(self) -> int:
        """Number of reversals recorded so far."""
        return len(self.reversal_values)

    @property
    def finished(self) -> bool:
        """``True`` when the stopping criterion has been met."""
        return self.n_reversals >= self.n_reversals_stop

    # ── core update rule ─────────────────────────────────────────────
    def update(self, correct: bool) -> None:
        """Register a participant response and advance the staircase.

        Parameters
        ----------
        correct : bool
            Whether the participant responded correctly on the current trial.
        """
        if self.finished:
            return

        self.responses.append(correct)

        # --- determine direction of change (if any) ---
        direction = 0  # 0 = no change, -1 = down, +1 = up

        if correct:
            self._consecutive_correct += 1
            self._consecutive_incorrect = 0
            if self._consecutive_correct >= self.n_down:
                direction = -1  # step down  → harder
                self._consecutive_correct = 0
        else:
            self._consecutive_incorrect += 1
            self._consecutive_correct = 0
            if self._consecutive_incorrect >= self.n_up:
                direction = +1  # step up  → easier
                self._consecutive_incorrect = 0

        # --- detect reversal & possibly shrink step ---
        if direction != 0:
            if self._last_direction != 0 and direction != self._last_direction:
                self.reversal_indices.append(len(self.intensities) - 1)
                self.reversal_values.append(self._intensity)

                # Halve the step size once at the specified reversal count.
                if self.n_reversals == self.step_shrink_after:
                    self._step_size /= 2.0

            self._last_direction = direction

            # Apply the step and clamp to floor.
            self._intensity += direction * self._step_size
            self._intensity = max(self._intensity, self.min_val)

        # Always record the (possibly unchanged) intensity for the next trial.
        self.intensities.append(self._intensity)

    # ── threshold estimate ───────────────────────────────────────────
    def threshold(self, last_k: int = 6) -> float:
        """Estimate threshold from the mean of the last *k* reversal values.

        Parameters
        ----------
        last_k : int
            Number of most-recent reversal values to average.

        Returns
        -------
        float
            Mean of the last *last_k* reversal intensities, or the current
            intensity if no reversals have been recorded yet.
        """
        if not self.reversal_values:
            return self._intensity
        k = min(last_k, len(self.reversal_values))
        return sum(self.reversal_values[-k:]) / k
