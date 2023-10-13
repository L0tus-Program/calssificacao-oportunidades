import pandas as pd
from datetime import datetime, timedelta
#import enviar_zoho as zoho
import sqlite3
import os # Verificar se o BD existe na pasta de arquivos
import json
import db

class Assessor:
    def __init__(self, codigo_assessor):
        self.codigo_assessor = codigo_assessor
        self.carteira_clientes = []
    # Carteira completa de clientes
    def carteira_cliente(self,codigo_xp):   
        self.carteira_clientes.append(codigo_xp)

    # Função para exportar carteira completa
    def export_carteira(self):
        df = pd.DataFrame()
        #df['Assessor'] = self.codigo_assessor
        df[f'Carteira assessor {self.codigo_assessor}'] = self.carteira_clientes
        # Exportar o DataFrame para um arquivo Excel (XLSX)
        df.to_excel(f'clientes{self.codigo_assessor}.xlsx', index=False)

        print("DataFrame exportado para 'clientes_relacionados.xlsx'.")
        #exportar = {f'Assessor {self.codigo_assessor}':{f'Carteira de clientes {self.carteira_cliente}'}}
    

    def rankear_oportunidades(self):
        print(f"Entrou rank oportunidades {self.codigo_assessor}")
        hoje = datetime.now().date()
       # adicionar_dias = timedelta(days = 1)
       # hoje = hoje + adicionar_dias
        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect('clientes.db')

      # Nome do arquivo do banco de dados SQLite
        db_file = 'clientes.db'

        # Nome da tabela que deseja registrar como um DataFrame
        table_name = 'Produtos'

        # Conectar ao banco de dados
        conn = sqlite3.connect(db_file)

        # Consulta SQL para selecionar todos os dados da tabela
        query = f'SELECT * FROM {table_name}'

        # Use o método read_sql_query do Pandas para criar um DataFrame a partir da consulta
        df_produtos = pd.read_sql_query(query, conn)
        conn.close()
        #print(df_produtos.head())


        # Filtra as oportunidades de acordo com as condições especificadas
        oportunidades_vencimento = df_produtos[
            (df_produtos['codigo_cliente_xp'].isin(self.carteira_clientes)) &
            (df_produtos['data_de_vencimento'] == hoje) &
            (df_produtos['net'] > 0)   # Filtra valores de net maiores que 0
            # net_em_m
            # data ultimo atendimento (relatorio DataAtendimento detalhado) acima de 15 dias passados para INVESTOR (hunter?)
            # 
        ].sort_values(by='net', ascending=False)  # Ordena pelo valor de net

        oportunidades_saldo = df_produtos[
            (df_produtos['codigo_cliente_xp'].isin(self.carteira_clientes)) &
            (df_produtos['sub_produto'] == 'Saldo em Conta') &
            (df_produtos['net'] > 0)  # Filtra valores de net maiores que 0
            # net_em_m > 50 mil
            # data ultimo atendimento >15 dias para investor
        ].sort_values(by='net', ascending=False)  # Ordena pelo valor de net

        # Junta as duas listas, colocando vencimento na frente
        todas_oportunidades = pd.concat([oportunidades_vencimento, oportunidades_saldo])

        # Define o número de oportunidades com base no código do assessor
        if self.codigo_assessor == 24851:
            num_oportunidades = 15
        elif self.codigo_assessor == "GERAL":
            num_oportunidades = 125
        else:
            num_oportunidades = 25

        melhores_oportunidades = todas_oportunidades.head(num_oportunidades)

        # Prepara o DataFrame de saída
        df_saida = pd.DataFrame({
            'Codigo Assessor': [self.codigo_assessor] * len(melhores_oportunidades),
            'Codigo Cliente': melhores_oportunidades['codigo_cliente_xp'].tolist()
        })

        # Exportando para .xlsx
        nome_arquivo = f'oportunidades_assessor_{self.codigo_assessor}.xlsx'
        df_saida.to_excel(nome_arquivo, index=False)
        print(f"Oportunidades exportadas para {nome_arquivo}")
        print("Encaminahndo webhook")
        """if codigo_assessor != "GERAL": # Geral precisamos implementar outro processo randomico
            zoho.webhook(self.codigo_assessor,melhores_oportunidades['codigo_cliente_xp'].tolist())"""
        #return melhores_oportunidades['codigo_cliente_xp'].tolist()
        #return melhores_oportunidades['codigo_cliente_xp'].tolist()
        
    
        """ def to_zoho(self):
                print("Entrando to_zoho")
                zoho.webhook(self.codigo_assessor,self.rankear_oportunidades())
        """
        return df_saida  # Retorne df_saida em vez da lista

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('clientes.db')
cursor = conn.cursor()

# Consulta SQL para selecionar a coluna 'nome' da tabela 'clientes'
cursor.execute('SELECT codigo_assessor FROM Assessores')

# Coletar os resultados em uma lista
codigo_assessores = [row[0] for row in cursor.fetchall()]
# Fechar a conexão com o banco de dados
conn.close()

# Cria objetos da classe com base na lista de itens
objetos = [Assessor(assessor) for assessor in codigo_assessores]

for assessor in objetos:
    print(f"Objeto Assessor criado: Código Assessor {assessor.codigo_assessor}")
"""
# Ainda preciso fazer isso ser dinamico com o banco de dados
print("Gerando assessores")
assessor1 = Assessor(73770)
assessor2 = Assessor(30927)
assessor3 = Assessor (24851)
assessor4 = Assessor (41849)
assessor5 = Assessor(29087)
assessorGeral = Assessor("GERAL") #aqueles que não tem carteira fixa"""




def carteiras(*assessores):
    
    # Distribuição nas carteiras
    assessores = assessores
    assessores_codigos = []
    for assessor in assessores:
        #print(assessor.codigo_assessor)
        assessores_codigos.append(assessor.codigo_assessor)
    print(assessores_codigos)
    #print(assessores)
    linhas = 0
    #verifica se existe a coluna de codigos xp na planilha e conta quantas linhas tem
    conn = sqlite3.connect('clientes.db')

    # Nome do arquivo do banco de dados SQLite
    db_file = 'clientes.db'

    # Nome da tabela que deseja registrar como um DataFrame
    table_name = 'Clientes'

    # Conectar ao banco de dados
    conn = sqlite3.connect(db_file)

    # Consulta SQL para selecionar todos os dados da tabela
    query = f'SELECT * FROM {table_name}'

    # Use o método read_sql_query do Pandas para criar um DataFrame a partir da consulta
    df_conexao = pd.read_sql_query(query, conn)
    conn.close()
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




# todos os assessores como parametro p/ função
def consolidar_oportunidades(*assessores):
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('clientes.db')

    # Nome do arquivo do banco de dados SQLite
    db_file = 'clientes.db'

    # Nome da tabela que deseja registrar como um DataFrame
    table_name = 'Produtos'

    # Conectar ao banco de dados
    conn = sqlite3.connect(db_file)

    # Consulta SQL para selecionar todos os dados da tabela
    query = f'SELECT * FROM {table_name}'

    # Use o método read_sql_query do Pandas para criar um DataFrame a partir da consulta
    df_produtos = pd.read_sql_query(query, conn)
    conn.close()
    dfs_oportunidades = []
    for assessor in assessores:
        dfs_oportunidades.append(assessor.rankear_oportunidades())

   
    df_consolidado = pd.concat(dfs_oportunidades, axis=0)

    # Exportando para um único arquivo Excel
    df_consolidado.to_excel('oportunidades_consolidadas.xlsx', index=False)
    print("Oportunidades consolidadas exportadas para 'oportunidades_consolidadas.xlsx'.")




def main():
    while True:
        print("Entrando main menu")
        menu = input("1 - Atualizar banco de dados\n3 - Gerar lista de oportunidades\n5 - Listar assessores\n0 - SAIR\n")
        match menu:
            case "1":
                db.verifica()
                carteiras()
            
            case "3":
                carteiras(*objetos)
                for assessor in objetos:
                    assessor.rankear_oportunidades()
                consolidar_oportunidades(*objetos)
                
            case "5":
                # Listar os códigos de assessor
                for assessor in codigo_assessores:
                    print(f"Código Assessor: {assessor}")
            
            case "0":
                os.system("cls")
                break
            
            case __:
                break

db.verifica()

main()