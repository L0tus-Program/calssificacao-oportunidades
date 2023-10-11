import sqlite3
import pandas as pd
from datetime import datetime

# Classe assessor
class assessor:
    def __init__(self, codigo_assessor):
        self.codigo_assessor = codigo_assessor
        self.carteira_clientes = []

    def carteira_cliente(self, codigo_xp):
        self.carteira_clientes.append(codigo_xp)

    def rankear_oportunidades(self):
        conn = sqlite3.connect('clientes.db')
        query = f'''
        SELECT * FROM Clientes
        JOIN Produtos ON Clientes.codigo_cliente_xp = Produtos.codigo_cliente_xp
        WHERE Clientes.codigo_cliente_xp IN ({','.join(map(str, self.carteira_clientes))})
        '''
        df_produtos = pd.read_sql_query(query, conn)
        hoje = datetime.now().date()
















def consolidar_oportunidades(*assessores):
    conn = sqlite3.connect('clientes.db')
    dfs_oportunidades = []

    for assessor in assessores:
        tabela_nome = f'oportunidades_assessor_{assessor.codigo_assessor}'
        df = pd.read_sql(f'SELECT * FROM {tabela_nome}', conn)
        dfs_oportunidades.append(df)

    df_consolidado = pd.concat(dfs_oportunidades, axis=0)
    df_consolidado.reset_index(drop=True, inplace=True)
    df_consolidado.to_sql('oportunidades_consolidadas', conn, if_exists='replace', index=False)
    print("Oportunidades consolidadas salvas no banco de dados.")
    conn.close()


consolidar_oportunidades(assessor1, assessor2, assessor3, assessor4, assessor5, assessorGeral)
