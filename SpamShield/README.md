# 🛡️ SpamShield – Spam Message Detector

SpamShield is a Python web application that detects whether a message is **Spam**
(fraudulent, unwanted or suspicious) or **Ham** (legitimate) using **Machine Learning**
and **Natural Language Processing**.

It uses a real **TF-IDF + Multinomial Naive Bayes** model trained on the
[UCI SMS Spam Collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection)
dataset (5,574 real SMS messages). No predictions are hard-coded.

| Metric (unseen test set, 1,035 msgs) | Score   |
|--------------------------------------|---------|
| Accuracy                             | ~98.6 % |
| Precision (spam)                     | ~96.8 % |
| Recall (spam)                        | ~92.4 % |
| F1-score (spam)                      | ~94.5 % |

---

## ✨ Features

- **Dashboard** – total analyzed, spam / safe counts, spam rate, charts and recent scans.
- **Detect Spam** – paste a message and get:
  - a stamped verdict: Safe (Ham), Suspicious, or Spam
  - a confidence score and spam / ham probabilities
  - a warning for suspicious messages
  - an explanation: the **words that raised the spam score** (taken from the model itself)
    and a checklist of **nine red-flag checks**, each marked Found / Not found
- **Message History** – search, filter by Spam / Safe, pagination, delete one or clear all (SQLite).
- **Analytics** – Spam vs Safe pie chart, daily bar chart, daily trend and spam rate,
  confidence distribution, daily table, and model performance (confusion matrix, top spam words).
- **About Project** – overview, problem statement, objectives, technologies, ML methodology, future scope.
- **Security** – input validation, 2,000-character limit, parameterised SQL queries, CSRF tokens on
  every form, friendly error pages (no tracebacks shown), security headers.
- **Professional UI ("Security Paper")** – a light, high-contrast design based on bank cheque
  security printing: ruled white sheets, a banking-green navigation rail, stamped verdicts and a
  guilloché verdict slip. Readable on a projector and a laptop, and fully responsive.
  Designed with the Impeccable design skill, drawing on Cloudflare Radar, VirusTotal, urlscan.io,
  Have I Been Pwned and Linear.

---

## 🧰 Technology Stack

| Layer            | Technology                                  |
|------------------|---------------------------------------------|
| Frontend         | HTML5, CSS3, JavaScript, Bootstrap 5 (reboot), custom SVG icons |
| Charts           | Chart.js                                    |
| Backend          | Python, Flask                               |
| Machine Learning | Scikit-learn (TF-IDF, Multinomial Naive Bayes, GridSearchCV) |
| NLP              | NLTK (RegexpTokenizer, stop-words, Porter Stemmer) |
| Data             | Pandas                                      |
| Model storage    | Joblib                                      |
| Database         | SQLite                                      |

---

## 📁 Project Structure

```
SpamShield/
├── app.py              # Flask app: routes, validation, CSRF, error pages
├── train_model.py      # Loads dataset, trains & evaluates model, saves it with Joblib
├── detector.py         # NLP preprocessing + SpamDetector class (prediction & explanation)
├── database.py         # SQLite functions (all queries parameterised)
├── requirements.txt
├── README.md
├── model/
│   ├── spam_model.pkl  # Trained TF-IDF vectorizer + Naive Bayes model + metrics
│   └── metrics.json    # Evaluation results in readable form
├── dataset/
│   └── spam.csv        # UCI SMS Spam Collection (label,message)
├── templates/
│   ├── base.html       # Layout: navigation rail, page header, notices, confirm dialog
│   ├── _logo.html      # Inline logo
│   ├── macros.html     # Reusable stamps, probability meters, empty states
│   ├── dashboard.html
│   ├── detect.html
│   ├── history.html
│   ├── analytics.html
│   ├── about.html
│   └── error.html      # 400 / 404 / 405 / 413 / 500 pages
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   ├── fonts/          # Archivo + Martian Mono (self-hosted)
│   └── images/         # logo.svg, guilloche-*.svg (verdict slip line-work)
└── database/
    └── spamshield.db   # Created automatically on first run
```

---

## 🚀 Installation & Running

**Requirements:** Python 3.9 or newer. An internet connection is needed the first time
(to install packages, download NLTK stop-words, and load Bootstrap's reboot and Chart.js from their CDNs). Fonts are bundled.

### 1. Open a terminal in the project folder

```bash
cd SpamShield
```

### 2. Create and activate a virtual environment

**Windows (PowerShell / CMD)**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Train the model (optional – a trained model is already included)

```bash
python train_model.py
```

Example output:

```
Loaded 5574 messages, 403 duplicates removed -> 5171 unique
Cleaning and preprocessing text...
Training Multinomial Naive Bayes (5-fold cross-validation for alpha)...
====================================================
 MODEL EVALUATION (test set of 1035 messages)
====================================================
 Best alpha      : 0.1
 Accuracy        : 98.65%
 Precision       : 96.8%
 Recall          : 92.37%
 F1-score        : 94.53%
 Confusion matrix: [[TN=900, FP=4], [FN=10, TP=121]]
```

> If `model/spam_model.pkl` is missing, `app.py` trains the model automatically on startup.

### 5. Run the web app

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

Stop the server with `Ctrl + C`.

---

## 📊 Dataset

`dataset/spam.csv` is the **UCI SMS Spam Collection** (Almeida & Hidalgo, 2011), converted to
CSV with two columns:

```
label,message
ham,"Go until jurong point, crazy.. Available only in bugis n great world la e buffet..."
spam,Free entry in 2 a wkly comp to win FA Cup final tkts 21st May 2005. Text FA to 87121 ...
```

- 5,574 messages: 4,827 ham, 747 spam (5,171 unique after removing duplicates).
- If you need to download it again:
  - UCI: <https://archive.ics.uci.edu/dataset/228/sms+spam+collection> (tab-separated
    `SMSSpamCollection` file → save as CSV with `label,message` columns), **or**
  - Kaggle "SMS Spam Collection Dataset" `spam.csv` (columns `v1,v2`) – put it in `dataset/`
    as-is; `train_model.py` detects this format and its `latin-1` encoding automatically.

---

## 🧠 How the Machine Learning Works

1. **Load data** – Pandas reads `spam.csv`; labels become `1 = spam`, `0 = ham`; duplicates removed.
2. **Clean text** (`detector.clean_text`)
   - lower-case
   - replace links → `urltoken`, emails → `emailtoken`, phone numbers / short codes → `phonetoken`,
     `£ $ € ₹` → `moneytoken`, other numbers → `numtoken`
   - remove all other symbols and punctuation
3. **Tokenize** with NLTK `RegexpTokenizer`, remove NLTK English **stop-words**, and **stem**
   each word with the **Porter Stemmer** (`winning → win`).
4. **TF-IDF vectorization** – each message becomes a vector of word weights:
   `TF-IDF = term frequency × log(N / documents containing the term)`.
5. **Train** a **Multinomial Naive Bayes** classifier on 80 % of the data (stratified split).
   The smoothing value `alpha` is chosen with **5-fold cross-validation** (`GridSearchCV`).
6. **Evaluate** on the remaining 20 % – accuracy, precision, recall, F1, confusion matrix.
7. **Save** vectorizer + model + metrics with **Joblib** → `model/spam_model.pkl`.
8. **Predict** – `app.py` loads the model once at start-up. For every message, the same
   cleaning is applied, TF-IDF transforms it, and `predict_proba` gives the spam probability.

**Decision rule:** spam probability ≥ 50 % → **Spam**. A message classified as ham but with a spam
probability ≥ 25 % (or 3+ red flags) is shown as **Suspicious**.

**Explanation:** for each word in the message SpamShield computes
`tfidf_weight × (log P(word | spam) − log P(word | ham))` from the trained Naive Bayes model.
Words with the highest positive values are shown as "words that raised the spam score".

---

## 🔒 Security & Validation

| Threat / requirement      | How SpamShield handles it |
|---------------------------|---------------------------|
| Empty input               | Rejected on the client (JS) **and** on the server |
| Very long input           | 2,000 character limit + 64 KB request size limit |
| SQL injection             | Every query uses `?` placeholders (`database.py`); `LIKE` wildcards escaped |
| CSRF                      | Random per-session token required on every POST form |
| XSS                       | Jinja2 auto-escapes all user text; chart data passed with `tojson` |
| Error leakage             | Custom error pages; real errors only written to the server log; `debug=False` |
| Clickjacking / sniffing   | `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff` headers |

---

## 🔌 JSON API (bonus)

| Method | URL            | Description |
|--------|----------------|-------------|
| GET    | `/api/stats`   | Overall statistics + last 14 days |
| POST   | `/api/analyze` | Body `{"message": "..."}`, header `X-CSRFToken` (from a page's session) |

---

## 🎓 Viva Quick Answers

- **Why Naive Bayes?** Fast, works very well with word-count / TF-IDF features, needs little data,
  and its probabilities are easy to explain.
- **Why "Multinomial"?** It models how often words occur, which suits text features.
- **What does "naive" mean?** It assumes words are independent of each other given the class.
- **Why TF-IDF instead of plain counts?** It lowers the weight of words that appear in almost every
  message and highlights distinctive words.
- **Why stemming?** "win", "wins", "winning" become one feature → smaller vocabulary, better generalisation.
- **Why remove duplicates before splitting?** So identical messages cannot be in both training and test
  sets, which would give an unrealistically high accuracy.
- **Precision vs Recall?** Precision = of messages flagged as spam, how many really were spam.
  Recall = of all real spam, how much we caught. High precision means few real messages are wrongly blocked.
- **What is alpha?** Laplace/additive smoothing – prevents zero probability for words never seen in a class.

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | Activate the virtual environment and run `pip install -r requirements.txt` |
| NLTK stop-words download fails (offline) | The app falls back to scikit-learn's stop-word list automatically. Retrain with `python train_model.py` once you are online so training and prediction use the same list. |
| Charts don't appear | Chart.js loads from a CDN – check your internet connection |
| "Your session expired" after restarting the server | Reload the page (a new security key is generated on every start; set `SPAMSHIELD_SECRET_KEY` to keep it fixed) |
| Port 5000 already in use | `set PORT=5001` (Windows) or `export PORT=5001` (macOS/Linux), then `python app.py` |

---

## 🔭 Future Scope

Multilingual detection (Hindi / Hinglish), deep-learning models (LSTM / BERT), live URL reputation
checks, Android / email integration, user feedback for continuous retraining, and user accounts.
