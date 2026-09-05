# Superconducting Resonator Characterization Pipeline

Data analysis notebooks, fitting routines, and processed cryogenic measurement data supporting the MSc Physics thesis:  
**"An Experimental Investigation into the Power-Dependent Quality Factors of Superconducting Cavities"**  
*Imperial College London (2026)*

## Overview
This repository contains the analysis routines and single-tone $S_{21}$ spectroscopy data used to extract power-dependent quality factors ($Q_{\mathrm{i}}$, $Q_{\mathrm{c}}$, $Q_{\mathrm{L}}$) and study two-level system (TLS) loss mechanisms on a ConScience QiB0 chip.

### Key Features
- **Taubin Circle Seeding:** Algebraic geometric circle fitting initialized with gradient normalization.
- **Complex Nonlinear Least-Squares:** Full $S_{21}$ resonance extraction with cable delay and phase-rotation corrections.
- **Covariance Error Propagation:** Rigorous parameter uncertainty estimation in inverse-loss ($1/Q_{\mathrm{i}}$) space.
- **TLS Power Scaling:** Nonlinear regression fits to power-dependent loss tangents and temporal stability analysis.
