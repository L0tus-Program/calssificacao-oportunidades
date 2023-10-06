import requests

url = "https://gptfree.appgps.com.br/prompt="
prompt = input("  ")
gpt = requests.post(url,prompt)
print(gpt)