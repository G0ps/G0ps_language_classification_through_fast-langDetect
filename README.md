# Telegram-Scale Language Detection & Analytics Suite

A lightweight benchmarking and analytics framework for testing `fast-langDetect` on large multilingual text datasets simulating Telegram-style message distributions.

The project evaluates language detection performance across multiple scripts and short-message scenarios using synthetic datasets generated from real language corpora.

---

# 🚀 Setup

## Requirements

* Python `3.13.9`

## Installation

```bash
git clone https://github.com/G0ps/G0ps_language_classification_through_fast-langDetect.git

cd G0ps_language_classification_through_fast-langDetect

pip install fast-langDetect
```

---

# ▶️ Running the Project

## Sample Output & Diagnostics

Runs small-scale tests and prints language predictions with confidence scores.

```bash
python sample_generator.py
```

## Full Analytics Benchmark

Runs the large-scale dataset benchmark and performance evaluation.

```bash
python languageClassifier_analytics.py
```

---

# 📂 Dataset Structure

The repository contains a folder called `gutenberg_corpus/` which stores source text files for different languages.

Each file contains text data used for generating benchmark samples and chunked message datasets.

Currently tested languages include:

* English (`en`)
* Tamil (`ta`)
* Hindi (`hi`)
* Arabic (`ar`)
* French (`fr`)
* Marathi (`mr`)

Additional languages can be added by placing new text files inside the `gutenberg_corpus/` directory.

---

# ⚙️ How It Works

The framework:

1. Loads text files from `gutenberg_corpus/`
2. Splits content into small, medium, and large message chunks
3. Assigns the correct ISO language code
4. Shuffles the dataset
5. Runs language detection using `fast-langDetect`
6. Measures accuracy and processing speed

The smaller chunk sizes are designed to simulate short Telegram-style messages.

---

# 📊 Benchmark Summary

| Metric              | Value                  |
| ------------------- | ---------------------- |
| Dataset Size        | 1,199,988 records      |
| Overall Accuracy    | 95.29%                 |
| Throughput          | ~25,293 inferences/sec |
| Avg Processing Time | ~0.0395 ms per message |

---
