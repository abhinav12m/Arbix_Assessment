# Yogyank Assessment

## Time

Start Time (IST): 8:10 pm

End Time (IST): 9:20 pm

Approximate Time Spent: 90 minutes

---

## Setup

Create and activate a virtual environment.

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

---

## Run

```bash
python fixed_yogyank_training.py
```

---

## Files Generated

* xgboost_baseline.pkl

---

## What I Completed

* Audited the provided training script.
* Removed future-information leakage.
* Removed target modification logic.
* Implemented temporal validation.
* Restricted preprocessing to training data.
* Excluded identifier fields from model features.
* Added simple handling for missing numeric values.
* Saved trained model artifact.

---

## What I Did Not Complete

* Production-grade monitoring.
* Feature contracts and schema validation.
* Explainability and reason-code generation.
* Hyperparameter optimization.

---

## Assumptions

* `defaulted_in_next_12_months` is not available at scoring time and was excluded due to leakage risk.
* PM-Kisan adjustments represent business policy and should not modify training labels.
* Remaining features are assumed to be available before scoring.
* `farmer_id` is treated as an identifier rather than a predictive feature.

---

## Validation Approach

Temporal holdout validation was used.

Training:

* 2022
* 2023

Testing:

* 2024

This better simulates future scoring than a random train/test split.

Validation Result:

* Temporal Holdout R²: **0.7110**

For comparison, the original script reported:

* Random Split R²: **0.6886**

The objective of the changes was to improve validation reliability rather than maximize the metric.

---

## Trust Level

The validation approach is more realistic than the original implementation. However, I have not independently verified that every feature would be available before scoring, so some leakage risks may still remain.
