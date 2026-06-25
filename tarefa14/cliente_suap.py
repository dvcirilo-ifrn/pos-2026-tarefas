import requests
from getpass import getpass

base_api = "https://suap.ifrn.edu.br/api"

usuario = input("Usuário: ")
senha = getpass("Senha: ")

credenciais = {
    "username": usuario,
    "password": senha
}

resposta_token = requests.post(f"{base_api}/token/pair", json=credenciais)

print("URL da requisição:", resposta_token.url)
print("Código de status:", resposta_token.status_code)

dados_token = resposta_token.json()
print(dados_token)

token_acesso = dados_token["access"]

cabecalhos = {
    "Authorization": f"Bearer {token_acesso}"
}

print(cabecalhos)

requests.get(
    f"{base_api}/v2/minhas-informacoes/meus-dados/",
    headers=cabecalhos
)

requests.get(
    f"{base_api}/ensino/meus-dados-aluno/",
    headers=cabecalhos
)

resposta_boletim = requests.get(
    f"{base_api}/ensino/meu-boletim/2025/1",
    headers=cabecalhos
)

print(resposta_boletim.text)
print(resposta_boletim)