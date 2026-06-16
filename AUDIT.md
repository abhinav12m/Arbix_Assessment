# Audit Memo

## Objective

Review the provided Yogyank baseline training script and identify risks that could affect model validity, future scoring performance, and auditability.

---

## Findings

### Finding 1: Future Information Leakage

The original script includes the feature:

`defaulted_in_next_12_months`

This feature contains information that would only become available after the scoring decision. A scoring engine cannot know whether a farmer will default in the following 12 months at the time the entitlement score is generated.

Using this feature introduces target leakage and can significantly inflate validation performance.

---

### Finding 2: Business Policy Applied Directly to Training Target

The original script modifies the target variable:

```python
df.loc[df["pm_kisan_status"] == "No",
       "target_entitlement_score"] -= 150
```

This mixes business policy with model training and changes the ground-truth target values.

As a result:

* Model behavior cannot be separated from policy behavior.
* Auditing becomes difficult.
* Future policy changes would require retraining.

Business rules should be applied after model prediction rather than modifying training labels.

---

### Finding 3: Random Train/Test Split

The original implementation performs a random shuffled split.

The dataset contains an `application_year` field. Random splitting allows records from future years to influence training and evaluation.

This can produce overly optimistic estimates of future performance.

A temporal validation strategy is more appropriate.

---

### Finding 4: Preprocessing Before Data Split

Categorical encoding is fit on the entire dataset before train/test separation.

This allows information from the test set to influence preprocessing and validation.

Preprocessing should be fit only on training data and then applied to test data.

---

## Changes Implemented

* Removed `defaulted_in_next_12_months` from model inputs.
* Preserved original target values.
* Kept business policy separate from model predictions.
* Replaced random split with temporal holdout validation.
* Fit categorical encoders using training data only.
* Excluded `farmer_id` from model features.
* Added simple missing-value handling for numeric fields with missing observations.

---

## Validation Approach

Training data:

* 2022
* 2023

Evaluation data:

* 2024

This approach better simulates future scoring than a random split.

---

## Remaining Limitations

### One Thing I Would Not Trust Yet

I have not confirmed that all features are available before scoring, so there may still be hidden leakage risks.

### One Thing I Would Improve With More Time

I would perform a formal feature availability review and establish a documented feature contract covering source systems, refresh frequency, and scoring-time availability.
