from clients import ClientAPI
import argparse
import json

api = ClientAPI(base_url="https://jsonplaceholder.typicode.com/users")

parser = argparse.ArgumentParser(description="CLI para gerenciar clientes")

parser.add_argument(
    "action",
    choices=["list", "create", "read", "update", "delete"],
    help="Ação a realizar"
)

parser.add_argument("--id", help="ID do cliente")
parser.add_argument("--name", type=str, help="Nome do cliente")
parser.add_argument("--email", type=str, help="Email do cliente")

args = parser.parse_args()

try:

    if args.action == "list":

        clients = api.list()

        for client in clients:
            print(f"{client['id']}: {client['name']} - {client['email']}")

    elif args.action == "read":

        if args.id is None:
            print("Erro: --id é necessário para visualizar um cliente.")

        else:
            client = api.read(args.id)

            print("\n=== DADOS DO CLIENTE ===")
            print(client)

    elif args.action == "create":

        if not args.name or not args.email:
            print("Erro: --name e --email são obrigatórios para cadastrar um cliente.")

        else:
            new_client = {
                "name": args.name,
                "email": args.email
            }

            client = api.create(new_client)

            print("Cliente cadastrado com sucesso:")
            print(client)

    elif args.action == "update":

        if not args.id or not args.name or not args.email:
            print("Erro: --id, --name e --email são obrigatórios para atualizar um cliente.")

        else:
            updated_client = {
                "name": args.name,
                "email": args.email
            }

            client = api.update(args.id, updated_client)

            print("Cliente atualizado com sucesso:")
            print(client)

    elif args.action == "delete":

        if not args.id:
            print("Erro: --id é necessário para remover um cliente.")

        else:
            result = api.delete(args.id)

            print("Cliente removido com sucesso:")
            print(result)

except Exception as e:
    print(f"Erro: {e}")