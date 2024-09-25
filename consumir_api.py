import requests

username = input('Qual é o id do usuário?')

url = f'http://127.0.0.1:5000/{username}'

response = requests.get(url)
data = response.json()

if response.status_code == 200:
    print(f'Nome completo: {data["nome"]}')
else:
    print('Não foi possível encontrar o usuário')