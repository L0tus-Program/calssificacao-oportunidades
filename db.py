import pandas as pd
from datetime import datetime, timedelta
import sqlite3
import os # Verificar se o BD existe na pasta de arquivos


def bd(df_conexao, df_produtos, df_assessores):
    print("Entrando na função bd")
    df_conexao = df_conexao
    df_produtos = df_produtos
    df_assessores = df_assessores
    print("Criando banco de dados")
    # Conexão com o sqlite
    conn = sqlite3.connect('clientes.db')
    #transforma o dataframe em tabela SQL
    df_conexao.to_sql('Clientes', conn, if_exists='replace')
    df_produtos.to_sql('Produtos', conn, if_exists='replace')
    df_assessores.to_sql('Assessores', conn, if_exists='replace')
    conn.commit()
    conn.close()




def verifica():
    # Nome do arquivo do banco de dados SQLite
    db_file = "clientes.db"
    print(f"Verificando se o arquivo {db_file} existe")
    # Verifica se o arquivo do banco de dados existe
    if os.path.isfile(db_file):
        print(f"O banco de dados {db_file} existe.")
    else:
        print(f"O banco de dados {db_file} não existe.")
        try:
            print("Carregando dataframes")
            df_conexao = pd.read_excel('clientes_conexao.xlsx')
            df_produtos = pd.read_excel('clientes_conexao_produtos.xlsx')
            df_assessores = pd.read_excel('assessores.xlsx')
            bd(df_conexao,df_produtos,df_assessores)
           # assessores()
        except:
            print("Sem planilhas para carregar")




def update():
    print("Carregando dataframes")
    df_conexao = pd.read_excel('clientes_conexao.xlsx')
    df_produtos = pd.read_excel('clientes_conexao_produtos.xlsx')
    df_assessores = pd.read_excel('assessores.xlsx')
    bd(df_conexao,df_produtos,df_assessores)
    




