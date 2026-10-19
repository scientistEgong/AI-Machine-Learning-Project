# AI-Powered Plant Disease Detection — Inference Engine

A deep-learning application for classifying plant leaf images into supported healthy or diseased categories. The project packages trained TensorFlow/Keras models behind a Streamlit interface so users can upload a leaf image, review a prediction, compare model outputs, and consult a reference library of plant-disease information. The application is available as a hosted Streamlit demo and as a Docker image published to Docker Hub.

- **Live application:** https://ai-powered-plant-detection-inference-engine.streamlit.app/
- **GitHub repository:** https://github.com/scientistEgong/AI-Machine-Learning-Project
- **Docker Hub image:** https://hub.docker.com/r/scientist1/ai-plant-disease-detection-inference-engine

> **Important:** This is an educational machine-learning demonstration and decision-support prototype, not a confirmed agricultural diagnosis. Do not use its prediction alone to decide on pesticide application, crop destruction, or other costly interventions. Confirm suspected disease with a qualified agricultural extension officer or plant-health specialist.

## Contents

- [Project overview](#project-overview)
- [Features](#features)
- [Dataset and supported classes](#dataset-and-supported-classes)
- [Models and recorded results](#models-and-recorded-results)
- [Inference workflow](#inference-workflow)
- [Technology stack](#technology-stack)
- [Repository structure](#repository-structure)
- [Run locally](#run-locally)
- [Using the application](#using-the-application)
- [Limitations](#limitations)
- [Improvement roadmap](#improvement-roadmap)
- [Deployment and containerization](#deployment-and-containerization)
- [Security status](#security-status)
- [Reproducibility and responsible use](#reproducibility-and-responsible-use)
- [Contributing](#contributing)
- [License](#license)

## Project overview

Plant diseases can reduce crop yield and quality, while visually similar symptoms can be difficult for non-specialists to distinguish. This project explores how computer vision can support an initial assessment by learning patterns from labelled leaf images.

The repository contains a Streamlit inference application and three saved models developed for a 29-class subset of the PlantVillage dataset. Streamlit provides the browser interface, and TensorFlow/Keras loads the trained models and produces predictions.

The system is designed to answer a limited question:

**“Which of the plant-health categories learned by the model most closely matches this uploaded image?”**

It does not establish the cause of every plant symptom, detect every possible disease, or replace field inspection and expert diagnosis.

## Features

- **Image inference:** Upload a JPG, JPEG, or PNG leaf image.
- **Image preprocessing:** Convert to RGB, resize to the configured input size, and prepare a batch for inference.
- **Multiple model options:** Select the Custom CNN, Feature Extraction, or Fine-Tuned MobileNetV3 model.
- **Model comparison:** Compare supported models through the application's comparison workflow.
- **Top predictions:** View ranked classes and their model scores.
- **Disease reference library:** Consult stored descriptions, symptoms, causes, treatment information, and prevention suggestions.
- **Performance page:** Explore the model-performance information exposed by the interface.
- **PDF reports:** Generate a report containing the predicted class, score, available disease information, and optionally the submitted image.
- **Browser interface:** Use the application without manually running inference commands.

Disease reference content is informational, not a live agricultural advisory service. Recommendations may not be appropriate for every location, crop variety, growth stage, or local regulation.

## Dataset and supported classes

The configured dataset is the **PlantVillage dataset**. The current class mapping contains **29 categories** covering selected apple, bell pepper, cherry, corn (maize), grape, peach, potato, strawberry, and tomato conditions. It includes healthy leaves and disease categories such as apple scab, bacterial spot, black rot, late blight, powdery mildew, leaf scorch, and tomato yellow leaf curl virus.

The exact ordered labels used during inference are stored in `artifacts/class_names.json`.

### Input expectations

- **File types:** JPG, JPEG, PNG
- **Configured input dimensions:** 128 × 128 pixels
- **Colour representation:** RGB
- **Output:** Ranked supported classes and model scores

The training dataset is not included as a raw image directory. The repository contains trained model files and supporting artifacts. Reproducing training from scratch requires obtaining the appropriate dataset, checking its provenance and usage terms, and following a documented training procedure.

## Models and recorded results

| Model option | Approach | Purpose |
|---|---|---|
| **Custom CNN** | Convolutional neural network trained from scratch | Provides a project-specific baseline. |
| **Feature Extraction** | MobileNetV3 transfer learning with a frozen feature extractor | Reuses pretrained visual features while training a task-specific classifier. |
| **Fine-Tuned MobileNetV3** | Transfer learning with fine-tuning | Adapts a pretrained network to the leaf-classification task. |

Model paths are configured in `config.py`; model artifacts are stored in `models/`.

### Recorded Custom CNN metrics

The committed artifact `artifacts/custom_cnn_results.json` records:

| Metric | Recorded value |
|---|---:|
| Test accuracy | 97.86% |
| Validation accuracy | 97.70% |
| Validation loss | 0.0751 |
| Recorded training epochs | 20 |

The metadata artifact records approximately **93.67% validation accuracy** for the MobileNetV3 feature-extraction model.

These are recorded results from particular evaluation runs, not guarantees of performance on new photographs or farms. Accuracy alone does not show which classes are confused, whether minority classes perform poorly, or how well the model generalizes. A fair model comparison should use the same held-out test set and report per-class precision and recall, macro-F1, a confusion matrix, and the evaluation protocol.

## Inference workflow

The primary prediction path is implemented in `utils/preprocess.py` and `utils/predictor.py`, with settings in `config.py`.

1. **Upload:** The user submits a leaf image through Streamlit.
2. **Validate:** The application checks the supported file extension.
3. **Prepare:** The image is opened, converted to RGB, resized to 128 × 128, converted to a NumPy array, and given a batch dimension.
4. **Load:** Saved Keras models are loaded from the configured paths. Streamlit resource caching helps avoid repeated loading during normal reruns.
5. **Predict:** The selected model returns class scores.
6. **Rank:** The application sorts the scores and returns the top five class labels and scores.
7. **Present:** The interface displays the leading prediction, alternatives, and associated reference information. A PDF report can also be generated.

The preprocessing code intentionally does not apply an additional normalization step because the project comments indicate preprocessing is incorporated into the trained models. Any replacement model must preserve and verify the preprocessing contract used during training.

A displayed confidence score is a model output. Unless calibration has been explicitly evaluated, it should **not** be interpreted as a calibrated probability that the prediction is correct.

## Technology stack

- **Python** — application and inference logic
- **Streamlit** — interactive browser interface
- **TensorFlow / Keras** — neural-network inference
- **MobileNetV3** — transfer-learning backbone used by two model options
- **NumPy** — arrays and score ranking
- **Pillow (PIL)** — image decoding and resizing
- **ReportLab** — PDF generation
- **JSON artifacts** — class mapping, model metadata, recorded metrics, and disease information
- **Git and GitHub** — source control and hosting
- **Streamlit Community Cloud** — hosted application deployment

## Repository structure

```text
AI-Machine-Learning-Project/
├── app.py                         # Streamlit interface and page routing
├── config.py                      # App settings, model paths, labels, input size
├── requirements.txt               # Python package requirements
├── Dockerfile                      # Container build instructions
├── .dockerignore                   # Files excluded from Docker build context
├── models/
│   ├── custom_cnn_final.keras
│   ├── tl_feature_extraction_final.keras
│   ├── tl_finetuned_final.keras
│   └── mobilenetv3_finetuned_final.keras
├── artifacts/
│   ├── class_names.json            # Ordered inference labels
│   ├── custom_cnn_results.json     # Recorded Custom CNN metrics
│   ├── disease_info.json           # Disease reference content
│   └── model_metadata.json         # Model and dataset metadata
├── assets/
│   └── logo.png
├── utils/
│   ├── predictor.py                # Model loading and prediction ranking
│   ├── preprocess.py               # Image validation and preprocessing
│   ├── disease_info.py             # Disease reference lookup
│   ├── reports.py                  # PDF report generation
│   ├── charts.py                   # Chart helpers
│   └── helpers.py                  # Shared utilities
├── notebooks/                      # Project and machine-learning lab notebooks
├── output/                         # Saved notebook visualizations
├── docs/                           # Supporting documentation
├── .gitignore
├── LICENSE
└── README.md
```

Some notebooks and output files relate to broader machine-learning coursework rather than being runtime requirements for the deployed inference interface. The essential runtime components are the entry point, configuration, utility modules, required artifacts, model files, and dependencies. The repository may contain additional model artifacts beyond the three exposed in the primary model selector.

## Run locally

### Prerequisites

- Git
- Python version compatible with the selected TensorFlow build
- pip
- Sufficient memory and disk space for TensorFlow and the saved models

**Dependency note:** The model metadata records TensorFlow 2.20.0 for an earlier training environment, while the current `requirements.txt` pins TensorFlow 2.21.0. Reconcile and test the training and inference environments before treating the setup as reproducible.

### 1. Clone the repository

```bash
git clone https://github.com/scientistEgong/AI-Machine-Learning-Project.git
cd AI-Machine-Learning-Project
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

**macOS/Linux:**

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Python 3.13 is a suggested starting point, not a guarantee that every pinned package will install. Use a Python/TensorFlow combination verified for the target environment.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

The current requirements file includes a broad set of packages used across the repository, including notebook and analysis dependencies. It is not yet a minimal inference-only requirements file. If installation fails, check the Python version and the exact package error rather than changing packages randomly.

### 4. Start Streamlit

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit, commonly `http://localhost:8501`.

### 5. Verify required files

Check that the model files referenced in `config.py` exist under `models/`, and that `artifacts/class_names.json` and `artifacts/disease_info.json` exist. Missing or incompatible model files can prevent inference from working.

## Using the application

1. Open the live app or run it locally.
2. Navigate to **Disease Detection**.
3. Upload a clear, well-lit photograph of a leaf. A single visible leaf is a useful starting point.
4. Select one supported model or the model-comparison option.
5. Review the predicted class, score, and alternative predictions.
6. Consult the Disease Library for related reference information.
7. Generate a PDF report if needed for review or record keeping.
8. If the result conflicts with visible symptoms or field observations, treat it as uncertain and seek expert assessment.

For testing, use healthy leaves, supported disease examples, images with different lighting conditions, and out-of-scope images. The current classifier may still assign an unsupported image to one of its known classes.

## Limitations

### 1. Limited class coverage

The model recognises only the 29 categories represented in its class mapping. It cannot reliably identify a crop or disease it was not trained to recognise. Similar symptoms can result from pests, nutrient deficiencies, drought, chemical injury, or multiple causes.

### 2. Dataset-to-field generalization

PlantVillage images do not represent every field condition. Real-world photos can contain busy backgrounds, multiple leaves, unusual angles, shadows, blur, mixed symptoms, and different cameras. The recorded metrics do not establish performance under all these conditions.

### 3. Evaluation uncertainty

High accuracy on one test split does not guarantee high accuracy on new data. Performance depends on class distribution, split strategy, possible near-duplicate images, and the evaluation protocol. Independent external validation is necessary before making strong field-performance claims.

### 4. Confidence can be misinterpreted

The displayed score is not a guarantee of correctness. Calibration has not been established, and the application may show a high score for an out-of-scope image.

### 5. Input validation can be strengthened

The current validation primarily checks the filename extension. More robust validation should inspect decoded image content, handle corrupted files, limit file size and image dimensions, and report clear errors for unsupported inputs.

### 6. Disease information is reference content

Descriptions and treatment/prevention suggestions are stored content, not verified advice for every region. Content should be reviewed by agricultural specialists, cite trustworthy sources, and account for local regulations and resistance-management guidance.

### 7. Limited explainability

Grad-CAM is disabled in the current configuration. The application does not provide a validated explanation of which image regions influenced a prediction. A heatmap, if added, should be treated as an inspection aid rather than proof of correctness.

### 8. Operational constraints

Loading multiple models can increase startup time and memory use. Hosted environments can have CPU/RAM limits and restart the application. Production-grade uptime, monitoring, persistent history, authentication, and service-level performance have not been established.

### 9. Reproducibility and dependency management

The requirements file pins a broad set of packages, and the TensorFlow version in model metadata differs from the current runtime pin. Training configuration, dataset provenance, artifact checksums, and a tested environment should be maintained.

### 10. No prospective field validation

The project has not established through a prospective field study that using its predictions reduces crop loss, improves yield, or improves treatment decisions.

## Improvement roadmap

### Model quality and evaluation

- Evaluate all models on the **same fixed, held-out test set**.
- Report per-class precision, recall, F1-score, macro-F1, confusion matrices, and inference latency.
- Inspect class imbalance and collect more examples for weak classes.
- Split by plant, source, or capture session where possible to reduce leakage from near-duplicate images.
- Test on independent field images across locations, seasons, devices, and lighting conditions.
- Calibrate scores and measure calibration quality.
- Add uncertainty or out-of-distribution handling so unsupported images can be marked “unable to assess” instead of being forced into a known class.
- Document training settings, dataset version, random seeds, model versions, and evaluation scripts.

### User experience and safety

- Improve handling of corrupt, oversized, and unsupported images.
- Explain supported crops and classes before upload.
- Clearly distinguish a prediction from a confirmed diagnosis.
- Present alternatives and uncertainty without encouraging overconfidence.
- Have disease-reference content reviewed by agricultural specialists and include sources and review dates.
- Test accessibility and mobile layouts.

### Explainability and monitoring

- Evaluate Grad-CAM or another suitable explanation method.
- Review explanations with domain experts; do not assume a heatmap validates a prediction.
- Add structured logging without unnecessarily retaining uploaded images or personal data.
- Monitor latency, model-loading failures, and prediction errors with privacy in mind.
- Establish a consent-based process for field feedback and periodic performance review.

### Engineering and production readiness

- Reduce `requirements.txt` to packages required for inference; separate training and notebook dependencies.
- Pin and test a supported Python/TensorFlow combination and reconcile it with the model-training environment.
- Add automated tests for preprocessing, label-index consistency, model loading, output shape, and PDF generation.
- Maintain the existing Dockerfile and `.dockerignore`; keep the image build reproducible and test inference after intentional changes.
- Consider a separate inference API if other clients need to consume the model; keep Streamlit as a client if the separation becomes useful.
- Add CI checks, dependency scanning, model artifact versioning, health checks, and release instructions.
- Choose an intentional strategy for large model artifacts and verify file hashes where appropriate.

## Deployment and containerization

The application is available through Streamlit Community Cloud and as a Docker image published to Docker Hub.

- **Live application:** https://ai-powered-plant-detection-inference-engine.streamlit.app/
- **GitHub repository:** https://github.com/scientistEgong/AI-Machine-Learning-Project
- **Docker Hub image:** https://hub.docker.com/r/scientist1/ai-plant-disease-detection-inference-engine

### Run the published Docker image

#### Prerequisites

- Docker Desktop installed and running, or a compatible Docker Engine installation.
- Sufficient disk space and memory for the image, dependencies, and saved model artifacts.

#### 1. Pull the image

```bash
docker pull scientist1/ai-plant-disease-detection-inference-engine:latest
```

#### 2. Start the container

```bash
docker run --rm -p 8501:8501 scientist1/ai-plant-disease-detection-inference-engine:latest
```

#### 3. Open the application

While the container is running, open http://localhost:8501 in a browser on the machine running Docker.

#### 4. Stop the application

Press `Ctrl + C` in the terminal running the container. The `--rm` option removes the stopped container automatically, but the downloaded image remains available locally.

### Build the image from source

Clone the repository and navigate to its root directory:

```bash
git clone https://github.com/scientistEgong/AI-Machine-Learning-Project.git
cd AI-Machine-Learning-Project
docker build -t plant-disease-detection-ai:latest .
```

Run the locally built image with:

```bash
docker run --rm -p 8501:8501 plant-disease-detection-ai:latest
```

### Containerization notes

- **Image size:** The locally built image was approximately 4.57 GB at the time of measurement. Actual size can vary between builds.
- **Model artifacts:** The image includes the saved model files required by the configured inference application.
- **PDF reports:** The report-generation workflow was tested locally. Files created inside a temporary container should not be assumed to persist after the container is removed.
- **Local access:** `http://localhost:8501` is an address on the machine running Docker; it is not the public hosting URL.
- **Resource requirements:** TensorFlow and the saved models require substantial storage and may require significant memory.
- **Security:** The published image has unresolved Docker Scout vulnerability findings. See [Security status](#security-status).

Successful container startup and functional testing demonstrate that the application can run in a Docker-managed environment. They do not establish production-grade availability, eliminate dependency vulnerabilities, or guarantee reliable agricultural diagnosis.

## Security status

Docker Scout was used to scan the published Docker image. At the time of the scan, Scout reported **85 findings**, including **one critical-severity finding** and multiple high-severity findings.

The findings included vulnerabilities associated with Python packages such as GitPython, urllib3, Pillow, Tornado, and setuptools, as well as a Debian system-library finding involving zlib. The scan showed the following installed package versions:

| Package | Version detected during the scan |
|---|---:|
| GitPython | 3.1.52 |
| urllib3 | 2.7.0 |
| Pillow | 12.2.0 |
| Tornado | 6.5.7 |
| setuptools | 70.3.0 |

Examples from the scan included a critical GitPython finding (`CVE-2026-78676`), a high-severity urllib3 finding (`CVE-2026-97689`), multiple Pillow findings, a Tornado finding (`GHSA-c2m8-h5v5-343r`), and a Debian zlib finding (`CVE-2026-85091`). This list is illustrative and is not a complete inventory of all 85 findings. Vulnerability status and available fixes can change as packages and advisories are updated.

**These findings have not been remediated as part of this release.** The published image should therefore be treated as containing known, unresolved security vulnerabilities. A successful build, a working application, or a clean `pip check` result does not mean that known vulnerabilities are absent; `pip check` checks declared dependency compatibility, not vulnerability status.

The scan does not by itself establish that the application has been compromised. However, users should review the findings and assess whether the image is suitable for their environment. Dependency updates, base-image maintenance, and a follow-up security scan remain possible future work and are not claimed to have been completed.

## Reproducibility and responsible use

- Preserve the class ordering in `artifacts/class_names.json` that matches the trained models.
- Preserve the expected image dimensions and preprocessing pipeline.
- Keep model files and metadata in sync.
- Record changes to dependencies, model artifacts, or class mappings.
- Evaluate changes against a documented, consistent test protocol.
- Do not present one prediction's confidence score as overall model accuracy.
- Consult a qualified local agricultural extension officer or plant-health professional for real decisions. Follow local regulations and product labels for any treatment.

This project is an educational and decision-support prototype, not a replacement for expert judgement.

## Contributing

Suggestions and improvements are welcome. Before submitting a change:

1. Describe the problem or improvement.
2. Keep model, preprocessing, and class-mapping changes consistent.
3. Test the affected workflow locally.
4. Document dependencies, evaluation results, and limitations.
5. Do not commit credentials, private data, or unapproved images.

## License

The repository includes an MIT License; review the included `LICENSE` file for its exact terms. Dataset and third-party assets may have separate terms, so verify their provenance and usage rights independently.