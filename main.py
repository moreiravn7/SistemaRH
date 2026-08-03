from banco import supabase
import os


def limpar_tela():
    os.system("clear")


def listar_funcionarios():

    limpar_tela()

    resposta = supabase.table("funcionarios").select("*").execute()

    print("\n===== FUNCIONÁRIOS CADASTRADOS =====\n")

    for f in resposta.data:
        print("--------------------------------")
        print("ID:", f["id_funcionario"])
        print("Nome:", f["nome"])
        print("Cargo:", f["cargo"])
        print("Salário: R$", f["salario"])
        print("Status:", f["status"])


def criar_funcionario():

    limpar_tela()

    print("\n===== NOVO FUNCIONÁRIO =====")

    id_funcionario = int(input("ID funcionário: "))
    id_departamento = int(input("ID departamento: "))
    nome = input("Nome: ")
    cpf = input("CPF: ")
    cargo = input("Cargo: ")
    salario = float(input("Salário: "))

    funcionario = {
        "id_funcionario": id_funcionario,
        "id_departamento": id_departamento,
        "nome": nome,
        "cpf": cpf,
        "cargo": cargo,
        "salario": salario,
        "status": "Ativo"
    }

    supabase.table("funcionarios").insert(funcionario).execute()

    print("\nFuncionário criado com sucesso! ✅")
def listar_dependentes():

    limpar_tela()

    resposta = supabase.table("dependentes").select("*").execute()

    print("\n===== DEPENDENTES =====\n")

    for d in resposta.data:
        print("--------------------------------")
        print("ID:", d)
        

def criar_dependente():

    limpar_tela()

    print("\n===== NOVO DEPENDENTE =====")

    id_funcionario = int(input("ID do funcionário: "))
    nome = input("Nome dependente: ")
    parentesco = input("Parentesco: ")

    dependente = {
        "id_funcionario": id_funcionario,
        "nome": nome,
        "parentesco": parentesco
    }

    supabase.table("dependentes").insert(dependente).execute()

    print("\nDependente cadastrado com sucesso! ✅")


def listar_pagamentos():

    limpar_tela()

    resposta = supabase.table("pagamentos").select("*").execute()

    print("\n===== PAGAMENTOS =====\n")

    for p in resposta.data:
        print("--------------------------------")
        print(p)



while True:

    print("""
========================
      SISTEMA RH
========================

1 - Listar funcionários
2 - Criar funcionário
3 - Listar dependentes
4 - Cadastrar dependente
5 - Ver pagamentos
6 - Sair
""")

    opcao = input("Escolha: ")


    if opcao == "1":
        listar_funcionarios()


    elif opcao == "2":
        criar_funcionario()


    elif opcao == "3":
        listar_dependentes()


    elif opcao == "4":
        criar_dependente()


    elif opcao == "5":
        listar_pagamentos()


    elif opcao == "6":
        print("Sistema encerrado.")
        break


    else:
        print("Opção inválida!")