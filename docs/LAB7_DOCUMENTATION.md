# Lab 7 — Neural Networks and Deep Learning for HVAC Fault Detection and Diagnostics

**Reg No:** 23/EG/CO/027

## 1. What This Project Solves

Modern buildings rely on **HVAC (Heating, Ventilation, and Air Conditioning)** systems to keep indoor spaces comfortable, healthy, and energy-efficient. 

At the heart of most commercial HVAC setups is the **Air Handling Unit (AHU)** — the component responsible for mixing, filtering, heating/cooling, and distributing air throughout a building.

AHUs are monitored by dozens of sensors (temperature, damper position, fan speed, valve control signals, etc.). Over time, components like dampers, filters, coils, fans, and sensors can degrade or fail. These faults are often **subtle** indicating that it is less likely to be noticed by most sensors.

Traditional fault detection approaches which include manual inspection, scheduled preventive maintenance, and rule-based BMS alarms struggle to scale in large sensor-rich buildings and often only catch faults **after** performance has already degraded. This lab builds an **Artificial Neural Network (ANN)** that learns the relationship between multiple sensor readings simultaneously, so it can flag faulted vs. unfaulted operation automatically and in near real time — supporting predictive maintenance rather than reactive repair.

**In short: this lab trains a binary classifier that takes AHU sensor readings as input and predicts whether the AHU is operating normally (`0`) or is faulted (`1`).**

---

## 2. Engineering Background (Why the Features Matter)

| Concept | Summary |
|---|---|
| **AHU** | The "lungs" of an HVAC system — mixes outdoor and return air, filters it, heats/cools it via coils, and pushes it through ducts via a supply fan. |
| **Dampers** | Movable flaps controlling how much outdoor vs. return air is mixed. A stuck damper causes abnormal mixed-air temperatures and wasted energy. |
| **Filters** | Remove dust/particulates; clogging reduces airflow and increases fan strain over time. |
| **Cooling/Heating Coils** | Exchange heat with chilled/hot water from a chiller/boiler; fouling or valve failure prevents the AHU from hitting target supply air temperature. |
| **Supply Fan** | Pushes conditioned air into the building; bearing wear or motor failure reduces airflow and comfort. |
| **Sensors** | Measure temperature, humidity, pressure, and airflow; sensor drift/failure can cause the controller to make *wrong* decisions even when the physical equipment is fine. |

Faults rarely show up as one sensor breaching a limit — they show up as a **pattern across several correlated sensors** (e.g., mixed air temperature no longer sitting between outdoor and return air temperature as expected). This is exactly the kind of nonlinear, multi-variable relationship a neural network is suited to learn, which is why an ANN — rather than simple if/else threshold rules — was chosen for this lab.

---

## 3. Dataset

- **Source file:** `SZCAV.csv` (single-zone constant air volume AHU sensor data)
- **Target variable:** `faulted` (binary: 0 = normal, 1 = fault present)
- **Features (after renaming columns):**
  - `datetime` *(dropped before training — timestamp only)*
  - `supply_air_temp`, `supply_air_temp_heating_sp`, `supply_air_temp_cooling_sp`
  - `outdoor_air_temp`, `mixed_air_temp`, `return_air_temp`
  - `supply_fan_status`, `supply_fan_speed_ctrl_sig`
  - `outdoor_damper_ctrl_sig`, `return_damper_ctrl_sig`, `exhaust_damper_ctrl_sig`
  - `cooling_valve_ctrl_sig`, `heating_valve_ctrl_sig`
  - `occupancy_mode`

**Data cleaning performed:**
- Explored the dataset with a yData/pandas profiling report to surface data quality issues.

- `mixed_air_temp` contained non-numeric strings — coerced to numeric with `pd.to_numeric(..., errors='coerce')`, and rows that became `NaN` were dropped.

- Features (`X`) and target (`y`) were separated, dropping `datetime` and `faulted` from `X`.

---

## 4. Methodology

### 4.1 Train/Test Split
- 80/20 split via `train_test_split`, **stratified on `y`** to preserve the class balance of faulted vs. unfaulted samples in both sets.

### 4.2 Feature Scaling
- `StandardScaler` fit on `X_train` and applied to both `X_train` and `X_test` (fit only on training data to avoid data leakage).
- Scaled arrays were reconstructed into DataFrames for sanity-checking via `.describe()`.

### 4.3 Model Architecture (Artificial Neural Network)

```
Input Layer        → shape = (number of features,)
Hidden Layer 1      → 12 neurons, ReLU activation
Hidden Layer 2      → 8 neurons, ReLU activation
Output Layer        → 1 neuron, Sigmoid activation (binary classification)
```

- **Framework:** TensorFlow / Keras `Sequential` API
- **Optimizer:** Adam (`learning_rate = 0.001`)
- **Loss function:** Binary Crossentropy
- **Metric:** Accuracy

### 4.4 Training
- `batch_size = 256`, `epochs = 100`, `validation_split = 0.2`
- Verbose logging (`verbose=1`) was used to observe per-epoch accuracy/loss; setting `verbose=0` suppresses this output entirely.

---

## 5. Results

Two training runs were logged and compared:

| Run | Train Accuracy (start → end) | Train Loss (start → end) | Validation Accuracy |
|---|---|---|---|
| Run 1 | 99.37% → 99.63% | 0.0197 → 0.0107 | ~99.6% |
| Run 2 | 99.68% → 99.92% | 0.0104 → 0.0051 | ~99.91% |

**Evaluation on the held-out test set** included:
- Confusion matrix (visualized as a Seaborn heatmap, saved to `../output/png_files/ann_confusion_matrix.png`)
- Accuracy, Precision, Recall, F1-Score, and a full `classification_report`
- **False Negative Rate (FNR)** and **False Positive Rate (FPR)** were explicitly computed — important in fault detection because a missed fault (false negative) is typically more costly than a false alarm.

**Observed run-to-run variation** (small differences in accuracy/loss between runs) is expected and attributed to:
- Random weight initialization
- Data shuffling during training
- Mini-batch stochasticity
- The stochastic nature of the Adam optimizer
- Continued learning if a model is retrained without reinitializing weights

Despite these minor fluctuations, all runs showed the same overall trend: steadily increasing accuracy and decreasing loss, indicating **stable, effective learning** rather than random noise.

---

## 6. Repository / File Notes

- **Notebook:** `lab7_hvac_23_EG_CO_027.ipynb` *(or equivalent — rename to match your actual file)*
- **Dataset path expected:** `../datasets/raw/SZCAV.csv`
- **Output path expected:** `../output/png_files/ann_confusion_matrix.png`
- Ensure these relative paths exist (or are updated) when cloning/running the notebook fresh.

**Dependencies:** `numpy`, `pandas`, `tensorflow`, `matplotlib`, `seaborn`, `scikit-learn`

---

## 7. Key Takeaways for Anyone Reading This Documentation

1. This project is a **binary fault classifier** for AHU sensors, not a full HVAC control system — it flags faulted vs. normal operation from sensor readings.
2. A neural network was chosen over rule-based thresholds because HVAC faults often only appear in the **combined relationship** between several sensors, not in any single reading.
3. The model achieved very high accuracy (>99%) on both training and test data across multiple runs, with the second run performing slightly better than the first.
4. FNR and FPR were tracked deliberately, since in a real deployment, missing an actual fault (false negative) has higher operational cost than a false alarm.
5. The neural network is intended to **support**, not replace, HVAC engineers and technicians — it acts as an early-warning layer within a broader predictive maintenance strategy.

---

## 8. Limitations & Next Steps

- Model was trained on a single-zone AHU dataset (`SZCAV`); generalization to other AHU configurations is untested.
- No hyperparameter tuning (layer sizes, learning rate, epochs) was systematically explored — current architecture (12 → 8 → 1) was a first-pass design.
- Fault types are treated as a single binary label; a natural extension would be **multi-class fault diagnosis** (identifying *which* component failed, not just *that* a fault occurred).
- Consider k-fold cross-validation to get a more robust estimate of generalization performance beyond a single train/test split.
