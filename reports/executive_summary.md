# Executive Summary: Experimentation Framework

**For:** Head of Product / CMO / VP of Growth  
**Author:** Jordan Shamukiga, Data Analyst  
**Date:** 2025  
**Project:** Experimentation Framework (Portfolio Project 5 of 5)

---

## The Problem This Framework Solves

Every week, product teams make decisions based on A/B tests. Most of the time, those
decisions rest on a single number: the p-value. But a p-value alone answers a narrow
question — "Is this result unlikely by chance?" — while the business question is much
broader: "Should we ship this?"

This framework provides a **complete decision toolkit** that answers the business
question, not just the statistical one.

---

## What We Built (in Plain English)

### 1. Know Your Test Will Work Before You Run It

**The Problem:** Running an experiment with too few users is like flipping a coin twice
and concluding it's biased. Small tests miss real effects — and the teams that ran them
never know.

**The Solution:** The **Power & Sample Size Calculator** tells you, before you spend a
single user impression, exactly how many users you need to detect a meaningful change
with confidence. Input your baseline rate, the smallest lift worth caring about, and the
tool outputs the required sample — with visualisations showing how power changes as you
scale traffic.

**Business Impact:** Eliminates experiments that were never going to teach you anything.
Protects engineering investment and user goodwill.

---

### 2. Stop Tests Early — But Only When It's Safe

**The Problem:** Teams peek at dashboards daily. When results look good, there's enormous
pressure to call the test and ship. But stopping early on a positive result inflates your
false positive rate — you'll ship changes that don't actually work, at a rate far higher
than your stated 5%.

**The Solution:** **Sequential Analysis** using two validated methods (SPRT and
O'Brien-Fleming boundaries) tells you exactly when a test *can* safely be called early
versus when it must run to completion. In 100,000 simulated tests with no real effect and
10 equally spaced looks at α = 0.05, stopping at the first "significant" look produced a
19.2% false positive rate. Calibrated O'Brien-Fleming boundaries kept it at 4.9%.

**Business Impact:** Allows a test to end early when the effect is large, without
raising the false positive rate above the stated 5%.

---

### 3. Stop Counting Wins When You're Testing 20 Things at Once

**The Problem:** When you run 20 simultaneous tests where nothing is real, chance alone
produces on average one "significant" false positive at α = 0.05. Teams that ignore this inflate their shipped
feature count with changes that do nothing — or worse, harm users.

**The Solution:** **Multiple Testing Corrections** show three validated approaches
(Bonferroni, Holm-Bonferroni, and Benjamini-Hochberg) side by side, with business
guidance on when to use each:

| Situation | Recommended Method |
|-----------|-------------------|
| Safety-critical (any false positive is unacceptable) | Bonferroni |
| Standard product experimentation | Holm-Bonferroni |
| Exploratory feature discovery (some false positives OK) | Benjamini-Hochberg (FDR) |

**Business Impact:** Fewer wasted engineering sprints shipping "winning" experiments that
don't actually win.

---

### 4. Replace "Significant or Not" with "How Confident Are We, and What Does It Cost to Be Wrong?"

**The Problem:** The frequentist p-value is binary — you either cross the threshold or
you don't. Real product decisions are rarely binary. You often want to know: *How
confident are we? What do we lose if we're wrong?*

**The Solution:** **Bayesian A/B Testing** produces:
- A probability distribution over the true conversion rate (not a point estimate)
- **Probability that treatment beats control**
- **Expected loss** — the average conversion-rate cost of making the wrong decision

This replaces "p < 0.05, ship it" with a statement of how likely treatment is to be
better and what being wrong would cost. In the notebook's simulated example
(5,000 users per arm), P(treatment > control) is 99.9% and the expected loss of
shipping treatment is 0.0002 pp.

**Business Impact:** Richer decisions. Less hedging. Clearer communication to leadership.

---

### 5. Templates That Make Good Experiment Hygiene the Default

Three ready-to-use documents ensure every experiment in your organisation is run with
the same rigour:

- **Experiment Brief** — aligns PM, engineering, and analytics before a single line of
  code is written
- **Pre-Registration Checklist** — locks in the hypothesis and analysis plan before data
  is collected, preventing post-hoc rationalisation
- **Results Write-Up** — a standardised format that makes it easy to compare learnings
  across experiments over time

---

## Connection to Prior Work

This framework was applied to the counts from
[Project 2: Marketing A/B Test Analysis](https://github.com/jordanshamu/Marketing-A-B-Test-Analysis):
ad 14,423 conversions of 564,577 users (2.555%) and PSA 420 of 23,524 (1.785%), a 43.1%
relative lift (p = 1.7e-13). Traffic was split about 96% ad / 4% PSA. Key findings:

- The small PSA arm limits precision. Power to detect a 10% relative lift (chosen in
  advance, not the observed effect) was **52.5%** with the actual split; the same
  588,101 users split 50/50 would have given 99.9%.
- The data has no exposure timestamps, so whether the test could have stopped early
  cannot be assessed. The notebook includes only a labelled simulation using the
  observed rates and allocation.
- The Bayesian posterior gives P(ad > PSA) = 1.0000 (all 200,000 posterior draws), with a
  95% credible interval for the relative lift of 29.9% to 57.5%. Both approaches agree.

---

## When to Use Each Testing Approach

| Scenario | Recommended Approach |
|----------|---------------------|
| Pre-launch planning | Power & Sample Size Calculator |
| Running a single, long experiment | Frequentist z-test / t-test |
| Need to make decisions before full runtime | Sequential (O'Brien-Fleming) |
| Testing many features or metrics simultaneously | Multiple testing correction |
| High-stakes decision; want probability + risk quantification | Bayesian A/B |
| All of the above, done right | **This framework** |

---

## Conclusion

Good experimentation is a competitive advantage. Teams that run tests correctly —
with adequate power, valid stopping rules, and proper multiple-comparison handling —
make better product decisions faster. This framework operationalises those practices
into reusable, documented and tested functions.

The complete technical implementation, source code, and worked examples are available
at [github.com/jordanshamu/experimentation-framework](https://github.com/jordanshamu).

---

*Jordan Shamukiga · Data Analyst · [datascienceportfol.io/jordanshamu](https://datascienceportfol.io/jordanshamu)*
