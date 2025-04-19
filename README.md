# análise do mercado de criptomoedas com dbt

projeto para análise de dados do mercado de criptomoedas, unindo dados numéricos de exchanges e notícias do setor. os dados são carregados em um banco postgresql, transformados com dbt e apresentados em um dashboard interativo com streamlit.

## arquitetura

- extração:
    /- dados numéricos das exchanges (extract_ccxt.py)
    /- notícias do mercado cripto (extract_criptopanic.py)

- carga: scripts em python para tabelas bronze_cripto_dados e bronze_cripto_news
- transformação: dbt (camadas bronze → silver → gold)
- armazenamento: postgresql no supabase
- análise: dashboard com streamlit + busca inteligente com openai
- orquestração: um único script executa todo o fluxo (orquestrador.py)

## modelos dbt

### bronze
- dados crus das exchanges e notícias  

### silver
- limpeza e padronização  
- cálculos e enriquecimento  

### gold
- métricas e sinais de mercado:
  - **sugestão de ação**: comprar, vender ou esperar  
  - análises combinadas com notícias  

## execução

```bash
# roda tudo: extração, carga, dbt e dashboard
python orquestrador.py
```

## tecnologias

- python

- criptopanic news/ccxt lib

- postgresql supabase

- dbt

- streamlit

- openai api