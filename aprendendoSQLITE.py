import pandas as pd
from datetime import datetime, timedelta
import enviar_zoho as zoho
import sqlite3
import os # Verificar se o BD existe na pasta de arquivos
import json

# Conexao
conn = sqlite3.connect("tutorial.db") 

# Cursos

cursor = conn.cursor()

try:
    
    cursor.execute(
        """
        CREATE TABLE ranking_oportunidade
        (id text,
        nome text,
        idade text,
        pontuacao int);
    """

    )

except:
    pass



table_name = 'ranking_oportunidade'

# Conectar ao banco de dados


# Consulta SQL para selecionar todos os dados da tabela
query = f'SELECT * FROM {table_name}'

# Use o método read_sql_query do Pandas para criar um DataFrame a partir da consulta
df_ranking = pd.read_sql_query(query, conn)
conn.close()

print(df_ranking.head())


