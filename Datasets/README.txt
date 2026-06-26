# SmartGrid-CyberPhysical-Attack-Dataset (v1.0)

## Overview

This dataset provides synchronized (cyber) and (physical) layer data for multiple cyber attack types in a smart grid environment. It is designed to support research on cyber-physical fusion, and other machine learning approaches for securing smart power grids.

---

## Dataset Structure

The dataset is organized into six folders — each representing one class:

* benign
* backdoor
* brute force
* FDI (False Data Injection)
* ransomware
* reverse shell

Each folder contains:

* cyber.csv — representing cyber-layer behavior (e.g., network traffic, system logs)
* physical.csv — representing physical-layer measurements (e.g., voltage, frequency, power flow)

---

## Applications

* Cyber-Physical Intrusion Detection
* Smart Grid Security Research
* Adversarial Attack & Defense Studies
* Machine Learning for CPS Security

---

## How to Use

1. Load `cyber.csv` and `physical.csv` files for each class.
2. Perform feature engineering and synchronize time indices if needed.
3. Train your ML / GNN models using the multi-domain features.
4. Evaluate detection performance on various attack classes.

---

## License

This dataset is released for (academic research and educational purposes).
For commercial use, please contact the authors.

