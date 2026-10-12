# Tank Leak Detection

A dependency-free tank-leak detection demonstration based on a mass-balance residual. The deterministic simulation tracks inflow, outflow, and measured level; a leak begins at step 120, and an alarm is raised after three consecutive residual threshold crossings.

## Run

```bash
python src/run_demo.py
```

Python 3.10 or newer is recommended. No third-party packages are required.

## Reproducible demo result

| Metric | Result |
|---|---:|
| Simulation steps | 240 |
| Precision | 100% |
| Recall | 98.33% |
| Leak begins | Step 120 |
| First alarm | Step 122 |
| Detection delay | 2 steps |

These metrics come from a deterministic synthetic process with Gaussian measurement noise. They demonstrate the detector and reporting pipeline, not performance on a physical tank.

Generated artifacts are committed under `results/`: `metrics.json`, `simulation.csv`, `simulation.svg`, `threshold_sweep.csv`, and `threshold_sweep.svg`.

For academic review, see the [methodology](docs/METHODOLOGY.md), [result interpretation](docs/RESULTS.md), and [data dictionary](docs/DATA_DICTIONARY.md). Run `python -m unittest discover -s tests -v` for an independent detector check.

## Method

The residual compares the predicted next level (`level + inflow - outflow`) with the measured next level. Requiring persistent threshold crossings suppresses isolated noise spikes.

## Next steps

Calibrate sensor units and uncertainty, model tank geometry, validate on fault-injection tests, and add adaptive thresholds for changing operating regimes.
