import ccxt
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

BD_POSTGRES=os.environ.get("DIRECT_URL")
engine = create_engine(BD_POSTGRES)

# lista das criptos para serem analisadas
criptos = [ 
    'BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'XRP/USDT', 'DOGE/USDT', 'SOL/USDT', 
    'ADA/USDT', 'DOT/USDT', 'LTC/USDT', 'SHIB/USDT', 'AVAX/USDT', 'TRX/USDT', 
    'UNI/USDT', 'XLM/USDT', 'ATOM/USDT', 'ETC/USDT', 'ICP/USDT', 'FIL/USDT', 
    'HBAR/USDT', 'VET/USDT', 'EGLD/USDT', 'MKR/USDT', 'ALGO/USDT', 'QNT/USDT', 
    'AXS/USDT', 'SAND/USDT', 'XTZ/USDT', 'AAVE/USDT' 
]

# extração dos dados das criptomoedas
def extrair_dados(criptos=criptos):
    exchange = ccxt.binance()

    dados = []

    for cripto in criptos:
        ticker = exchange.fetch_ticker(cripto)
        order_book = exchange.fetch_order_book(cripto)

        dados.append({
        'cripto': cripto,
        'price': ticker['last'],
        'high': ticker['high'],
        'low': ticker['low'],
        'bid': ticker['bid'],  
        'ask': ticker['ask'],
        'volume': ticker['baseVolume'],
        'quote_volume': ticker['quoteVolume'],
        'order_book_bid': order_book['bids'][0][0] if order_book['bids'] else None,
        'order_book_ask': order_book['asks'][0][0] if order_book['asks'] else None,
        })

    return dados

# load dos dados extraidos para o postgres
def carregar_dados(dados, schema='dw'):
    df = pd.DataFrame(dados)
    df.to_sql("bronze-criptosinfo", engine, schema='dw', if_exists="replace", index=False)

if __name__ == "__main__":
    criptodados = extrair_dados()
    carregar_dados(criptodados)
