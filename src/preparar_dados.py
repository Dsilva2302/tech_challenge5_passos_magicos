import os
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_ORIGEM = os.path.join(BASE_DIR, "data", "raw", "BASE DE DADOS PEDE 2024 - DATATHON.xlsx")
ARQUIVO_SAIDA = os.path.join(BASE_DIR, "data", "processed", "datathon_base_tratada.csv")


def normalizar_ano(df: pd.DataFrame, ano: int) -> pd.DataFrame:
    def get_col(*nomes):
        for nome in nomes:
            if nome in df.columns:
                return df[nome]
        return pd.Series([np.nan] * len(df))

    out = pd.DataFrame({
        "RA": get_col("RA"),
        "ANO": ano,
        "FASE": get_col("Fase"),
        "TURMA": get_col("Turma"),
        "NOME": get_col("Nome Anonimizado", "Nome"),
        "IDADE": get_col("Idade", f"Idade {str(ano)[-2:]}"),
        "GENERO": get_col("Gênero"),
        "ANO_INGRESSO": get_col("Ano ingresso"),
        "INSTITUICAO_ENSINO": get_col("Instituição de ensino"),
        "PEDRA": get_col(f"Pedra {ano}", f"Pedra {str(ano)[-2:]}"),
        "INDE": get_col(f"INDE {ano}", f"INDE {str(ano)[-2:]}"),
        "IAA": get_col("IAA"),
        "IEG": get_col("IEG"),
        "IPS": get_col("IPS"),
        "IPP": get_col("IPP"),
        "IDA": get_col("IDA"),
        "IPV": get_col("IPV"),
        "IAN": get_col("IAN"),
        "MAT": get_col("Mat", "Matem"),
        "POR": get_col("Por", "Portug"),
        "ING": get_col("Ing", "Inglês"),
        "ATINGIU_PV": get_col("Atingiu PV"),
        "INDICADO": get_col("Indicado"),
        "FASE_IDEAL": get_col("Fase Ideal", "Fase ideal"),
        "DEFASAGEM": get_col("Defasagem", "Defas"),
        "REC_PSICOLOGIA": get_col("Rec Psicologia"),
        "DESTAQUE_IEG": get_col("Destaque IEG"),
        "DESTAQUE_IDA": get_col("Destaque IDA"),
        "DESTAQUE_IPV": get_col("Destaque IPV"),
        "ESCOLA": get_col("Escola"),
        "STATUS": get_col("Ativo/ Inativo"),
    })

    return out


def preparar_dados() -> pd.DataFrame:
    abas = {
        "PEDE2022": 2022,
        "PEDE2023": 2023,
        "PEDE2024": 2024,
    }

    bases = []
    for aba, ano in abas.items():
        print(f"📖 Lendo aba {aba}...")
        df = pd.read_excel(ARQUIVO_ORIGEM, sheet_name=aba)
        bases.append(normalizar_ano(df, ano))

    base = pd.concat(bases, ignore_index=True)

    numericas = [
        "INDE", "IAA", "IEG", "IPS", "IPP", "IDA", "IPV", "IAN",
        "DEFASAGEM", "IDADE", "ANO_INGRESSO", "MAT", "POR", "ING"
    ]

    for col in numericas:
        base[col] = pd.to_numeric(base[col], errors="coerce")

    base["PEDRA"] = base["PEDRA"].replace({"Ágata": "Agata"})

    # Alvo do modelo:
    # risco quando há defasagem negativa ou IAN baixo.
    base["RISCO_DEFASAGEM"] = ((base["DEFASAGEM"] < 0) | (base["IAN"] <= 5)).astype(int)
    base["RISCO_LABEL"] = np.where(base["RISCO_DEFASAGEM"].eq(1), "Risco", "Sem risco")

    os.makedirs(os.path.dirname(ARQUIVO_SAIDA), exist_ok=True)
    base.to_csv(ARQUIVO_SAIDA, index=False, sep=";", encoding="utf-8-sig", decimal=",")

    print(f"✅ Base tratada salva em: {ARQUIVO_SAIDA}")
    print(f"📊 Linhas: {len(base):,} | Colunas: {len(base.columns):,}")
    return base


if __name__ == "__main__":
    preparar_dados()
