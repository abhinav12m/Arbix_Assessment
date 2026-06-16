# LLM_NOTES

## Tools Used

* ChatGPT

## Where They Were Used

* Reviewing the provided training script.
* Discussing validation strategy.
* Assisting with the structure and wording of the audit memo and README.

---

## Actual Prompt 1

Help me audit this ML training script and identify severe and high-risk issues.

---

## Actual Prompt 2

Suggest a safer validation strategy for a scoring engine dataset that contains application years.

---

## Actual Prompt 3

Help me prepare audit_memo.md and README.md for this assessment.

---

## Suggestions Accepted

* Remove `defaulted_in_next_12_months` because it introduces future information leakage.
* Use a temporal validation split instead of a random train/test split.
* Keep business policy separate from model training.
* Improve the structure and clarity of the audit memo and README.

---

## Suggestions Rejected

Suggestions involving more complex feature engineering and model pipelines were not adopted in order to keep the solution simple and focused on the main risks identified in the audit.

---

## Personally Verified

* Leakage reasoning.
* Validation split approach.
* Model training and execution.
* Generated model artifact.
