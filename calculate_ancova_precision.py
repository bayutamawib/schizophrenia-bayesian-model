"""
ANCOVA + Variance-Based Proxy Pipeline
=======================================
Calculates the Adjusted Standard Deviation (ITPC Proxy) of the efference copy
signal (C3_B1) for Healthy Controls and Schizophrenia patients.

Pipeline:
1. Per subject: Calculate Mean(C3_B1) and SD(C3_B1) across Condition 1 trials
2. Regress SD ~ Mean (linear regression across all subjects within each group)
3. Extract Residuals = Adjusted SD (the ITPC Proxy)
4. Compare Adjusted SD between HC and SZ groups

"""

import pandas as pd
import numpy as np
from scipy import stats


def load_and_prepare_data():
    """Load and merge trial data with demographics, filter rejected trials."""
    print("Loading data...")
    df_trials = pd.read_excel('mergedTrialData.xlsx')
    df_demo = pd.read_excel('demographic.xlsx')
    df_demo.columns = df_demo.columns.str.strip()

    df = pd.merge(df_trials, df_demo, on='subject')

    # Filter out rejected trials
    df_clean = df[df['rejected'] == 0].copy()
    print(f"Total clean trials: {len(df_clean)}")
    return df_clean


def calculate_subject_stats(df_clean):
    """
    For each subject, calculate:
    - Mean of C3_B1 across all Condition 1 trials
    - SD of C3_B1 across all Condition 1 trials
    - Trial count
    """
    df_c1 = df_clean[df_clean['condition'] == 1].copy()

    subject_stats = df_c1.groupby(['subject', 'group']).agg(
        mean_C3_B1=('C3_B1', 'mean'),
        sd_C3_B1=('C3_B1', 'std'),
        trial_count=('C3_B1', 'count')
    ).reset_index()

    print(f"\nSubjects with Condition 1 data: {len(subject_stats)}")
    print(f"  Healthy Controls (HC, group=0): "
          f"{len(subject_stats[subject_stats['group'] == 0])}")
    print(f"  Schizophrenia (SZ, group=1): "
          f"{len(subject_stats[subject_stats['group'] == 1])}")

    return subject_stats


def perform_ancova_regression(subject_stats):
    """
    Regress SD ~ Mean across ALL subjects (pooled) to remove
    mathematical coupling between SD and Mean.
    The residuals = Adjusted SD (ITPC Proxy).
    """
    print("\n" + "=" * 60)
    print("STEP 1: ANCOVA Regression (SD ~ Mean, pooled across groups)")
    print("=" * 60)

    x = subject_stats['mean_C3_B1'].values
    y = subject_stats['sd_C3_B1'].values

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    print(f"  Regression: SD = {intercept:.4f} + {slope:.4f} * Mean")
    print(f"  R-squared: {r_value**2:.4f}")
    print(f"  p-value: {p_value:.6f}")

    # Calculate predicted SD and residuals
    predicted_sd = intercept + slope * x
    residuals = y - predicted_sd

    subject_stats['predicted_sd'] = predicted_sd
    subject_stats['adjusted_sd'] = residuals

    regression_info = {
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_value**2,
        'p_value': p_value,
        'std_err': std_err
    }

    return subject_stats, regression_info


def compare_groups(subject_stats):
    """Compare Adjusted SD between HC and SZ groups."""
    print("\n" + "=" * 60)
    print("STEP 2: Group Comparison of Adjusted SD (ITPC Proxy)")
    print("=" * 60)

    hc = subject_stats[subject_stats['group'] == 0]
    sz = subject_stats[subject_stats['group'] == 1]

    results = {}

    for label, group_data in [("Healthy Controls (HC)", hc),
                               ("Schizophrenia (SZ)", sz)]:
        print(f"\n--- {label} ---")
        print(f"  N = {len(group_data)}")
        print(f"  Mean of C3_B1 (Efference Copy Strength):"
              f"  {group_data['mean_C3_B1'].mean():.4f} µV")
        print(f"  Raw SD of C3_B1:"
              f"  {group_data['sd_C3_B1'].mean():.4f} µV")
        print(f"  Adjusted SD (ITPC Proxy):"
              f"  {group_data['adjusted_sd'].mean():.4f} µV")

        results[label] = {
            'n': len(group_data),
            'mean_C3_B1': group_data['mean_C3_B1'].mean(),
            'raw_sd': group_data['sd_C3_B1'].mean(),
            'adjusted_sd_mean': group_data['adjusted_sd'].mean(),
            'adjusted_sd_std': group_data['adjusted_sd'].std()
        }

    # Independent t-test on Adjusted SD
    t_stat, p_value = stats.ttest_ind(
        hc['adjusted_sd'].values,
        sz['adjusted_sd'].values
    )

    print(f"\n--- Independent t-test (Adjusted SD: HC vs SZ) ---")
    print(f"  t-statistic: {t_stat:.4f}")
    print(f"  p-value: {p_value:.6f}")
    print(f"  Significant (p < 0.05): {'YES' if p_value < 0.05 else 'NO'}")

    # Effect size (Cohen's d)
    hc_adj = hc['adjusted_sd'].values
    sz_adj = sz['adjusted_sd'].values
    pooled_std = np.sqrt(
        ((len(hc_adj) - 1) * hc_adj.std()**2 +
         (len(sz_adj) - 1) * sz_adj.std()**2) /
        (len(hc_adj) + len(sz_adj) - 2)
    )
    cohens_d = (hc_adj.mean() - sz_adj.mean()) / pooled_std

    print(f"  Cohen's d: {cohens_d:.4f}")

    results['t_test'] = {
        't_stat': t_stat,
        'p_value': p_value,
        'cohens_d': cohens_d
    }

    return results


def compare_raw_vs_adjusted(subject_stats):
    """Show the difference between raw SD and adjusted SD analysis."""
    print("\n" + "=" * 60)
    print("STEP 3: Raw SD vs Adjusted SD Comparison")
    print("=" * 60)

    hc = subject_stats[subject_stats['group'] == 0]
    sz = subject_stats[subject_stats['group'] == 1]

    # Raw SD t-test
    t_raw, p_raw = stats.ttest_ind(
        hc['sd_C3_B1'].values, sz['sd_C3_B1'].values
    )
    # Adjusted SD t-test
    t_adj, p_adj = stats.ttest_ind(
        hc['adjusted_sd'].values, sz['adjusted_sd'].values
    )

    print(f"  Raw SD     -> t={t_raw:.4f}, p={p_raw:.6f}")
    print(f"  Adjusted SD -> t={t_adj:.4f}, p={p_adj:.6f}")
    print(f"\n  ANCOVA correction changed p-value from"
          f" {p_raw:.6f} to {p_adj:.6f}")

    return {
        'raw_t': t_raw, 'raw_p': p_raw,
        'adj_t': t_adj, 'adj_p': p_adj
    }


def display_per_subject_table(subject_stats):
    """Print a summary table of all subjects."""
    print("\n" + "=" * 60)
    print("STEP 4: Per-Subject Summary Table")
    print("=" * 60)

    display_cols = ['subject', 'group', 'trial_count',
                    'mean_C3_B1', 'sd_C3_B1', 'adjusted_sd']
    df_display = subject_stats[display_cols].copy()
    df_display['group_label'] = df_display['group'].map({0: 'HC', 1: 'SZ'})

    for group_label in ['HC', 'SZ']:
        group_data = df_display[df_display['group_label'] == group_label]
        print(f"\n--- {group_label} ---")
        print(group_data.to_string(index=False, float_format='%.4f'))


def main():
    print("=" * 60)
    print("ANCOVA + Variance-Based Proxy Pipeline")
    print("Efference Copy Precision Analysis (ITPC Proxy)")
    print("=" * 60)

    # Load data
    df_clean = load_and_prepare_data()

    # Calculate per-subject stats
    subject_stats = calculate_subject_stats(df_clean)

    # Perform ANCOVA regression
    subject_stats, regression_info = perform_ancova_regression(subject_stats)

    # Compare groups
    group_results = compare_groups(subject_stats)

    # Compare raw vs adjusted
    comparison = compare_raw_vs_adjusted(subject_stats)

    # Display per-subject table
    display_per_subject_table(subject_stats)

    # Save per-subject results to CSV
    output_file = 'ancova_subject_results.csv'
    subject_stats.to_csv(output_file, index=False)
    print(f"\nPer-subject results saved to: {output_file}")

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
