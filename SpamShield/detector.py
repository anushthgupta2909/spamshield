"""
detector.py
-----------
Text preprocessing (NLP) and the SpamDetector class used by the web app.

The SAME `clean_text()` function is used during training (train_model.py)
and during prediction (app.py). This is important: the model can only
understand text that was prepared in exactly the same way it was trained on.
"""

import re
from pathlib import Path

import joblib
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "spam_model.pkl"

# A message is labelled spam when the model's spam probability is >= 50%.
SPAM_THRESHOLD = 0.50
# A "safe" message whose spam probability is above this value is shown
# with a "suspicious" warning so the user stays careful.
SUSPICIOUS_THRESHOLD = 0.25

# ---------------------------------------------------------------------------
# NLP helpers
# ---------------------------------------------------------------------------

# Special placeholder tokens. Instead of throwing away links, phone numbers
# and money amounts, we replace them with a single word. The model can then
# learn that "a message containing a link" is often spam.
URL_TOKEN = "urltoken"
EMAIL_TOKEN = "emailtoken"
PHONE_TOKEN = "phonetoken"
MONEY_TOKEN = "moneytoken"
NUMBER_TOKEN = "numtoken"

# Friendly names shown to the user when explaining a prediction.
TOKEN_LABELS = {
    URL_TOKEN: "a web link",
    EMAIL_TOKEN: "an email address",
    PHONE_TOKEN: "a phone number / short code",
    MONEY_TOKEN: "a money symbol (£ $ €)",
    NUMBER_TOKEN: "numbers",
}

URL_RE = re.compile(r"(https?://\S+|www\.\S+|\b\S+\.(com|net|org|co\.uk|info|biz|ly)\b\S*)", re.I)
EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
PHONE_RE = re.compile(r"\+?\d[\d\s-]{3,}\d")   # 5+ digits: phone numbers & SMS short codes
MONEY_RE = re.compile(r"[£$€₹]|\b(usd|gbp|eur|inr|rs)\b", re.I)
NUMBER_RE = re.compile(r"\d+")

_tokenizer = RegexpTokenizer(r"[a-z]+")
_stemmer = PorterStemmer()


def _load_stopwords():
    """
    Load the English stop-word list from NLTK (words like 'the', 'is', 'and'
    that carry little meaning). If the NLTK data is not downloaded yet we try
    to download it; if there is no internet we fall back to scikit-learn's
    built-in list so the app still works.
    """
    try:
        from nltk.corpus import stopwords
        return set(stopwords.words("english"))
    except LookupError:
        try:
            nltk.download("stopwords", quiet=True)
            from nltk.corpus import stopwords
            return set(stopwords.words("english"))
        except Exception:
            from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
            return set(ENGLISH_STOP_WORDS)


STOP_WORDS = _load_stopwords()


def tokenize_message(text):
    """
    Run the full NLP pipeline on one message and return a list of
    (stemmed_token, original_word) pairs.

    Steps:
      1. Lower-case the text.
      2. Replace links, emails, phone numbers, money symbols and numbers
         with placeholder tokens.
      3. Remove all remaining symbols / punctuation.
      4. Tokenize (split into words).
      5. Remove stop words and 1-letter words.
      6. Stem each word with the Porter Stemmer ("winning" -> "win").
    """
    text = str(text).lower()

    # Step 2: replace special patterns (order matters: URLs before numbers)
    text = URL_RE.sub(f" {URL_TOKEN} ", text)
    text = EMAIL_RE.sub(f" {EMAIL_TOKEN} ", text)
    text = PHONE_RE.sub(f" {PHONE_TOKEN} ", text)
    text = MONEY_RE.sub(f" {MONEY_TOKEN} ", text)
    text = NUMBER_RE.sub(f" {NUMBER_TOKEN} ", text)

    # Step 3: keep only letters and spaces
    text = re.sub(r"[^a-z\s]", " ", text)

    # Steps 4-6
    pairs = []
    for word in _tokenizer.tokenize(text):
        if word in STOP_WORDS or len(word) < 2:
            continue
        if word in TOKEN_LABELS:
            pairs.append((word, word))          # placeholder tokens are not stemmed
        else:
            pairs.append((_stemmer.stem(word), word))
    return pairs


def clean_text(text):
    """Return the cleaned, stemmed version of a message as one string."""
    return " ".join(stem for stem, _ in tokenize_message(text))


# ---------------------------------------------------------------------------
# Rule-based checks (used only to EXPLAIN a prediction, not to make it)
# ---------------------------------------------------------------------------

KEYWORD_RULES = [
    {
        "id": "money",
        "title": "Money or prize language",
        "detail": "Spam often promises cash, prizes or rewards to grab attention.",
        "words": ["cash", "prize", "won", "winner", "win", "reward", "lottery", "jackpot",
                  "bonus", "gift", "voucher", "million", "claim"],
    },
    {
        "id": "urgency",
        "title": "Urgency or pressure",
        "detail": "Words like 'urgent' or 'expires' push people to act without thinking.",
        "words": ["urgent", "immediately", "expires", "expire", "limited", "hurry", "final",
                  "last chance", "act now", "today only", "asap", "suspended"],
    },
    {
        "id": "free",
        "title": "Too-good-to-be-true offer",
        "detail": "Words like 'free', 'offer' and 'discount' are common in promotional spam.",
        "words": ["free", "offer", "discount", "deal", "cheap", "guaranteed", "selected",
                  "congratulations", "congrats", "exclusive"],
    },
    {
        "id": "action",
        "title": "Asks you to call, text or click",
        "detail": "Requests to call, text, reply or click are typical of spam campaigns.",
        "words": ["call now", "txt", "text to", "reply", "click", "subscribe", "unsubscribe",
                  "stop to", "apply now", "visit our"],
    },
    {
        "id": "personal",
        "title": "Asks for passwords or bank details",
        "detail": "Real organisations rarely ask for passwords, PINs or bank details by message.",
        "words": ["password", "account", "bank", "verify", "pin", "otp", "credit card",
                  "ssn", "login", "kyc", "confirm your", "bank details"],
    },
]


def run_checks(message):
    """
    Run every rule-based check on the original message.

    Returns ALL checks in a fixed order (like a virus scanner listing every
    engine), each as a dict:
        {id, title, detail, found (True/False), evidence (short text)}
    """
    text = message.lower()
    checks = []

    links = URL_RE.findall(message)
    checks.append({"id": "link", "title": "Web link",
                   "detail": "Unknown links can lead to phishing or malware websites.",
                   "found": bool(links),
                   "evidence": f"{len(links)} link{'s' if len(links) != 1 else ''}" if links else ""})

    phones = PHONE_RE.findall(message)
    checks.append({"id": "phone", "title": "Phone number or short code",
                   "detail": "Spam often asks you to call or text premium-rate numbers.",
                   "found": bool(phones),
                   "evidence": ", ".join(p.strip() for p in phones[:2])})

    for rule in KEYWORD_RULES:
        matches = [w for w in rule["words"] if re.search(r"\b" + re.escape(w) + r"\b", text)]
        checks.append({"id": rule["id"], "title": rule["title"], "detail": rule["detail"],
                       "found": bool(matches), "evidence": ", ".join(matches[:4])})

    letters = [c for c in message if c.isalpha()]
    caps_ratio = sum(c.isupper() for c in letters) / len(letters) if letters else 0
    caps_found = len(letters) >= 10 and caps_ratio > 0.4
    checks.append({"id": "caps", "title": "Excessive capital letters",
                   "detail": "Shouting in capitals is a classic attention-grabbing tactic.",
                   "found": caps_found, "evidence": f"{caps_ratio:.0%} capitals" if letters else ""})

    bangs = message.count("!")
    checks.append({"id": "bangs", "title": "Many exclamation marks",
                   "detail": "Over-excited punctuation is common in promotional spam.",
                   "found": bangs >= 3, "evidence": f"{bangs} mark{'s' if bangs != 1 else ''}" if bangs else ""})
    return checks


# ---------------------------------------------------------------------------
# The detector
# ---------------------------------------------------------------------------

class SpamDetector:
    """Loads the trained model from disk and classifies messages."""

    def __init__(self, model_path=MODEL_PATH):
        # The saved bundle contains the TF-IDF vectorizer, the Naive Bayes
        # model and the evaluation metrics produced by train_model.py.
        bundle = joblib.load(model_path)
        self.vectorizer = bundle["vectorizer"]
        self.model = bundle["model"]
        self.metrics = bundle.get("metrics", {})
        # Index of the "spam" class (label 1) inside predict_proba's output.
        self.spam_index = list(self.model.classes_).index(1)
        self.ham_index = 1 - self.spam_index

    def _top_spam_words(self, message, features, limit=6):
        """
        Explain WHICH words pushed the prediction towards spam.

        Multinomial Naive Bayes learns, for every word, how likely it is to
        appear in spam vs. ham. For each word in the message we compute:

            contribution = tfidf_weight * (log P(word|spam) - log P(word|ham))

        A positive contribution means the word is more typical of spam.
        """
        log_probs = self.model.feature_log_prob_
        diff = log_probs[self.spam_index] - log_probs[self.ham_index]
        vocab = self.vectorizer.get_feature_names_out()

        # Map each stem back to a word the user actually typed.
        originals = {}
        for stem, original in tokenize_message(message):
            originals.setdefault(stem, original)

        row = features.tocoo()
        scored = []
        for col, weight in zip(row.col, row.data):
            score = weight * diff[col]
            if score > 0:
                stem = vocab[col]
                label = TOKEN_LABELS.get(stem, originals.get(stem, stem))
                scored.append({"word": label, "score": round(float(score), 3)})
        scored.sort(key=lambda item: item["score"], reverse=True)
        return scored[:limit]

    def predict(self, message):
        """
        Classify a single message.

        Returns a dict with:
          label            -> "spam" or "ham"
          risk_level       -> "spam", "suspicious" or "safe"
          confidence       -> probability (0-100) of the predicted label
          spam_probability -> probability (0-100) that the message is spam
          checks           -> every rule-based check, found or not
          indicators       -> only the checks that were found (red flags)
          top_words        -> words that pushed the model towards spam
          explanation      -> short human-readable summary
        """
        cleaned = clean_text(message)
        features = self.vectorizer.transform([cleaned])
        probabilities = self.model.predict_proba(features)[0]
        spam_prob = float(probabilities[self.spam_index])

        is_spam = spam_prob >= SPAM_THRESHOLD
        label = "spam" if is_spam else "ham"
        confidence = spam_prob if is_spam else 1 - spam_prob

        checks = run_checks(message)
        indicators = [c for c in checks if c["found"]]
        top_words = self._top_spam_words(message, features)

        if is_spam:
            risk_level = "spam"
        elif spam_prob >= SUSPICIOUS_THRESHOLD or len(indicators) >= 3:
            risk_level = "suspicious"
        else:
            risk_level = "safe"

        # A probabilistic model is never truly 100% sure, so keep the
        # displayed percentages between 0.01% and 99.99%.
        def as_percent(p):
            return min(max(round(p * 100, 2), 0.01), 99.99)

        return {
            "label": label,
            "risk_level": risk_level,
            "confidence": as_percent(confidence),
            "spam_probability": as_percent(spam_prob),
            "checks": checks,
            "indicators": indicators,
            "top_words": top_words,
            "explanation": self._build_explanation(risk_level, confidence, top_words,
                                                   indicators, cleaned),
        }

    @staticmethod
    def _build_explanation(risk_level, confidence, top_words, indicators, cleaned):
        """
        Create a short plain-English explanation of the result.
        (The probability itself is shown separately, so it is not repeated here.)
        """
        words = ", ".join(f"'{w['word']}'" for w in top_words[:3])
        total_checks = len(KEYWORD_RULES) + 4
        flags = (f"{len(indicators)} of the {total_checks} red-flag checks found something"
                 if indicators else f"none of the {total_checks} red-flag checks found anything")

        if not cleaned:
            return ("The message has very few meaningful words, so the model relied mostly on "
                    f"general patterns. {flags.capitalize()}.")
        if risk_level == "spam":
            text = ""
            if words:
                text = f"Words such as {words} appear far more often in the spam messages the model was trained on. "
            return text + f"{flags.capitalize()}."
        if risk_level == "suspicious":
            text = "The model leans towards legitimate, but the message shares traits with spam."
            if words:
                text += f" Words like {words} are common in spam."
            return text + f" {flags.capitalize()}."
        return ("The wording matches everyday personal conversation rather than promotional or "
                f"fraudulent text, and {flags}.")
