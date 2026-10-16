"""Aspect keywords and summary helpers for the book review analysis."""
import re

ASPECTS = {
    "pacing":     ["pace", "pacing", "paced", "slow", "drag", "dragged", "drags", "rushed"],
    "characters": ["character", "characters", "protagonist", "heroine", "narrator"],
    "plot":       ["plot", "storyline", "story", "twist", "twists"],
    "ending":     ["ending", "endings", "finale", "epilogue"],
    "writing":    ["writing", "prose", "style", "narration", "writer",
                   "well written", "well-written", "poorly written",
                   "badly written", "beautifully written"],
    "emotion":    ["emotional", "emotions", "heartbreaking", "touching", "tears", "cried"],
}
ASPECT_RE = {a: re.compile(r"\b(" + "|".join(k) + r")\b") for a, k in ASPECTS.items()}

MIN_N = 30      # fewer sentences than this: not enough data
LOW_N = 100     # fewer than this: low confidence


def verdict(pct, n):
    if n < MIN_N:
        return "not enough data"
    if pct >= 70:
        return "mostly praised"
    if pct >= 55:
        return "mixed reactions"
    return "often criticized"


def summarize(rows):
    """rows: a DataFrame with columns aspect, pct_positive, n_sentences."""
    lines = []
    for _, r in rows.sort_values("pct_positive", ascending=False).iterrows():
        note = " (low confidence)" if MIN_N <= r["n_sentences"] < LOW_N else ""
        lines.append(f"{r['aspect']}: {verdict(r['pct_positive'], r['n_sentences'])}{note} "
                     f"({int(r['pct_positive'])}% positive, {int(r['n_sentences'])} sentences)")
    return lines