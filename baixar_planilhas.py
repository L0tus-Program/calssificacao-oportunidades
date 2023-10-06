
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager


# Configurações
username = "felipe.messem@messeminvestimentos.com.br"
password = "Messem@2023"
#file_name = "nome-do-arquivo.xlsx"
servico = Service(ChromeDriverManager().install())
# Inicialize o navegador
#navegador = webdriver.Chrome("chromenavegador.exe")
#navegador = webdriver.Chrome(ChromenavegadorManager().install())
navegador = webdriver.Chrome(service=servico) #, options= chrome_options)

# Acesse a página de login
navegador.get("https://onedrive.live.com/login/")
time.sleep(10)
# Preencha o formulário de login
navegador.find_element(By.CLASS_NAME,"form-control").send_keys(username)
time.sleep(10)
navegador.find_element(By.ID, "idSIButton9").click()
time.sleep(10)
navegador.find_element(By.ID,"i0118").send_keys(password)
time.sleep(10)
navegador.find_element(By.ID,"idSIButton9").click()
navegador.find_element(By.ID, "idSIButton9").click()
navegador.find_element(By.XPATH, "FICHEIRO").click()

# Aguarde a autenticação (pode ser necessário adicionar um tempo de espera)
#time.sleep(50000000)

# Navegue até o arquivo desejado
navegador.get("https://messem1-my.sharepoint.com/:x:/r/personal/mariana_oliveira_messeminvestimentos_com_br/_layouts/15/Doc.aspx?sourcedoc=%7B05A123A9-A3CD-43CB-ACB2-8264045723BD%7D&file=clientes_conexao_produtos.xlsx&action=default&mobileredirect=true" )#+ file_name)

# Baixe o arquivo
download_link = navegador.find_element(By.CLASS_NAME, "download-link")
download_link.click()

# Encerre o navegador
#navegador.quit()
