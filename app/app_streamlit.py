
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "modelo_risco_defasagem.pkl"
FEATURES_PATH = BASE_DIR / "models" / "features.json"

st.set_page_config(
    page_title="Passos Mágicos — Risco de Defasagem",
    page_icon="✨",
    layout="wide"
)

st.title("✨ Passos Mágicos — Modelo Preditivo de Risco de Defasagem")
st.write("Aplicação para estimar a probabilidade de risco de defasagem com base nos indicadores educacionais.")

@st.cache_resource
def carregar_modelo():
    modelo = joblib.load(MODEL_PATH)
    with open(FEATURES_PATH, "r", encoding="utf-8") as f:
        meta = json.load(f)
    return modelo, meta

modelo, meta = carregar_modelo()
features = meta["features"]

st.sidebar.header("Entrada dos indicadores")

idade = st.sidebar.number_input("Idade", min_value=5, max_value=30, value=12)
ano_ingresso = st.sidebar.number_input("Ano de ingresso", min_value=1990, max_value=2030, value=2022)

ano = st.sidebar.selectbox("Ano", [2022, 2023, 2024])
fase = st.sidebar.text_input("Fase", "ALFA")
turma = st.sidebar.text_input("Turma", "ALFA A - G0/G1")
genero = st.sidebar.selectbox("Gênero", ["Feminino", "Masculino", "Outro"])
instituicao = st.sidebar.selectbox("Instituição de ensino", ["Pública", "Particular", "Outro"])

iaa = st.sidebar.slider("IAA — Autoavaliação", 0.0, 10.0, 7.0, 0.1)
ieg = st.sidebar.slider("IEG — Engajamento", 0.0, 10.0, 7.0, 0.1)
ips = st.sidebar.slider("IPS — Psicossocial", 0.0, 10.0, 7.0, 0.1)
ipp = st.sidebar.slider("IPP — Psicopedagógico", 0.0, 10.0, 7.0, 0.1)
ida = st.sidebar.slider("IDA — Desempenho acadêmico", 0.0, 10.0, 7.0, 0.1)
matematica = st.sidebar.slider("Matemática", 0.0, 10.0, 7.0, 0.1)
portugues = st.sidebar.slider("Português", 0.0, 10.0, 7.0, 0.1)
ingles = st.sidebar.slider("Inglês", 0.0, 10.0, 7.0, 0.1)
ipv = st.sidebar.slider("IPV — Ponto de Virada", 0.0, 10.0, 7.0, 0.1)

entrada = {
    "IDADE": idade,
    "ANO_INGRESSO": ano_ingresso,
    "IAA": iaa,
    "IEG": ieg,
    "IPS": ips,
    "IPP": ipp,
    "IDA": ida,
    "MATEMATICA": matematica,
    "PORTUGUES": portugues,
    "INGLES": ingles,
    "IPV": ipv,
    "DIF_AUTOAVALIACAO_DESEMPENHO": iaa - ida,
    "DIF_ENGAJAMENTO_DESEMPENHO": ieg - ida,
    "MEDIA_INDICADORES_SEM_IAN": np.mean([iaa, ieg, ips, ipp, ida, ipv]),
    "QTD_INDICADORES_ABAIXO_5": sum(np.array([iaa, ieg, ips, ipp, ida, ipv]) < 5),
    "QTD_INDICADORES_ABAIXO_7": sum(np.array([iaa, ieg, ips, ipp, ida, ipv]) < 7),
    "ANO": ano,
    "FASE": fase,
    "TURMA": turma,
    "GENERO": genero,
    "INSTITUICAO_ENSINO": instituicao,
}

df_entrada = pd.DataFrame([entrada])

for col in features:
    if col not in df_entrada.columns:
        df_entrada[col] = np.nan

df_entrada = df_entrada[features]

prob = modelo.predict_proba(df_entrada)[0, 1]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Probabilidade de risco", f"{prob * 100:.1f}%")

with col2:
    if prob >= 0.60:
        classe = "Alto"
    elif prob >= 0.30:
        classe = "Médio"
    else:
        classe = "Baixo"
    st.metric("Classificação", classe)

with col3:
    st.metric("Modelo", meta.get("modelo", "Modelo treinado"))

if prob >= 0.60:
    st.error("Aluno em risco alto. Recomenda-se intervenção prioritária.")
elif prob >= 0.30:
    st.warning("Aluno em risco médio. Recomenda-se acompanhamento.")
else:
    st.success("Aluno em risco baixo. Manter acompanhamento regular.")

st.subheader("Dados informados")
st.dataframe(df_entrada)

st.subheader("Como interpretar")
st.write(
    "O modelo estima risco com base em indicadores acadêmicos, engajamento, autoavaliação e aspectos psicossociais/psicopedagógicos. A previsão deve ser usada como apoio à decisão, não como decisão automática."
)
