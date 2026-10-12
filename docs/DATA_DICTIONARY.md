# Data dictionary

`results/simulation.csv` contains one row per simulation step.

| Column | Meaning |
|---|---|
| `step` | Sequential time index, 0–239 |
| `inflow` | Simulated material entering per step |
| `outflow` | Simulated measured material leaving per step |
| `true_leak` | Injected loss: 0 before step 120, then 0.42 |
| `measured_level` | Simulated tank level with Gaussian noise |
| `residual` | Predicted minus measured next level |
| `detected` | 1 after the persistent threshold rule alarms, otherwise 0 |

`threshold_sweep.csv` contains threshold, precision, recall, and detection delay. Blank delay means no alarm occurred. `metrics.json` records the primary operating point and explicitly labels the data as synthetic.
