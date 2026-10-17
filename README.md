# Tank Leak Detection

**Mass-balance residual monitoring with persistent-threshold leak alarms**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Data](https://img.shields.io/badge/data-synthetic-orange) ![Method](https://img.shields.io/badge/method-residual%20monitoring-informational)

## Overview

A lightweight demonstration of **model-based fault detection** for a simulated liquid storage tank. A mass-balance model predicts the next tank level, a residual compares the prediction with noisy measurement, and a persistence condition reduces isolated false alarms.

This example illustrates process monitoring principles; it is not a tested industrial leak-detection product.

## Process model

For one unit-time step, the synthetic tank state is updated by

$$h_{t+1}=h_t+q_{in,t}-q_{out,t}-\ell_t,$$

where $h_t$ is the simulated level and $\ell_t$ is the leak quantity. The predictor omits the leak term and compares its predicted level with the simulated measurement to construct an alarm residual.

### Simulation configuration

| Parameter | Setting |
|---|---:|
| Simulated steps | 240 |
| Initial level | 55 units |
| Leak onset | Step 120 |
| Leak magnitude | 0.42 level units/step |
| Measurement noise SD | 0.035 level units |
| Residual threshold | 0.22 |
| Required consecutive exceedances | 3 |
| Random seed | 23 |

A threshold sweep from 0.10 to 0.50 (steps of 0.05) studies the sensitivity of the decision rule.

## Reported synthetic-demo results

| Metric | Value |
|---|---:|
| Precision | 100% |
| Recall | 98.33% |
| First alarm | Step 122 |
| Detection delay | 2 steps |

![Tank levels and alarm response](results/simulation.svg)

![Residual threshold sensitivity](results/threshold_sweep.svg)

**Interpretation:** A two-step delay reflects the chosen three-exceedance persistence rule. All quantities and results belong to a simplified deterministic simulation; they are not calibrated physical sensor measurements.

## Evaluation artifacts

The [`results/`](results/) directory contains `simulation.csv`, `threshold_sweep.csv`, `metrics.json`, and the figures above.

## Limitations and next steps

The model assumes unit tank geometry and calibrated, synchronized flows and level measurements. Real deployment would require tank geometry, sampling units, measurement uncertainty, disturbances, variable leak rates, and physical fault-injection testing.

## Reproduce the results

```bash
git clone https://github.com/nabinkandel07/Tank-Leak-Detection.git
cd Tank-Leak-Detection
python src/run_demo.py
python -m unittest discover -s tests -v
```

**Requirements:** Python 3.10 or later is recommended. The current demonstration uses only the Python standard library; no third-party dependencies are required.

## Repository structure

```text
.
├── src/run_demo.py       # Runnable demonstration
├── tests/test_demo.py    # Verification tests
├── docs/
│   ├── METHODOLOGY.md    # Model and experimental design
│   ├── RESULTS.md        # Result interpretation and limitations
│   └── DATA_DICTIONARY.md
├── requirements.txt
├── CITATION.cff
└── README.md
```

See the `results/` directory for the committed evaluation artifacts and figures, except the robotics repository, which uses `Results/`.

## Documentation and citation

Detailed assumptions and experimental settings are documented in [Methodology](docs/METHODOLOGY.md). See [Results](docs/RESULTS.md) for interpretation and [Data Dictionary](docs/DATA_DICTIONARY.md) for exported fields. Citation metadata is provided in [CITATION.cff](CITATION.cff).

## Author

**Nabin Kandel**  
Control Science and Engineering, Zhejiang Sci-Tech University  
[GitHub](https://github.com/nabinkandel07) · [Email](mailto:nabinkandel60@gmail.com)
