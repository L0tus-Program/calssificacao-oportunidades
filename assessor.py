import pandas as pd
from datetime import datetime, timedelta
import enviar_zoho as zoho
import sqlite3
import os # Verificar se o BD existe na pasta de arquivos
import json


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
        hoje = datetime.now().date()
       # adicionar_dias = timedelta(days = 1)
       # hoje = hoje + adicionar_dias
        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect('seu_banco_de_dados.db')

        # Consulta SQL para buscar os dados da tabela 'produtos' (substitua 'produtos' pelo nome da tabela correta)
        query = f'''
            SELECT *
            FROM produtos
            WHERE codigo_cliente_xp IN {tuple(self.carteira_clientes)}
            AND data_de_vencimento = "{hoje}"
            AND net > 0
            ORDER BY net DESC
        '''

        # Ler os dados da tabela 'produtos' e criar um DataFrame
        df_produtos = pd.read_sql_query(query, conn)

        conn.close()

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