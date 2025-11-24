from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import shap
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor

BASE_DIR = Path(__file__).resolve().parent
DATA_X_PATH = BASE_DIR / "Data" / "X.csv"
DATA_Y_PATH = BASE_DIR / "Data" / "y.csv"
TARGET_NAME = "phq9_total"
RISK_THRESHOLD = 10
DEFAULT_FEATURES = [
    "gpa_all",
    "sad",
    "happy",
    "sleep_hours",
    "sleep_quality",
    "exercise",
    "positive_event_score",
    "negative_event_score",
]
FEATURE_LABELS: Dict[str, str] = {
    "gpa_all": "Overall GPA",
    "sad": "Self-reported sadness",
    "happy": "Self-reported happiness",
    "sleep_hours": "Sleep duration (hrs)",
    "sleep_quality": "Sleep quality",
    "exercise": "Duration of vigorous exercise per day",
    "walk": "Minutes walked per day",
    "positive_event_score": "Intensity of the most positive event",
    "negative_event_score": "Intensity of the most negative event",
    "emotion_range": "Spread between positive and negative event intensities.",
    "has_positive_text": "Whether the student logged a positive text snippet.",
    "has_negative_text": "Whether the student logged a negative text snippet.",
    "anxious": "Anxiexty EMA",
    "calm": "Behavior EMA calmness score",
    "stress": "Stress EMA level",
    "due": "Indicator for assignments/quizzes/exams due today.",
    "hours": "Hours spent on coursework outside class",
    "exercise_schedule": "Whether they skipped exercise due to schedule.",
}

FEATURE_DESCRIPTIONS: Dict[str, str] = {
    "gpa_all": "Cumulative GPA pulled from course records.",
    "sad": "Intensity of sadness reported in the Mood EMA (1=a little, 4=extremely).",
    "happy": "Intensity of happiness from the Mood EMA (1=a little, 4=extremely).",
    "sadornot": "Binary flag for whether the student reported feeling sad right now.",
    "happyornot": "Binary flag for whether the student reported feeling happy right now.",
    "sleep_hours": "Hours slept last night.",
    "sleep_quality": "Self-rated sleep quality (1=very good, 4=very bad).",
    "sleepiness": "How often they almost fell asleep in class or meals.",
    "exercise": "Duration of vigorous exercise that day (ordinal bins).",
    "walk": "Minutes walked that day (ordinal bins).",
    "positive_event_score": "Intensity of the most positive event yesterday (1-7).",
    "negative_event_score": "Intensity of the most negative event yesterday (1-7).",
    "emotion_range": "Spread between positive and negative event intensities.",
    "has_positive_text": "Whether the student logged a positive text snippet.",
    "has_negative_text": "Whether the student logged a negative text snippet.",
    "anxious": "Self-rated anxiety from the Behavior EMA (1-5).",
    "calm": "Behavior EMA calmness score (1-5).",
    "stress": "Stress EMA level (1=little stressed, 3=stressed out, 5=feeling great).",
    "due": "Indicator for assignments/quizzes/exams due today.",
    "hours": "Hours spent on coursework outside class since last session.",
    "exercise_schedule": "Whether they skipped exercise due to schedule.",
}


def pretty_name(column: str) -> str:
    return FEATURE_LABELS.get(column, column.replace("_", " ").title())


@st.cache_data(show_spinner="Loading cleaned StudentLife features...")
def load_dataset() -> pd.DataFrame:
    """Load feature matrix (X) and PHQ-9 targets (y)."""
    if not DATA_X_PATH.exists() or not DATA_Y_PATH.exists():
        raise FileNotFoundError("Expected Data/X.csv and Data/y.csv to be present.")

    X = pd.read_csv(DATA_X_PATH, index_col=0)
    y = pd.read_csv(DATA_Y_PATH, index_col=0).rename(columns={"total_score": TARGET_NAME})
    df = X.join(y, how="inner")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    return df


@st.cache_resource(show_spinner="Training models & initializing SHAP explainers...")
def train_models(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """Train multiple models for PHQ-9 prediction and compute explainability assets."""
    feature_cols = [c for c in df.columns if c != TARGET_NAME]
    X = df[feature_cols]
    y = df[TARGET_NAME]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    background_sample = X_train.sample(min(200, len(X_train)), random_state=42)
    evaluation_sample = X.sample(min(600, len(X)), random_state=0)

    model_library = {
        "Random Forest": RandomForestRegressor(
            n_estimators=400,
            max_depth=10,
            min_samples_leaf=3,
            random_state=42,
            n_jobs=-1,
        ),
        "XGBoost": XGBRegressor(
            n_estimators=500,
            learning_rate=0.05,
            max_depth=4,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_lambda=1.0,
            random_state=42,
            n_jobs=-1,
        ),
        "Neural Network": Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                (
                    "mlp",
                    MLPRegressor(
                        hidden_layer_sizes=(128, 64),
                        activation="relu",
                        learning_rate_init=0.001,
                        max_iter=500,
                        random_state=42,
                    ),
                ),
            ]
        ),
    }

    assets: Dict[str, Dict[str, Any]] = {}

    for name, model in model_library.items():
        model.fit(X_train, y_train)

        # Wrapper
        def pipeline_predict(X):
            return model.predict(X)

        y_pred = model.predict(X_test)
        metrics = {"r2": r2_score(y_test, y_pred), "mae": mean_absolute_error(y_test, y_pred)}

        explainer = shap.Explainer(pipeline_predict, background_sample, feature_names=feature_cols)
        shap_values = explainer(evaluation_sample)
        global_importance = pd.Series(
            np.abs(shap_values.values).mean(axis=0), index=feature_cols, name="importance"
        ).sort_values(ascending=False)

        assets[name] = {
            "model": model,
            "feature_cols": feature_cols,
            "metrics": metrics,
            "explainer": explainer,
            "global_importance": global_importance,
            "evaluation_sample": evaluation_sample,
            "shap_values": shap_values,
        }

    return assets


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Build sidebar filters and return the filtered dataframe."""
    st.sidebar.header("Filter the cohort")
    filter_features = st.sidebar.multiselect(
        "Select variables to filter",
        options=[c for c in df.columns if c != TARGET_NAME],
        default=["gpa_all", "sleep_hours", "sad"],
    )

    filtered = df.copy()
    for feature in filter_features:
        min_val = float(filtered[feature].min())
        max_val = float(filtered[feature].max())
        if math.isclose(min_val, max_val):
            continue
        if feature in filtered.select_dtypes(include=[np.number]).columns:
            step = max((max_val - min_val) / 50, 0.1)
            selected_range = st.sidebar.slider(
                pretty_name(feature),
                min_value=min_val,
                max_value=max_val,
                value=(min_val, max_val),
                step=step,
            )
            filtered = filtered[
                (filtered[feature] >= selected_range[0]) & (filtered[feature] <= selected_range[1])
            ]
        else:
            choices = st.sidebar.multiselect(
                f"{pretty_name(feature)} values",
                options=sorted(filtered[feature].dropna().unique().tolist()),
                default=sorted(filtered[feature].dropna().unique().tolist()),
            )
            filtered = filtered[filtered[feature].isin(choices)]

    return filtered


def render_background_section():
    st.markdown("### Dataset & EMA context")
    st.write(
        """
        The dashboard summarizes Dartmouth's 2013 StudentLife study, where 48 students were tracked for a
        10-week term via smartphone sensing, ecological momentary assessments (EMAs), and weekly PHQ-9
        surveys. EMAs are short in-the-moment check-ins asking about mood, sleep, stress, exercise, social
        contact, and academic workload. The cleaned dataset combines those EMA responses with passive
        features (e.g., sleep duration inferred from phone sensors), academic records (e.g., GPA), and
        PHQ-9 scores so we can examine how daily behaviors correlate with depression severity.
        """
    )
    st.caption(
        "Source references: StudentLife dataset documentation (Dartmouth) and EMA question definitions in Data/Data_Raw/EMA/EMA_definition.json."
    )


def render_feature_glossary(df: pd.DataFrame):
    st.markdown("### EMA variable glossary")
    glossary_rows = []
    for feature in sorted(df.columns):
        if feature == TARGET_NAME:
            continue
        glossary_rows.append(
            {
                "Variable": pretty_name(feature),
                "Raw column": feature,
                "Description": FEATURE_DESCRIPTIONS.get(
                    feature, "Derived feature from StudentLife sensors/EMAs."
                ),
            }
        )
    glossary_df = pd.DataFrame(glossary_rows)
    st.dataframe(glossary_df, use_container_width=True)


def show_kpis(df: pd.DataFrame):
    high_risk_pct = (df[TARGET_NAME] >= RISK_THRESHOLD).mean() * 100 if len(df) else 0.0

    c1, c2, c3 = st.columns(3)
    c1.metric("Average PHQ-9", f"{df[TARGET_NAME].mean():.1f}")
    c2.metric("High-risk students", f"{high_risk_pct:.1f} %")
    c3.metric("Records", len(df))


def show_cohort_snapshot(df: pd.DataFrame):
    if df.empty:
        st.caption("Snapshot of filtered cohort")
        st.info("No records match the current filters.")
        return

    st.caption("Snapshot of filtered cohort")
    available = [f for f in DEFAULT_FEATURES if f in df.columns]
    c1, c2 = st.columns(2)

    if available:
        feature_means = df[available].mean().rename(index=pretty_name).sort_values(ascending=True)
        c1.plotly_chart(
            px.bar(
                feature_means,
                orientation="h",
                labels={"value": "Average (normalized units)", "index": "Factor"},
                title="Key factor averages",
            ),
            use_container_width=True,
        )
    else:
        c1.info("Key factors not available in current view.")

    risk_bins = pd.cut(
        df[TARGET_NAME],
        bins=[-1, 4, 9, 14, 19, 27],
        labels=["Minimal", "Mild", "Moderate", "Moderately severe", "Severe"],
    )
    risk_counts = risk_bins.value_counts().sort_index()
    risk_summary = pd.DataFrame(
        {
            "Cohort share (%)": (risk_counts / max(len(df), 1) * 100).round(1),
            "Students": risk_counts.astype(int),
        }
    )
    c2.dataframe(risk_summary, use_container_width=True)


def factor_deep_dive(df: pd.DataFrame):
    st.subheader("Explore how each factor tracks with PHQ-9")

    numeric_features = [
        c for c in df.columns if c != TARGET_NAME and np.issubdtype(df[c].dtype, np.number)
    ]
    if not numeric_features:
        st.info("No numeric features available for exploration.")
        return

    selected_feature = st.selectbox(
        "Choose a factor",
        options=numeric_features,
        format_func=pretty_name,
        index=numeric_features.index("gpa_all") if "gpa_all" in numeric_features else 0,
    )

    fig_scatter = px.scatter(
        df,
        x=selected_feature,
        y=TARGET_NAME,
        trendline="ols",
        opacity=0.65,
        title=f"{pretty_name(selected_feature)} vs PHQ-9",
        labels={
            selected_feature: pretty_name(selected_feature),
            TARGET_NAME: "PHQ-9 score",
        },
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    col_a, col_b = st.columns(2)

    corr_series = (
        df[numeric_features + [TARGET_NAME]]
        .corr()[TARGET_NAME]
        .drop(TARGET_NAME)
        .sort_values(key=lambda s: s.abs(), ascending=False)
    )
    col_a.subheader("Correlation strength")
    corr_display = corr_series.iloc[:10]
    corr_display.index = [pretty_name(i) for i in corr_display.index]
    col_a.plotly_chart(
        px.bar(corr_display, labels={"value": "Correlation", "index": "Feature"}),
        use_container_width=True,
    )

    col_b.subheader("Distribution of selected factor")
    col_b.plotly_chart(
        px.histogram(
            df,
            x=selected_feature,
            nbins=20,
            color_discrete_sequence=["#4e79a7"],
            labels={selected_feature: pretty_name(selected_feature)},
        ),
        use_container_width=True,
    )


def explainability_section(df: pd.DataFrame, assets: Dict[str, Dict[str, Any]]):
    st.subheader("Predict & explain PHQ-9 scores")
    model_name = st.selectbox("Choose a model", list(assets.keys()))
    model_assets = assets[model_name]

    model = model_assets["model"]
    feature_cols = model_assets["feature_cols"]
    explainer = model_assets["explainer"]
    metrics = model_assets["metrics"]
    global_importance = model_assets["global_importance"]
    evaluation_sample = model_assets["evaluation_sample"]
    shap_values = model_assets["shap_values"]

    st.caption(
        f"{model_name} trained on an 80/20 split. Use the sliders to simulate different student profiles "
        "and see how factors push risk up or down."
    )

    cols = st.columns(len(DEFAULT_FEATURES))
    user_input = {}
    defaults = df[feature_cols].median()
    for idx, feature in enumerate(DEFAULT_FEATURES):
        if feature not in feature_cols:
            continue
        col = cols[idx % len(cols)]
        feature_min = float(df[feature].min())
        feature_max = float(df[feature].max())
        if math.isclose(feature_min, feature_max):
            user_input[feature] = feature_min
            continue
        default_val = float(defaults.get(feature, df[feature].median()))
        step = max((feature_max - feature_min) / 50, 0.1)
        user_input[feature] = col.slider(
            pretty_name(feature),
            min_value=feature_min,
            max_value=feature_max,
            value=default_val,
            step=step,
        )

    if st.button("Run prediction", use_container_width=True, key=f"predict-{model_name}"):
        base_row = defaults.copy()
        base_row.update(user_input)
        input_df = pd.DataFrame([base_row], columns=feature_cols).fillna(defaults)
        prediction = model.predict(input_df[feature_cols])[0]
        st.success(f"Predicted PHQ-9 score: {prediction:.1f}")
        st.caption("Scores ≥ 10 usually indicate moderate to severe depression risk.")

        single_explanation = explainer(input_df[feature_cols])
        contributions = pd.Series(
            single_explanation.values[0], index=feature_cols, name="contribution"
        )
        feature_values = input_df.iloc[0]
        contrib_df = pd.DataFrame(
            {"feature": feature_cols, "contribution": contributions, "value": feature_values}
        )
        top_contrib = (
            contrib_df.set_index("feature")
            .reindex(DEFAULT_FEATURES)
            .dropna()
            .sort_values("contribution")
        )
        top_contrib = top_contrib.rename(index=pretty_name)

        st.markdown("**Feature contributions for this profile**")
        st.plotly_chart(
            px.bar(
                top_contrib.reset_index(),
                x="contribution",
                y="feature",
                orientation="h",
                hover_data=["value"],
                color="contribution",
                color_continuous_scale="RdBu",
            ),
            use_container_width=True,
        )

    st.markdown("---")
    st.subheader("Global explainability snapshots")

    c1, c2 = st.columns(2)
    c1.metric("Model R² (test)", f"{metrics['r2']:.2f}")
    c2.metric("MAE (test)", f"{metrics['mae']:.2f}")

    st.markdown("**Top drivers based on permutation-free feature importance**")
    top_global = global_importance.head(12)
    top_global.index = [pretty_name(i) for i in top_global.index]
    st.plotly_chart(
        px.bar(
            top_global.reset_index(),
            x="index",
            y="importance",
            orientation="h",
            labels={"importance": "Importance", "index": "Feature"},
        ),
        use_container_width=True,
    )

    st.markdown("**SHAP summary (sample of the cohort)**")
    shap.summary_plot(
        shap_values,
        evaluation_sample,
        feature_names=[pretty_name(col) for col in evaluation_sample.columns],
        show=False,
    )
    shap_fig = plt.gcf()
    st.pyplot(shap_fig, use_container_width=True)
    plt.clf()


def risk_simulator_section(df: pd.DataFrame, assets: Dict[str, Dict[str, Any]]):
    st.subheader("Student risk simulator")
    st.caption(
        "Tune the sliders to represent a student profile and estimate PHQ-9 risk. \n This information is not a medical diagnosis, and anyone seeking one should consult a medical professional. "
    )

    model_name = st.selectbox("Simulation model", list(assets.keys()), key="sim-model")
    model_assets = assets[model_name]
    model = model_assets["model"]
    feature_cols = model_assets["feature_cols"]

    defaults = df[feature_cols].median()
    cols = st.columns(len(DEFAULT_FEATURES))
    user_input = {}
    for idx, feature in enumerate(DEFAULT_FEATURES):
        if feature not in feature_cols:
            continue
        col = cols[idx % len(cols)]
        feature_min = float(df[feature].min())
        feature_max = float(df[feature].max())
        if math.isclose(feature_min, feature_max):
            user_input[feature] = feature_min
            continue
        default_val = float(defaults.get(feature, df[feature].median()))
        step = max((feature_max - feature_min) / 50, 0.1)
        user_input[feature] = col.slider(
            pretty_name(feature),
            min_value=feature_min,
            max_value=feature_max,
            value=default_val,
            step=step,
            key=f"sim-{feature}",
        )

    base_row = defaults.copy()
    base_row.update(user_input)
    input_df = pd.DataFrame([base_row], columns=feature_cols).fillna(defaults)
    prediction = float(model.predict(input_df[feature_cols])[0])
    severity = categorize_phq9(prediction)

    c1, c2 = st.columns(2)
    c1.metric("Predicted PHQ-9", f"{prediction:.1f}")
    c2.metric("Risk band", severity)
    st.progress(min(prediction / 27, 1.0))
    st.caption(
        "Clinical bands: 0-4 Minimal, 5-9 Mild, 10-14 Moderate, 15-19 Moderately severe, 20-27 Severe."
    )

    st.markdown("**Input summary**")
    summary_df = pd.DataFrame(
        {"Factor": [pretty_name(k) for k in user_input], "Value": list(user_input.values())}
    )
    st.dataframe(summary_df, use_container_width=True)


def categorize_phq9(score: float) -> str:
    if score < 5:
        return "Minimal"
    if score < 10:
        return "Mild"
    if score < 15:
        return "Moderate"
    if score < 20:
        return "Moderately severe"
    return "Severe"


def main():
    st.set_page_config(page_title="Student Mental Health Explainability Hub", layout="wide")
    st.title("Student Mental Health Explainability Hub")
    st.write(
        """
        Interactive dashboard built on the StudentLife dataset to spotlight the lifestyle, academic, and behavioral
        factors that shape students' PHQ-9 depression scores. Use the filters to focus on specific cohorts and lean on the
        explainable AI section to see how key levers move risk up or down for individual students.
        """
    )
    render_background_section()

    df = load_dataset()
    assets = train_models(df)
    filtered_df = apply_filters(df)

    overview_tab, simulator_tab, explain_tab, glossary_tab = st.tabs(
        ["Overview", "Risk simulator", "Explainability", "Glossary"]
    )

    with overview_tab:
        st.markdown("### Cohort overview")
        show_kpis(filtered_df)
        show_cohort_snapshot(filtered_df)
        factor_deep_dive(filtered_df if len(filtered_df) >= 2 else df)

    with simulator_tab:
        risk_simulator_section(
            filtered_df if len(filtered_df) >= len(DEFAULT_FEATURES) else df, assets
        )

    with explain_tab:
        explainability_section(
            filtered_df if len(filtered_df) >= len(DEFAULT_FEATURES) else df, assets
        )

    with glossary_tab:
        render_feature_glossary(df)


if __name__ == "__main__":
    main()
