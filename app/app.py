import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT / "src"))
from aspects import summarize  # noqa: E402

RESULTS = ROOT / "app" / "results"

st.set_page_config(page_title="What Makes a Good Book?", layout="wide")


@st.cache_data
def load_results():
    return (pd.read_csv(RESULTS / "book_aspects.csv"),
            pd.read_csv(RESULTS / "book_examples.csv"))


def find_model_dir():
    models = ROOT / "models"
    if not models.exists():
        return None
    hits = list(models.rglob("config.json"))
    return hits[0].parent if hits else None


@st.cache_resource
def load_model(path):
    from transformers import pipeline
    return pipeline("text-classification", model=str(path), device=-1)


summary, examples = load_results()

st.title("What Makes a Good Book?")
st.caption("Aspect-level analysis of Amazon book reviews, plus a fine-tuned DistilBERT sentiment model.")

st.sidebar.header("Read this first")
st.sidebar.markdown(
    "- Aspects are found with keywords, and sentiment comes from a binary model, "
    "so percentages are **approximate**.\n"
    "- Compare books and aspects against each other rather than reading numbers literally.\n"
    "- Aspects with few sentences are marked *low confidence* or *not enough data*.\n"
    "- The keywords assume fiction."
)

tab1, tab2 = st.tabs(["Analyze a book", "Test a review"])

with tab1:
    book = st.selectbox("Choose a book", sorted(summary["title"].unique()))
    rows = summary[summary["title"] == book]

    left, right = st.columns(2)
    with left:
        st.subheader("What readers say")
        for line in summarize(rows):
            st.markdown("- " + line)
    with right:
        st.subheader("% positive sentences")
        st.bar_chart(rows.set_index("aspect")["pct_positive"])

    st.subheader("Evidence: example sentences")
    for aspect in rows.sort_values("n_sentences", ascending=False)["aspect"]:
        n = int(rows.loc[rows["aspect"] == aspect, "n_sentences"].iloc[0])
        if n < 30:
            continue
        with st.expander(f"{aspect} ({n} sentences)"):
            ex = examples[(examples["title"] == book) & (examples["aspect"] == aspect)]
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Scored positive**")
                for s in ex[ex["positive"]]["sentence"]:
                    st.markdown("- " + s)
            with c2:
                st.markdown("**Scored negative**")
                for s in ex[~ex["positive"]]["sentence"]:
                    st.markdown("- " + s)

with tab2:
    st.subheader("Paste a book review")
    model_dir = find_model_dir()
    if model_dir is None:
        st.info("The fine-tuned model is not available in this copy of the app "
                "(the models/ folder is not stored on GitHub).")
    else:
        text = st.text_area("Review text", height=150)
        if st.button("Analyze") and text.strip():
            result = load_model(model_dir)(text, truncation=True, max_length=256)[0]
            positive = result["label"] in ("LABEL_1", "POSITIVE")
            st.write("**Prediction:**", "positive" if positive else "negative")
            st.write("**Confidence:**", round(result["score"], 3))