import json
import os
import sys

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import GroupShuffleSplit, cross_val_score, GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from ml.rules import DIFFICULTIES, FEATURES  # noqa: E402

DATA = os.path.join(HERE, "..", "data", "student_interactions.csv")


def main():
    df = pd.read_csv(DATA)
    df = df.dropna().drop_duplicates()
    X, y, groups = df[FEATURES], df["next_difficulty"], df["student_id"]

    splitter = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    train_idx, test_idx = next(splitter.split(X, y, groups))
    X_tr, X_te, y_tr, y_te = X.iloc[train_idx], X.iloc[test_idx], y.iloc[train_idx], y.iloc[test_idx]

    models = {
        "Logistic Regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
        "Decision Tree": DecisionTreeClassifier(max_depth=8, min_samples_leaf=20, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=200, max_depth=12, min_samples_leaf=10,
                                                random_state=42, n_jobs=-1),
    }

    results, fitted = {}, {}
    for name, model in models.items():
        cv = cross_val_score(model, X_tr, y_tr, groups=groups.iloc[train_idx],
                             cv=GroupKFold(n_splits=5), scoring="f1_macro")
        model.fit(X_tr, y_tr)
        pred = model.predict(X_te)
        results[name] = {
            "cv_f1_macro": round(float(cv.mean()), 4),
            "test_accuracy": round(float(accuracy_score(y_te, pred)), 4),
            "test_f1_macro": round(float(f1_score(y_te, pred, average="macro")), 4),
        }
        fitted[name] = model
        print(f"{name:20s} CV F1={results[name]['cv_f1_macro']:.3f}  "
              f"test acc={results[name]['test_accuracy']:.3f}  "
              f"test F1={results[name]['test_f1_macro']:.3f}")

    best_name = max(results, key=lambda n: results[n]["cv_f1_macro"])
    # Scores this close are a tie; prefer Random Forest (explainable, has feature importances).
    if results["Random Forest"]["cv_f1_macro"] >= results[best_name]["cv_f1_macro"] - 0.005:
        best_name = "Random Forest"
    best = fitted[best_name]
    pred = best.predict(X_te)
    print(f"\nBest model: {best_name}\n")
    print(classification_report(y_te, pred, target_names=DIFFICULTIES))
    cm = confusion_matrix(y_te, pred).tolist()
    print("Confusion matrix (rows=true, cols=predicted):", cm)

    importances = None
    if hasattr(best, "feature_importances_"):
        importances = dict(zip(FEATURES, [round(float(v), 4) for v in best.feature_importances_]))
        print("Feature importances:", importances)

    joblib.dump({"model": best, "features": FEATURES, "name": best_name}, os.path.join(HERE, "model.pkl"))
    with open(os.path.join(HERE, "metrics.json"), "w") as fh:
        json.dump({"best_model": best_name, "results": results, "confusion_matrix": cm,
                   "feature_importances": importances}, fh, indent=2)
    print("\nSaved ml/model.pkl and ml/metrics.json")


if __name__ == "__main__":
    main()
