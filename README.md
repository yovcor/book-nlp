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

<!-- C:\venvs\book-nlp\Scripts\Activate.ps1 -->