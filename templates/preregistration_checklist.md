# Pre-Registration Checklist

> Complete **before** launching the experiment. Pre-registration prevents HARKing
> (Hypothesising After Results are Known) and protects against p-hacking.
>
> **Rule:** Once the experiment is live, this document is locked. Deviations must be
> noted in the results write-up with explicit justification.

---

## Analyst / Owner Declaration

I, **[Name]**, confirm that all items below were completed **before** the experiment
was launched and before any data collection began.

**Signature:** ___________________  **Date:** [YYYY-MM-DD]

---

## Section A — Hypothesis

- [ ] Primary hypothesis is stated in the Experiment Brief in the format:  
      *"If [change], then [metric] will [direction] because [reason]"*
- [ ] The hypothesis was written before seeing any experimental data
- [ ] The hypothesis has not been revised after peeking at results

---

## Section B — Metrics

- [ ] Primary metric is defined and has a single clear owner
- [ ] Secondary metrics are listed and ranked by priority
- [ ] Counter-metrics (guardrails) are defined
- [ ] All metrics are instrumented and tested in staging

---

## Section C — Sample Size & Power

- [ ] Minimum Detectable Effect (MDE) is specified in absolute terms
- [ ] MDE is motivated by business significance (not just statistical convenience)
- [ ] Required n per variant calculated using: `sample_size_proportion()` or `sample_size_ttest()`
- [ ] Significance level α = 0.05 (deviations must be justified)
- [ ] Power = 0.80 (deviations must be justified)
- [ ] Expected runtime documented (based on current daily traffic)
- [ ] Experiment will run for **at least 2 full business cycles** (typically 2 weeks)

---

## Section D — Stopping Rules

- [ ] The experiment will **not** be stopped early based on naive significance
- [ ] If early stopping is needed, the valid method is documented:
  - [ ] SPRT boundaries: `sprt_boundaries(alpha=0.05, beta=0.20)` 
  - [ ] O'Brien-Fleming schedule: `obrien_fleming_boundaries(n_looks=N, alpha=0.05)`
- [ ] Number of planned interim looks is pre-specified: **[N looks]**

---

## Section E — Multiple Testing

- [ ] All metrics being tested simultaneously are listed
- [ ] If testing multiple metrics/segments: correction method is pre-specified:
  - [ ] Bonferroni (conservative; any false positive unacceptable)
  - [ ] Holm-Bonferroni (recommended default)
  - [ ] Benjamini-Hochberg FDR (exploratory; some false discoveries acceptable)
- [ ] Subgroup analyses are pre-specified (post-hoc subgroup analyses = exploratory only)

---

## Section F — Analysis Plan

- [ ] Statistical test type is specified (z-test / t-test / other)
- [ ] Analysis will be conducted on **intent-to-treat** basis (all assigned users)
- [ ] Decision criteria defined:
  - Primary metric significant → [action]
  - Primary metric not significant → [action]
  - Counter-metric degraded → [action]
- [ ] Bayesian sanity check will be run alongside frequentist results: Y / N

---

## Section G — Logistics

- [ ] Experiment is registered in the team experiment tracker
- [ ] No conflicting experiments running on the same population
- [ ] Rollback procedure documented
- [ ] Stakeholder notification plan confirmed

---

*Completed checklists should be stored alongside the experiment results for audit purposes.*
