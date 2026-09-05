# Superconducting Resonator Characterization Pipeline

Data analysis notebooks, fitting routines, and processed cryogenic measurement data supporting the MSc Physics thesis:

**"An Experimental Investigation into the Power-Dependent Quality Factors of Superconducting Cavities"**
Imperial College London (2026)

## Overview

This repository contains the analysis routines and single-tone S21 spectroscopy data used to extract power-dependent quality factors (Q<sub>i</sub>, Q<sub>c</sub>, Q<sub>L</sub>) and study two-level system (TLS) loss mechanisms on a ConScience QiB0 chip.

## Key Features

- **Taubin Circle Seeding** — algebraic geometric circle fitting initialized with gradient normalization.
- **Complex Nonlinear Least-Squares** — full S21 resonance extraction with cable delay and phase-rotation corrections.
- **Covariance Error Propagation** — rigorous parameter uncertainty estimation in inverse-loss (1/Q<sub>i</sub>) space.
- **TLS Power Scaling** — nonlinear regression fits to power-dependent loss tangents and temporal stability analysis.

## Repository Layout

```
msc-thesis-resonator-analysis/
├── Data/
│   ├── pwr_sweep_013 (res 1)/      # Power sweep, Resonator 1
│   ├── pwr_sweep_014 (res2)/       # Power sweep, Resonator 2
│   ├── pwr_sweep_021 (res1 low)/   # Low-power extension, Resonator 1
│   ├── pwr_sweep_029 (res2 low)/   # Low-power extension, Resonator 2
│   ├── pwr_sweep_044 .. 049/       # Additional power sweep runs
│   ├── time_sweep_001/             # Repeated fixed-power scans (TLS drift)
│   └── time_sweep_003/             # Repeated fixed-power scans (TLS drift)
│
└── code/
    ├── Figures/                    # Standalone plotting scripts (thesis figures)
    │   ├── 1_double_well_tls.py            # STM double-well potential schematic
    │   ├── 2_kasa_vs_taubin.py             # Kåsa vs. Taubin circle-fit bias comparison
    │   ├── 3_time_sweep_max_fluctuation.py # Per-power max-deviation-from-mean panels
    │   └── 4_loglog_fluctuation_scaling.py # Fitted TLS fluctuation scaling law
    │
    └── data-analysis/
        └── resonator_analysis_covonly.ipynb  # Main pipeline: raw VNA data → Qi/Qc/QL,
                                                # covariance errors, TLS fit
```

### `Data/`

Raw and pre-processed VNA measurements, one subfolder per sweep. Resonator assignment and roles (from `CONFIG` in `resonator_analysis_covonly.ipynb`):

| Folder | Resonator | Tier | Atten | Role |
|---|---|---|---|---|
| `pwr_sweep_013 (res 1)` | Resonator 1 (f<sub>c</sub> ≈ 6.901285 GHz) | `m30_bw100` | −30 dB | Main power sweep |
| `pwr_sweep_021 (res1 low)` | Resonator 1 | `m30_bw10` | −30 dB | Low-power extension |
| `pwr_sweep_047` | Resonator 1 | `m70` | −70 dB | Very-low-power tier |
| `pwr_sweep_048` | Resonator 1 | `m70` | −70 dB | Very-low-power tier |
| `pwr_sweep_049` | Resonator 1 | `m70` | −70 dB | Very-low-power tier |
| `pwr_sweep_014 (res2)` | Resonator 2 (f<sub>c</sub> ≈ 6.718 GHz) | `m30_bw100` | −30 dB | Main power sweep |
| `pwr_sweep_029 (res2 low)` | Resonator 2 | `m30_bw10` | −30 dB | Low-power extension |
| `pwr_sweep_044` | Resonator 2 | `m70` | −70 dB | Very-low-power tier |
| `pwr_sweep_045` | Resonator 2 | `m70` | −70 dB | Very-low-power tier |
| `pwr_sweep_046` | Resonator 2 | `m70` | −70 dB | Very-low-power tier |
| `time_sweep_001` | Resonator 2 | — | −70 dB (assumed) | Repeated fixed-power scans, +3 dBm VNA output |
| `time_sweep_003` | Resonator 2 | — | −70 dB (assumed) | Repeated fixed-power scans, +10 dBm VNA output |

- **`pwr_sweep_*`** — single-tone S21 traces taken across a range of input powers, used to extract the power dependence of Q<sub>i</sub>. The `tier` (`m30_bw100` / `m30_bw10` / `m70`) encodes the manual attenuator setting and VNA IF bandwidth for that sweep.
- **`time_sweep_*`** — repeated S21 traces taken at *fixed* power over time, on Resonator 2 only. These quantify TLS-induced temporal fluctuations in the fitted Q<sub>i</sub>, independent of fit-covariance noise, and the resulting fluctuation-vs-power scaling law is applied to Resonator 1 as a proxy (it has no time sweeps of its own). Note `time_sweep_002` exists on disk but is excluded from the analysis — it was taken while the system was still settling after the power step.

### `code/data-analysis/`

`resonator_analysis_covonly.ipynb` is the main analysis pipeline: it loads the raw sweep data, performs the Taubin-seeded complex nonlinear least-squares fit to the notch-resonator model, propagates covariance errors, and fits the TLS power-scaling model.

### `code/Figures/`

Standalone, self-contained scripts (no dependency on the main notebook) that regenerate the illustrative/schematic thesis figures:

| Script | Figure |
|---|---|
| `1_double_well_tls.py` | Standard Tunneling Model double-well potential, with E<sub>L</sub>, E<sub>R</sub>, V<sub>0</sub>, d, Δ labeled |
| `2_kasa_vs_taubin.py` | Kåsa vs. Taubin algebraic circle-fit bias on well-sampled vs. truncated IQ arcs |
| `3_time_sweep_max_fluctuation.py` | Max deviation from the mean across repeated time-sweep scans, per power |
| `4_loglog_fluctuation_scaling.py` | Empirical fluctuation anchor points mapped to a fitted log-linear scaling law |

Each script writes its output figure to `outputs/` and can be run independently:

```bash
pip install numpy matplotlib scipy circle-fit
python 1_double_well_tls.py
```

## Requirements

```
numpy
scipy
matplotlib
circle-fit
jupyter
```

## Citation

If you use this pipeline, please cite the accompanying thesis (Imperial College London, 2026).
