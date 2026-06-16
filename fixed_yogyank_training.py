"""
Changes from original:
- Removed future leakage feature
- Removed business policy modification of target
- Replaced random split with temporal validation
- Fit encoders using training data only
- Excluded farmer_id identifier field
- Added simple missing value handling
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score
import xgboost as xgb
import joblib


def load_and_prep_data(path="farmer_scoring_sample_yogyank_round1.csv"):
    return pd.read_csv(path)


def train_model():
    df = load_and_prep_data()

    target = "target_entitlement_score"

    features = [
        "application_year",
        "district",
        "land_area_acres",
        "crop_type",
        "pm_kisan_status",
        "historical_repayment_score",
        "irrigation_type",
        "land_ownership",
        "soil_type",
        "sales_channel",
        "annual_income_inr",
        "liability_ratio_pct",
        "rainfall_deviation_pct",
        "ndvi_score",
    ]

    train_df = df[df["application_year"] < 2024].copy()
    test_df = df[df["application_year"] == 2024].copy()

    if len(train_df) == 0 or len(test_df) == 0:
        raise ValueError(
            "Temporal split failed. Expected train data before 2024 "
            "and test data for 2024."
        )

    X_train = train_df[features].copy()
    X_test = test_df[features].copy()

    y_train = train_df[target]
    y_test = test_df[target]

    # Missing value handling using training data only
    for col in ["rainfall_deviation_pct", "ndvi_score"]:
        median_value = X_train[col].median()

        X_train[col] = X_train[col].fillna(median_value)
        X_test[col] = X_test[col].fillna(median_value)

    categorical_columns = [
        "district",
        "crop_type",
        "pm_kisan_status",
        "irrigation_type",
        "land_ownership",
        "soil_type",
        "sales_channel",
    ]

    encoders = {}

    print("Encoding categorical variables...")

    for col in categorical_columns:
        encoder = LabelEncoder()

        X_train[col] = encoder.fit_transform(X_train[col])
        X_test[col] = encoder.transform(X_test[col])

        encoders[col] = encoder

    print("Training XGBoost...")

    model = xgb.XGBRegressor(
        n_estimators=60,
        max_depth=4,
        learning_rate=0.1,
        random_state=42,
        n_jobs=1,
        tree_method="hist",
    )

    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    score = r2_score(y_test, preds)

    print(f"Temporal Holdout R2 Score: {score:.4f}")

    joblib.dump(
        {
            "model": model,
            "encoders": encoders,
            "features": features,
        },
        "xgboost_baseline.pkl",
    )

    print("Model saved to xgboost_baseline.pkl")


if __name__ == "__main__":
    train_model()