# What Makes a Good Book? An NLP Analysis of Reader Reviews

Machine learning and NLP project that analyzes Amazon book reviews to find out
what readers praise or criticize, and predicts whether a review is positive or negative.

## Purpose

Star ratings alone are a weak measure of a book's quality, so this project works with the
review text instead, to learn *why* readers liked or disliked a book. It covers a full NLP
pipeline: text cleaning, feature extraction (TF-IDF, Word2Vec, transformer embeddings),
classic ML baselines, and a fine-tuned transformer (DistilBERT).

Ratings are a proxy for quality, not a measure of it (see Limitations).

## Research questions

1. Can a review's sentiment (positive or negative) be predicted from its text?
2. Which words and phrases separate positive from negative reviews?
3. What do readers praise or criticize about a given book (pacing, characters, ending)? *(in progress)*

## Data

- Source: Amazon Books Reviews dataset (Kaggle), file `books_rating.csv`
- Sampling: random 3% sample taken in chunks across the whole file (89,994 reviews)
- Cleaning steps: duplicates and reviews under 5 words removed, non-English reviews removed
  (langdetect), 3-star reviews dropped
- Label: positive = 4 to 5 stars, negative = 1 to 2 stars
- Final dataset: **79,788 reviews** (86.8% positive, 13.2% negative)
- Split: 63,830 train / 15,958 test, stratified, `random_state=42`

The data is not included in this repository because of its size.

## Method

| Step | What was done |
|---|---|
| Text cleaning | HTML decoding, lowercasing, spaCy lemmatization, stop-word removal with negations kept ("not", "no", "never") |
| Features | TF-IDF (1-2 grams, 50,000 features), Word2Vec (averaged, 100 dims), MiniLM sentence embeddings (384 dims) |
| Classic models | Naive Bayes, Complement Naive Bayes, Logistic Regression (balanced class weights) |
| Transformer | DistilBERT fine-tuned on 30,000 training reviews, 2 epochs, max length 256, learning rate 2e-5, on a free Colab T4 GPU |

Macro-F1 is the main metric, because the classes are imbalanced.

## Results (run on YYYY-MM-DD)

All models are evaluated on the same 15,958 test reviews.

| Features | Model | Accuracy | Macro-F1 |
|---|---|---|---|
| (none) | Always predict positive | 0.8677 | 0.4646 |
| TF-IDF | Naive Bayes | 0.8781 | 0.5397 |
| Word2Vec (averaged) | Logistic regression (balanced) | 0.8213 | 0.7195 |
| MiniLM embeddings (frozen) | Logistic regression (balanced) | 0.8252 | 0.7230 |
| TF-IDF | Complement Naive Bayes | 0.9164 | 0.7963 |
| TF-IDF | Logistic regression (balanced) | 0.9004 | 0.8126 |
| Fine-tuned DistilBERT | (end-to-end) | **0.9546** | **0.8984** |

## Key findings

- **Accuracy is misleading here.** Predicting "positive" every time gets 86.8% accuracy but a
  macro-F1 of only 0.46. Complement Naive Bayes had the best accuracy among the classic models
  but a lower macro-F1 than logistic regression.
- **Frozen general-purpose embeddings did not beat TF-IDF** (0.72 vs 0.81 macro-F1). These
  embeddings capture what a text is about more than how the reader feels, and averaging
  Word2Vec vectors loses word order and negation.
- **Fine-tuning gave the biggest improvement**: macro-F1 rose from 0.81 (TF-IDF) to 0.90, even
  though DistilBERT trained on fewer reviews. Negative-class precision improved from 0.59 to
  0.85.
- **TF-IDF mistakes were mostly context errors.** Positive reviews containing words like
  "garbage", "headaches" or "NOT" in a defending or joking sense were flagged as negative.
- **Words the logistic regression linked to negative reviews:** boring, disappointed, waste,
  not recommend, not worth, dull. **To positive reviews:** great, excellent, wonderful, love,
  highly recommend, not disappoint, fascinating, powerful.

## Limitations

- Ratings are a rough stand-in for quality. Reviewers who loved or hated a book are more
  likely to write, and popular or hyped books get skewed reviews.
- Some reviews are mixed or purely plot summaries, so rating and text sentiment do not always agree.
- The data includes nonfiction and self-help as well as novels, and the model was not
  analyzed per genre.
- Only the first 2 epochs of one DistilBERT run with one random seed were evaluated. Validation
  loss rose in epoch 2, a sign of mild overfitting. The test set was also used for
  per-epoch evaluation, though no model selection was done with it.
- Promotional or fake reviews were not filtered out.

## Project structure

```
book-nlp/
  notebooks/
    01_eda.ipynb            # sampling, exploration, label
    02_cleaning.ipynb       # text cleaning
    03_baselines.ipynb      # TF-IDF, Word2Vec, classic models
    04_transformers.ipynb   # MiniLM embeddings and DistilBERT (Colab)
  src/
  app/
  requirements.txt
  README.md
```

## How to run

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

1. Download `books_rating.csv` from the Kaggle "Amazon Books Reviews" dataset into `data/raw/`.
2. Run the notebooks in order. Use Google Colab with a GPU for `04_transformers.ipynb`.

Tested with Python 3.12.

## Status and next steps

- [x] Data sampling and exploration
- [x] Text cleaning
- [x] Baselines (TF-IDF, Word2Vec, MiniLM embeddings)
- [x] Fine-tuned DistilBERT
- [ ] Aspect-based sentiment summaries (pacing, characters, ending)
- [ ] Streamlit app
- [ ] Genre-level analysis