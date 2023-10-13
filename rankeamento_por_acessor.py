import pandas as pd
from datetime import datetime, timedelta
import enviar_zoho as zoho
import sqlite3
#import json
#import csv

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
    

    def rankear_oportunidades(self, df_produtos):
        hoje = datetime.now().date()
       # adicionar_dias = timedelta(days = 1)
       # hoje = hoje + adicionar_dias

        # Filtra as oportunidades de acordo com as condições especificadas
        oportunidades_vencimento = df_produtos[
            (df_produtos['codigo_cliente_xp'].isin(self.carteira_clientes)) &
            (df_produtos['data_de_vencimento'] == hoje) &
            (df_produtos['net'] > 0)   # Filtra valores de net maiores que 0
        ].sort_values(by='net', ascending=False)  # Ordena pelo valor de net

        oportunidades_saldo = df_produtos[
            (df_produtos['codigo_cliente_xp'].isin(self.carteira_clientes)) &
            (df_produtos['sub_produto'] == 'Saldo em Conta') &
            (df_produtos['net'] > 0)  # Filtra valores de net maiores que 0
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

"""print("Criando banco de dados")
# Conexão com o sqlite
conn = sqlite3.connect('clientes.db')
#transforma o dataframe em tabela SQL
df_conexao.to_sql('Clientes', conn, if_exists='replace')
df_produtos.to_sql('Produtos', conn, if_exists='replace')
# Fecha a conexão 
conn.close()"""

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
assessor1.rankear_oportunidades(df_produtos)
assessor2.rankear_oportunidades(df_produtos)
assessor3.rankear_oportunidades(df_produtos)
assessor4.rankear_oportunidades(df_produtos)
assessor5.rankear_oportunidades(df_produtos)
assessorGeral.rankear_oportunidades(df_produtos)


#assessor1.to_zoho()
# Opção de exportar a carteira inteira

#assessor1.export_carteira()
#assessor2.export_carteira()
#assessor3.export_carteira()
#assessor4.export_carteira()
#assessor5.export_carteira()
#assessorGeral.export_carteira()





