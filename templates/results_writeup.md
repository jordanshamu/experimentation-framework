# Experiment Results Write-Up

> **Template** — complete one per experiment at conclusion.
> Distribute to stakeholders within 5 business days of experiment completion.

---

## Header

| Field | Details |
|-------|---------|
| **Experiment Name** | [name from Brief] |
| **Analyst** | [name] |
| **Report Date** | [YYYY-MM-DD] |
| **Experiment Period** | [start] → [end] |
| **Status** | Complete |
| **Decision** | 🟢 Ship / 🔴 Revert / 🟡 Iterate |

---

## 1. Executive Summary (TL;DR)

> *2–3 sentences. Write for a VP who will read only this section.*

[Treatment name] **[increased / did not significantly change]** [primary metric] by
**[X pp / X%]** (95% CI: [lo, hi]), which is **[above / below / at]** the pre-specified
MDE of [MDE]. The result was [statistically significant at α=0.05 / not significant].

**Recommendation:** [Ship / Revert / Iterate — one sentence on why.]

---

## 2. Results at a Glance

| Metric | Control | Treatment | Absolute Δ | Relative Δ | p-value | Significant? |
|--------|---------|-----------|------------|------------|---------|--------------|
| [Primary]  | — | — | — | — | — | — |
| [Secondary] | — | — | — | — | — | — |
| [Counter]  | — | — | — | — | — | — |

---

## 3. Statistical Details

### 3a. Frequentist Results

```
Control   : n=[N], conversions=[X], rate=[p]
Treatment : n=[N], conversions=[X], rate=[p]
Absolute lift  : [Δ] (95% CI: [lo, hi])
Relative lift  : [Δ%]
z-statistic    : [z]
p-value        : [p]
Significant    : [Yes / No]
```

### 3b. Bayesian Sanity Check

```
P(treatment > control) : [prob]
Expected loss (ship)   : [loss — in percentage points]
Expected loss (revert) : [loss — in percentage points]
Bayesian recommendation: [Deploy / Continue / Revert]
```

> Both methods [agree / disagree]. [Brief explanation of any divergence.]

---

## 4. Segment Analysis *(pre-specified only)*

| Segment | Control Rate | Treatment Rate | Δ | Significant? | Note |
|---------|-------------|----------------|---|--------------|------|
| [e.g., Mobile] | — | — | — | — | — |
| [e.g., New Users] | — | — | — | — | — |

> ⚠️ Any segment analysis NOT listed in the pre-registration checklist is **exploratory**
> and should be labelled as such. Do not make ship decisions based on exploratory segments.

---

## 5. Quality Checks

| Check | Result | Notes |
|-------|--------|-------|
| Sample Ratio Mismatch | ✅ Pass / ❌ Fail | [actual split] |
| A/A test (if run) | ✅ Pass / N/A | — |
| Novelty effect check | ✅ Pass / ⚠️ Monitor | [week-over-week trend] |
| Metric instrumentation | ✅ Validated | — |

---

## 6. Decision & Next Steps

**Decision:** [Ship / Revert / Iterate]

**Rationale:** [2–3 sentences]

**Next Steps:**

| Action | Owner | Due Date |
|--------|-------|----------|
| [e.g., Full rollout to 100%] | Eng | [date] |
| [e.g., Monitor for 2 weeks post-ship] | Analytics | [date] |
| [e.g., Log learnings in experiment registry] | PM | [date] |

---

## 7. Learnings & Follow-Up Experiments

> *What did we learn that changes our thinking? What would we test next?*

- [Learning 1]
- [Learning 2]
- **Suggested follow-up:** [brief description]

---

*This document follows the pre-registration committed to in [link to checklist].*
