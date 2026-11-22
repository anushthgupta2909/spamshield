# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Two audiences on the same screens:

- **Everyday person** who received an odd SMS, email or chat message and wants a fast, trustworthy verdict: is this spam or not, and why.
- **Analyst-minded reviewer** (including college examiners evaluating the project) who wants to see the evidence underneath: probabilities, which words drove the decision, history, trends, and model evaluation metrics.

The product is a college Python project, demonstrated live in a viva. It is shown both on a classroom projector and up close on a laptop screen, so it must stay legible and high-contrast in both settings.

## Product Purpose

SpamShield classifies a message as Spam or Ham (legitimate) using a real machine-learning model (TF-IDF + Multinomial Naive Bayes, scikit-learn) with NLTK preprocessing, then explains the verdict. Every analysis is stored in SQLite so the user can search history and see analytics. Success: a visitor gets a verdict in one step, understands why, and an examiner can verify the ML is real and evaluated.

## Positioning

The verdict is explainable and auditable: each result shows the model's spam probability, the specific words that pushed the score (derived from the trained Naive Bayes log-probabilities), and a checklist of rule-based red flags. Model accuracy, precision, recall, F1 and the confusion matrix on a held-out test set are shown in the product itself, not claimed.

## Operating Context

- Flask web app run locally (`python app.py`, http://127.0.0.1:5000); Jinja templates, Bootstrap 5 grid, Chart.js, vanilla JS.
- Pages: Dashboard, Detect Spam, Message History, Analytics, About Project.
- Used in a live demo: presenter pastes sample messages, shows the verdict, then history and analytics; examiners ask viva questions about the methodology.

## Capabilities and Constraints

- Verdict levels: Spam (spam probability ≥ 50%), Suspicious (ham but spam probability ≥ 25% or 3+ red flags), Safe.
- Message limit 2,000 characters; CSRF-protected forms; parameterised SQL.
- Dataset: UCI SMS Spam Collection, 5,574 messages (5,171 unique). Test-set metrics: ~98.65% accuracy, ~96.8% precision, ~92.4% recall.
- Required tech stays: HTML/CSS/JS, Bootstrap 5, Flask, Chart.js.

## Brand Commitments

- Name: SpamShield. Existing shield logo (`static/images/logo.svg`) may be redrawn.
- The user explicitly rejected: glowing gradients, glassmorphism, neon edges, dark-navy-plus-cyan "hacker" scheme, decorative icon tiles and emojis, and generic marketing copy. The original brief's dark navy / cyan / glass requirements are dropped.
- Must look like a credible, professional security product, not an AI-generated template. Reference sites the user wants drawn from (inspiration, not copies): Cloudflare Radar, VirusTotal, urlscan.io, Have I Been Pwned, Linear, Google Safe Browsing, Sentry, 1Password.

## Evidence on Hand

- Real model metrics in `model/metrics.json`; real dataset in `dataset/spam.csv`.
- No users, testimonials, customers or deployment claims exist; none may be invented.

## Product Principles

1. Verdict first, evidence one glance below.
2. Show the machine learning working; never decorate around it.
3. Every number on screen is real and traceable.
4. Legible on a projector and on a laptop alike.

## Accessibility & Inclusion

Must remain readable on a washed-out classroom projector: strong contrast, no meaning carried by color alone (spam/safe also labelled in words).
