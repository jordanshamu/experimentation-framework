import os
import sys

import numpy as np
import pytest
from statsmodels.stats.multitest import multipletests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from stats_utils import (  # noqa: E402
    benjamini_hochberg,
    frequentist_ab_summary,
    holm_bonferroni,
    obrien_fleming_boundaries,
    power_curve,
    simulate_sequential_test,
)


# ── Holm-Bonferroni ──────────────────────────────────────────────────────────
def test_holm_known_answer():
    res = holm_bonferroni(np.array([0.01, 0.03, 0.04]), alpha=0.05)
    np.testing.assert_allclose(res["adjusted_p"], [0.03, 0.06, 0.06])
    assert res["rejected"].tolist() == [True, False, False]


@pytest.mark.parametrize("seed", range(20))
def test_holm_matches_statsmodels(seed):
    rng = np.random.default_rng(seed)
    m = int(rng.integers(2, 40))
    p = np.concatenate([rng.uniform(0, 1, m // 2), rng.beta(0.3, 8, m - m // 2)])
    rej_sm, adj_sm, _, _ = multipletests(p, alpha=0.05, method="holm")
    res = holm_bonferroni(p, alpha=0.05)
    np.testing.assert_allclose(res["adjusted_p"], adj_sm, rtol=1e-12, atol=1e-12)
    assert res["rejected"].tolist() == rej_sm.tolist()


@pytest.mark.parametrize("seed", range(20))
def test_bh_matches_statsmodels(seed):
    rng = np.random.default_rng(1000 + seed)
    m = int(rng.integers(2, 40))
    p = np.concatenate([rng.uniform(0, 1, m // 2), rng.beta(0.3, 8, m - m // 2)])
    rej_sm, adj_sm, _, _ = multipletests(p, alpha=0.05, method="fdr_bh")
    res = benjamini_hochberg(p, alpha=0.05)
    np.testing.assert_allclose(res["adjusted_p"], adj_sm, rtol=1e-12, atol=1e-12)
    assert res["rejected"].tolist() == rej_sm.tolist()


# ── power_curve ──────────────────────────────────────────────────────────────
def test_power_one_sided_zero_effect_equals_alpha():
    pwr = power_curve(0.10, [0.0], n_per_variant=1000, alpha=0.05, two_tailed=False)
    assert pwr[0] == pytest.approx(0.05, abs=1e-12)


def test_power_one_sided_negative_effect_below_alpha():
    pwr = power_curve(0.10, [-0.02], n_per_variant=1000, alpha=0.05, two_tailed=False)
    assert pwr[0] < 0.05


def test_power_two_sided_zero_effect_equals_alpha():
    pwr = power_curve(0.10, [0.0], n_per_variant=1000, alpha=0.05, two_tailed=True)
    assert pwr[0] == pytest.approx(0.05, abs=1e-12)


# ── O'Brien-Fleming ──────────────────────────────────────────────────────────
@pytest.mark.parametrize("n_looks, C", [(2, 1.977), (5, 2.040), (10, 2.087)])
def test_obf_constant_known_answers(n_looks, C):
    b = obrien_fleming_boundaries(n_looks, alpha=0.05)
    assert b[-1] == pytest.approx(C, abs=1e-3)
    k = np.arange(1, n_looks + 1)
    np.testing.assert_allclose(b, b[-1] * np.sqrt(n_looks / k))


def _null_crossing_rate(bounds, n_sims, seed):
    """Seeded Monte Carlo: Z_k = S_k / sqrt(k) with S_k a sum of iid N(0,1)."""
    K = len(bounds)
    rng = np.random.default_rng(seed)
    z = np.cumsum(rng.standard_normal((n_sims, K)), axis=1) / np.sqrt(np.arange(1, K + 1))
    return float((np.abs(z) >= bounds).any(axis=1).mean())


@pytest.mark.parametrize("n_looks", [2, 5, 10])
def test_obf_null_simulation_holds_alpha(n_looks):
    n_sims = 1_000_000
    rate = _null_crossing_rate(obrien_fleming_boundaries(n_looks, 0.05), n_sims, seed=n_looks)
    mc_se = np.sqrt(0.05 * 0.95 / n_sims)
    assert abs(rate - 0.05) < 4 * mc_se


def test_naive_peeking_inflates_alpha():
    rate = _null_crossing_rate(np.full(10, 1.959964), 1_000_000, seed=0)
    assert 0.18 < rate < 0.20


def test_obf_binomial_null_simulation():
    """End-to-end on binomial data: 10 looks, 10,000 users per arm, p = 0.10."""
    rng = np.random.default_rng(2024)
    n_sims, K, n = 100_000, 10, 10_000
    batch = n // K
    xc = np.cumsum(rng.binomial(batch, 0.10, (n_sims, K)), axis=1)
    xt = np.cumsum(rng.binomial(batch, 0.10, (n_sims, K)), axis=1)
    m = batch * np.arange(1, K + 1)
    pp = (xc + xt) / (2 * m)
    z = (xt - xc) / m / np.sqrt(2 * pp * (1 - pp) / m)
    rate = float((np.abs(z) >= obrien_fleming_boundaries(K, 0.05)).any(axis=1).mean())
    assert abs(rate - 0.05) < 4 * np.sqrt(0.05 * 0.95 / n_sims)


# ── simulate_sequential_test ─────────────────────────────────────────────────
def test_simulate_sequential_test_uses_n_per_arm():
    sim = simulate_sequential_test(0.10, 0.10, n_per_arm=5_000, n_looks=5, seed=1)
    assert sim["n_per_arm"] == 5_000
    assert sim["results"]["n_seen"].iloc[-1] == 5_000


# ── frequentist_ab_summary ───────────────────────────────────────────────────
def test_frequentist_ci_follows_alpha():
    r95 = frequentist_ab_summary(5000, 500, 5000, 560, alpha=0.05)
    r99 = frequentist_ab_summary(5000, 500, 5000, 560, alpha=0.01)
    assert r95["ci_level"] == pytest.approx(0.95)
    assert r99["ci_level"] == pytest.approx(0.99)
    w95 = r95["ci_diff"][1] - r95["ci_diff"][0]
    w99 = r99["ci_diff"][1] - r99["ci_diff"][0]
    assert w99 / w95 == pytest.approx(2.575829 / 1.959964, rel=1e-2)


def test_frequentist_p_value_not_rounded():
    r = frequentist_ab_summary(23_524, 420, 564_577, 14_423)
    assert 0 < r["p_value"] < 1e-6
    r2 = frequentist_ab_summary(5000, 500, 5000, 560)
    assert r2["p_value"] != round(r2["p_value"], 6)
