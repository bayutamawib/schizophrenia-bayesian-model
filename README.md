# Bayesian Inference Model of Corollary Discharge Dysfunction in Schizophrenia

A computational analysis applying Bayesian predictive coding theory to EEG data, quantifying efference copy precision deficits in schizophrenia patients.

## Overview

This project formalizes the corollary discharge process — a neural mechanism by which the brain predicts sensory consequences of its own actions — as a linear Bayesian model. Using EEG data from 81 participants (32 healthy controls, 49 schizophrenia patients), we quantify how the brain weights motor preparation signals into auditory predictions.

### Key Findings

| Metric | Healthy Controls (N=32) | Schizophrenia (N=49) |
|---|---|---|
| Efference Copy Strength (C3_B1) | 1.4425 µV | 0.7856 µV |
| N100 Suppression | 2.0181 µV | 1.4818 µV |
| Precision Weight (x) | -1.3990 | -1.8862 |
| Linear Model | y = c − 1.3990x | y = c − 1.8862x |

**Core finding:** The efference copy signal is ~45% weaker in schizophrenia, yet the brain paradoxically applies a *higher* precision weight, suggesting an active but unsuccessful compensatory mechanism.

## Project Structure

```
├── README.md
├── calculate_weights.py              # Bayesian precision weight calculation
├── calculate_ancova_precision.py     # ANCOVA + variance-based ITPC proxy
├── generate_paper_draft.py           # Academic paper draft generator
├── bayesian_model_report.md          # Bayesian model analysis report
├── ancova_precision_report.md        # ANCOVA precision analysis report
├── mergedTrialData.xlsx              # Per-trial EEG data (N100, P200, Baseline)
├── demographic.xlsx                  # Participant demographics
├── ancova_subject_results.csv        # Per-subject ANCOVA results
└── paper_draft.docx                  # Generated academic paper draft
```

## The Bayesian Model

The corollary discharge process is modeled as:

```
N100_Active = N100_Passive − x × Motor_Prep
```

Where:
- **N100_Active** = Auditory response during self-generated sound (Prediction Error)
- **N100_Passive** = Auditory response during passive listening (Sensory Baseline)
- **Motor_Prep** = C3 electrode baseline activity before button press (Efference Copy)
- **x** = Precision Weight (how strongly the brain integrates motor signals into predictions)

## Dataset

Based on the EEG experiment by Ford et al. (2014):
- **81 participants**: 32 healthy controls, 49 schizophrenia patients
- **3 conditions**: Active Button Press + Tone, Passive Tone Playback, Button Press Only
- **9 EEG electrodes**: Fz, FCz, Cz, FC3, FC4, C3, C4, CP3, CP4
- **~24,000 trials** with N100, P200, and baseline measurements

## Requirements

```
pip install pandas openpyxl scipy numpy python-docx
```

## Usage

### Calculate Bayesian Weights
```bash
python calculate_weights.py
```

### Run ANCOVA Precision Analysis
```bash
python calculate_ancova_precision.py
```

### Generate Paper Draft
```bash
python generate_paper_draft.py
```

## References

1. Ford, J. M., et al. (2014). *Did I Do That? Abnormal Predictive Processes in Schizophrenia When Button Pressing to Deliver a Tone.* Schizophrenia Bulletin, 40(4), 804–812.
2. Adams, R. A., & Friston, K. J. (2016). *Brain Computations in Schizophrenia.* The Neurobiology of Schizophrenia, 283–295.
3. Fletcher, P. C., & Frith, C. D. (2008). *Perceiving is believing: a Bayesian approach to explaining the positive symptoms of schizophrenia.* Nature Reviews Neuroscience, 10, 48–58.
4. Pynn, L. K., & DeSouza, J. F. X. (2012). *The function of efference copy signals: Implications for symptoms of schizophrenia.* Vision Research, 76, 124–133.
5. Valton, V., et al. (2017). *Comprehensive review: Computational modelling of Schizophrenia.* Neuroscience & Biobehavioral Reviews, 83, 631–646.

## License

This project is for academic/research purposes.
