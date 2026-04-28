
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

st.set_page_config(
    page_title="Passos Mágicos - Risco de Defasagem",
    layout="wide"
)

st.title("Passos Mágicos - Modelo Preditivo de Risco de Defasagem")
st.write("Aplicação para estimar a probabilidade de um aluno entrar em risco de defasagem.")

BASE_DIR = Path(__file__).resolve().parent
MODELO_PATH = BASE_DIR / "models" / "modelo_risco_defasagem.joblib"

if not MODELO_PATH.exists():
    st.error("Modelo não encontrado. Rode o script de treinamento antes.")
    st.stop()

pacote = joblib.load(MODELO_PATH)
modelo = pacote["modelo"]
features = pacote["features"]

st.sidebar.header("Entrada dos Indicadores")

dados = {}

for feature in features:
    dados[feature] = st.sidebar.number_input(
        feature,
        min_value=0.0,
        max_value=10.0,
        value=6.0,
        step=0.1
    )

entrada = pd.DataFrame([dados])

st.subheader("Dados informados")
st.dataframe(entrada)

prob = modelo.predict_proba(entrada)[0, 1]
pred = modelo.predict(entrada)[0]

st.subheader("Resultado")

st.metric("Probabilidade de risco de defasagem", f"{prob * 100:.2f}%")

if pred == 1:
    st.error("Aluno classificado com risco de defasagem.")
else:
    st.success("Aluno não classificado em risco de defasagem.")

st.info("O resultado deve ser usado como apoio à decisão pedagógica, não como decisão automática.")
