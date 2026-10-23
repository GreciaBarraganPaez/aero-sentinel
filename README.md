# Aero Sentinel ✈️

**Early warning of aircraft engine degradation using machine learning and NASA C-MAPSS sensor data.**

A Data Mining and Machine Learning course project investigating patterns in simulated turbofan engine sensor data and evaluating machine-learning approaches for advance warning relative to recorded engine failures.

## Project tracking

- [Development board](https://github.com/users/GreciaBarraganPaez/projects/1/views/1)
- [Issues / backlog](https://github.com/GreciaBarraganPaez/aero-sentinel/issues)
- [Sprint plan and working agreement](docs/project-management.md)
- [Sprint 1 development and evidence log](docs/logs/sprint-01.md)

## Data

Dataset: [NASA C-MAPSS](https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data).

We plan to start with FD001. Downloaded raw data should be kept locally under `data/raw/` and should not be committed to Git.

**Important limitation:** C-MAPSS is simulated run-to-failure data and does not label the exact physical onset of degradation. The project will evaluate predictions or warnings against recorded failure cycles, not claim to identify the true physical onset of damage.

## Status

Sprint 1 — scope definition, dataset setup and exploratory analysis. Results will be documented as work is completed.
