# gvs-staircase

Analyse the effect of galvanic vestibular stimulation (GVS) on stair-climbing biomechanics. This project simulates an adaptive psychophysical staircase procedure to robustly estimate perceptual thresholds. By modelling participant responses with a logistic psychometric function, we can evaluate the reliability and bias of threshold recovery methods before deploying them in physical experimental designs.

## Methodology

This simulation employs a **transformed up-down staircase** procedure to adaptively target specific performance levels. Unlike simple staircases (1-down, 1-up) which converge on 50% performance, transformed staircases change the stimulus intensity based on specific strings of correct or incorrect responses.

For example, a **3-down, 1-up** staircase design is widely used because it converges on approximately 79.4% correct performance. In this scheme, the stimulus intensity decreases (making the task harder) only after three consecutive correct responses, but increases (making the task easier) after a single incorrect response. At equilibrium, the probability of stepping down must equal the probability of stepping up: $p^3 = 0.5$. Solving for $p$ yields $p = \sqrt[3]{0.5} \approx 0.7937$, or 79.4%.

This repository implements configurable N-down/M-up logic alongside dynamic step-shrinkage rules and reversal-based stopping criteria, providing a highly flexible engine for designing threshold experiments.

## Installation

Ensure you have Python installed, then install the core dependencies via `pip`:

```bash
pip install -r requirements.txt
```

## Usage

You can run the full multi-participant simulation using the provided module entry point:

```bash
python -m staircase
```

This script will run with sensible defaults, simulate a cohort of participants, compute error and bias statistics, and generate visualizations in the `figures/` directory.

## Simulation Outputs

### Staircase Trajectories

![Staircase Trajectories](figures/trajectories.png)
*Trial-by-trial intensity trajectories for simulated participants. The red markers indicate "reversals"—points where the sequence of correctness flips the direction of the staircase. Notice how the step size halves after a set number of initial reversals to finer-tune the target estimate.*

### Threshold Recovery

![Threshold Recovery](figures/recovery.png)
*A histogram comparing the empirically recovered threshold estimates against the known underlying true threshold.*

When running the default simulation with a 50-participant cohort (using a 2-down, 1-up staircase), we obtain an output profile similar to the following:

```text
Simulation Summary:
True Threshold : 1.500 mA
Mean Estimate  : 1.827 mA
Standard Dev.  : 0.146 mA
Bias           : +0.327 mA
```

The threshold recovery plot visually demonstrates the mechanics of the staircase procedure. In this example, we observe a consistent, deliberate tracking bias (roughly `+0.327 mA`) above the true 50% midpoint threshold. This occurs precisely because the 2-down, 1-up sequence converges precisely on the $\approx 70.7\%$ performance mark lying further up the logistic psychometric curve. This clearly illustrates the value of simulation: allowing researchers to accurately quantify intrinsic experimental biases prior to deploying clinical trials.

## References

Levitt, H. (1971). Transformed up-down methods in psychoacoustics. *The Journal of the Acoustical society of America*, 49(2B), 467-477.
