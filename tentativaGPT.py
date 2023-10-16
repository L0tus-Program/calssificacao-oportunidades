import pandas as pd
from datetime import datetime, timedelta
import sqlite3
import os
import json
import db

class Assessor:
    def __init__(self, codigo_assessor):
        self.codigo_assessor = codigo_assessor
        self.carteira_clientes = []

    def carteira_cliente(self, codigo_xp):
        self.carteira_clientes.append(codigo_xp)

    def export_carteira(self):
        df = pd.DataFrame()
        df[f'Carteira assessor {self.codigo_assessor}'] = self.carteira_clientes
        df.to_excel(f'clientes{self.codigo_assessor}.xlsx', index=False)
        print("DataFrame exportado para 'clientes_relacionados.xlsx'.")

    def rankear_oportunidades(self):
        print(f"Entrou rank oportunidades {self.codigo_assessor}")
        hoje = datetime.now().date()
        conn = sqlite3.connect('clientes.db')
        db_file = 'clientes.db'
        table_name = 'Produtos'
        conn = sqlite3.connect(db_file)
        query = f'SELECT * FROM {table_name}'
        df_produtos = pd.read_sql_query(query, conn)
        conn.close()

        oportunidades_vencimento = df_produtos[
            (df_produtos['codigo_cliente_xp'].isin(self.carteira_clientes)) &
            (df_produtos['data_de_vencimento'] == hoje) &
            (df_produtos['net'] > 0)
        ].sort_values(by='net', ascending=False)

        oportunidades_saldo = df_produtos[
            (df_produtos['codigo_cliente_xp'].isin(self.carteira_clientes)) &
            (df_produtos['sub_produto'] == 'Saldo em Conta') &
            (df_produtos['net'] > 0)
        ].sort_values(by='net', ascending=False)

        todas_oportunidades = pd.concat([oportunidades_vencimento, oportunidades_saldo])

        if self.codigo_assessor == 24851:
            num_oportunidades = 15
        elif self.codigo_assessor == "GERAL":
            num_oportunidades = 125
        else:
            num_oportunidades = 25

        melhores_oportunidades = todas_oportunidades.head(num_oportunidades)

        df_saida = pd.DataFrame({
            'Codigo Assessor': [self.codigo_assessor] * len(melhores_oportunidades),
            'Codigo Cliente': melhores_oportunidades['codigo_cliente_xp'].tolist()
        })

        nome_arquivo = f'oportunidades_assessor_{self.codigo_assessor}.xlsx'
        df_saida.to_excel(nome_arquivo, index=False)
        print(f"Oportunidades exportadas para {nome_arquivo}")
        print("Encaminhando webhook")

        return df_saida

def create_assessors_from_db():
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT codigo_assessor FROM Assessores')
    codigo_assessores = [row[0] for row in cursor.fetchall()]
    conn.close()
    return [Assessor(assessor) for assessor in codigo_assessores]

def carteiras(assessors):
    conn = sqlite3.connect('clientes.db')
    db_file = 'clientes.db'
    table_name = 'Clientes'
    conn = sqlite3.connect(db_file)
    query = f'SELECT * FROM {table_name}'
    df_conexao = pd.read_sql_query(query, conn)
    conn.close()
    print(df_conexao.head())
    for index, row in df_conexao.iterrows():
        codigo_xp = row['codigo_cliente_xp']
        codigo_assessor = row['assessor_cod_assessor']

        for assessor in assessors:
            if codigo_assessor == assessor.codigo_assessor:
                assessor.carteira_cliente(codigo_xp)
                break


def consolidar_oportunidades(assessors):
    conn = sqlite3.connect('clientes.db')
    db_file = 'clientes.db'
    table_name = 'Produtos'
    conn = sqlite3.connect(db_file)
    query = f'SELECT * FROM {table_name}'
    df_produtos = pd.read_sql_query(query, conn)
    conn.close()
    dfs_oportunidades = []
    for assessor in assessors:
        dfs_oportunidades.append(assessor.rankear_oportunidades())

    df_consolidado = pd.concat(dfs_oportunidades, axis=0)
    df_consolidado.to_excel('oportunidades_consolidadas.xlsx', index=False)
    print("Oportunidades consolidadas exportadas para 'oportunidades_consolidadas.xlsx'")


def main():
    db.verifica()
    assessors = create_assessors_from_db()
    carteiras(assessors)
    consolidar_oportunidades(assessors)


main()
