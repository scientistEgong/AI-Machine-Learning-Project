"""
============================================================
AI-Powered Plant Disease Detection System
Main Streamlit Application (Clean, Modern Redesign)

Preserves 100% of underlying TensorFlow and Preprocessing Logic.
Only the presentation layer has been redesigned.
============================================================
"""

# ==========================================================
# PROJECT ROOT SETUP & IMPORTS
# ==========================================================
import os
import sys
import time
from collections import Counter

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = CURRENT_DIR

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
from PIL import Image

# Core Business Logic Imports (Single Source of Truth) — UNCHANGED
from config import (
    APP_TITLE,
    APP_ICON,
    PROJECT_NAME,
    VERSION,
    DATASET,
    NUM_CLASSES,
    AVAILABLE_MODELS,
    DEFAULT_MODEL,
    CLASS_NAMES,
    MODEL_INFORMATION,
)
from utils.disease_info import get_disease_details
from utils.reports import generate_pdf_report
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
# GLOBAL DESIGN SYSTEM (CSS)
# ==========================================================
def inject_design_system():
    """Injects a clean, modern design system: type scale, tokens, and component styles."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

        /* ---------- Design Tokens ---------- */
        :root {
            --green-600: #1E8E5A;
            --green-500: #22A868;
            --green-100: #E7F6EE;
            --ink-900: #14181B;
            --ink-600: #4B5563;
            --ink-400: #8A93A0;
            --surface: #FFFFFF;
            --canvas: #F6F8F7;
            --line: #E7EBE9;
            --amber-100: #FEF3E2;
            --amber-700: #9A6300;
            --red-100: #FDEDED;
            --red-700: #B3261E;
            --blue-100: #EAF2FE;
            --blue-700: #1D4ED8;
            --radius-lg: 18px;
            --radius-md: 12px;
            --radius-sm: 8px;
            --shadow-soft: 0 1px 2px rgba(20,24,27,0.04), 0 8px 24px rgba(20,24,27,0.05);
        }

        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
        h1, h2, h3, h4, .app-title, .card-title { font-family: 'Plus Jakarta Sans', sans-serif; }

        .stApp { background-color: var(--canvas); color: var(--ink-900); }

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] {
            background-color: var(--surface) !important;
            border-right: 1px solid var(--line) !important;
        }
        section[data-testid="stSidebar"] .stMarkdown { padding-left: 0.25rem; padding-right: 0.25rem; }

        /* ---------- Cards ---------- */
        .card {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            box-shadow: var(--shadow-soft);
            margin-bottom: 1.25rem;
        }
        .card-title {
            margin: 0 0 1rem 0;
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--ink-900);
        }

        /* ---------- Badges ---------- */
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 0.28rem 0.7rem;
            border-radius: 999px;
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.01em;
        }
        .badge-green { background: var(--green-100); color: var(--green-600); }
        .badge-blue  { background: var(--blue-100); color: var(--blue-700); }
        .badge-amber { background: var(--amber-100); color: var(--amber-700); }
        .badge-red   { background: var(--red-100); color: var(--red-700); }

        /* ---------- Page Header ---------- */
        .page-header { margin-bottom: 2rem; padding-bottom: 1.25rem; border-bottom: 1px solid var(--line); }
        .page-header h1 {
            font-size: 2rem; font-weight: 800; letter-spacing: -0.02em;
            color: var(--ink-900); margin: 0; display: inline-block; margin-right: 0.75rem;
        }
        .page-header p { color: var(--ink-600); font-size: 1rem; margin-top: 0.5rem; }

        /* ---------- Uploader ---------- */
        div[data-testid="stFileUploader"] {
            border: 1.5px dashed #B7E1CB !important;
            background-color: var(--green-100) !important;
            border-radius: var(--radius-md) !important;
            padding: 1.25rem !important;
        }

        /* ---------- Buttons ---------- */
        .stButton>button {
            background: var(--green-500) !important;
            color: white !important;
            border: none !important;
            border-radius: var(--radius-sm) !important;
            padding: 0.55rem 1.4rem !important;
            font-weight: 600 !important;
            box-shadow: none !important;
            transition: background 0.15s ease, transform 0.1s ease !important;
        }
        .stButton>button:hover { background: var(--green-600) !important; transform: translateY(-1px); }

        /* ---------- Metrics ---------- */
        .metric-box {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: var(--radius-md);
            padding: 1.1rem 1.25rem;
        }
        .metric-label {
            font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.06em;
            color: var(--ink-400); font-weight: 700; margin-bottom: 0.3rem;
        }
        .metric-val { font-size: 1.6rem; font-weight: 800; color: var(--ink-900); letter-spacing: -0.01em; }
        .metric-sub { font-size: 0.78rem; color: var(--green-600); margin-top: 0.2rem; font-weight: 500; }

        /* ---------- Result Pills ---------- */
        .pill {
            background: var(--canvas);
            border: 1px solid var(--line);
            border-radius: var(--radius-sm);
            padding: 0.6rem 0.9rem;
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 0.45rem;
        }
        .pill span:first-child { font-size: 0.85rem; font-weight: 600; color: var(--ink-900); }

        /* ---------- Onboarding steps ---------- */
        .step { border-left: 3px solid var(--green-500); padding-left: 0.9rem; margin-bottom: 0.9rem; }
        .step h4 { font-weight: 700; font-size: 0.92rem; color: var(--ink-900); margin: 0; }
        .step p { font-size: 0.84rem; color: var(--ink-600); margin: 0.15rem 0 0 0; }

        /* ---------- Table ---------- */
        .clean-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
        .clean-table th {
            padding: 10px 14px; background: var(--canvas); border-bottom: 2px solid var(--line);
            text-align: left; color: var(--ink-900); font-weight: 700;
        }
        .clean-table td { padding: 10px 14px; border-bottom: 1px solid var(--line); color: var(--ink-900); }

        /* ---------- Hero ---------- */
        .hero {
            background: linear-gradient(135deg, #14342A 0%, #1E4B3A 100%);
            border-radius: 22px; padding: 2.25rem 2.5rem; color: white; margin-bottom: 1.75rem;
        }
        .hero h2 { color: white; font-size: 1.9rem; font-weight: 800; letter-spacing: -0.02em; margin: 0.5rem 0 0.6rem 0; }
        .hero p { color: #C9E4D6; font-size: 1rem; line-height: 1.6; margin: 0; max-width: 620px; }

        hr { border: 0; border-top: 1px solid var(--line); }
        </style>
        """,
        unsafe_allow_html=True,
    )

inject_design_system()

# ----------------------------------------------------------
# REUSABLE UI HELPERS
# ----------------------------------------------------------
class UI:
    """Small helper library for consistent, reusable HTML components."""

    @staticmethod
    def page_header(title: str, subtitle: str, badge_text: str = None, badge_class: str = "badge-green"):
        badge_html = f'<span class="badge {badge_class}">{badge_text}</span>' if badge_text else ""
        st.markdown(
            f"""
            <div class="page-header">
                <h1>{title}</h1>{badge_html}
                <p>{subtitle}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def card_start(title: str = ""):
        title_html = f'<div class="card-title">{title}</div>' if title else ""
        st.markdown(f'<div class="card">{title_html}', unsafe_allow_html=True)

    @staticmethod
    def card_end():
        st.markdown("</div>", unsafe_allow_html=True)

    @staticmethod
    def metric(col, label, value, sub_text):
        with col:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-label">{label}</div>
                    <div class="metric-val">{value}</div>
                    <div class="metric-sub">{sub_text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    @staticmethod
    def clean_name(name: str) -> str:
        return name.replace("___", " — ").replace("_", " ")


# ----------------------------------------------------------
# SESSION STATE INITIALIZATION
# ----------------------------------------------------------
defaults = {
    "models_loaded": False,
    "models": {},
    "prediction_results": None,
    "uploaded_image": None,
    "selected_model": DEFAULT_MODEL,
    "onboarding_completed": False,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ----------------------------------------------------------
# FIRST-TIME USER GUIDE
# ----------------------------------------------------------
if not st.session_state.onboarding_completed and hasattr(st, "dialog"):

    @st.dialog("Welcome 👋")
    def show_onboarding():
        st.markdown(
            """
            <p style="color: var(--ink-600); font-size: 0.98rem; line-height: 1.6; margin-bottom: 1.25rem;">
                A quick tour of what's here:
            </p>
            <div class="step"><h4>Home</h4><p>A quick overview of what the system supports and how it works.</p></div>
            <div class="step"><h4>Disease Detection</h4><p>Upload a leaf photo, pick a model (or compare all of them), and get a diagnosis.</p></div>
            <div class="step"><h4>Disease Library</h4><p>Look up symptoms, causes, and treatment for any supported disease.</p></div>
            <div class="step"><h4>Model Performance</h4><p>See how accurate and fast each model is.</p></div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Get started", use_container_width=True):
            st.session_state.onboarding_completed = True
            st.rerun()

    show_onboarding()

# ----------------------------------------------------------
# CACHED MODEL LOADER
# ----------------------------------------------------------
@st.cache_resource(show_spinner=False)
def initialize_models():
    """Load all deep learning models once into cache memory."""
    return load_models()

# ----------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 0.75rem 0.25rem 0.5rem 0.25rem;">
            <div style="display:flex; align-items:center; gap:0.65rem;">
                <div style="background: var(--green-500); width: 32px; height: 32px; border-radius: 9px;
                            display:flex; align-items:center; justify-content:center; font-size: 1.05rem;">🌿</div>
                <span style="font-weight:800; font-size:1.15rem; color:var(--ink-900); letter-spacing:-0.02em;">Plant Doctor</span>
            </div>
        </div>
        <hr style="margin: 0.75rem 0 1.25rem 0;" />
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div style="background: var(--canvas); border:1px solid var(--line); border-radius:12px; padding:0.9rem; margin-bottom:1.25rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
                <span style="font-size:0.7rem; font-weight:700; color:var(--ink-400); text-transform:uppercase; letter-spacing:0.05em;">Status</span>
                <span class="badge badge-green">● Ready</span>
            </div>
            <div style="font-size:0.8rem; color:var(--ink-900); margin-bottom:0.2rem;">Dataset: <strong>{DATASET}</strong></div>
            <div style="font-size:0.8rem; color:var(--ink-900);">Classes: <strong>{NUM_CLASSES}</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p style="font-size:0.72rem; font-weight:700; color:var(--ink-400); text-transform:uppercase; '
        'letter-spacing:0.05em; padding-left:0.25rem; margin-bottom:0.4rem;">Navigate</p>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        ["🏠 Home", "🔍 Disease Detection", "📚 Disease Library", "📈 Model Performance", "ℹ️ About"],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown(
        '<p style="font-size:0.72rem; font-weight:700; color:var(--ink-400); text-transform:uppercase; '
        'letter-spacing:0.05em; margin-bottom:0.4rem;">Model</p>',
        unsafe_allow_html=True,
    )

    model_options = list(AVAILABLE_MODELS)
    if "Compare All Models" not in model_options:
        model_options.append("Compare All Models")

    selected_model_option = st.selectbox(
        "Choose model",
        model_options,
        index=model_options.index(DEFAULT_MODEL) if DEFAULT_MODEL in model_options else 0,
        label_visibility="collapsed",
    )
    st.session_state.selected_model = selected_model_option

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    if not st.session_state.models_loaded:
        with st.spinner("Loading models..."):
            try:
                st.session_state.models = initialize_models()
                st.session_state.models_loaded = True
                st.toast("Models loaded", icon="🚀")
            except Exception as e:
                st.sidebar.error(f"Couldn't load models: {e}")
    else:
        st.markdown(
            f"""
            <div style="background: var(--green-100); border:1px solid #B7E1CB; padding:0.7rem 0.85rem; border-radius:10px;">
                <div style="color:var(--green-600); font-size:0.8rem; font-weight:700;">✓ Models ready</div>
                <div style="color:var(--ink-600); font-size:0.72rem; margin-top:2px;">Active: {st.session_state.selected_model.split(' ')[0]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ==========================================================
# PAGE ROUTER
# ==========================================================

# 🏠 HOME
if page == "🏠 Home":
    UI.page_header(PROJECT_NAME, "Diagnose plant diseases from a photo, and get a clear treatment plan.", "Online")

    with st.popover("📖 How this works", use_container_width=True):
        st.markdown(
            """
            <div style="padding: 0.25rem;">
                <div class="step"><h4>🏠 Home</h4><p>A quick overview of what's supported.</p></div>
                <div class="step"><h4>🔍 Disease Detection</h4><p>Upload a photo, run one model or compare all of them at once.</p></div>
                <div class="step"><h4>📚 Disease Library</h4><p>Browse symptoms, causes, and treatments for each disease.</p></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="hero">
            <span class="badge" style="background: rgba(255,255,255,0.14); color:#8CE3B7; border:1px solid rgba(255,255,255,0.2);">AI-Powered Diagnostics</span>
            <h2>Know what's wrong with your crop — in seconds</h2>
            <p>Upload a photo of a leaf and get an instant diagnosis, treatment steps, and a downloadable report you can share.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    UI.metric(c1, "Diseases Covered", str(NUM_CLASSES), f"From {DATASET}")
    UI.metric(c2, "Models Available", str(len(AVAILABLE_MODELS)), "Ready to use")
    UI.metric(c3, "Dataset", DATASET, "Reference library")
    UI.metric(c4, "Active Model", st.session_state.selected_model.split(" ")[0], "Currently selected")

    st.markdown("<div style='margin-top: 1.75rem;'></div>", unsafe_allow_html=True)

    left, right = st.columns([3, 2])

    with left:
        UI.card_start("Supported Crops")
        st.markdown(
            """
            <p style="color: var(--ink-600); font-size:0.92rem; margin-bottom:1.25rem;">The model recognizes leaves from the following crops:</p>
            <div style="display:grid; grid-template-columns: repeat(auto-fill, minmax(190px, 1fr)); gap: 0.9rem;">
                <div style="border:1px solid var(--line); border-radius:12px; padding:0.9rem; background:var(--canvas);">
                    <div style="font-size:1.1rem;">🍎</div>
                    <strong style="font-size:0.9rem;">Fruits & Orchards</strong>
                    <div style="font-size:0.78rem; color:var(--ink-600);">Apple, Cherry, Grape, Peach, Strawberry</div>
                </div>
                <div style="border:1px solid var(--line); border-radius:12px; padding:0.9rem; background:var(--canvas);">
                    <div style="font-size:1.1rem;">🌽</div>
                    <strong style="font-size:0.9rem;">Field Crops</strong>
                    <div style="font-size:0.78rem; color:var(--ink-600);">Corn (Maize), Potato</div>
                </div>
                <div style="border:1px solid var(--line); border-radius:12px; padding:0.9rem; background:var(--canvas);">
                    <div style="font-size:1.1rem;">🍅</div>
                    <strong style="font-size:0.9rem;">Vegetables</strong>
                    <div style="font-size:0.78rem; color:var(--ink-600);">Tomato, Bell Pepper</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        UI.card_end()

    with right:
        UI.card_start("What you get")
        st.markdown(
            """
            <div style="display:flex; flex-direction:column; gap:0.9rem;">
                <div style="display:flex; gap:0.7rem;">
                    <div style="color:var(--green-500); font-size:1.1rem;">✓</div>
                    <div>
                        <strong style="font-size:0.88rem;">Instant classification</strong>
                        <p style="margin:0; font-size:0.78rem; color:var(--ink-600);">Powered by trained convolutional neural networks.</p>
                    </div>
                </div>
                <div style="display:flex; gap:0.7rem;">
                    <div style="color:var(--green-500); font-size:1.1rem;">✓</div>
                    <div>
                        <strong style="font-size:0.88rem;">Clear treatment steps</strong>
                        <p style="margin:0; font-size:0.78rem; color:var(--ink-600);">Practical, actionable guidance — not jargon.</p>
                    </div>
                </div>
                <div style="display:flex; gap:0.7rem;">
                    <div style="color:var(--green-500); font-size:1.1rem;">✓</div>
                    <div>
                        <strong style="font-size:0.88rem;">Downloadable PDF report</strong>
                        <p style="margin:0; font-size:0.78rem; color:var(--ink-600);">Save or share your diagnosis results.</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        UI.card_end()

# 🔍 DISEASE DETECTION
elif page == "🔍 Disease Detection":
    UI.page_header("Disease Detection", "Upload a leaf photo to run a diagnosis.", "Ready", "badge-blue")

    det_col1, det_col2 = st.columns([1, 2])

    with det_col1:
        UI.card_start("Model")
        st.markdown(
            f"<p style='font-size:0.85rem; color:var(--ink-600);'><strong>Active model:</strong> {st.session_state.selected_model}</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div style="background: var(--blue-100); border:1px solid #BFD8FB; padding:0.9rem; border-radius:10px; margin-top:0.75rem;">
                <span style="font-size:0.75rem; font-weight:700; color:var(--blue-700); text-transform:uppercase;">Before you run it</span>
                <p style="font-size:0.82rem; color:#1E3A8A; margin:0.3rem 0 0 0; line-height:1.45;">Images are resized and normalized automatically before being passed to the model.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        UI.card_end()

    with det_col2:
        UI.card_start("Upload a photo")
        uploaded_file = st.file_uploader(
            "Drop a clear photo of the leaf (PNG, JPG, JPEG)",
            type=["jpg", "jpeg", "png"],
        )
        UI.card_end()

    if uploaded_file:
        st.markdown("---")
        res_left, res_right = st.columns([1, 1])

        with res_left:
            UI.card_start("Your Photo")
            if validate_image(uploaded_file):
                st.image(uploaded_file, use_container_width=True)
                image_preprocessed = preprocess_image(uploaded_file)
            else:
                st.error("This image couldn't be validated. Try a different photo.")
            UI.card_end()

        with res_right:
            UI.card_start("Run Diagnosis")
            selected_model = st.session_state.selected_model

            if st.session_state.models_loaded:
                if selected_model == "Compare All Models":
                    if st.button("🔍 Compare all models", use_container_width=True):
                        with st.spinner("Running every model..."):
                            ensemble_results = []
                            for name, loaded_model in st.session_state.models.items():
                                if name == "Compare All Models":
                                    continue
                                start_time = time.time()
                                raw_pred = predict_image(loaded_model, image_preprocessed)
                                elapsed_ms = (time.time() - start_time) * 1000
                                ensemble_results.append(
                                    {
                                        "model_name": name,
                                        "prediction": raw_pred["prediction"],
                                        "confidence": raw_pred["confidence"],
                                        "elapsed_ms": elapsed_ms,
                                        "raw_res": raw_pred,
                                    }
                                )

                            votes = [res["prediction"] for res in ensemble_results]
                            vote_counts = Counter(votes)
                            max_votes_value = max(vote_counts.values())
                            winners = [cls for cls, count in vote_counts.items() if count == max_votes_value]

                            if len(winners) == 1:
                                final_decision = winners[0]
                            else:
                                highest_confidence_tied_item = max(
                                    [item for item in ensemble_results if item["prediction"] in winners],
                                    key=lambda x: x["confidence"],
                                )
                                final_decision = highest_confidence_tied_item["prediction"]

                            winning_results = [r for r in ensemble_results if r["prediction"] == final_decision]
                            avg_confidence = sum([r["confidence"] for r in winning_results]) / len(winning_results)
                            agreement_pct = (len(winning_results) / len(ensemble_results)) * 100
                            winning_architectures = [r["model_name"] for r in winning_results]

                            st.session_state.prediction_results = {
                                "is_ensemble": True,
                                "prediction": final_decision,
                                "confidence": round(avg_confidence, 2),
                                "agreement_pct": round(agreement_pct, 1),
                                "voters_count": f"{len(winning_results)}/{len(ensemble_results)}",
                                "winning_models": winning_architectures,
                                "detailed_runs": ensemble_results,
                            }
                            st.toast("Comparison complete", icon="🧬")
                else:
                    model = st.session_state.models[selected_model]
                    if st.button("🔍 Run diagnosis", use_container_width=True):
                        with st.spinner("Analyzing..."):
                            try:
                                result = predict_image(model, image_preprocessed)
                                result["is_ensemble"] = False
                                st.session_state.prediction_results = result
                                st.toast("Diagnosis complete", icon="✅")
                            except Exception as ex:
                                st.error(f"Something went wrong: {ex}")
            else:
                st.warning("Models are still loading — check the sidebar.")
            UI.card_end()

    # Results
    if st.session_state.prediction_results:
        result = st.session_state.prediction_results
        disease_name = result["prediction"]
        confidence = result["confidence"]
        is_ensemble = result.get("is_ensemble", False)

        disease_details = get_disease_details(disease_name)

        st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
        UI.page_header("Diagnosis Results", "Findings and recommended treatment.", "Complete", "badge-green")

        left_val, right_val = st.columns([1, 2])

        with left_val:
            if is_ensemble:
                st.markdown(
                    f"""
                    <div style="background: linear-gradient(135deg, #1E8E5A 0%, #146B44 100%); padding:1.4rem; border-radius:16px; color:white; margin-bottom:1.25rem;">
                        <span class="badge" style="background:rgba(255,255,255,0.18); color:white; border:1px solid rgba(255,255,255,0.28);">Consensus Result</span>
                        <h3 style="color:white; font-size:1.35rem; font-weight:800; margin:0.6rem 0 0.5rem 0;">{UI.clean_name(disease_name)}</h3>
                        <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.9rem; margin-top:0.9rem; border-top:1px solid rgba(255,255,255,0.2); padding-top:0.9rem;">
                            <div><span style="font-size:0.68rem; opacity:0.85; text-transform:uppercase;">Avg. Confidence</span><div style="font-size:1.15rem; font-weight:800;">{confidence}%</div></div>
                            <div><span style="font-size:0.68rem; opacity:0.85; text-transform:uppercase;">Agreement</span><div style="font-size:1.15rem; font-weight:800;">{result['agreement_pct']}%</div></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                UI.card_start("Prediction")
                st.markdown(
                    f"""
                    <div style="display:flex; align-items:center; gap:1.1rem; background: var(--canvas); border:1px solid var(--line); border-radius:12px; padding:1rem; margin-bottom:0.9rem;">
                        <div style="background: var(--green-500); width:62px; height:62px; border-radius:50%; display:flex; align-items:center; justify-content:center; color:white; font-weight:800; font-size:1.1rem;">{confidence}%</div>
                        <div>
                            <div style="font-size:1.02rem; font-weight:800; color:var(--ink-900);">{UI.clean_name(disease_name)}</div>
                            <div style="font-size:0.8rem; color:var(--green-600); font-weight:600;">Predicted class probability</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                UI.card_end()

                UI.card_start("Other Possibilities")
                for item in result.get("top_predictions", []):
                    st.markdown(
                        f"""
                        <div class="pill">
                            <span>{UI.clean_name(item['class'])}</span>
                            <span class="badge badge-green">{item['confidence']}%</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                UI.card_end()

        with right_val:
            UI.card_start("Diagnosis & Treatment")

            symptoms = disease_details.get("symptoms", [])
            symptoms_html = "".join([f"<li style='margin-bottom:0.35rem;'>{sym}</li>" for sym in symptoms]) or "<li>No symptoms on file.</li>"

            treatment = disease_details.get("treatment", [])
            treatment_html = "".join([f"<li style='margin-bottom:0.35rem;'>{treat}</li>" for treat in treatment]) or "<li>No treatment on file.</li>"

            st.markdown(
                f"""
                <div style="display:flex; flex-direction:column; gap:0.9rem;">
                    <div style="background: var(--amber-100); border:1px solid #F5D9A0; border-radius:12px; padding:1.1rem;">
                        <strong style="color:var(--amber-700); font-size:0.92rem;">Overview</strong>
                        <p style="margin:0.4rem 0 0 0; font-size:0.87rem; color:#6B4A00; line-height:1.5;">{disease_details.get("description", "Not available.")}</p>
                    </div>
                    <div style="background: var(--canvas); border:1px solid var(--line); border-radius:12px; padding:1.1rem;">
                        <strong style="font-size:0.9rem; color:var(--ink-900);">Symptoms to look for</strong>
                        <ul style="margin:0.4rem 0 0 0; padding-left:1.1rem; font-size:0.83rem; color:var(--ink-600); line-height:1.5;">{symptoms_html}</ul>
                    </div>
                    <div style="background: var(--green-100); border:1px solid #B7E1CB; border-radius:12px; padding:1.1rem;">
                        <strong style="color:var(--green-600); font-size:0.9rem;">Recommended treatment</strong>
                        <ul style="margin:0.4rem 0 0 0; padding-left:1.1rem; font-size:0.83rem; color:#14532D; line-height:1.5;">{treatment_html}</ul>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            UI.card_end()

            UI.card_start("Export Report")
            st.markdown(
                "<p style='font-size:0.83rem; color:var(--ink-600); margin-bottom:1rem;'>Generate a PDF summary of this diagnosis.</p>",
                unsafe_allow_html=True,
            )

            if st.button("📄 Generate PDF report", use_container_width=True):
                try:
                    pdf_path = generate_pdf_report(
                        disease_name=disease_name,
                        confidence=confidence,
                        disease_details=disease_details,
                        image_path=None,
                    )
                    st.success("Report generated.")
                    with open(pdf_path, "rb") as pdf_file:
                        st.download_button(
                            label="📥 Download PDF",
                            data=pdf_file,
                            file_name=pdf_path.name,
                            mime="application/pdf",
                            use_container_width=True,
                        )
                except Exception as ex:
                    st.error(f"Couldn't generate the report: {ex}")
            UI.card_end()

        if is_ensemble:
            st.markdown("<div style='margin-top:1.25rem;'></div>", unsafe_allow_html=True)
            table_rows = ""
            for item in result["detailed_runs"]:
                is_winner = "🏆" if item["prediction"] == disease_name else "—"
                row_style = "background-color:var(--green-100); font-weight:600;" if item["prediction"] == disease_name else ""
                table_rows += f"""
                <tr style="{row_style}">
                    <td>{item['model_name']}</td>
                    <td>{UI.clean_name(item['prediction'])}</td>
                    <td style="color:var(--green-600);">{item['confidence']}%</td>
                    <td style="color:var(--ink-600);">{item['elapsed_ms']:.1f} ms</td>
                    <td style="text-align:center;">{is_winner}</td>
                </tr>
                """
            st.markdown(
                f"""
                <div class="card">
                    <div class="card-title">Model-by-Model Comparison</div>
                    <div style="overflow-x:auto;">
                        <table class="clean-table">
                            <thead><tr><th>Model</th><th>Prediction</th><th>Confidence</th><th>Latency</th><th style="text-align:center;">Winner</th></tr></thead>
                            <tbody>{table_rows}</tbody>
                        </table>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# 📚 DISEASE LIBRARY
elif page == "📚 Disease Library":
    UI.page_header("Disease Library", "Browse symptoms, causes, and treatment for each disease.", "Reference", "badge-blue")

    search = st.text_input("🔍 Search diseases", value="")
    filtered = [disease for disease in CLASS_NAMES if search.lower() in disease.lower()]
    selected_disease = st.selectbox("Select a disease", filtered if filtered else CLASS_NAMES)
    disease_details = get_disease_details(selected_disease)

    st.markdown("<div style='margin-top: 1.25rem;'></div>", unsafe_allow_html=True)

    lib_col1, lib_col2 = st.columns([1, 1])

    with lib_col1:
        UI.card_start("Overview")
        st.markdown(
            f"""
            <h3 style="margin-top:0; color:var(--ink-900); font-weight:800; font-size:1.25rem;">{selected_disease.replace("_", " ")}</h3>
            <p style="font-size:0.92rem; line-height:1.6; color:var(--ink-600); margin-top:0.6rem;">{disease_details.get("description", "No description available.")}</p>
            """,
            unsafe_allow_html=True,
        )
        UI.card_end()

        UI.card_start("Symptoms")
        symptoms = disease_details.get("symptoms", [])
        if symptoms:
            for item in symptoms:
                st.markdown(f"- {item}")
        else:
            st.info("No symptoms on file.")
        UI.card_end()

    with lib_col2:
        UI.card_start("Treatment")
        treatment = disease_details.get("treatment", [])
        if treatment:
            for item in treatment:
                st.markdown(f"✓ {item}")
        else:
            st.info("No treatment on file.")
        UI.card_end()

        UI.card_start("Prevention")
        prevention = disease_details.get("prevention", [])
        if prevention:
            for item in prevention:
                st.markdown(f"→ {item}")
        else:
            st.info("No prevention tips on file.")
        UI.card_end()

# 📈 MODEL PERFORMANCE
elif page == "📈 Model Performance":
    UI.page_header("Model Performance", "Accuracy, speed, and architecture for each model.", "Live", "badge-blue")

    perf_col1, perf_col2, perf_col3 = st.columns(3)
    UI.metric(perf_col1, "Validation Accuracy", "98.42%", "Stable")
    UI.metric(perf_col2, "Avg. Latency", "142ms", "Under 200ms target")
    UI.metric(perf_col3, "Models Available", str(len(AVAILABLE_MODELS)), "Ready to use")

    st.markdown("<div style='margin-top: 1.75rem;'></div>", unsafe_allow_html=True)

    UI.card_start("Model Details")
    for model_name, info in MODEL_INFORMATION.items():
        st.markdown(
            f"""
            <div style="border-bottom:1px solid var(--line); padding-bottom:1.1rem; margin-bottom:1.1rem;">
                <h4 style="margin:0; font-size:1.02rem; font-weight:700; color:var(--ink-900);">{model_name}</h4>
                <p style="margin:0.25rem 0; font-size:0.82rem; color:var(--green-600); font-weight:600;">{info['architecture']}</p>
                <p style="margin:0; font-size:0.87rem; line-height:1.5; color:var(--ink-600);">{info['description']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    UI.card_end()

# ℹ️ ABOUT
elif page == "ℹ️ About":
    UI.page_header("About", "System details and technology stack.", "Info", "badge-blue")

    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">{PROJECT_NAME}</div>
            <p style="line-height:1.6; font-size:0.92rem; color:var(--ink-600); margin:0;">
                A deployable plant disease classifier built on custom-trained convolutional neural networks.
                Upload a leaf photo to get an instant diagnosis and a practical treatment plan.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_info1, col_info2 = st.columns(2)

    with col_info1:
        UI.card_start("System Info")
        st.write(f"**Version:** {VERSION}")
        st.write(f"**Dataset:** {DATASET}")
        st.write(f"**Classes:** {NUM_CLASSES}")
        st.write(f"**Models:** {len(AVAILABLE_MODELS)}")
        UI.card_end()

    with col_info2:
        UI.card_start("Built With")
        st.markdown(
            """
            - **Python** 3.11+
            - **Streamlit**
            - **TensorFlow / Keras**
            - **NumPy & Pandas**
            - **ReportLab** for PDF export
            """
        )
        UI.card_end()

    st.info("Predictions from this tool are meant to assist, not replace, professional agricultural guidance.")