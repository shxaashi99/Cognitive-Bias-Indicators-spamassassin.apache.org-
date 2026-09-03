# Phishing Cognitive Bias Detection — BPRSM Artefact

A Computational Framework for Identifying and Quantifying Cognitive Bias Indicators in Phishing: An Analysis of the SpamAssassin Corpus

This repository contains the implementation artefact for the Bias-Based Phishing Risk Scoring Model (BPRSM), developed as part of an MSc research project at the University of the West of England (UWE Bristol).It analyses raw email text from the [SpamAssassin Public Corpus](https://spamassassin.apache.org/old/publiccorpus/), extracts four categories of cognitive bias indicators (Authority, Urgency, Fear, Elicitation), trains a classifier to validate their predictive power, and surfaces the results through an interactive, explainable risk dashboard.


## Contents

- [How it works](#how-it-works)
- [Repository layout](#repository-layout)
- [Getting started](#getting-started)
- [Running the pipeline](#running-the-pipeline)
- [Using the dashboard](#using-the-dashboard)
- [Understanding the outputs](#understanding-the-outputs)
- [Customising the model](#customising-the-model)
- [Known limitations](#known-limitations)
- [Citation](#citation)
- [Contact](#contact)


## How it works

Each email is scored against a 31-keyword taxonomy spanning four psychological bias categories (regex stems, so `immediat` also matches "immediately", `unauthoriz` also matches "unauthorized", etc.):

| Category | Example trigger stems |
|---|---|
| **Authority** | `ceo`, `admin`, `official`, `director`, `management`, `department`, `security` |
| **Urgency** | `immediat`, `now`, `deadline`, `urgent`, `asap`, `expir`, `limit`, `quick` |
| **Fear** | `suspend`, `risk`, `unauthoriz`, `breach`, `lock`, `warn`, `legal`, `compromis` |
| **Elicitation** | `click`, `login`, `updat`, `submit`, `download`, `confirm`, `verify`, `access` |

From these hit-counts, two complementary scoring mechanisms are produced:

1. **Random Forest classifier** (100 trees, 80/20 stratified train/test split) trained on the four category counts plus an overall **Trigger Density** metric (`total hits ÷ word count × 100`). This is the model actually validated against ham/spam labels precision, recall, F1, and ROC-AUC are reported at runtime.
2. **BPRSM heuristic score**, a transparent, human-readable formula used to drive the dashboard's per-email risk narrative:

   ```
   S_final = Σ(category hits × category weight) + synergy bonus
   ```

   | Category | Weight |
   |---|---|
   | Authority | 4 |
   | Urgency | 5 |
   | Fear | 4 |
   | Elicitation | 3 |

   A **synergy bonus of +2.5** is added whenever an email triggers *both* Authority and Urgency indicators together — operationalising the project's "Compliance Trap" hypothesis, that layered biases (e.g. an "official" sender plus a "deadline") induce cognitive narrowing more effectively than either bias alone. Risk is then banded as **Low** (< 10), **Moderate** (10–14.9), or **Critical** (≥ 15).

   > The BPRSM formula is explicitly a demonstration/explainability layer the actual ham vs. phishing *validation* is done by the Random Forest model, not this weighted sum.

## Repository layout

| File / folder | Description |
|---|---|
| `20021010_*.tar.bz2`, `20030228_*.tar.bz2`, `20050311_spam_2.tar.bz2` | Raw SpamAssassin Public Corpus archives (ham and spam, 2002–2005 snapshots) |
| `process_emails.py` | Standalone helper that parses the extracted corpus into a `text` / `label` DataFrame and prints an email count. Useful for a quick sanity check of the raw data; not required by the main pipeline. |
| `comprehensive_analysis.py` | The main, self-contained pipeline: loads the extracted corpus, extracts bias features, trains and evaluates the Random Forest model, generates all five diagnostic plots, and exports `dashboard_data.json`. |
| `new risk_dashboard.html` | Interactive, client-side dashboard — paste any email text in for an instant BPRSM risk score and forensic narrative, and browse the pre-computed sample results. |
| `risk_dashboard old.html` | Earlier version of the dashboard, kept for reference only. |
| `confusion_matrix.png` | Random Forest confusion matrix on the held-out test set. |
| `feature_importance.png` | Relative importance of each bias category / Trigger Density in the trained model. |
| `trigger_density.png` | Violin plot comparing Trigger Density between ham and spam. |
| `synergy_matrix.png` | Correlation heatmap between bias categories, computed on spam emails only. |
| `synergy_co_occurrence.png` | Co-occurrence count matrix — how often each pair of bias categories appears together. |
| `Risk Mails.docx` | Full research write-up: methodology, literature review, results, and discussion. |

> **Note:** file names containing spaces (`new risk_dashboard.html`, `risk_dashboard old.html`, `Risk Mails.docx`) need to be quoted or escaped on the command line.

## Getting started

### Prerequisites

- Python 3.8+
- `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`

```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```

(`os`, `re`, `json`, and `email` are standard library and need no separate install.)

### Prepare the corpus

The analysis scripts read email files from **extracted folders**, not directly from the `.tar.bz2` archives, so extract each archive first. Both scripts look for folders named exactly:

```
easy_ham/  easy_ham_2/  hard_ham/  spam/  spam_2/
```

```bash
for f in *.tar.bz2; do tar -xjf "$f"; done
```

Several archives map to the same category (e.g. both the 2002-10-10 and 2003-02-28 `spam` snapshots extract into a folder ultimately used as `spam/`) — merge their contents into the single expected folder per category so all messages are picked up.

## Running the pipeline

Run the main analysis directly — it handles loading, feature extraction, model training/evaluation, plotting, and the dashboard export in one pass:

```bash
python comprehensive_analysis.py
```

This will:

1. Load every email under `easy_ham/`, `easy_ham_2/`, `hard_ham/`, `spam/`, and `spam_2/` (ham → label 0, spam → label 1).
2. Count keyword hits per bias category and compute Trigger Density for each email.
3. Train a Random Forest (100 estimators, 80/20 stratified split, `random_state=42`) and print a classification report plus ROC-AUC to the terminal.
4. Save five diagnostic plots to the repository root: `confusion_matrix.png`, `feature_importance.png`, `trigger_density.png`, `synergy_matrix.png`, `synergy_co_occurrence.png`.
5. Export `dashboard_data.json` summary statistics, sample ham/spam emails with their BPRSM scores, and the taxonomy definition for the HTML dashboard to consume.

Optionally, run `python process_emails.py` first as a quick standalone check that the corpus extracted correctly (it just prints the number of emails loaded).

## Using the dashboard

Open `new risk_dashboard.html` directly in a modern browser:

```bash
# macOS
open "new risk_dashboard.html"

# Windows
start "new risk_dashboard.html"

# Linux
xdg-open "new risk_dashboard.html"
```

**Features:**

- **Holistic Risk Index (HRI)** -a colour-coded gauge (Low / Moderate / Critical) built from the BPRSM formula above.
- **Pathological Profile** -bar chart of hit counts per bias category for the email in view.
- **Forensic Narrative** =plain-language explanation linking detected triggers to known social-engineering techniques (e.g. "Institutional Mimicry", "Crisis-Driven Semantic Framing").
- **Synergy Indicator** =flags when Authority and Urgency co-occur and shows the synergy bonus being applied.
- **Paste-and-analyse** = paste any email text in directly; the dashboard runs the same keyword-based scoring client-side, so nothing is sent to a server.

If `dashboard_data.json` hasn't been generated yet, ad-hoc paste-and-analyse still works — only the pre-computed sample-email section will be empty.

## Understanding the outputs

| Plot | What it shows |
|---|---|
| `confusion_matrix.png` | True vs. predicted labels on the held-out test set — overall accuracy and false positive/negative balance. |
| `feature_importance.png` | Which bias categories (and Trigger Density) the Random Forest relied on most. |
| `trigger_density.png` | Distribution of Trigger Density for ham vs. spam — spam should skew higher and more concentrated. |
| `synergy_matrix.png` | Pearson correlation between bias categories, computed on spam emails only. |
| `synergy_co_occurrence.png` | Raw counts of how often each pair of bias categories appears together in the same email. |

## Customising the model

All of the following live in `comprehensive_analysis.py`:

- **Keyword taxonomy** — edit the `TAXONOMY` dict to add, remove, or refine regex stems per category.
- **BPRSM weights** — edit `BPRSM_WEIGHTS` (defaults: Authority 4, Urgency 5, Fear 4, Elicitation 3).
- **Synergy bonus** — edit `SYNERGY_BONUS` (default `2.5`).
- **Risk banding** — edit `RISK_THRESHOLD` (default `15.0`, Critical cutoff) and the `10` cutoff used for Moderate inside `prepare_dashboard_data()`.

## Known limitations

- **Corpus age** the SpamAssassin corpus spans 2002–2005 and reflects phishing tactics from that era; it does not capture more recent techniques (spear-phishing, QR-code lures, AI-generated pretexting, etc.).
- **Keyword-based feature extraction** =the taxonomy relies on simple regex stem matching over lowercased text, which will miss obfuscated, paraphrased, or non-English triggers.
- **`process_emails.py` and `comprehensive_analysis.py` are independent**  the main pipeline does not read a pickled DataFrame from `process_emails.py`; it re-implements its own loading/parsing. Run `comprehensive_analysis.py` on its own.
- **Dashboard summary statistics are partly illustrative** `dashboard_data.json`'s `accuracy` (0.90) and `roc_auc` (0.9365) fields are fixed values written by `prepare_dashboard_data()`, rather than the freshly computed metrics printed to the terminal on each run. Treat the terminal output as the authoritative result for a given run.
- **BPRSM formula is a demonstration layer** =the weighted-sum score exists for explainability in the dashboard; model *validation* (precision/recall/ROC-AUC) is performed by the Random Forest classifier, not the formula itself.

For full methodology, related work, and discussion of these limitations, see `Risk Mails.docx`.

## Citation

If you build on this work, please cite the accompanying research write-up (`Risk Mails.docx`) and reference this repository:

```
Sheikh, I. A. (2026). A Computational Framework for Identifying and Quantifying
Cognitive Bias Indicators in Phishing: An Analysis of the SpamAssassin Corpus.
MSc research artefact, University of the West of England (UWE Bristol).
```

## Contact

**Ibrahim Abdullahi Sheikh**
University of the West of England (UWE Bristol)
Email: [Shxaashi99@gmail.com](mailto:Shxaashi99@gmail.com)
