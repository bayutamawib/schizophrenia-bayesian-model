# ANCOVA + Variance-Based Proxy: Efference Copy Precision Report

## Overview
Since raw trial-level time-series data is unavailable for true ITPC (Hilbert Transform) calculation, we implemented an **ANCOVA + Variance-based Proxy** pipeline to estimate the **temporal precision** of the efference copy signal (`C3_B1`) for both Healthy Controls (HC) and Schizophrenia patients (SZ).

The goal: remove the mathematical coupling between SD and Mean amplitude, isolating **pure variability** as a proxy for phase jitter.

---

## Pipeline

1. Per subject → Calculate **Mean** and **SD** of `C3_B1` across all Condition 1 (Active Button Press) trials
2. Regress **SD ~ Mean** (pooled across all 81 subjects) to model the coupling
3. Extract **Residuals** = Adjusted SD (ITPC Proxy)
4. Compare groups via independent t-test

---

## Results

### ANCOVA Regression (SD ~ Mean)

` SD = 10.9922 + (-0.7913) * Mean `

| Metric | Value |
|---|---|
| R-squared | 0.1398 |
| p-value | 0.000586 |

The regression is highly significant (p < 0.001), confirming that **~14% of the variance in SD is explained by Mean amplitude alone**. This validates the need for ANCOVA correction — without it, raw SD would be contaminated by amplitude effects.

### Group Comparison

| Metric | HC (N=32) | SZ (N=49) |
|---|---|---|
| Mean C3_B1 (Efference Copy Strength) | 1.4425 µV | 0.7856 µV |
| Raw SD of C3_B1 | 9.4648 µV | 10.6226 µV |
| **Adjusted SD (ITPC Proxy)** | **-0.3859 µV** | **0.2520 µV** |

### Statistical Test (Adjusted SD: HC vs SZ)

| Metric | Value |
|---|---|
| t-statistic | -0.7445 |
| p-value | 0.4588 |
| Significant (p < 0.05) | **NO** |
| Cohen's d | -0.1712 (small effect) |

### Raw SD vs Adjusted SD Comparison

| Metric | t-stat | p-value |
|---|---|---|
| Raw SD | -1.2613 | 0.2109 |
| Adjusted SD (ANCOVA corrected) | -0.7445 | 0.4588 |

---

## Interpretation

### Key Finding: The Precision Difference is NOT Statistically Significant

After ANCOVA correction, the Adjusted SD difference between HC and SZ is **not significant** (p = 0.459, Cohen's d = -0.17).

**What does this mean for our Bayesian model?**

The direction is correct — SZ patients show a **positive** Adjusted SD (+0.25), meaning slightly more variability than predicted by their mean amplitude, while HC shows **negative** Adjusted SD (-0.39), meaning slightly less variability than expected. However, the effect is **too small** to be reliable with this sample size.

### Why the Difference is Not Significant

1. **Small sample size**: Only 32 HC and 49 SZ subjects. ITPC-like measures typically need larger samples to detect subtle timing differences.
2. **Amplitude proxy ≠ True phase**: The Adjusted SD captures amplitude consistency, not true temporal phase coherence. The actual timing jitter may be more pronounced than what amplitude variability can capture.
3. **C3_B1 is already a summary feature**: Each trial's `C3_B1` value is itself an average over a time window, which smooths out trial-to-trial phase jitter.

### Implications for the Full Bayesian Model

The **amplitude-based weight** (`y = c + wx`) from our earlier analysis remains the **stronger predictor** of group differences. The efference copy *strength* (Mean C3_B1: 1.44 vs 0.79 µV) is where the core deficit lies, not its trial-to-trial consistency.

The updated Bayesian model interpretation:
- **Primary deficit**: Efference copy **strength** is ~46% weaker in SZ (confirmed by weight model)
- **Secondary deficit**: Efference copy **precision** trends in the expected direction but is not statistically significant with this proxy method

---

## Files Generated

- [calculate_ancova_precision.py](file:///Users/narendrabayutamaw/Documents/MSc%20Application%20Portfolio/Schizophrenia%20Project/calculate_ancova_precision.py) — Full pipeline script
- [ancova_subject_results.csv](file:///Users/narendrabayutamaw/Documents/MSc%20Application%20Portfolio/Schizophrenia%20Project/ancova_subject_results.csv) — Per-subject results with Adjusted SD values
