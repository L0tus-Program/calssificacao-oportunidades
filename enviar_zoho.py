import requests
import json

# envia um webhook

"""def webhook(assessor,codigo_xp):
    i = 0
    for i in codigo_xp:
        print(codigo_xp[i])


    link = "https://flow.zoho.com/815771232/flow/webhook/incoming?zapikey=1001.8fb63478c8d5eaced825a2e92b4349c0.335ce3ce70e63ff554eec611594ccc74&isdebug=true"

    dicionario = {

        "assessor": f"{assessor}",
        "codigo_XP": f"{codigo_xp}",

    }

    dicionario_ajustado = json.dumps(dicionario)
    print(dicionario_ajustado)
    #requests.post(link, data=dicionario_ajustado)



codigo_xp = [123,1234,4567,23413,123523]

webhook("O cara",codigo_xp)"""


def webhook(assessor, codigo_xp):
    print("Entrando webhook")
    for item in codigo_xp:  # 'item' para iterar sobre os elementos da lista
        print(item)
        link = "https://flow.zoho.com/815771232/flow/webhook/incoming?zapikey=1001.30bf0049e9d772502ce75f704a9623f1.07cd1af2982b4b152a570b83d98570ef&isdebug=true"
        dicionario = {
            "assessor": f"{assessor}",
            "codigo_XP": f"{item}",
        }

        dicionario_ajustado = json.dumps(dicionario)
        print(dicionario_ajustado)
        try:
            requests.post(link, data=dicionario_ajustado)
            print("Webhook enviado")
        except:
            print(f"Erro no envio do webhook")
    

#codigo_xp = [123, 1234, 4567, 23413, 123523]

#webhook("O cara", codigo_xp)
