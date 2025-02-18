
# README - Análise do Teste A/B - Campanha de Cupons no iFood

## 📌 Visão Geral

Este projeto tem como objetivo analisar o impacto de uma campanha de cupons realizada pelo iFood, utilizando um teste A/B. O estudo avalia a retenção de clientes, ticket médio e viabilidade financeira da campanha. Além disso, inclui uma proposta de segmentação e recomendações para futuras estratégias.

## 📂 Estrutura do Projeto

```
|-- data/                     # Diretório para armazenar os arquivos Parquet originais
|-- parquet_data/             # Dados processados em formato Parquet
|-- scripts/                  # Scripts Python para análise e ETL
    |-- extract.py            # Extrai os dados brutos
    |-- transform.py          # Processa e transforma os dados
    |-- consolidate.py        # Consolida os dados transformados
    |-- analyze_ab_test.py    # Executa as análises estatísticas do experimento
    |-- financial_analysis.py # Avaliação da viabilidade financeira
|-- reports/                  # Resultados e gráficos gerados
    |-- analise_financeira.csv
    |-- taxa_retencao_top_cidades.png
    |-- frequencia_pedidos.png
    |-- taxa_retencao.png
    |-- ticket_medio.png
    |-- Apresentacao_Campanha_iFood.pdf
|-- README.md                 # Documentação do projeto
```

---

## 🚀 Como Executar o Projeto

### **1️⃣ Preparação do Ambiente**

1. Instale o Python (>= 3.8) se ainda não tiver.
2. Instale as dependências do projeto:

```
pip install -r requirements.txt
```

3. Certifique-se de que os arquivos Parquet estão na pasta `<span>parquet_data/</span>`.

---

### **2️⃣ Executar a Pipeline de ETL**

Os scripts de ETL processam os diferentes conjuntos de dados. Execute-os na seguinte ordem:

```
python scripts/extract.py
python scripts/transform.py
python scripts/consolidate.py
```

Esses scripts:

* Extraem os dados brutos.
* Processam e transformam os dados.
* Consolidam os dados prontos para análise na pasta `<span>parquet_data/</span>`.

---

### **3️⃣ Executar Análises Estatísticas**

O script `<span>analyze_ab_test.py</span>` realiza a análise do teste A/B, gerando conclusões e gráficos.
Execute:

```
python scripts/analyze_ab_test.py
```

Saídas geradas:

* **Resultados no terminal** com taxas de retenção, ticket médio e conclusões.
* **Gráficos salvos na pasta ******`<span><strong>reports/</strong></span>`:
  * `<span>taxa_retencao_top_cidades.png</span>`
  * `<span>frequencia_pedidos.png</span>`
  * `<span>taxa_retencao.png</span>`
  * `<span>ticket_medio.png</span>`

---

### **4️⃣ Executar Análise Financeira**

Para avaliar o impacto financeiro da campanha, execute:

```
python scripts/financial_analysis.py
```

Saídas:

* **Resultados no terminal** com ROI estimado.
* **Arquivo CSV gerado em **`<span><strong>reports/analise_financeira.csv</strong></span>` com métricas detalhadas.

---

### **5️⃣ Relatório Final e Apresentação**

A apresentação final foi criada manualmente e está disponível em:

```
reports/Apresentacao_Campanha_iFood.pdf
```

Este documento contém todos os insights e recomendações baseados na análise realizada.

---

## 📌 Conclusão

Este projeto demonstra a eficácia do uso de testes A/B e análises financeiras para validar campanhas promocionais. Com os scripts fornecidos, qualquer pessoa pode reproduzir as análises e adaptar para novas iniciativas.
