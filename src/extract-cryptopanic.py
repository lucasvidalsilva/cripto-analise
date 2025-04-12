import requests
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

BD_POSTGRES=os.environ.get("DIRECT_URL")
engine = create_engine(BD_POSTGRES)

API_KEY = os.environ.get("API_CRYPTOPANIC")
url = "https://cryptopanic.com/api/v1/posts/"

# parametros para requisição das noticias de criptomoedas
params = {
    'auth_token': API_KEY,
    'public': 'true',
    'filter': 'hot',
    'kind': 'news'
}

# extração das noticias sobre criptomoedas
def extrair_noticias(url=url, params=params):

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        posts = data.get('results', [])
        
        noticias = []

        for post in posts:
            noticias.append({
                'titulo': post['title'],
                'url': post['url'],
                'moedas': ','.join([currency['code'] for currency in post.get('currencies', [])]),
                'publicado_em': post['published_at'],
                'fonte': post['domain']
            })
    else:
        print("Erro:", response.status_code)
        print(response.text)
    
    return noticias

# carregamento das noticias no postgres
def carregar_noticias(noticias):
    df = pd.DataFrame(noticias)
    df.to_sql("bronze-criptosnews", engine, schema='dw', if_exists="replace", index=False)

if __name__ == "__main__":
    dadosnoticias = extrair_noticias()
    carregar_noticias(dadosnoticias)
