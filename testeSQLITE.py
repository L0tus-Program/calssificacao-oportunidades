import pandas as pd
from datetime import datetime, timedelta
import enviar_zoho as zoho
import sqlite3
#import json
#import csv

# Conectar ou criar o banco de dados SQLite
conn = sqlite3.connect('clientes.db')

# Criar as tabelas no banco de dados SQLite
conn.execute('''
CREATE TABLE IF NOT EXISTS Clientes (
    codigo_cliente_xp INTEGER,
    assessor INTEGER,
    PRIMARY KEY(codigo_cliente_xp)
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS Produtos (
    codigo_xp INTEGER,
    net REAL,
    saldo_em_conta REAL,
    data_de_vencimento DATE,
    FOREIGN KEY(codigo_xp) REFERENCES Clientes(codigo_cliente_xp)
)
''')

conn.commit()
conn.close()

def atualizar_banco_de_dados(arquivo_conexao, arquivo_produtos):
    df_conexao = pd.read_excel(arquivo_conexao)
    df_produtos = pd.read_excel(arquivo_produtos)
    conn = sqlite3.connect('clientes.db')
    df_conexao.to_sql('Clientes', conn, if_exists='replace', index=False)
    df_produtos.to_sql('Produtos', conn, if_exists='replace', index=False)
    conn.close()




class assessor:
    def __init__(self, codigo_assessor):
        self.codigo_assessor = codigo_assessor
        self.carteira_clientes = []

    def carteira_cliente(self, codigo_xp):
        self.carteira_clientes.append(codigo_xp)


    def export_carteira(self):
        df = pd.DataFrame()
        df[f'Carteira assessor {self.codigo_assessor}'] = self.carteira_clientes
        df.to_excel(f'clientes{self.codigo_assessor}.xlsx', index=False)
        print(f"DataFrame exportado para 'clientes{self.codigo_assessor}.xlsx'.")

    def rankear_oportunidades(self):
        conn = sqlite3.connect('clientes.db')
        query = f'''
        SELECT * FROM Clientes
        JOIN Produtos ON Clientes.codigo_cliente_xp = Produtos.codigo_cliente_xp
        WHERE Clientes.codigo_cliente_xp IN ({','.join(map(str, self.carteira_clientes))})
        '''
        df_produtos = pd.read_sql_query(query, conn)
        hoje = datetime.now().date()

        # Assume-se que o código para filtrar e ordenar oportunidades permanece o mesmo
        # Por exemplo:
        oportunidades_vencimento = df_produtos[
            (df_produtos['data_de_vencimento'] == hoje) &
            (df_produtos['net'] > 0)
        ].sort_values(by='net', ascending=False)

        oportunidades_saldo = df_produtos[
            (df_produtos['sub_produto'] == 'Saldo em Conta') 
            #(df_produtos['net'] > 0)
        ]#.sort_values(by='net', ascending=False)

        oportunidades_saldo = oportunidades_saldo.drop(columns=["codigo_cliente_xp"])
        todas_oportunidades = pd.concat([oportunidades_vencimento, oportunidades_saldo])


        if self.codigo_assessor == 24851:
            num_oportunidades = 15
        elif self.codigo_assessor == "GERAL":
            num_oportunidades = 125
        else:
            num_oportunidades = 25

        melhores_oportunidades = todas_oportunidades.head(num_oportunidades)
       
        print(melhores_oportunidades.head())



       # print(melhores_oportunidades['codigo_cliente_xp'].head())
  
      
        df_saida = pd.DataFrame({
    'Codigo Assessor': [self.codigo_assessor] * len(melhores_oportunidades),
    'Codigo Cliente': [str(codigo) for codigo in melhores_oportunidades['codigo_cliente_xp'].values]
})

        # Salvar df_saida no banco de dados
        df_saida.to_sql(f'oportunidades_assessor_{self.codigo_assessor}', conn, if_exists='replace', index=False)
        print(f"Oportunidades do assessor {self.codigo_assessor} salvas no banco de dados.")
        conn.close()

    def atualizar_banco_de_dados(self, arquivo_conexao, arquivo_produtos):
        atualizar_banco_de_dados(arquivo_conexao, arquivo_produtos)

        

print("Gerando assessores")
assessor1 = assessor(73770)
assessor2 = assessor(30927)
assessor3 = assessor (24851)
assessor4 = assessor (41849)
assessor5 = assessor(29087)
assessorGeral = assessor("GERAL") #aqueles que não tem carteira fixa


# Carregando as planilhas em dataframes
print("Carregando dataframes")
df_conexao = pd.read_excel('clientes_conexao.xlsx')
df_produtos = pd.read_excel('clientes_conexao_produtos.xlsx')


print("Criando banco de dados")
# Conexão com o sqlite
conn = sqlite3.connect('clientes.db')
#transforma o dataframe em tabela SQL
df_conexao.to_sql('Clientes', conn, if_exists='replace')
df_produtos.to_sql('Produtos', conn, if_exists='replace')
# Fecha a conexão 
conn.close()

# Distribuição nas carteiras

linhas = 0
#verifica se existe a coluna de codigos xp na planilha e conta quantas linhas tem
if 'codigo_cliente_xp' in df_conexao.columns:
    # Contagem das linhas na coluna 'codigo_cliente_xp'
    linhas = df_conexao['codigo_cliente_xp'].count()
    print("Número de linhas na coluna 'codigo_cliente_xp':", linhas)
else:
    print("A coluna 'codigo_cliente_xp' não foi encontrada no DataFrame.")

#print(f"Linhas = {linhas}")


# Varrer planilha para formar carteira do assessor
print("Chamando loop")
i = 0

while i <= linhas:
    try:
        #captura código de cliente e assessor
        codigo_xp = df_conexao.at[i,"codigo_cliente_xp"]
        codigo_assessor = df_conexao.at[i,"assessor_cod_assessor"]
        #transforma codigos em inteiros
        codigo_xp_int = int(codigo_xp)
        codigo_assessor_int = int(codigo_assessor)
        #Soma 1 no indice
        i+=1
        

        #Distribui os clientes em seus assessores
        match codigo_assessor_int:
                case 73770:
                    #print("Entrou case 73770")
                    assessor1.carteira_cliente(codigo_xp)
                case 30927:
                    assessor2.carteira_cliente(codigo_xp)
                case 24851:
                    assessor3.carteira_cliente(codigo_xp)
                case 41849:
                    assessor4.carteira_cliente(codigo_xp)
                case 29087:
                    assessor5.carteira_cliente(codigo_xp)
                case 13136 :
                    assessorGeral.carteira_cliente(codigo_xp)
                case 72738 :
                    assessorGeral.carteira_cliente(codigo_xp)
                case 26904 :
                    assessorGeral.carteira_cliente(codigo_xp)
                case _:
                    #print("Não encontrou case")
                    pass

    except:
        print("Fim das linhas")
        break



# Rankeando e exportando oportunidades

print("Exportando ranking dos assessores")
assessor1.rankear_oportunidades()
assessor2.rankear_oportunidades()
assessor3.rankear_oportunidades()
assessor4.rankear_oportunidades()
assessor5.rankear_oportunidades()
assessorGeral.rankear_oportunidades()


#assessor1.to_zoho()
# Opção de exportar a carteira inteira

#assessor1.export_carteira()
#assessor2.export_carteira()
#assessor3.export_carteira()
#assessor4.export_carteira()
#assessor5.export_carteira()
#assessorGeral.export_carteira()

"""
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
"""