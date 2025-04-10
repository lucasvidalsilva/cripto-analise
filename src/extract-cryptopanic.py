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

params = {
    'auth_token': API_KEY,
    'public': 'true',
    'filter': 'hot',
    'kind': 'news'
}

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
    
    df = pd.DataFrame(noticias)
    print(df.head())
    
    df.to_sql("bronze-criptosnews", engine, schema='dw', if_exists="replace", index=False)

else:
    print("Erro:", response.status_code)
    print(response.text)
