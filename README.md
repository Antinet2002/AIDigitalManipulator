# AI Digital Manipulation Detector

A Flask + NLP project that analyzes text for predefined linguistic patterns associated with manipulation, emotional pressure, guilt-tripping, blame shifting, threats, urgency, gaslighting-style wording, and excessive dependency.

## Important limitation

This is NOT a real lie detector. Text alone cannot reliably establish whether someone is lying. The project therefore reports a **Manipulation Risk Score** based on detectable language patterns.

## Features

- Web interface
- Message analysis
- Manipulation risk score (0-100)
- Risk level: Low / Moderate / High
- Pattern categories
- Sentence-level highlighting
- Basic sentiment/tone analysis
- Interpretation checks
- No external API required

## Project structure

```text
AI_Digital_Manipulation_Detector/
│
├── app.py
├── analyzer.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── app.js
```

## Run on Windows

Open the project folder in VS Code terminal:

```bash
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

Then open:

http://127.0.0.1:5000

## Sample input

```text
If you really cared about me, you would answer me right now.
After everything I've done for you, you clearly don't care.
This is your fault, and you'll regret ignoring me.
You have to answer immediately.
```

## Example result

```text
Manipulation Risk: 100/100
Risk Level: High

Detected:
- Guilt-tripping
- Emotional pressure
- Urgency / pressure
- Blame shifting
- Threatening language

Tone:
Negative / emotionally charged
```

The exact score can change if you modify the text.

## Interview explanation

"I built a web-based NLP application that detects predefined linguistic patterns associated with digital manipulation. The Flask backend processes user text, checks it against categorized linguistic patterns, calculates a weighted risk score, performs basic sentiment analysis, and returns sentence-level explanations to the frontend. I deliberately describe it as a manipulation-risk detector rather than a lie detector because text alone cannot reliably prove deception."

## Future improvements

- Transformer-based emotion classification
- Fine-tuned text classifier
- Multilingual support
- OCR for screenshots
- Explainable AI dashboard
- User history and analytics
- Dataset-based evaluation
