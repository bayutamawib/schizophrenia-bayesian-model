"""
Bayesian Model Weight Calculator (Subject-Level Aggregation)
============================================================
Calculates the precision weight (x) in the model:
    N100_Active = N100_Passive - x * Motor_Prep

Method: First averages per subject, then computes the grand mean
across subjects (subject-level aggregation), ensuring each participant
contributes equally regardless of their trial count.
"""

import pandas as pd


def calculate_weights_subject_level():
    print("Loading data...")
    df_trials = pd.read_excel('mergedTrialData.xlsx')
    df_demo = pd.read_excel('demographic.xlsx')

    # Clean column names
    df_demo.columns = df_demo.columns.str.strip()

    # Merge
    df = pd.merge(df_trials, df_demo, on='subject')

    # Exclude rejected trials
    df_clean = df[df['rejected'] == 0]

    groups = {
        0: "Healthy Controls (HC)",
        1: "Schizophrenia Patients (SZ)"
    }

    results = {}

    for group_id, group_name in groups.items():
        df_group = df_clean[df_clean['group'] == group_id]

        # --- Condition 1 (Active): average per subject first ---
        df_c1 = df_group[df_group['condition'] == 1]
        subject_means_c1 = df_c1.groupby('subject').agg({
            'Fz_N100': 'mean',
            'FCz_N100': 'mean',
            'Cz_N100': 'mean',
            'C3_B1': 'mean'
        }).reset_index()

        # --- Condition 2 (Passive): average per subject first ---
        df_c2 = df_group[df_group['condition'] == 2]
        subject_means_c2 = df_c2.groupby('subject').agg({
            'Fz_N100': 'mean',
            'FCz_N100': 'mean',
            'Cz_N100': 'mean'
        }).reset_index()

        # --- Grand Mean across subjects ---
        # N100 Active (Condition 1)
        n100_c1_per_subject = (subject_means_c1['Fz_N100']
                               + subject_means_c1['FCz_N100']
                               + subject_means_c1['Cz_N100']) / 3
        n100_c1 = n100_c1_per_subject.mean()

        # Motor Prep C3_B1 (Condition 1)
        c3_b1_c1 = subject_means_c1['C3_B1'].mean()

        # N100 Passive (Condition 2)
        n100_c2_per_subject = (subject_means_c2['Fz_N100']
                               + subject_means_c2['FCz_N100']
                               + subject_means_c2['Cz_N100']) / 3
        n100_c2 = n100_c2_per_subject.mean()

        # --- Calculate Precision Weight (x) ---
        # Formula: N100_C1 = N100_C2 - (C3_B1_C1 * x)
        # Therefore: x = (N100_C2 - N100_C1) / C3_B1_C1
        if c3_b1_c1 != 0:
            x = (n100_c2 - n100_c1) / c3_b1_c1
        else:
            x = float('inf')

        results[group_name] = {
            'N100_Active (C1)': n100_c1,
            'N100_Passive (C2)': n100_c2,
            'Motor_Prep (C3_B1)': c3_b1_c1,
            'Weight (x)': x
        }

        print(f"\n--- {group_name} ---")
        print(f"N subjects: {len(subject_means_c1)}")
        print(f"N100 Active (Condition 1): {n100_c1:.4f} µV")
        print(f"N100 Passive (Condition 2): {n100_c2:.4f} µV")
        print(f"Motor Prep C3_B1 (Condition 1): {c3_b1_c1:.4f} µV")
        print(f"Calculated Weight (x): {x:.4f}")


if __name__ == "__main__":
    calculate_weights_subject_level()
