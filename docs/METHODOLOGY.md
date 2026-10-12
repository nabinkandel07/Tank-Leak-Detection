# Methodology

## Research question

Can a persistent mass-balance residual detect a simulated tank leak while avoiding alarms during leak-free operation?

## Process model

The simulation contains 240 unit-time steps and starts at level 55. Inflow and outflow vary smoothly with time. The state update is `next_level = level + inflow - outflow - leak`. A leak of 0.42 level units per step begins at step 120. Gaussian level-measurement noise has standard deviation 0.035; seed 23 makes the experiment repeatable.

## Detector

The residual is the predicted next level minus the measured next level. The primary detector uses threshold 0.22 and requires three consecutive threshold crossings. This persistence rule trades two steps of delay for noise rejection.

## Evaluation

Leak state is positive from step 120 onward. The script reports precision, recall, first detection, and delay. A sensitivity study evaluates thresholds from 0.10 through 0.50 in increments of 0.05 using the identical simulated sequence.

## Limitations

The model assumes synchronized and calibrated flow/level measurements, unit tank area, no evaporation, no unmeasured transfers, and a constant leak after onset. A physical study needs tank geometry, sensor uncertainty, timestamp alignment, variable leaks, and fault-free data across operating regimes.
