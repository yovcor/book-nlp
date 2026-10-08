# What Makes a Good Book? 
## An NLP and Machine Learning Project

### Problem Statement
The goal of this project is to collect thousands of book reviews and ratings, transform the raw text into numerical features, and train machine learning models to uncover the patterns that separate loved books from disliked ones. Ultimately, the project builds an interactive application that summarizes what readers think about a book by analyzing its reviews.

### Research Questions
1. **Prediction:** Can we predict whether a review is positive or negative (or its star rating) from its text alone[cite: 1]?
2. **Explanation:** Which words and phrases most strongly separate high-rated reviews from low-rated ones[cite: 1]?
3. **Aspects:** For a given book, what do readers praise or criticize (pacing, characters, ending, writing style)[cite: 1]?
4. **Book Level (Optional):** Do things like genre, page count, or number of ratings relate to a book's average rating[cite: 1]?

### Target Definition
* **Positive Review:** 4 to 5 stars (labeled as `1`)[cite: 1]
* **Negative Review:** 1 to 2 stars (labeled as `0`)[cite: 1]
* **Neutral Review:** 3-star reviews are **dropped** from the primary classification dataset[cite: 1]

### Limitations
* Ratings are not a direct measure of objective quality[cite: 1].
* Popular books attract disproportionately more reviews, and people who strongly love or hate a book review it more frequently than neutral readers[cite: 1].
* Review sentiment is heavily influenced by hype and reader expectations[cite: 1].

## Results (run on 2026-08-10)

Data: 79,788 English Amazon book reviews (random 3% sample), 3-star reviews
removed. Binary label: positive = 4-5 stars (86.8%), negative = 1-2 stars (13.2%).
Split: 63,830 train / 15,958 test, stratified, random_state=42.

| Features | Model | Accuracy | Macro-F1 |
|---|---|---|---|
| (none) | Always predict positive | 0.8677 | 0.4646 |
| TF-IDF | Naive Bayes | 0.8781 | 0.5397 |
| TF-IDF | Complement Naive Bayes | 0.9164 | 0.7963 |
| TF-IDF | Logistic regression (balanced) | 0.9004 | 0.8126 |
| Word2Vec (averaged) | Logistic regression (balanced) | 0.8213 | 0.7195 |

Macro-F1 is the headline metric because the classes are imbalanced.

<!-- C:\venvs\book-nlp\Scripts\Activate.ps1 -->