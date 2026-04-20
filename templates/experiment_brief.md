# Experiment Brief

> **Version:** 1.0  |  **Template Owner:** Analytics / Product  |  **Last Updated:** [DATE]

---

## 1. Overview

| Field | Details |
|-------|---------|
| **Experiment Name** | [descriptive name, e.g., "Checkout CTA Colour Test"] |
| **Experiment Owner** | [name + team] |
| **Start Date (planned)** | [YYYY-MM-DD] |
| **End Date (planned)** | [YYYY-MM-DD — calculated from power analysis] |
| **Status** | Draft / Approved / Running / Complete |

---

## 2. Business Context

**Problem Statement**  
*What user or business problem are we trying to solve?*

> [2–4 sentences describing the opportunity or pain point]

**Hypothesis**  
> If we [**change**] for [**target audience**], then [**primary metric**] will [**increase/decrease**] by [**X%**] because [**mechanism / reasoning**].

---

## 3. Metrics

| Type | Metric | Direction | Owner |
|------|--------|-----------|-------|
| **Primary (guardrail)** | [e.g., Checkout Conversion Rate] | ↑ Increase | [team] |
| **Secondary** | [e.g., Average Order Value] | ↑ Increase | [team] |
| **Counter-metric** | [e.g., Customer Support Contacts] | ↓ Must not increase | [team] |

> ⚠️ **Decision rule:** The experiment is a success only if the **primary metric** moves in the desired direction AND the **counter-metric** is not degraded.

---

## 4. Experimental Design

| Parameter | Value |
|-----------|-------|
| **Test type** | Two-proportion z-test / t-test / other |
| **Number of variants** | 2 (Control + Treatment) |
| **Traffic split** | 50% / 50% |
| **Target population** | [e.g., all logged-in users on checkout page] |
| **Exclusion criteria** | [e.g., returning users who saw previous test] |
| **Significance level (α)** | 0.05 |
| **Power (1-β)** | 0.80 |
| **Minimum Detectable Effect** | [absolute] |
| **Required n per variant** | [from power calculator] |
| **Estimated runtime** | [days, based on daily traffic] |

---

## 5. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Novelty effect | Medium | Medium | Run for full weekly cycles (min 2 weeks) |
| Sample Ratio Mismatch | Low | High | Monitor traffic split daily |
| Instrumentation error | Low | High | QA tracking before launch |
| Interaction with other tests | Medium | Medium | Check experiment registry for conflicts |

---

## 6. Launch Plan

- [ ] Hypothesis documented and reviewed by PM + Data
- [ ] Metrics instrumented and validated
- [ ] Pre-registration checklist completed
- [ ] Rollback plan defined
- [ ] Stakeholder sign-off received

---

## 7. References

- [Link to pre-registration checklist]
- [Link to dashboard / tracking]
- [Link to prior analysis or related experiments]
