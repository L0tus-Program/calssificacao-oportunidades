# Como fazer o DF virar uma tabela ?

# Talvez seja melhor separar as funções de atualizar BD em outro arquivo. 
# Apenas gerar os assessores e voltar a utilizar as principais funções dentro deles

import pandas as pd
from datetime import datetime, timedelta
import enviar_zoho as zoho
import sqlite3
import os # Verificar se o BD existe na pasta de arquivos
import json

# Classe Assessor
class assessor:
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


# Criar banco de dados
# Conectar ou criar o banco de dados SQLite
def bd(df_conexao, df_produtos):
    df_conexao = df_conexao
    df_produtos = df_produtos
    print("Criando banco de dados")
    # Conexão com o sqlite
    conn = sqlite3.connect('clientes.db')
    #transforma o dataframe em tabela SQL
    df_conexao.to_sql('Clientes', conn, if_exists='replace')
    df_produtos.to_sql('Produtos', conn, if_exists='replace')
    conn.close()


# Atualizar banco de dados

def atualizar_banco_de_dados():
    df_conexao = pd.read_excel('clientes_conexao.xlsx')
    df_produtos = pd.read_excel('clientes_conexao_produtos.xlsx')
    print ("Atualizando banco de dados")
    conn = sqlite3.connect('clientes.db')
    df_conexao.to_sql('Clientes', conn, if_exists='replace', index=False)
    df_produtos.to_sql('Produtos', conn, if_exists='replace', index=False)
    conn.close()



# verificar se existem carteiras dos assessores. Caso não então criar e distribuir
def atualizar_carteiras(assessores):
    # Distribuição nas carteiras
    assessores = assessores
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

def criar_assessores(): # versão antiga, preciso alterar para criação pelo BD
    print("Gerando assessores")
    assessor1 = assessor(73770)
    assessor2 = assessor(30927)
    assessor3 = assessor (24851)
    assessor4 = assessor (41849)
    assessor5 = assessor(29087)
    assessorGeral = assessor("GERAL") #aqueles que não tem carteira fixa
    
    assessores = [assessor1,assessor2,assessor3,assessor4,assessor5,assessorGeral]
    atualizar_carteiras(assessores)
    #return assessor1.codigo_assessor,assessor2.codigo_assessor
    return assessor1,assessor2,assessor3,assessor4,assessor5,assessorGeral
    

def assessores(): # apenas registra no BD
    # Nome do arquivo do banco de dados SQLite
    db_file = 'clientes.db'
    
    # Conectar ao banco de dados
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Verificar se a tabela "assessores" já existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='assessores'")
    tabela_existe = cursor.fetchone()
    # lista de assessores a incluir ou criar na tabela. Futuramente deve ter outra fonte de dados ou inserção manual
    lista_assessores = [
            {"id": "73770"},
            {"id": "30927"},
            {"id": "24851"},
            {"id": "41849"},
            {"id": "29087"},
            {"id": "GERAL"},
            {"id": "teste"}
           
        ]
    if tabela_existe is None:
        # Se a tabela não existir, crie-a
        cursor.execute('''
            CREATE TABLE assessores (
                id TEXT PRIMARY KEY,
                carteira TEXT
            )
        ''')

        # Exemplo de lista de assessores a serem cadastrados
         ### Ta tendo que excluir o banco de dados pra ele registrar novos assessores

        for assessor in lista_assessores:
            id_assessor = assessor.get("id")
            carteira = []

            # Converter a carteira em JSON
            carteira_json = json.dumps(carteira)

            # Inserir o assessor na tabela
            cursor.execute("INSERT INTO assessores (id, carteira) VALUES (?, ?)",
                           (id_assessor, carteira_json))
    else:
        # A tabela já existe, não é necessário criá-la novamente

       

        for assessor in lista_assessores:
            id_assessor = assessor.get("id")
            carteira = []

            # Converter a carteira em JSON
            carteira_json = json.dumps(carteira)

            # Inserir o assessor na tabela ou atualizá-lo se o ID já existir
            cursor.execute("INSERT OR REPLACE INTO assessores (id, carteira) VALUES (?, ?)",
                           (id_assessor, carteira_json))

    conn.commit()
    conn.close()

def consultar_assessores():
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()

    # Consulta SQL para buscar os IDs dos assessores na tabela 'assessores'
    cursor.execute('SELECT id FROM assessores')
    ids = [row[0] for row in cursor.fetchall()]

    conn.close()

    return ids

# Menu principal
def main():
    # Menu 
    print(criar_assessores())
    while True:
        
        menu = input ("1 - Atualizar banco de dados\n2 - Atualizar carteiras\n3 - Gerar lista de oportunidades\n4 - Salvar assessores\n5 - Listar assessores\n0 - SAIR\n")
        match menu:
            case "1":
                atualizar_banco_de_dados()
            case "2":
                atualizar_carteiras(criar_assessores) # Adaptar para pegar dados do banco de dados
            case "3":
                # Criar a tupla de assessores
                assessores = criar_assessores()

                # Chamar o método rankear_oportunidades em todos os objetos da tupla
                for assessor in assessores:
                    assessor.rankear_oportunidades()
            case "4":
                assessores()
            case "5":
                print(consultar_assessores())
            case "9":
                criar_assessores()
            case "0":
                os.system("cls")
                break
            case __:
                break
            
# Nome do arquivo do banco de dados SQLite
db_file = "clientes.db"

# Verifica se o arquivo do banco de dados existe
if os.path.isfile(db_file):
    print(f"O banco de dados {db_file} existe.")
else:
    print(f"O banco de dados {db_file} não existe.")
    try:
        print("Carregando dataframes")
        df_conexao = pd.read_excel('clientes_conexao.xlsx')
        df_produtos = pd.read_excel('clientes_conexao_produtos.xlsx')
        bd(df_conexao,df_produtos)
        assessores()
    except:
        print("Sem planilhas para carregar")

    






main() # Invocada ao inicio do codigo