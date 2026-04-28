
# Storytelling — Datathon Passos Mágicos

## 1. Contexto

A Associação Passos Mágicos atua para transformar a vida de crianças e jovens em vulnerabilidade social por meio da educação, apoio psicossocial, apoio psicopedagógico e desenvolvimento do protagonismo.

## 2. Base analisada

Foram analisados dados de 2022, 2023 e 2024.

Resumo anual:

|   ANO |   alunos |   INDE_medio |   IDA_medio |   IEG_medio |   IAA_medio |   IPS_medio |   IPP_medio |   IPV_medio |   IAN_medio |   DEFASAGEM_media |   risco_defasagem_pct |
|------:|---------:|-------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------------:|----------------------:|
|  2022 |      860 |        7.036 |       6.093 |       7.891 |       8.274 |       6.905 |     nan     |       7.254 |       6.424 |           nan     |                 0.699 |
|  2023 |     1014 |        7.356 |       6.663 |       8.699 |       6.903 |       5.12  |       7.563 |       8.028 |       7.244 |            -0.655 |                 0.544 |
|  2024 |     1156 |        7.393 |       6.351 |       7.375 |       8.544 |       6.83  |       7.548 |       7.354 |       7.684 |            -0.409 |                 0.462 |

## 3. Principais achados

### Defasagem e IAN

A análise do IAN e da defasagem permite segmentar alunos por adequação de nível.
Alunos com defasagem negativa ou IAN baixo foram classificados como risco de defasagem.

### Desempenho acadêmico

O IDA foi usado como indicador central de desempenho acadêmico, complementado pelas notas de matemática, português e inglês.

### Engajamento

O IEG foi analisado com IDA e IPV.
Alunos com bom engajamento e baixo desempenho representam grupo com alta possibilidade de recuperação mediante intervenção acadêmica direcionada.

### Autoavaliação

A diferença entre IAA e IDA mostra desalinhamentos entre percepção do aluno e desempenho real.
Quando a autoavaliação é alta e o desempenho é baixo, pode haver necessidade de devolutivas pedagógicas mais claras.

### Aspectos psicossociais e psicopedagógicos

IPS e IPP ajudam a identificar fatores não exclusivamente acadêmicos.
Esses indicadores podem anteceder quedas de desempenho ou engajamento.

## 4. Modelo preditivo

Foi construído um modelo de classificação para prever risco de defasagem.

Alvo:
- risco = 1 quando DEFASAGEM < 0 ou IAN <= 5;
- risco = 0 nos demais casos.

Para evitar vazamento de dados, IAN, DEFASAGEM, INDE e PEDRA não foram usados como variáveis explicativas.

Métricas finais:

{
    "modelo": "Gradient Boosting",
    "accuracy": 0.8562005277044855,
    "precision": 0.7980952380952381,
    "recall": 0.9928909952606635,
    "f1": 0.8848996832101372,
    "roc_auc": 0.9212085308056871,
    "features": [
        "IDADE",
        "ANO_INGRESSO",
        "IAA",
        "IEG",
        "IPS",
        "IPP",
        "IDA",
        "INGLES",
        "IPV",
        "DIF_AUTOAVALIACAO_DESEMPENHO",
        "DIF_ENGAJAMENTO_DESEMPENHO",
        "MEDIA_INDICADORES_SEM_IAN",
        "QTD_INDICADORES_ABAIXO_5",
        "QTD_INDICADORES_ABAIXO_7",
        "ANO",
        "FASE",
        "TURMA",
        "GENERO",
        "INSTITUICAO_ENSINO"
    ]
}

## 5. Recomendações

1. Priorizar alunos com maior probabilidade de risco.
2. Criar plano de intervenção por perfil: acadêmico, engajamento, psicossocial e psicopedagógico.
3. Acompanhar evolução anual dos indicadores.
4. Usar o app Streamlit como ferramenta de triagem.
5. Validar os alertas do modelo com a equipe pedagógica.

## 6. Conclusão

A análise mostra que os indicadores podem ser usados para antecipar riscos, orientar intervenções e apoiar decisões da Passos Mágicos com base em dados.
