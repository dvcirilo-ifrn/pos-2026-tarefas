import requests
import getpass

print("=" * 50)
print("        CLIENTE SUAP - BOLETIM DO ALUNO        ")
print("=" * 50)

# 1. Entrada de dados do usuário
usuario = input("Usuário SUAP: ").strip()
senha = getpass.getpass("Senha: ")

print("-" * 50)
ano = input("Digite o Ano Letivo (Ex: 2024, 2025 ou 2026): ").strip()
periodo = input("Digite o Período (Ex: 1 ou 2): ").strip()
print("-" * 50)

# Configurações da API do SUAP
URL_BASE = "https://suap.ifrn.edu.br/api/v2"
URL_AUTENTICACAO = f"{URL_BASE}/autenticacao/token/"
# Atenção à barra '/' no final da URL do boletim, o SUAP exige ela!
URL_BOLETIM = f"{URL_BASE}/minhas-informacoes/boletim/{ano}/{periodo}/"

print("\nAutenticando...")

try:
    # 2. Realizando a autenticação para obter o Token JWT
    payload_auth = {
        "username": usuario,
        "password": senha
    }
    
    resposta_auth = requests.post(URL_AUTENTICACAO, json=payload_auth)
    
    if resposta_auth.status_code == 200:
        print("✓ Autenticação bem-sucedida!")
        token = resposta_auth.json().get("access") or resposta_auth.json().get("token")
        
        # Configura os cabeçalhos com o Token obtido
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        print(f"Obtendo boletim do período {ano}/{periodo}...")
        
        # 3. Requisição dos dados do boletim
        resposta_boletim = requests.get(URL_BOLETIM, headers=headers)
        
        if resposta_boletim.status_code == 200:
            boletim_dados = resposta_boletim.json()
            
            print("\n" + "=" * 50)
            print(f"       BOLETIM - PERÍODO {ano}/{periodo}       ")
            print("=" * 50)
            
            # Se a API retornar uma lista de disciplinas
            if isinstance(boletim_dados, list) and len(boletim_dados) > 0:
                for materia in boletim_dados:
                    disciplina = materia.get('disciplina', 'Disciplina Sem Nome')
                    # Remove o código longo da disciplina para ficar mais limpo se quiser
                    disciplina_limpa = disciplina.split(') ')[-1] if ') ' in disciplina else disciplina
                    
                    nota = materia.get('media_final_disciplina', '-')
                    situacao = materia.get('situacao', '-')
                    
                    print(f"• {disciplina_limpa[:35]:<35} | Nota: {nota:<4} | Situação: {situacao}")
            else:
                print("Nenhum dado ou disciplina encontrado para este período.")
                
            print("=" * 50)
            
        elif resposta_boletim.status_code == 404:
            print(f"✕ Erro ao obter boletim. Código HTTP: 404")
            print(f"\nDica profissional: O SUAP retornou que a URL '{URL_BOLETIM}' não existe.")
            print("Isso geralmente acontece por dois motivos:")
            print(f"1. O período '{ano}/{periodo}' ainda não foi gerado no sistema para você.")
            print("2. Tente rodar o script novamente usando um ano passado (ex: 2024 / período: 1) para testar.")
            
        else:
            print(f"✕ Erro inesperado ao obter boletim. Código HTTP: {resposta_boletim.status_code}")
            
    elif resposta_auth.status_code == 401:
        print("✕ Erro de Autenticação: Usuário ou senha incorretos.")
    else:
        print(f"✕ Erro ao autenticar. Código HTTP: {resposta_auth.status_code}")

except requests.exceptions.RequestException as e:
    print(f"\n✕ Erro de conexão com o servidor do SUAP: {e}")