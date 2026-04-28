import os
import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_BASE = os.path.join(BASE_DIR, "data", "processed", "datathon_base_tratada.csv")
PASTA_MODELOS = os.path.join(BASE_DIR, "models")
PASTA_REPORTS = os.path.join(BASE_DIR, "reports")


def treinar_modelo():
    print("📖 Lendo base tratada...")
    df = pd.read_csv(ARQUIVO_BASE, sep=";", encoding="utf-8-sig", decimal=",")

    features_num = [
        "IDADE", "ANO_INGRESSO", "INDE", "IAA", "IEG", "IPS",
        "IPP", "IDA", "IPV", "MAT", "POR", "ING"
    ]

    features_cat = [
        "ANO", "FASE", "GENERO", "INSTITUICAO_ENSINO", "PEDRA",
        "ATINGIU_PV", "INDICADO", "REC_PSICOLOGIA"
    ]

    # IMPORTANTE:
    # IAN e DEFASAGEM não entram como features para evitar vazamento de informação.
    X = df[features_num + features_cat].copy()
    y = df["RISCO_DEFASAGEM"].astype(int)

    for col in features_cat:
        X[col] = X[col].astype("string").fillna("Não informado")

    preprocessador = ColumnTransformer([
        ("num", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ]), features_num),
        ("cat", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore"))
        ]), features_cat),
    ])

    modelo = RandomForestClassifier(
        n_estimators=300,
        max_depth=8,
        min_samples_leaf=8,
        random_state=42,
        class_weight="balanced"
    )

    pipeline = Pipeline([
        ("preprocess", preprocessador),
        ("model", modelo)
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    print("🤖 Treinando modelo...")
    pipeline.fit(X_train, y_train)

    pred = pipeline.predict(X_test)
    proba = pipeline.predict_proba(X_test)[:, 1]

    metricas = {
        "accuracy": round(float(accuracy_score(y_test, pred)), 4),
        "precision": round(float(precision_score(y_test, pred)), 4),
        "recall": round(float(recall_score(y_test, pred)), 4),
        "f1": round(float(f1_score(y_test, pred)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, proba)), 4),
        "confusion_matrix": confusion_matrix(y_test, pred).tolist(),
        "target_definition": "RISCO_DEFASAGEM = 1 quando DEFASAGEM < 0 ou IAN <= 5. IAN e DEFASAGEM não são usados como features."
    }

    os.makedirs(PASTA_MODELOS, exist_ok=True)
    os.makedirs(PASTA_REPORTS, exist_ok=True)

    joblib.dump(pipeline, os.path.join(PASTA_MODELOS, "modelo_risco_defasagem.pkl"))

    with open(os.path.join(PASTA_MODELOS, "features.json"), "w", encoding="utf-8") as f:
        json.dump({
            "numeric_features": features_num,
            "categorical_features": features_cat
        }, f, indent=2, ensure_ascii=False)

    with open(os.path.join(PASTA_REPORTS, "metricas_modelo.json"), "w", encoding="utf-8") as f:
        json.dump(metricas, f, indent=2, ensure_ascii=False)

    print("✅ Modelo salvo em models/modelo_risco_defasagem.pkl")
    print("📈 Métricas:")
    print(json.dumps(metricas, indent=2, ensure_ascii=False))
    print("\nRelatório de classificação:")
    print(classification_report(y_test, pred))

    return pipeline, metricas


if __name__ == "__main__":
    treinar_modelo()
