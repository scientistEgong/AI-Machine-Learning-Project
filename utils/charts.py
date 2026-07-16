"""
============================================================
Chart Utilities

Project : AI-Powered Plant Disease Detection System

Purpose
-------
Visualization functions for:
- Prediction confidence charts
- Model comparison charts
- Performance visualization

Framework
----------
Streamlit + Matplotlib
============================================================
"""


# ==========================================================
# PROJECT ROOT SETUP
# ==========================================================

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ==========================================================
# IMPORTS
# ==========================================================

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


from config import (
    TOP_K,
    CONFIDENCE_DECIMALS,
    CLASS_NAMES,
)



# ==========================================================
# CONFIDENCE CHART
# ==========================================================

def plot_confidence_chart(
        class_names,
        probabilities,
        top_k=TOP_K
):
    """
    Create a horizontal confidence bar chart.

    Parameters
    ----------
    class_names : list
        Disease class labels

    probabilities : array/list
        Prediction probabilities

    top_k : int
        Number of predictions to display

    Returns
    -------
    matplotlib figure
    """


    probabilities = np.array(probabilities)


    indices = np.argsort(probabilities)[::-1][:top_k]


    labels = [
        class_names[index]
        for index in indices
    ]


    scores = [
        probabilities[index] * 100
        for index in indices
    ]


    fig, ax = plt.subplots(
        figsize=(8, 4)
    )


    ax.barh(
        labels[::-1],
        scores[::-1]
    )


    ax.set_xlabel(
        "Confidence (%)"
    )


    ax.set_title(
        "Top Disease Predictions"
    )


    for i, score in enumerate(scores[::-1]):

        ax.text(
            score,
            i,
            f"{score:.{CONFIDENCE_DECIMALS}f}%",
            va="center"
        )


    plt.tight_layout()


    return fig



# ==========================================================
# MODEL COMPARISON CHART
# ==========================================================

def plot_model_comparison(
        model_names,
        accuracies
):
    """
    Compare model performance.

    Parameters
    ----------
    model_names : list

    accuracies : list
        Accuracy percentages

    Returns
    -------
    matplotlib figure
    """


    fig, ax = plt.subplots(
        figsize=(8, 4)
    )


    ax.bar(
        model_names,
        accuracies
    )


    ax.set_ylabel(
        "Accuracy (%)"
    )


    ax.set_title(
        "Model Performance Comparison"
    )


    plt.xticks(
        rotation=45,
        ha="right"
    )


    plt.tight_layout()


    return fig



# ==========================================================
# STREAMLIT DISPLAY HELPERS
# ==========================================================

def display_chart(fig):
    """
    Display matplotlib chart in Streamlit.
    """

    st.pyplot(
        fig,
        clear_figure=True
    )



# ==========================================================
# TEST MODULE
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Chart Utilities Test")
    print("=" * 60)


    print(
        f"Loaded classes: {len(CLASS_NAMES)}"
    )


    print(
        f"Top K predictions: {TOP_K}"
    )


    print(
        "Charts module loaded successfully."
    )