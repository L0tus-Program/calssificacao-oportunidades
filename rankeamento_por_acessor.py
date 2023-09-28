import pandas as pd
from datetime import datetime, timedelta
import json
import csv


class assessor:
    def __init__(self, codigo_assessor):
        self.codigo_assessor = codigo_assessor
        self.carteira_clientes = []
    def carregar_planilhas(self):
        pass 
    def carteira_cliente(self,codigo_xp):   
        self.carteira_clientes.append(codigo_xp)
    def export_carteira(self):
        df = pd.DataFrame()
        #df['Assessor'] = self.codigo_assessor
        df[f'Carteira assessor {self.codigo_assessor}'] = self.carteira_clientes
        # Exportar o DataFrame para um arquivo Excel (XLSX)
        df.to_excel(f'clientes{self.codigo_assessor}.xlsx', index=False)

        print("DataFrame exportado para 'clientes_relacionados.xlsx'.")
        #exportar = {f'Assessor {self.codigo_assessor}':{f'Carteira de clientes {self.carteira_cliente}'}}

        #Salvando o resultado em um arquivo JSON
        """with open('carteira{codigo_assessor}.json', 'w') as file:
            json.dump(exportar, file, indent=4)"""
        pass
    def ranking_carteira(self):
        pass
        

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


# Distribuição nas carteiras
#id_clientes = df_conexao["codigo_cliente_xp"]

linhas = 0
#verifica se existe a coluna de codigos xp na planilha e conta quantas linhas tem
if 'codigo_cliente_xp' in df_conexao.columns:
    # Contagem das linhas na coluna 'codigo_cliente_xp'
    linhas = df_conexao['codigo_cliente_xp'].count()
    print("Número de linhas na coluna 'codigo_cliente_xp':", linhas)
else:
    print("A coluna 'codigo_cliente_xp' não foi encontrada no DataFrame.")

print(f"Linhas = {linhas}")
i = 0

# Varrer planilha para formar carteira do assessor
print("Chamando loop")

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
        #print(f"Codigo XP do Cliente {codigo_xp}")
        #print (type(codigo_xp))

        #print(f"Codigo do assessor {codigo_assessor}")

        #print (type(codigo_assessor_int))

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


assessor1.export_carteira()
assessor2.export_carteira()
assessor3.export_carteira()
assessor4.export_carteira()
assessor5.export_carteira()
assessorGeral.export_carteira()

"""
print(f"Carteira assessor 1 {assessor1.carteira_clientes}")
print(f"Carteira assessor 2 {assessor2.carteira_clientes}")
print(f"Carteira assessor 3 {assessor3.carteira_clientes}")
print(f"Carteira assessor 4 {assessor4.carteira_clientes}")
print(f"Carteira assessor 5 {assessor5.carteira_clientes}")


"""





# ordenar coluna por ordem crescente de assessor -> Dica vitor



# Filtrando vencimentos por data
data_atual = datetime.now()
limite_data = data_atual #+ timedelta(days=3)

# Filtrando registros para duas condições:

#  registros com sub_produto "Saldo em Conta" e net maior que 0
condicao_data_vencimento = (
    (df_produtos['data_de_vencimento'].notna()) & 
    (df_produtos['data_de_vencimento'] >= data_atual) &
    (df_produtos['data_de_vencimento'] <= limite_data)
)
condicao_saldo_em_conta = (df_produtos['sub_produto'] == 'Saldo em Conta') & (df_produtos['net'] > 0)

df_produtos_filtrado = df_produtos[condicao_data_vencimento | condicao_saldo_em_conta]


# Junção dos dataframes
df_juncao = pd.merge(df_conexao, df_produtos_filtrado, on='codigo_cliente_xp')