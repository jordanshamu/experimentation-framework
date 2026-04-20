"""
stats_utils.py  –  Experimentation Framework · Portfolio Project 5
Author: Jordan Shamukiga
"""
from __future__ import annotations
from typing import Optional
import numpy as np
import pandas as pd
from scipy import stats

# ── helpers ──────────────────────────────────────────────────────────────────
def _za(alpha, two_tailed=True):
    return stats.norm.ppf(1 - alpha / (2 if two_tailed else 1))
def _zb(power):
    return stats.norm.ppf(power)

# ── 1. POWER & SAMPLE SIZE ───────────────────────────────────────────────────
def sample_size_proportion(p_baseline, mde, alpha=0.05, power=0.80, two_tailed=True):
    """n per variant for a two-proportion z-test."""
    p_t   = p_baseline + mde
    p_avg = (p_baseline + p_t) / 2
    za, zb = _za(alpha, two_tailed), _zb(power)
    num = (za*np.sqrt(2*p_avg*(1-p_avg)) + zb*np.sqrt(p_baseline*(1-p_baseline)+p_t*(1-p_t)))**2
    n = int(np.ceil(num / mde**2))
    return dict(n_per_variant=n, total_n=2*n, p_control=p_baseline,
                p_treatment=round(p_t,4), mde=mde, alpha=alpha, power=power)

def sample_size_ttest(mean_baseline, std_baseline, mde, alpha=0.05, power=0.80, two_tailed=True):
    """n per variant for independent-samples t-test."""
    za, zb = _za(alpha, two_tailed), _zb(power)
    d = mde / std_baseline
    n = int(np.ceil(2 * ((za+zb)/d)**2))
    return dict(n_per_variant=n, total_n=2*n, mean_baseline=mean_baseline,
                std_baseline=std_baseline, mde=mde, cohens_d=round(d,4),
                alpha=alpha, power=power)

def power_curve(p_baseline, mde_range, n_per_variant, alpha=0.05, two_tailed=True):
    """Power at each MDE for a fixed n per variant."""
    za = _za(alpha, two_tailed)
    out = []
    for mde in mde_range:
        p_t = p_baseline + mde
        se  = np.sqrt(p_baseline*(1-p_baseline)/n_per_variant + p_t*(1-p_t)/n_per_variant)
        ncp = abs(mde) / max(se, 1e-12)
        out.append(1 - stats.norm.cdf(za - ncp) + stats.norm.cdf(-za - ncp))
    return np.array(out)

def sample_size_curve(p_baseline, mde_range, alpha=0.05, power=0.80):
    """Required n per variant across a range of MDEs."""
    return np.array([sample_size_proportion(p_baseline, m, alpha, power)["n_per_variant"]
                     for m in mde_range])

# ── 2. SEQUENTIAL ANALYSIS ───────────────────────────────────────────────────
def sprt_boundaries(alpha=0.05, beta=0.20):
    """Wald SPRT log thresholds: (lower, upper)."""
    return np.log(beta/(1-alpha)), np.log((1-beta)/alpha)

def sprt_llr(x_treatment, n_treatment, p0, p1):
    """Cumulative log-likelihood ratio (treatment arm)."""
    return (x_treatment*np.log(p1/p0) +
            (n_treatment-x_treatment)*np.log((1-p1)/(1-p0)))

def obrien_fleming_boundaries(n_looks, alpha=0.05, two_tailed=True):
    """O'Brien-Fleming critical z-values at each interim look."""
    fracs = np.linspace(1/n_looks, 1.0, n_looks)
    return _za(alpha, two_tailed) / np.sqrt(fracs)

def simulate_sequential_test(p_control, p_treatment, n_total,
                              alpha=0.05, beta=0.20, n_looks=10, seed=42):
    """
    Simulate streaming experiment; compare naive peeking vs O'Brien-Fleming.
    Returns dict with DataFrame of per-look stats and stopping info.
    """
    rng  = np.random.default_rng(seed)
    ctrl = rng.binomial(1, p_control,   n_total)
    trt  = rng.binomial(1, p_treatment, n_total)
    sizes     = [int(n_total*(i+1)/n_looks) for i in range(n_looks)]
    of_bounds = obrien_fleming_boundaries(n_looks, alpha)
    z_naive   = _za(alpha)
    rows, ns, os_ = [], None, None
    for idx, n in enumerate(sizes):
        xc, xt = ctrl[:n].sum(), trt[:n].sum()
        rc, rt = xc/n, xt/n
        pp = (xc+xt)/(2*n)
        se = max(np.sqrt(2*pp*(1-pp)/n), 1e-12)
        z  = (rt-rc)/se
        nr = abs(z) >= z_naive
        or_ = abs(z) >= of_bounds[idx]
        if ns is None and nr:  ns  = dict(look=idx+1, n=n, z=round(z,3))
        if os_ is None and or_: os_ = dict(look=idx+1, n=n, z=round(z,3),
                                            boundary=round(of_bounds[idx],3))
        rows.append(dict(look=idx+1, n_seen=n, r_control=round(rc,4),
                         r_treatment=round(rt,4), z_stat=round(z,3),
                         naive_boundary=round(z_naive,3),
                         obf_boundary=round(of_bounds[idx],3),
                         naive_reject=nr, obf_reject=or_))
    return dict(results=pd.DataFrame(rows), naive_stopped=ns, obf_stopped=os_,
                true_effect=round(p_treatment-p_control,4),
                n_looks=n_looks, n_total=n_total)

# ── 3. MULTIPLE TESTING CORRECTIONS ─────────────────────────────────────────
def bonferroni(p_values, alpha=0.05):
    m   = len(p_values)
    adj = np.minimum(p_values*m, 1.0)
    rej = adj <= alpha
    return dict(method="Bonferroni", adjusted_p=adj, rejected=rej, n_rejected=int(rej.sum()))

def holm_bonferroni(p_values, alpha=0.05):
    m, idx = len(p_values), np.argsort(p_values)
    adj, rej, ok = np.zeros(m), np.zeros(m, bool), True
    for rank, i in enumerate(idx):
        adj[i] = min(p_values[i]*(m-rank), 1.0)
        if ok and p_values[i] <= alpha/(m-rank): rej[i] = True
        else: ok = False
    return dict(method="Holm-Bonferroni", adjusted_p=adj, rejected=rej, n_rejected=int(rej.sum()))

def benjamini_hochberg(p_values, alpha=0.05):
    m, idx = len(p_values), np.argsort(p_values)
    thr  = (np.arange(1,m+1)/m)*alpha
    below = p_values[idx] <= thr
    rej  = np.zeros(m, bool)
    if below.any(): rej[idx[:np.where(below)[0].max()+1]] = True
    adj  = np.zeros(m)
    for rank, i in enumerate(idx): adj[i] = min(p_values[i]*m/(rank+1), 1.0)
    a_s = adj[idx]
    for j in range(m-2,-1,-1): a_s[j] = min(a_s[j], a_s[j+1])
    adj[idx] = a_s
    return dict(method="BH-FDR", adjusted_p=adj, rejected=rej, n_rejected=int(rej.sum()))

def multiple_testing_summary(p_values, alpha=0.05, labels=None):
    if labels is None: labels = [f"H{i+1}" for i in range(len(p_values))]
    bon, holm, bh = bonferroni(p_values,alpha), holm_bonferroni(p_values,alpha), benjamini_hochberg(p_values,alpha)
    return pd.DataFrame({
        "Hypothesis":           labels,
        "Raw p":                p_values.round(4),
        "Reject (raw)":         p_values <= alpha,
        "Adj p (Bonferroni)":   bon["adjusted_p"].round(4),
        "Reject (Bonferroni)":  bon["rejected"],
        "Adj p (Holm)":         holm["adjusted_p"].round(4),
        "Reject (Holm)":        holm["rejected"],
        "Adj p (BH-FDR)":       bh["adjusted_p"].round(4),
        "Reject (BH-FDR)":      bh["rejected"],
    })

# ── 4. BAYESIAN A/B TESTING ──────────────────────────────────────────────────
def beta_posterior(a_prior, b_prior, conversions, trials):
    return a_prior+conversions, b_prior+(trials-conversions)

def prob_b_beats_a(a_a, b_a, a_b, b_b, n=200_000, seed=42):
    rng = np.random.default_rng(seed)
    return float((rng.beta(a_b,b_b,n) > rng.beta(a_a,b_a,n)).mean())

def expected_loss(a_a, b_a, a_b, b_b, n=200_000, seed=42):
    rng = np.random.default_rng(seed)
    sa, sb = rng.beta(a_a,b_a,n), rng.beta(a_b,b_b,n)
    return float(np.maximum(sb-sa,0).mean()), float(np.maximum(sa-sb,0).mean())

def bayesian_ab_summary(n_control, x_control, n_treatment, x_treatment,
                         alpha_prior=1.0, beta_prior=1.0,
                         credible_interval=0.95, n_samples=200_000, seed=42):
    a_a,b_a = beta_posterior(alpha_prior,beta_prior,x_control,n_control)
    a_b,b_b = beta_posterior(alpha_prior,beta_prior,x_treatment,n_treatment)
    lo,hi   = (1-credible_interval)/2, 1-(1-credible_interval)/2
    ma,mb   = stats.beta.mean(a_a,b_a), stats.beta.mean(a_b,b_b)
    cia,cib = stats.beta.ppf([lo,hi],a_a,b_a), stats.beta.ppf([lo,hi],a_b,b_b)
    pw      = prob_b_beats_a(a_a,b_a,a_b,b_b,n_samples,seed)
    la,lb   = expected_loss(a_a,b_a,a_b,b_b,n_samples,seed)
    rec     = ("Deploy Treatment" if pw>0.95 else
               "Continue Testing" if pw>0.80 else "Keep Control")
    p = int(credible_interval*100)
    return dict(mean_control=round(ma,4), mean_treatment=round(mb,4),
                uplift=round(mb-ma,4), relative_uplift_pct=round((mb-ma)/ma*100,2),
                **{f"ci{p}_control": cia.round(4).tolist()},
                **{f"ci{p}_treatment": cib.round(4).tolist()},
                prob_treatment_wins=round(pw,4),
                expected_loss_choose_control=round(la,6),
                expected_loss_choose_treatment=round(lb,6),
                recommendation=rec,
                posterior_control=(a_a,b_a), posterior_treatment=(a_b,b_b),
                n_control=n_control, n_treatment=n_treatment)

def frequentist_ab_summary(n_control, x_control, n_treatment, x_treatment, alpha=0.05):
    pc,pt = x_control/n_control, x_treatment/n_treatment
    pp    = (x_control+x_treatment)/(n_control+n_treatment)
    se    = max(np.sqrt(pp*(1-pp)*(1/n_control+1/n_treatment)), 1e-12)
    z     = (pt-pc)/se
    pv    = 2*(1-stats.norm.cdf(abs(z)))
    se2   = np.sqrt(pc*(1-pc)/n_control+pt*(1-pt)/n_treatment)
    ci    = [(pt-pc)+stats.norm.ppf(q)*se2 for q in [0.025,0.975]]
    return dict(p_control=round(pc,4), p_treatment=round(pt,4),
                absolute_lift=round(pt-pc,4),
                relative_lift_pct=round((pt-pc)/pc*100,2),
                z_statistic=round(z,4), p_value=round(pv,6),
                significant=bool(pv<alpha),
                ci_95_diff=[round(c,4) for c in ci], alpha=alpha)
