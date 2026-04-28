# Tech Challenge / Datathon FIAP - Fase 05
## Case Passos Mágicos

Este projeto foi montado para atender ao Datathon da Fase 05 da PósTech FIAP/Data Analytics.

### Objetivo
Construir uma análise gerencial e analítica sobre os indicadores educacionais da Associação Passos Mágicos e desenvolver um modelo preditivo para estimar a probabilidade de um aluno entrar em risco de defasagem.

### Base utilizada
Arquivo principal:
`data/raw/BASE DE DADOS PEDE 2024 - DATATHON.xlsx`

Abas:
- PEDE2022
- PEDE2023
- PEDE2024

### Definição do alvo do modelo
Foi criada a variável `RISCO_DEFASAGEM`:

`RISCO_DEFASAGEM = 1` quando:
- `DEFASAGEM < 0`, ou
- `IAN <= 5`

Observação: para evitar vazamento de informação, o modelo não usa `IAN` nem `DEFASAGEM` como variáveis explicativas.

### Indicadores principais analisados
- INDE: indicador global
- IAN: adequação ao nível
- IDA: desempenho acadêmico
- IEG: engajamento
- IAA: autoavaliação
- IPS: psicossocial
- IPP: psicopedagógico
- IPV: ponto de virada

### Principais resultados encontrados
Resumo anual:

| Ano | Alunos | INDE médio | IDA médio | IEG médio | IAN médio | Risco de defasagem |
|---|---:|---:|---:|---:|---:|---:|
| 2022 | 860 | 7.036 | 6.093 | 7.891 | 6.424 | 69.9% |
| 2023 | 1014 | 7.342 | 6.663 | 8.699 | 7.244 | 54.4% |
| 2024 | 1156 | 7.397 | 6.351 | 7.375 | 7.684 | 46.2% |

### Leitura gerencial
O programa mostra sinais positivos de efetividade: o INDE médio cresce de 2022 para 2024 e o risco estimado de defasagem cai de 69,9% para 46,2%. A adequação ao nível, medida pelo IAN médio, também melhora no período. Porém, há alerta em 2024: o IDA e o IEG caem em relação a 2023, sugerindo a necessidade de reforço em desempenho acadêmico e engajamento.

### Modelo preditivo
Modelo usado:
- Random Forest Classifier

Métricas no conjunto de teste:
- Accuracy: 0.7968
- Precision: 0.7991
- Recall: 0.8483
- F1-score: 0.823
- ROC-AUC: 0.8711

### Estrutura do projeto

```text
tech_challenge_passos_magicos/
├─ app/
│  └─ app_streamlit.py
├─ data/
│  ├─ raw/
│  └─ processed/
├─ models/
│  ├─ modelo_risco_defasagem.pkl
│  └─ features.json
├─ notebooks/
│  └─ 01_datathon_passos_magicos.ipynb
├─ reports/
│  ├─ figures/
│  ├─ correlacoes_indicadores.csv
│  ├─ metricas_modelo.json
│  ├─ resumo_anual.csv
│  └─ roteiro_storytelling.md
├─ src/
│  ├─ preparar_dados.py
│  └─ treinar_modelo.py
├─ requirements.txt
└─ README.md
```

### Como executar

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o treinamento:

```bash
python src/preparar_dados.py
python src/treinar_modelo.py
```

Execute o Streamlit:

```bash
streamlit run app/app_streamlit.py
```

### Entregáveis FIAP
- Notebook Python: `notebooks/01_datathon_passos_magicos.ipynb`
- Código de limpeza e modelagem: pasta `src`
- App Streamlit: `app/app_streamlit.py`
- Modelo treinado: pasta `models`
- Roteiro para apresentação/vídeo: `reports/roteiro_storytelling.md`
