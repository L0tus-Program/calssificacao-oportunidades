import sqlite3

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('clientes.db')
cursor = conn.cursor()

# Consulta SQL para selecionar a coluna 'codigo_assessor' da tabela 'Assessores'
cursor.execute('SELECT codigo_assessor FROM Assessores')

# Coletar os resultados em uma lista
codigo_assessores = [row[0] for row in cursor.fetchall()]

# Fechar a conexão com o banco de dados
conn.close()

# Defina a classe
class Assessor:
    def __init__(self, valor):
        self.valor = valor
        print(f"Valor: {self.valor}")

# Crie objetos da classe com base na lista de itens
objetos = [Assessor(assessor) for assessor in codigo_assessores]
