# Experimentation Framework

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Portfolio Project](https://img.shields.io/badge/Portfolio-Project%205%20of%205-brightgreen)](https://datascienceportfol.io/jordanshamu)
[![Status: Complete](https://img.shields.io/badge/Status-Complete-success)](https://github.com/jordanshamu/experimentation-framework)

> **A tested toolkit for planning and analysing A/B tests.** It addresses a question every product team faces: *"How do we run experiments that we can actually trust?"*

**Jordan Shamukiga** · [Portfolio](https://datascienceportfol.io/jordanshamu) · [GitHub](https://github.com/jordanshamu) · [LinkedIn](#)

---

## What This Framework Solves

Running a single A/B test is easy. Running experiments *correctly at scale* is hard. This framework addresses the four most common and costly mistakes:

| Problem | Real Cost | This Framework's Solution |
|---------|-----------|---------------------------|
| **Underpowered tests** | Missed true effects; wasted traffic | Power & Sample Size Calculator |
| **Peeking & early stopping** | Inflated false positives (Type I error) | Sequential Analysis (SPRT + O'Brien-Fleming) |
| **Testing too many metrics** | False discoveries from multiple comparisons | Bonferroni, Holm, Benjamini-Hochberg |
| **Binary p-value thinking** | Ignores uncertainty, misses nuance | Bayesian A/B Testing with Expected Loss |

---

## Repository Structure

```
experimentation-framework/
├── notebooks/
│   └── experimentation_framework.ipynb   ← main analysis (synthetic data + Project 2 counts)
├── src/
│   └── stats_utils.py                    ← all statistical functions (importable module)
├── tests/
│   └── test_stats_utils.py               ← pytest suite (known answers, statsmodels checks, null simulations)
├── templates/
│   ├── experiment_brief.md               ← template for experiment planning
│   ├── preregistration_checklist.md      ← pre-registration before launch
│   └── results_writeup.md                ← standardised results template
├── reports/
│   └── executive_summary.md              ← non-technical stakeholder summary
├── visualizations/                       ← all plots auto-saved on notebook run
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

## Framework Components

### 1 · Power & Sample Size Calculator
Interactive functions for **proportion tests** and **t-tests** that output required sample sizes given significance level (α), power (1-β), and minimum detectable effect (MDE). Includes:
- Power curves across a range of MDEs at fixed sample sizes
- Sample size curves across a range of MDEs at fixed power
- Side-by-side scenario comparison table

### 2 · Sequential Analysis / Early Stopping
Two valid approaches to monitoring experiments in real time:
- **SPRT (Sequential Probability Ratio Test)** — Wald's method with explicit H0/H1 boundaries
- **O'Brien-Fleming** — boundaries c_k = C·√(K/k), with C solved numerically so the overall Type I error rate across all looks equals α
- Simulation comparing naive peeking against both valid methods on identical data

### 3 · Multiple Testing Corrections
Side-by-side comparison on 20 simultaneous simulated hypotheses:
- **Bonferroni** — most conservative; controls FWER; use when any false positive is unacceptable
- **Holm-Bonferroni** — uniformly more powerful than Bonferroni; same FWER guarantee
- **Benjamini-Hochberg (FDR)** — controls false discovery rate; best for exploratory feature tests

### 4 · Bayesian A/B Testing
Beta-Binomial conjugate model for conversion-rate experiments:
- Posterior distributions with credible intervals (not confidence intervals)
- **Probability of being best** (P(treatment > control))
- **Expected loss** — the decision-theoretic criterion that replaces the binary reject/fail-to-reject
- Direct comparison with frequentist conclusions on the same dataset

### 5 · Test Design Templates
Three markdown-formatted deliverables a PM or analyst team would actually use:
- **Experiment Brief** — defines hypothesis, metrics, duration, rollout plan
- **Pre-registration Checklist** — prevents HARKing and p-hacking
- **Results Write-Up** — standardised format for sharing conclusions

### 6 · Project 2 Tie-Back
A notebook section applies this framework to the counts from the 588,101-user [Marketing A/B Test](https://github.com/jordanshamu/Marketing-A-B-Test-Analysis) (ad 14,423 / 564,577 = 2.555%; PSA 420 / 23,524 = 1.785%; 43.1% relative lift; about 96/4 allocation):
- Power for the unequal arms at a pre-chosen minimum effect (10% relative lift), not at the observed effect
- A clearly labelled simulation of O'Brien-Fleming monitoring using the observed rates and allocation (the data has no timestamps, so the real test's stopping behaviour cannot be analysed)
- The Bayesian posterior for the observed counts

---

## Getting Started

### Prerequisites
- Python 3.8+
- Jupyter Lab 4.x

### Installation

```bash
git clone https://github.com/jordanshamu/experimentation-framework.git
cd experimentation-framework
pip install -r requirements.txt
jupyter lab notebooks/experimentation_framework.ipynb
```

Run the tests:

```bash
pytest tests
```

No external datasets are required. Sections 1–5 generate synthetic data inline; Section 6 uses the Project 2 summary counts, which are entered in the notebook.

### Using `stats_utils` in Your Own Project

```python
import sys
sys.path.append("src/")
from stats_utils import sample_size_proportion, bayesian_ab_summary

# How many users do I need to detect a 2pp lift from a 10% baseline?
result = sample_size_proportion(p_baseline=0.10, mde=0.02, alpha=0.05, power=0.80)
print(result)
# {'n_per_variant': 3841, 'total_n': 7682, ...}

# Run a full Bayesian summary
summary = bayesian_ab_summary(n_control=5000, x_control=500,
                               n_treatment=5000, x_treatment=560)
print(summary["recommendation"])
# 'Deploy Treatment'
```

---

## Key Results & Insights

| Component | Key Finding |
|-----------|-------------|
| Power analysis | A 2 pp MDE from a 10% baseline requires **3,841 users/variant** at 80% power |
| Sequential testing | In 100,000 simulated null tests with 10 equally spaced looks at α = 0.05, stopping at the first \|z\| ≥ 1.96 gave a **19.2%** false positive rate; calibrated O'Brien-Fleming boundaries gave 4.9% |
| Multiple testing | 20 simultaneous tests at α=0.05 → expected **1 false discovery**; BH-FDR reduces this to ≤1 |
| Bayesian vs. frequentist | Both methods agree directionally, but Bayesian expected loss gives a **richer decision signal** |
| Project 2 retro | Ad 2.555% vs PSA 1.785% (43.1% relative lift, p = 1.7e-13). With the 96/4 split, power for a 10% relative lift was **52.5%**; the same 588,101 users split 50/50 would give 99.9% |

---

## Technical Stack

`Python 3.8+` · `NumPy` · `SciPy` · `Pandas` · `Matplotlib` · `Seaborn` · `Jupyter Lab`

All statistical routines are implemented from first principles in `src/stats_utils.py` — no black-box testing libraries.

---

## Methodology Decisions

**Why Beta-Binomial (not MCMC)?**  
The conjugate model is analytically exact for conversion-rate experiments and runs in milliseconds. MCMC (PyMC) adds complexity without benefit when the likelihood is Binomial.

**Why simulate rather than use a real dataset?**  
Simulated data makes every assumption explicit, ensures reproducibility, and eliminates dataset licensing concerns. The results in Sections 1–5 are illustrative, not empirical claims. Section 6 is the exception: it uses the real Project 2 counts.

**Why implement corrections from scratch?**  
Understanding the mechanics of each correction is critical for explaining trade-offs to stakeholders. A one-line `statsmodels` call gives answers; this framework gives *understanding*.

---

## 📬 Contact

**Jordan Shamukiga**  
[Portfolio](https://datascienceportfol.io/jordanshamu) · [GitHub](https://github.com/jordanshamu) · [LinkedIn](#)

---

