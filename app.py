"""
============================================================
AI-Powered Plant Disease Detection System

Main Streamlit Application

Project:
AI-Powered Plant Disease Detection System

Phase 1
--------
Application Foundation

Features
--------
✓ Project initialization
✓ Streamlit configuration
✓ Professional UI
✓ Sidebar navigation
✓ Session State
✓ Model initialization
✓ Application routing

Author:
AI Plant Doctor
============================================================
"""

# ==========================================================
# PROJECT ROOT SETUP
# ==========================================================

import os
import sys

# Project display imports
from utils.disease_info import get_disease_details
from utils.reports import generate_pdf_report

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = CURRENT_DIR

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ==========================================================
# IMPORTS
# ==========================================================

import streamlit as st

from config import (
    APP_TITLE,
    APP_ICON,
    PROJECT_NAME,
    VERSION,
    DATASET,
    NUM_CLASSES,
    AVAILABLE_MODELS,
    DEFAULT_MODEL,
)

# from utils.predictor import load_models
from utils.preprocess import (
    validate_image,
    preprocess_image,
)

from utils.predictor import (
    load_models,
    predict_image,
)

# ==========================================================
# STREAMLIT CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
<style>

.main-header{
    background:linear-gradient(135deg,#1B4D3E,#2E8B57);
    color:white;
    padding:30px;
    border-radius:15px;
    margin-bottom:25px;
}

.metric-card{
    background:white;
    border-radius:12px;
    padding:18px;
    border-left:5px solid #1B4D3E;
    box-shadow:0 3px 10px rgba(0,0,0,0.08);
    margin-bottom:15px;
}

.metric-title{
    font-size:14px;
    color:#777;
}

.metric-value{
    font-size:26px;
    font-weight:bold;
    color:#1B4D3E;
}

.section-title{
    color:#1B4D3E;
    font-weight:700;
}

</style>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# SESSION STATE
# ==========================================================

if "models_loaded" not in st.session_state:
    st.session_state.models_loaded = False

if "models" not in st.session_state:
    st.session_state.models = {}

if "prediction_results" not in st.session_state:
    st.session_state.prediction_results = None

if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

if "selected_model" not in st.session_state:
    st.session_state.selected_model = DEFAULT_MODEL

# ==========================================================
# MODEL LOADER
# ==========================================================

@st.cache_resource(show_spinner=False)
def initialize_models():
    """
    Load all trained models once.
    """

    return load_models()

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.image("assets/logo.png", width=100)

    st.title("AI Plant Doctor")

    st.caption(f"Version {VERSION}")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "🔍 Disease Detection",
            "📚 Disease Library",
            "📈 Model Performance",
            "ℹ️ About",
        ],
    )

    st.divider()

    st.subheader("Inference Model")

    selected_model = st.selectbox(
        "Choose Model",
        AVAILABLE_MODELS,
        index=AVAILABLE_MODELS.index(DEFAULT_MODEL),
    
    )

    st.session_state.selected_model = selected_model

    st.divider()

    if not st.session_state.models_loaded:

        with st.spinner("Loading AI models..."):

            try:
                st.session_state.models = initialize_models()

                st.session_state.models_loaded = True

                # MODELS = initialize_models()

                # st.session_state.models_loaded = True

                # st.success("✔Models Loaded")
                st.success("✅ AI Models Ready")

                st.success("✅ Models Loaded Successfully")

            except Exception as e:

                st.error(e)

    else:

        st.success("✅ Models Ready")

    st.divider()

    st.caption(f"Dataset : {DATASET}")
    st.caption(f"Classes : {NUM_CLASSES}")

# ==========================================================
# PAGE ROUTER
# ==========================================================

if page == "🏠 Home":
    # ======================================================
    # HERO SECTION
    # ======================================================

    st.markdown(
        f"""
        <div class="main-header">
            <h1>{PROJECT_NAME}</h1>
            <h3>AI-Powered Plant Disease Detection System</h3>
            <p>
            Detect plant diseases from leaf images using deep learning models,
            receive instant diagnosis, treatment recommendations,
            prevention strategies and downloadable PDF reports.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ======================================================
    # QUICK STATS
    # ======================================================

    st.subheader("System Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Plant Diseases</div>
                <div class="metric-value">{NUM_CLASSES}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Deep Learning Models</div>
                <div class="metric-value">{len(AVAILABLE_MODELS)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Dataset</div>
                # <div class="metric-value">PlantVillage</div>
                <div class="metric-value">{DATASET}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Version</div>
                <div class="metric-value">{VERSION}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # ======================================================
    # FEATURES
    # ======================================================

    st.subheader("Key Features")

    feature1, feature2, feature3 = st.columns(3)

    with feature1:

        st.success("### Image Classification")

        st.write("""
    Upload a clear image of a plant leaf and let the AI classify
    its health status or disease.
    """)

    with feature2:

        st.success("### Disease Knowledge")

        st.write("""
    Receive detailed information including symptoms,
    causes, treatment and prevention methods.
    """)

    with feature3:

        st.success("### PDF Reports")

        st.write("""
    Generate professional PDF diagnosis reports
    that can be downloaded and shared.
    """)

    st.divider()

    # ======================================================
    # SUPPORTED CROPS
    # ======================================================

    st.subheader("Supported Crops")

    crop1, crop2, crop3 = st.columns(3)

    with crop1:

        st.markdown("""
    ### 🍎 Fruits

    - Apple
    - Cherry
    - Grape
    - Peach
    - Strawberry
    """)

    with crop2:

        st.markdown("""
    ### 🌽 Field Crops

    - Corn (Maize)
    - Potato
    """)

    with crop3:

        st.markdown("""
    ### 🍅 Vegetables

    - Tomato
    - Bell Pepper
    """)

    st.divider()

    # ======================================================
    # AVAILABLE MODELS
    # ======================================================

    st.subheader("Available AI Models")

    for model_name in AVAILABLE_MODELS:

        st.markdown(f"✅ **{model_name}**")

    st.divider()

    # ======================================================
    # SYSTEM INFORMATION
    # ======================================================

    left, right = st.columns([2,1])

    with left:

        st.subheader("About the System")

        st.write(
            """
    This application leverages Convolutional Neural Networks (CNNs)
    and Transfer Learning to identify plant diseases from leaf images.

    The system assists farmers, agricultural researchers,
    extension officers, and students by providing rapid disease
    identification along with treatment recommendations.
    """
        )

    with right:

        st.info(
    f"""
    Project

    **{PROJECT_NAME}**

    Dataset

    **{DATASET}**

    Version

    **{VERSION}**
    """
        )

    st.divider()

    # ======================================================
    # GET STARTED
    # ======================================================

    st.subheader("Get Started")

    st.write(
        """
    Navigate to **Disease Detection** from the sidebar to upload
    a plant leaf image and begin diagnosis.
    """
    )

    if st.button("Go to Disease Detection →", use_container_width=True):
        st.success(
            "Select **Disease Detection** from the sidebar to continue."
        )

elif page == "🔍 Disease Detection":

    st.title("🔍 Plant Disease Detection")

    st.success("Disease Detection page is loading")


    st.write(
        """
Upload a plant leaf image and the AI model will analyze
the image and predict possible diseases.
"""
    )


    uploaded_file = st.file_uploader(
        "Upload Leaf Image",
        type=["jpg", "jpeg", "png"]
    )


    if uploaded_file:


        if validate_image(uploaded_file):


            image = preprocess_image(uploaded_file)


            st.image(
                uploaded_file,
                caption="Uploaded Image",
                use_container_width=True
            )


            selected_model = st.session_state.selected_model


            if selected_model == "Compare All Models":

                st.warning(
                    "Model comparison will be implemented later."
                )


            else:


                if st.session_state.models_loaded:


                    model = st.session_state.models[selected_model]


                    if st.button(
                        "🔍 Diagnose Plant",
                        use_container_width=True
                    ):


                        with st.spinner(
                            "Analyzing image..."
                        ):


                            result = predict_image(
                                model,
                                image
                            )


                            st.session_state.prediction_results = result



        else:

            st.error(
                "Invalid image format."
            )


    # DISPLAY RESULTS

    if st.session_state.prediction_results:


        result = st.session_state.prediction_results

        disease_name = result["prediction"]

        confidence = result["confidence"]

        disease_details = get_disease_details(disease_name)
        
        st.divider()

        st.header("Disease Diagnosis")

        st.subheader("Description")

        st.write(
            disease_details.get(
                "description",
                "No description available."
            )
        )
        
        st.subheader("Symptoms")

        symptoms = disease_details.get("symptoms", [])

        if symptoms:

            for symptom in symptoms:

                st.markdown(f"- {symptom}")

        else:

            st.info("No symptoms available.")

            st.subheader("Causes")

            causes = disease_details.get("causes", [])

            if causes:

                for cause in causes:

                    st.markdown(f"- {cause}")

            else:

                st.info("No causes available.")  

            st.subheader("Treatment")

            treatment = disease_details.get("treatment", [])

            if treatment:

                for step in treatment:

                    st.markdown(f"- {step}")

            else:

                st.info("No treatment information available.")      

            st.subheader("Prevention")

            prevention = disease_details.get("prevention", [])

            if prevention:

                for step in prevention:

                    st.markdown(f"- {step}")

            else:

                st.info("No prevention information available.")
        

        st.divider()
        st.subheader(
                    "Diagnosis Result"
                )
        if st.button(
            "Generate PDF Report",
            use_container_width=True
        ):

            try:

                pdf_path = generate_pdf_report(
                    disease_name=disease_name,
                    confidence=confidence,
                    disease_details=disease_details,
                    image_path=None
                )

                st.success("PDF report generated successfully.")

                with open(pdf_path, "rb") as pdf_file:

                    st.download_button(
                        label="Download PDF Report",
                        data=pdf_file,
                        file_name=pdf_path.name,
                        mime="application/pdf"
                    )

            except Exception as error:

                st.error(
                    f"Unable to generate report.\n{error}"
                )

        st.success(
                        f"""
            Prediction:

            {result['prediction']}


            Confidence:

            {result['confidence']}%
            """
                    )


        st.subheader(
            "Top Predictions"
        )


        for item in result["top_predictions"]:

            st.write(
                        f"""
        **{item['class']}**

        Confidence: {item['confidence']}%
        """
            )

elif page == "📚 Disease Library":

    st.title("📚 Disease Library")

    st.write(
        """
Browse every disease currently supported by the AI system.
Select a disease to view its description, symptoms,
causes, treatment and prevention methods.
"""
    )

    from config import CLASS_NAMES
    
    search = st.text_input("Search disease")
    filtered = [
    disease
    for disease in CLASS_NAMES
    if search.lower() in disease.lower()
]
    selected_disease = st.selectbox(
        "Select Disease",
        filtered if filtered else CLASS_NAMES
    )

    disease = get_disease_details(selected_disease)

    st.divider()

    st.subheader(selected_disease.replace("_", " "))

    st.markdown("### Description")
    st.write(disease.get("description", "Not available."))

    st.markdown("### Symptoms")

    symptoms = disease.get("symptoms", [])

    if symptoms:
        for item in symptoms:
            st.markdown(f"- {item}")
    else:
        st.info("No symptoms available.")

    st.markdown("### Causes")

    causes = disease.get("causes", [])

    if causes:
        for item in causes:
            st.markdown(f"- {item}")
    else:
        st.info("No causes available.")

    st.markdown("### Treatment")

    treatment = disease.get("treatment", [])

    if treatment:
        for item in treatment:
            st.markdown(f"- {item}")
    else:
        st.info("No treatment available.")

    st.markdown("### Prevention")

    prevention = disease.get("prevention", [])

    if prevention:
        for item in prevention:
            st.markdown(f"- {item}")
    else:
        st.info("No prevention available.")


elif page == "📈 Model Performance":

    st.title("📈 Model Performance")

    st.write(
        """
Overview of the trained AI models available
within this application.
"""
    )

    from config import MODEL_INFORMATION

    for model_name, info in MODEL_INFORMATION.items():

        st.subheader(model_name)

        st.write(
            f"**Architecture:** {info['architecture']}"
        )

        st.write(
            info["description"]
        )

        st.divider()


elif page == "ℹ️ About":

    st.title("ℹ️ About")

    st.markdown(
                f"""
        # {PROJECT_NAME}

        An AI-powered web application developed for automatic plant disease
        identification using Deep Learning and TensorFlow.

        The application enables users to upload images of plant leaves,
        predict diseases, view detailed agricultural information,
        and generate professional PDF diagnosis reports.
        """
            )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Project Information")

        st.write(f"**Version:** {VERSION}")
        st.write(f"**Dataset:** {DATASET}")
        st.write(f"**Classes:** {NUM_CLASSES}")
        st.write(f"**Models:** {len(AVAILABLE_MODELS)}")

    with col2:

        st.subheader("Technology Stack")

        st.markdown("""
        - Python
        - Streamlit
        - TensorFlow / Keras
        - MobileNetV3
        - NumPy
        - Pillow
        - ReportLab
        """)

    st.divider()

    st.subheader("Project Features")

    st.markdown("""
        - ✅ AI-powered disease detection
        - ✅ Multiple trained deep learning models
        - ✅ Disease information library
        - ✅ PDF diagnosis reports
        - ✅ Image preprocessing pipeline
        - ✅ Modern Streamlit interface
        """)

    st.divider()

    st.info(
            """
    This project was developed for educational and research purposes.
    Predictions should support—not replace—expert agricultural advice.
    """
    )
    st.divider()

    st.caption(
        f"{PROJECT_NAME} | Version {VERSION} | Powered by Streamlit & TensorFlow"
    )
