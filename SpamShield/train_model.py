"""
train_model.py
--------------
Trains the SpamShield machine-learning model.

Pipeline:
    1. Load the SMS spam dataset (dataset/spam.csv)
    2. Clean & preprocess every message (detector.clean_text)
    3. Split into training (80%) and testing (20%) sets
    4. Convert text to numbers with TF-IDF vectorization
    5. Train a Multinomial Naive Bayes classifier
       (the smoothing parameter "alpha" is tuned with 5-fold cross-validation)
    6. Evaluate accuracy, precision, recall, F1-score and the confusion matrix
    7. Save the vectorizer + model + metrics to model/spam_model.pkl (Joblib)

Run it with:
    python train_model.py
"""

import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import joblib
import nltk
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix,
                             f1_score, precision_score, recall_score)
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "dataset" / "spam.csv"
MODEL_DIR = BASE_DIR / "model"
MODEL_PATH = MODEL_DIR / "spam_model.pkl"
METRICS_PATH = MODEL_DIR / "metrics.json"

RANDOM_STATE = 42


def ensure_nltk_data():
    """Download the NLTK stop-word list if it is not already installed."""
    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        print("Downloading NLTK stopwords...")
        nltk.download("stopwords", quiet=True)


def load_dataset(path=DATASET_PATH):
    """
    Load the dataset into a DataFrame with two columns:
        label   -> 1 for spam, 0 for ham
        message -> the raw text

    Two common formats are supported:
      * label,message           (the file shipped with this project)
      * v1,v2,...  latin-1      (the popular Kaggle "spam.csv" download)
    """
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {path}. Download the 'SMS Spam Collection' dataset "
            "and save it as dataset/spam.csv (see README.md)."
        )
    try:
        df = pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="latin-1")

    if {"v1", "v2"}.issubset(df.columns):           # Kaggle format
        df = df.rename(columns={"v1": "label", "v2": "message"})
    df = df[["label", "message"]].dropna()

    df["label"] = df["label"].str.strip().str.lower().map({"spam": 1, "ham": 0})
    df = df.dropna(subset=["label"])
    df["label"] = df["label"].astype(int)
    df["message"] = df["message"].astype(str)

    # Remove exact duplicate messages so the same text cannot appear in both
    # the training set and the test set (that would inflate the accuracy).
    before = len(df)
    df = df.drop_duplicates(subset="message").reset_index(drop=True)
    print(f"Loaded {before} messages, {before - len(df)} duplicates removed -> {len(df)} unique")
    return df


def build_stem_lookup(messages):
    """
    Stems such as 'guarante' are hard to read, so remember the most common
    original word for every stem ('guarante' -> 'guaranteed').
    """
    from detector import tokenize_message
    counts = defaultdict(Counter)
    for message in messages:
        for stem, original in tokenize_message(message):
            counts[stem][original] += 1
    return {stem: words.most_common(1)[0][0] for stem, words in counts.items()}


def top_spam_words(vectorizer, model, stem_lookup, n=15):
    """Return the n words that the model considers most indicative of spam."""
    from detector import TOKEN_LABELS
    spam_idx = list(model.classes_).index(1)
    ham_idx = 1 - spam_idx
    diff = model.feature_log_prob_[spam_idx] - model.feature_log_prob_[ham_idx]
    vocab = vectorizer.get_feature_names_out()
    best = np.argsort(diff)[::-1][:n]
    return [{"word": TOKEN_LABELS.get(vocab[i], stem_lookup.get(vocab[i], vocab[i])),
             "score": round(float(diff[i]), 3)}
            for i in best]


def train(verbose=True):
    """Train, evaluate and save the model. Returns the metrics dictionary."""
    from detector import clean_text   # imported here so NLTK data is ready first

    ensure_nltk_data()
    df = load_dataset()

    # ---- Step 2: preprocessing -------------------------------------------
    print("Cleaning and preprocessing text...")
    df["clean"] = df["message"].apply(clean_text)

    # ---- Step 3: train / test split --------------------------------------
    # stratify keeps the same spam/ham ratio in both sets.
    X_train, X_test, y_train, y_test = train_test_split(
        df["clean"], df["label"], test_size=0.2, random_state=RANDOM_STATE, stratify=df["label"]
    )

    # ---- Steps 4 & 5: TF-IDF + Multinomial Naive Bayes -------------------
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=False,            # text is already lower-cased
            token_pattern=r"(?u)\b\w+\b",
            sublinear_tf=True,          # use 1 + log(tf) to dampen repeated words
            min_df=1,
        )),
        ("nb", MultinomialNB()),
    ])

    # Try several smoothing values and keep the one with the best F1-score.
    param_grid = {"nb__alpha": [0.01, 0.05, 0.1, 0.2, 0.5, 1.0]}
    print("Training Multinomial Naive Bayes (5-fold cross-validation for alpha)...")
    search = GridSearchCV(pipeline, param_grid, cv=5, scoring="f1", n_jobs=1)
    search.fit(X_train, y_train)

    best = search.best_estimator_
    vectorizer = best.named_steps["tfidf"]
    model = best.named_steps["nb"]

    # ---- Step 6: evaluation on unseen test data --------------------------
    y_pred = best.predict(X_test)
    cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
    metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred) * 100, 2),
        "precision": round(precision_score(y_test, y_pred) * 100, 2),
        "recall": round(recall_score(y_test, y_pred) * 100, 2),
        "f1_score": round(f1_score(y_test, y_pred) * 100, 2),
        "confusion_matrix": {
            "true_ham": int(cm[0][0]), "false_spam": int(cm[0][1]),
            "false_ham": int(cm[1][0]), "true_spam": int(cm[1][1]),
        },
        "best_alpha": search.best_params_["nb__alpha"],
        "cv_f1": round(search.best_score_ * 100, 2),
        "dataset_size": int(len(df)),
        "spam_count": int(df["label"].sum()),
        "ham_count": int((df["label"] == 0).sum()),
        "train_size": int(len(X_train)),
        "test_size": int(len(X_test)),
        "vocabulary_size": int(len(vectorizer.vocabulary_)),
        "algorithm": "Multinomial Naive Bayes",
        "vectorizer": "TF-IDF",
        "top_spam_words": top_spam_words(vectorizer, model, build_stem_lookup(df["message"])),
        "trained_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    if verbose:
        print("\n" + "=" * 52)
        print(" MODEL EVALUATION (test set of %d messages)" % len(X_test))
        print("=" * 52)
        print(f" Best alpha      : {metrics['best_alpha']}")
        print(f" Accuracy        : {metrics['accuracy']}%")
        print(f" Precision       : {metrics['precision']}%")
        print(f" Recall          : {metrics['recall']}%")
        print(f" F1-score        : {metrics['f1_score']}%")
        print(f" Confusion matrix: [[TN={cm[0][0]}, FP={cm[0][1]}], [FN={cm[1][0]}, TP={cm[1][1]}]]")
        print("-" * 52)
        print(classification_report(y_test, y_pred, target_names=["ham", "spam"], digits=4))

    # ---- Step 7: save with Joblib ----------------------------------------
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump({"vectorizer": vectorizer, "model": model, "metrics": metrics}, MODEL_PATH)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(f"Model saved to   {MODEL_PATH}")
    print(f"Metrics saved to {METRICS_PATH}")
    return metrics


if __name__ == "__main__":
    train()
