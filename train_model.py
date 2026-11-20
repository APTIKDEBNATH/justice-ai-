"""
Justice AI - Machine Learning & NLP Model Training Pipeline
Trains calibrated multi-class text classifiers for:
1. Legal Jurisdiction Classification (IN, DE, US, UK, EU, GLOBAL)
2. Legal Intent / Domain Classification (Tenancy, Consumer, Commercial, Privacy, Employment, Criminal, Emergency)

Evaluates accuracy, macro F1-score, precision, recall, and exports serializable model artifacts.
"""

import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, f1_score, precision_score, recall_score, confusion_matrix
import joblib

def train_and_evaluate_models():
    data_path = os.path.join(os.path.dirname(__file__), "data", "legal_nlp_training_dataset.csv")
    models_dir = os.path.join(os.path.dirname(__file__), "models")
    os.makedirs(models_dir, exist_ok=True)

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}. Run data_generator.py first.")

    df = pd.read_csv(data_path)
    print(f"Loaded dataset: {len(df)} samples.\n")

    # -------------------------------------------------------------
    # MODEL 1: LEGAL JURISDICTION CLASSIFIER
    # -------------------------------------------------------------
    print("=" * 60)
    print("🚀 TRAINING MODEL 1: LEGAL JURISDICTION CLASSIFIER")
    print("=" * 60)

    X = [str(t) for t in df["text"].tolist()]
    y_jur = [str(j) for j in df["jurisdiction"].tolist()]
    y_dom = [str(d) for d in df["domain"].tolist()]

    X_train_j, X_test_j, y_train_j, y_test_j = train_test_split(
        X, y_jur, test_size=0.20, random_state=42, stratify=y_jur
    )

    jur_pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 3),
            max_features=3000,
            sublinear_tf=True,
            token_pattern=r"(?u)\b\w+\b"
        )),
        ("clf", LogisticRegression(
            C=2.5,
            max_iter=500,
            solver="lbfgs",
            random_state=42
        ))
    ])

    jur_pipeline.fit(X_train_j, y_train_j)
    y_pred_j = jur_pipeline.predict(X_test_j)

    acc_j = accuracy_score(y_test_j, y_pred_j)
    f1_j = f1_score(y_test_j, y_pred_j, average="macro")
    prec_j = precision_score(y_test_j, y_pred_j, average="macro", zero_division=0)
    rec_j = recall_score(y_test_j, y_pred_j, average="macro", zero_division=0)

    print(f"Jurisdiction Model Test Accuracy: {acc_j * 100:.2f}%")
    print(f"Jurisdiction Model Macro F1-Score: {f1_j * 100:.2f}%")
    print(f"Jurisdiction Model Precision:     {prec_j * 100:.2f}%")
    print(f"Jurisdiction Model Recall:        {rec_j * 100:.2f}%\n")
    print("Detailed Classification Report:\n")
    print(classification_report(y_test_j, y_pred_j, zero_division=0))

    jur_model_path = os.path.join(models_dir, "jurisdiction_classifier.joblib")
    joblib.dump(jur_pipeline, jur_model_path)
    print(f"✅ Saved Jurisdiction Classifier to: {jur_model_path}\n")

    # -------------------------------------------------------------
    # MODEL 2: LEGAL INTENT / DOMAIN CLASSIFIER
    # -------------------------------------------------------------
    print("=" * 60)
    print("🚀 TRAINING MODEL 2: LEGAL DOMAIN & INTENT CLASSIFIER")
    print("=" * 60)

    X_train_d, X_test_d, y_train_d, y_test_d = train_test_split(
        X, y_dom, test_size=0.20, random_state=42, stratify=y_dom
    )

    dom_pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 3),
            max_features=3000,
            sublinear_tf=True
        )),
        ("clf", LogisticRegression(
            C=3.0,
            max_iter=500,
            solver="lbfgs",
            random_state=42
        ))
    ])

    dom_pipeline.fit(X_train_d, y_train_d)
    y_pred_d = dom_pipeline.predict(X_test_d)

    acc_d = accuracy_score(y_test_d, y_pred_d)
    f1_d = f1_score(y_test_d, y_pred_d, average="macro")
    prec_d = precision_score(y_test_d, y_pred_d, average="macro", zero_division=0)
    rec_d = recall_score(y_test_d, y_pred_d, average="macro", zero_division=0)

    print(f"Domain Model Test Accuracy:  {acc_d * 100:.2f}%")
    print(f"Domain Model Macro F1-Score: {f1_d * 100:.2f}%")
    print(f"Domain Model Precision:      {prec_d * 100:.2f}%")
    print(f"Domain Model Recall:         {rec_d * 100:.2f}%\n")
    print("Detailed Classification Report:\n")
    print(classification_report(y_test_d, y_pred_d, zero_division=0))

    dom_model_path = os.path.join(models_dir, "domain_classifier.joblib")
    joblib.dump(dom_pipeline, dom_model_path)
    print(f"✅ Saved Domain Classifier to: {dom_model_path}\n")

    # -------------------------------------------------------------
    # EXPORT TRAINING AUDIT METRICS JSON
    # -------------------------------------------------------------
    metrics_payload = {
        "dataset_statistics": {
            "total_samples": len(df),
            "train_samples": len(X_train_j),
            "test_samples": len(X_test_j),
            "split_ratio": "80/20 Stratified",
            "jurisdiction_classes": list(np.unique(y_jur)),
            "domain_classes": list(np.unique(y_dom))
        },
        "model_1_jurisdiction": {
            "architecture": "TF-IDF (1-3 ngrams, sublinear) + Multinomial Logistic Regression (L2)",
            "hyperparameters": {
                "max_features": 3000,
                "regularization_C": 2.5,
                "optimizer": "L-BFGS",
                "loss": "Multinomial Cross-Entropy (log_loss)"
            },
            "metrics": {
                "accuracy": round(float(acc_j), 4),
                "macro_f1": round(float(f1_j), 4),
                "macro_precision": round(float(prec_j), 4),
                "macro_recall": round(float(rec_j), 4)
            }
        },
        "model_2_domain": {
            "architecture": "TF-IDF (1-3 ngrams, sublinear) + Multinomial Logistic Regression (L2)",
            "hyperparameters": {
                "max_features": 3000,
                "regularization_C": 3.0,
                "optimizer": "L-BFGS",
                "loss": "Multinomial Cross-Entropy (log_loss)"
            },
            "metrics": {
                "accuracy": round(float(acc_d), 4),
                "macro_f1": round(float(f1_d), 4),
                "macro_precision": round(float(prec_d), 4),
                "macro_recall": round(float(rec_d), 4)
            }
        }
    }

    metrics_path = os.path.join(models_dir, "training_metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics_payload, f, indent=2)

    print(f"✅ Exported Training Metrics to: {metrics_path}")
    print("\n🎉 MODEL TRAINING COMPLETED WITH ZERO ERRORS!")

if __name__ == "__main__":
    train_and_evaluate_models()
