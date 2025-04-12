import subprocess
import os
from datetime import datetime

PATH_SCRIPT_EXTRACT_LOAD='./src/extract-ccxt.py'
PATH_DBT='./dw'

def extract_load():
    print(f"[{datetime.now()}] Iniciando extração...")
    subprocess.run(['python', PATH_SCRIPT_EXTRACT_LOAD], check=True)
    print(f"[{datetime.now()}] Extração feita.")

def executar_dbt():
    print(f"[{datetime.now()}] Iniciando dbt run...")
    subprocess.run(['dbt', 'run'], cwd=PATH_DBT, check=True)
    print(f"[{datetime.now()}] projeto dbt executado.")

if __name__ == "__main__":
    extract_load()
    executar_dbt()