import pandas as pd
from datetime import datetime, timedelta
import enviar_zoho as zoho
import sqlite3
import requests
import os # Verificar se o BD existe na pasta de arquivos
import db
import ast
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import json
#import email.message


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
    
    def carregar_carteira(self):
        conn = sqlite3.connect('clientes.db')
        
        
        consulta = f"SELECT carteira FROM Assessores WHERE codigo_assessor = '{self.codigo_assessor}'"

        # Executar a consulta e recuperar a carteira
        cursor = conn.cursor()
        cursor.execute(consulta)
        resultado = cursor.fetchone()
        self.carteira_clientes = resultado[0]
        self.carteira_clientes = ast.literal_eval(self.carteira_clientes)
        conn.close()
        
       
    def rankear_oportunidades(self):
        print(f"Entrou rank oportunidades {self.codigo_assessor}")
        
       # adicionar_dias = timedelta(days = 1)
       # hoje = hoje + adicionar_dias
        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect('clientes.db')

        self.carregar_carteira()
      # Nome do arquivo do banco de dados SQLite
        db_file = 'clientes.db'

        # Nome da tabela que deseja registrar como um DataFrame
        table_name = "Produtos"

        # Conectar ao banco de dados
        conn = sqlite3.connect(db_file)

        # Consulta SQL para selecionar todos os dados da tabela
        query = f'SELECT * FROM {table_name}'
        df_produtos = pd.read_sql_query(query,conn)
        df_clientes = pd.read_sql_query('SELECT * FROM Clientes',conn)
        # Use o método read_sql_query do Pandas para criar um DataFrame a partir da consulta
        produtos = pd.read_sql_query(query, conn)

        atendimentos = pd.read_sql_query('SELECT * FROM Atendimentos',conn)
        atendimentos = atendimentos.sort_values(by='data_atendimento', ascending=False)
        atendimentos = atendimentos.drop_duplicates(subset='codigo_cliente_xp', keep='first')
        atendimentos = atendimentos.reset_index(drop=True)
       
        conn.close()
        
        hoje = datetime.now().date()
        print(hoje)
        # Agora você pode aplicar as condições necessárias na junção para filtrar as oportunidades
        oportunidades_vencimento = df_produtos[
            (df_produtos['codigo_cliente_xp'].isin(self.carteira_clientes)) &
            (df_produtos['data_de_vencimento'] == hoje) &
            (df_produtos['net'] > 0)   # Filtra valores de net maiores que 0
            #(df_joined['net_em_m'] > 50000)   # Filtra net_em_m maior que 50000
            #(df_joined['data_ultimo_atendimento'] > (hoje - timedelta(days=15)))  # Filtra data de último atendimento acima de 15 dias
        ].sort_values(by='net', ascending=False)  # Ordena pelo valor de net
        
        #print(f"Testando dataframe : \n {df_produtos['codigo_cliente_xp']}")
        oportunidades_saldo = df_produtos[
            (df_produtos['codigo_cliente_xp'].isin(self.carteira_clientes)) &
            (df_produtos['sub_produto'] == 'Saldo em Conta') &
            (df_produtos['net'] > 0)  # Filtra valores de net maiores que 0
            # net_em_m > 50 mil
            # data ultimo atendimento >15 dias para investor
        ].sort_values(by='net', ascending=False)  # Ordena pelo valor de net

        # Junta as duas listas, colocando vencimento na frente
        todas_oportunidades = pd.concat([oportunidades_vencimento, oportunidades_saldo])
        print(f"Oportunidades vencimento = {oportunidades_vencimento}")
        print(f"Oportunidades saldo = {oportunidades_saldo}")
       

        # Define o número de oportunidades com base no código do assessor
        if self.codigo_assessor == "24851":
            num_oportunidades = 15
        elif self.codigo_assessor == 'GERAL':
            num_oportunidades = 125
        else:
            num_oportunidades = 25
        # Remove oportunidades duplicadas 
        todas_oportunidades = todas_oportunidades.drop_duplicates(subset=["codigo_cliente_xp"], keep='first')
        melhores_oportunidades = todas_oportunidades.head(num_oportunidades)
        print(todas_oportunidades)

        # Prepara o DataFrame de saída
        df_saida = pd.DataFrame({
            'Codigo Assessor': [self.codigo_assessor] * len(melhores_oportunidades),
            'Codigo Cliente': melhores_oportunidades['codigo_cliente_xp'].tolist()
        })
        print (melhores_oportunidades['codigo_cliente_xp'])
        #print(f"Carteira = {self.carteira_clientes}")
        # Exportando para .xlsx
        geral = [13136,72738,26904,67114]
        if self.codigo_assessor not in geral :
            nome_arquivo = f'oportunidades_assessor_{self.codigo_assessor}.xlsx'
            df_saida.to_excel(nome_arquivo, index=False)
            print(f"Oportunidades exportadas para {nome_arquivo}")
            
        
        else:
            print("Assessor geral")
            
            
        
        return df_saida  # Retorne df_saida em vez da lista


db.verifica()

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

geral = [13136,72738,26904,67114]

def carteiras(*assessores):
    print("Entrou CARTEIRAS")
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()

    # Consulta SQL para recuperar os dados de clientes e seus assessores
    query = 'SELECT codigo_cliente_xp, assessor_cod_assessor FROM Clientes'
    cursor.execute(query)
    resultados = cursor.fetchall()

    # Dicionário para mapear códigos de assessores para listas de clientes
    carteiras_assessores = {}

    for codigo_cliente, codigo_assessor in resultados:
        if codigo_assessor not in carteiras_assessores:
            carteiras_assessores[codigo_assessor] = []

        # Adicione o cliente à lista de clientes do assessor
        """    if (codigo_assessor == "13136") or (codigo_assessor == "72738") or (codigo_assessor == "26904"):
            print("Entrou assessor geral")
            codigo_assessor_temp = 'GERAL'
            carteiras_assessores['GERAL'].append(codigo_cliente)
        else:"""
        carteiras_assessores[codigo_assessor].append(codigo_cliente)
        #carteiras_assessores[codigo_assessor].append(codigo_cliente)

        
    # Atualize a coluna "carteira" na tabela "Assessores" com as carteiras calculadas
    for codigo_assessor, carteira in carteiras_assessores.items():
       # print(f"Assessor {codigo_assessor}\nCarteira = {carteira}\n Carteiras assessores = {carteiras_assessores}")
        carteira_str = ','.join(map(str, carteira))
        query = "UPDATE Assessores SET carteira = ? WHERE codigo_assessor = ?"

        if codigo_assessor in carteiras_assessores:
            """print(f"Entrou geral")
            if codigo_assessor == 'GERAL':
                query = "UPDATE Assessores SET carteira = ? WHERE codigo_assessor = 'GERAL'"
                cursor.execute(query, (carteira_str))
            else:"""
            query = "UPDATE Assessores SET carteira = ? WHERE codigo_assessor = ?"
            cursor.execute(query, (carteira_str, codigo_assessor))
        else:
            cursor.execute(query, (carteira_str, codigo_assessor))
    
    conn.commit()
    # Feche a conexão com o banco de dados
    conn.close()





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
    #df_produtos = pd.read_sql_query(query, conn)
    conn.close()
    dfs_oportunidades = []
    dfs_gerais = []
    for assessor in assessores:
        if assessor.codigo_assessor in geral:
            dfs_gerais.append(assessor.rankear_oportunidades())
        else:
            dfs_oportunidades.append(assessor.rankear_oportunidades())
        
    
    """gerais = assessores in geral 
    print(f'Gerais = {gerais}')"""
    df_gerais = pd.concat(dfs_gerais, axis=0)
    df_gerais.to_excel('oportunidades_gerais.xlsx', index=False)
    print("Oportunidades gerais exportadas para 'oportunidades_gerais.xlsx'.")
    #dfs_oportunidades.append(dfs_gerais)
    df_consolidado = pd.concat(dfs_oportunidades + dfs_gerais, axis=0)

    # Exportando para um único arquivo Excel
    df_consolidado.to_excel('oportunidades_consolidadas.xlsx', index=False)
    print("Oportunidades consolidadas exportadas para 'oportunidades_consolidadas.xlsx'.")

def mail():
    with open("email.json", encoding='utf-8') as meu_json:
        dados_email = json.load(meu_json)
   # print (dados_email)
    #print(dados_email)
    print("Entrando na função mail")
    hoje = datetime.now().date()
    # Dados de autenticação
    username = dados_email['usuario']  # Substitua com seu endereço de e-mail
    password = dados_email['senha']  # Substitua com sua senha de e-mail
    emailDestino = "felipe.gomes@messeminvestimentos.com.br"  # Substitua com o e-mail do destinatário
    assunto = "Relatório de oportunidades"
    conteudo = f"Gerado em {hoje}"

    # Crie o objeto MIMEMultipart
    msg = MIMEMultipart()
    msg['To'] = emailDestino
    msg['From'] = username
    msg['Subject'] = assunto

    # Adicione o conteúdo do e-mail
    msg.attach(MIMEText(conteudo, 'plain', 'utf-8'))

    # Anexe o arquivo Excel
    file_path = "oportunidades_consolidadas.xlsx"  # Substitua com o caminho para o arquivo Excel
    with open(file_path, 'rb') as file:
        attachment = MIMEApplication(file.read(), _subtype="xlsx")
        attachment.add_header('content-disposition', 'attachment', filename="oportunidades_consolidades.xlsx")
        msg.attach(attachment)

    # Enviando o e-mail
    with smtplib.SMTP("email-ssl.com.br", 587) as server:
        server.starttls()
        server.login(username, password)
        server.sendmail(username, emailDestino, msg.as_string())

    print("E-mail enviado com sucesso!")


def main():
    #os.system("cls")
    while True:
        print("Entrando main menu")
        menu = input("1 - Atualizar banco de dados\n2 - Ajuste carteira\n3 - Gerar lista de oportunidades\n4 - Enviar op consolidadas por e-mail\n5 - Listar assessores\n0 - SAIR\n")
        match menu:
            case "1":
                # Regrava dados com base nas planilhas
                db.update()
                carteiras(*objetos)
               
            case "2":
                for assessor in objetos:
                    print(f"{assessor.carteira_clientes}")
                #carteiras(*objetos)
            case "3":
                # invoca a função rankear_oportunidades em cada assessor
                """for assessor in objetos:
                    assessor.rankear_oportunidades()"""
                consolidar_oportunidades(*objetos)

            case "4":
                mail()
                
            case "5":
                # Listar os códigos de assessor
                for assessor in codigo_assessores:
                    print(f"Código Assessor: {assessor}")
            
            case "0":
                os.system("cls")
                break
            
            case __:
                break

# Distribui as carteiras na primeira execução
carteiras(*objetos)
main()