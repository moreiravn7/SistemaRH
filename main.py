from banco import supabase
import os


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPressione [Enter] para continuar...")


def obter_mapa_departamentos():
    """Retorna um dicionário {id_departamento: nome_departamento}."""
    resp = supabase.table("departamentos").select("*").execute()
    return {d["id_departamento"]: d["nome"] for d in resp.data}


def obter_mapa_funcionarios():
    """Retorna um dicionário {id_funcionario: dict_funcionario}."""
    resp = supabase.table("funcionarios").select("*").execute()
    return {f["id_funcionario"]: f for f in resp.data}


def listar_departamentos():
    limpar_tela()
    print("=" * 65)
    print("                 DEPARTAMENTOS DA EMPRESA")
    print("=" * 65)

    dept_resp = supabase.table("departamentos").select("*").execute()
    func_resp = supabase.table("funcionarios").select("*").execute()

    # Contagem de colaboradores por departamento
    contagem = {}
    for f in func_resp.data:
        did = f.get("id_departamento")
        contagem[did] = contagem.get(did, 0) + 1

    if not dept_resp.data:
        print("Nenhum departamento cadastrado.")
    else:
        for d in dept_resp.data:
            did = d["id_departamento"]
            qtd = contagem.get(did, 0)
            print(f"[{did}] {d['nome'].upper()} ({qtd} colaboradores)")
            if d.get("descricao"):
                print(f"    Descrição: {d['descricao']}")
            print("-" * 65)

    pausar()


def cadastrar_departamento():
    limpar_tela()
    print("=" * 65)
    print("               CADASTRAR NOVO DEPARTAMENTO")
    print("=" * 65)

    nome = input("Nome do departamento: ").strip()
    if not nome:
        print("❌ O nome não pode ser vazio.")
        pausar()
        return

    descricao = input("Descrição do departamento: ").strip()

    try:
        supabase.table("departamentos").insert({
            "nome": nome,
            "descricao": descricao
        }).execute()
        print("\n✅ Departamento cadastrado com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro ao cadastrar departamento: {e}")

    pausar()


def listar_funcionarios():
    limpar_tela()
    dept_map = obter_mapa_departamentos()
    resposta = supabase.table("funcionarios").select("*").execute()

    print("=" * 95)
    print("                      QUADRO GERAL DE FUNCIONÁRIOS")
    print("=" * 95)

    if not resposta.data:
        print("Nenhum funcionário cadastrado.")
        pausar()
        return

    print(f"Total de funcionários cadastrados: {len(resposta.data)}\n")
    print(f"{'ID':<6}{'NOME':<28}{'DEPARTAMENTO':<22}{'CARGO':<28}{'SALÁRIO':>10}")
    print("-" * 95)

    # Ordenar por ID para exibição limpa
    funcionarios_ordenados = sorted(resposta.data, key=lambda x: x.get("id_funcionario", 0))

    for f in funcionarios_ordenados:
        fid = f.get("id_funcionario", "-")
        nome = f.get("nome", "-")
        cargo = f.get("cargo", "-")
        salario = f.get("salario", 0.0)
        dept_id = f.get("id_departamento")
        dept_nome = dept_map.get(dept_id, "Não atribuído")

        print(f"{fid:<6}{nome[:26]:<28}{dept_nome[:20]:<22}{cargo[:26]:<28}R$ {salario:>8.2f}")

    print("=" * 95)
    pausar()


def listar_funcionarios_por_departamento():
    limpar_tela()
    print("=" * 80)
    print("           FUNCIONÁRIOS ORGANIZADOS POR DEPARTAMENTO")
    print("=" * 80)

    dept_resp = supabase.table("departamentos").select("*").execute()
    func_resp = supabase.table("funcionarios").select("*").execute()

    funcs_por_dep = {}
    for f in func_resp.data:
        did = f.get("id_departamento")
        funcs_por_dep.setdefault(did, []).append(f)

    for dep in dept_resp.data:
        did = dep["id_departamento"]
        nome_dep = dep["nome"]
        funcs = funcs_por_dep.get(did, [])

        print(f"\n📁 DEPARTAMENTO: {nome_dep.upper()} ({len(funcs)} colaboradores)")
        print("-" * 80)
        if not funcs:
            print("   (Nenhum colaborador neste departamento)")
        else:
            for f in sorted(funcs, key=lambda x: x.get("id_funcionario", 0)):
                print(f"   [{f['id_funcionario']}] {f['nome']:<28} | Cargo: {f['cargo']:<30} | R$ {f['salario']:>8.2f}")

    # Sem departamento
    sem_dep = funcs_por_dep.get(None, [])
    if sem_dep:
        print("\n📁 SEM DEPARTAMENTO ATRIBUÍDO")
        print("-" * 80)
        for f in sem_dep:
            print(f"   [{f['id_funcionario']}] {f['nome']:<28} | Cargo: {f['cargo']:<30} | R$ {f['salario']:>8.2f}")

    print("\n" + "=" * 80)
    pausar()


def criar_funcionario():
    limpar_tela()
    print("=" * 65)
    print("                    NOVO FUNCIONÁRIO")
    print("=" * 65)

    # Exibir departamentos disponíveis
    dept_map = obter_mapa_departamentos()
    if dept_map:
        print("Departamentos disponíveis:")
        for did, dnome in dept_map.items():
            print(f"  [{did}] {dnome}")
        print("-" * 65)

    try:
        id_funcionario = int(input("ID do funcionário: "))
        id_departamento = int(input("ID do departamento: "))
        nome = input("Nome completo: ").strip()
        cpf = input("CPF (ex: 000.000.000-00): ").strip()
        cargo = input("Cargo / Função: ").strip()
        salario = float(input("Salário (R$): "))

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
        print("\n✅ Funcionário criado com sucesso!")
    except ValueError:
        print("\n❌ Valor inválido informado. Operação cancelada.")
    except Exception as e:
        print(f"\n❌ Erro ao cadastrar funcionário: {e}")

    pausar()


def atualizar_funcionario():
    limpar_tela()
    print("=" * 65)
    print("             ATUALIZAR CARGO / DEPARTAMENTO / SALÁRIO")
    print("=" * 65)

    try:
        id_func = int(input("ID do funcionário a atualizar: "))
    except ValueError:
        print("❌ ID inválido.")
        pausar()
        return

    resp = supabase.table("funcionarios").select("*").eq("id_funcionario", id_func).execute()
    if not resp.data:
        print(f"❌ Funcionário ID {id_func} não encontrado.")
        pausar()
        return

    func = resp.data[0]
    dept_map = obter_mapa_departamentos()
    print(f"\nFuncionário atual: {func['nome']}")
    print(f"Departamento atual: [{func['id_departamento']}] {dept_map.get(func['id_departamento'], 'N/A')}")
    print(f"Cargo atual: {func['cargo']}")
    print(f"Salário atual: R$ {func['salario']:.2f}")
    print("-" * 65)

    novo_cargo = input("Novo cargo (Enter para manter o mesmo): ").strip()
    novo_salario_str = input("Novo salário (Enter para manter o mesmo): ").strip()
    novo_dept_str = input("Novo ID do departamento (Enter para manter o mesmo): ").strip()

    atualizacoes = {}
    if novo_cargo:
        atualizacoes["cargo"] = novo_cargo
    if novo_salario_str:
        try:
            atualizacoes["salario"] = float(novo_salario_str)
        except ValueError:
            print("⚠️ Salário inválido, campo ignorado.")
    if novo_dept_str:
        try:
            atualizacoes["id_departamento"] = int(novo_dept_str)
        except ValueError:
            print("⚠️ Departamento inválido, campo ignorado.")

    if not atualizacoes:
        print("\nNenhuma alteração informada.")
    else:
        try:
            supabase.table("funcionarios").update(atualizacoes).eq("id_funcionario", id_func).execute()
            print("\n✅ Funcionário atualizado com sucesso!")
        except Exception as e:
            print(f"\n❌ Erro ao atualizar funcionário: {e}")

    pausar()


def listar_dependentes():
    limpar_tela()
    resposta = supabase.table("dependentes").select("*").execute()
    func_map = obter_mapa_funcionarios()

    print("=" * 95)
    print("                    LISTAGEM COMPLETA DE DEPENDENTES")
    print("=" * 95)

    if not resposta.data:
        print("Nenhum dependente cadastrado.")
        pausar()
        return

    print(f"Total de dependentes cadastrados: {len(resposta.data)}\n")
    print(f"{'ID':<6}{'NOME DO DEPENDENTE':<26}{'PARENTESCO':<16}{'RESPONSÁVEL (TITULAR)':<32}{'ID TIT.'}")
    print("-" * 95)

    for d in sorted(resposta.data, key=lambda x: x.get("id_dependente", 0)):
        dep_id = d.get("id_dependente", "-")
        nome_dep = d.get("nome", "-")
        parentesco = d.get("parentesco", "-")
        id_titular = d.get("id_funcionario")

        func_titular = func_map.get(id_titular)
        nome_titular = func_titular["nome"] if func_titular else f"[Titular ID {id_titular} não encontrado]"

        print(f"{dep_id:<6}{nome_dep[:24]:<26}{parentesco[:14]:<16}{nome_titular[:30]:<32}{str(id_titular):<6}")

    print("=" * 95)
    pausar()


def criar_dependente():
    limpar_tela()
    print("=" * 65)
    print("                    NOVO DEPENDENTE")
    print("=" * 65)

    try:
        id_funcionario = int(input("ID do funcionário responsável (titular): "))
        func_resp = supabase.table("funcionarios").select("*").eq("id_funcionario", id_funcionario).execute()
        if not func_resp.data:
            print(f"❌ Funcionário com ID {id_funcionario} não encontrado.")
            pausar()
            return

        titular = func_resp.data[0]
        print(f"👉 Responsável selecionado: {titular['nome']} ({titular['cargo']})")

        nome = input("Nome completo do dependente: ").strip()
        parentesco = input("Grau de parentesco (ex: Filho(a), Cônjuge): ").strip()
        data_nasc = input("Data de nascimento (AAAA-MM-DD ou Enter para pular): ").strip()

        dependente = {
            "id_funcionario": id_funcionario,
            "nome": nome,
            "parentesco": parentesco,
        }
        if data_nasc:
            dependente["data_nascimento"] = data_nasc

        supabase.table("dependentes").insert(dependente).execute()
        print("\n✅ Dependente cadastrado com sucesso e vinculado ao responsável!")
    except ValueError:
        print("\n❌ Valor inválido informado. Operação cancelada.")
    except Exception as e:
        print(f"\n❌ Erro ao cadastrar dependente: {e}")

    pausar()


def listar_pagamentos():
    limpar_tela()
    resposta = supabase.table("pagamentos").select("*").execute()
    func_map = obter_mapa_funcionarios()

    print("=" * 95)
    print("                    FOLHA DE PAGAMENTOS")
    print("=" * 95)

    if not resposta.data:
        print("Nenhum pagamento registrado.")
        pausar()
        return

    print(f"{'MÊS':<9}{'FUNCIONÁRIO':<28}{'SAL. BRUTO':>12}{'DESCONTOS':>12}{'BENEFÍCIOS':>12}{'LÍQUIDO':>14}")
    print("-" * 95)

    total_bruto = 0.0
    total_liquido = 0.0

    for p in sorted(resposta.data, key=lambda x: x.get("id_pagamento", 0)):
        id_func = p.get("id_funcionario")
        func = func_map.get(id_func)
        nome = func["nome"] if func else f"ID {id_func}"

        bruto = p.get("salario_base", 0.0)
        desc = p.get("descontos", 0.0)
        ben = p.get("beneficios", 0.0)
        liq = p.get("valor_liquido", 0.0)
        mes = p.get("mes_referencia", "-")

        total_bruto += bruto
        total_liquido += liq

        print(f"{mes:<9}{nome[:26]:<28}R$ {bruto:>9.2f}R$ {desc:>9.2f}R$ {ben:>9.2f}R$ {liq:>11.2f}")

    print("-" * 95)
    print(f"TOTAIS DA FOLHA:                           R$ {total_bruto:>9.2f}                           R$ {total_liquido:>11.2f}")
    print("=" * 95)
    pausar()


def menu_principal():
    while True:
        limpar_tela()
        print("""
=================================================
                 SISTEMA RH
=================================================
  1 - Listar funcionários (Quadro Geral)
  2 - Listar funcionários por departamento
  3 - Cadastrar novo funcionário
  4 - Atualizar funcionário (cargo, depto, salário)
  5 - Listar dependentes (com nome do responsável)
  6 - Cadastrar dependente
  7 - Listar departamentos
  8 - Cadastrar departamento
  9 - Ver folha de pagamentos
  0 - Sair
=================================================""")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            listar_funcionarios()
        elif opcao == "2":
            listar_funcionarios_por_departamento()
        elif opcao == "3":
            criar_funcionario()
        elif opcao == "4":
            atualizar_funcionario()
        elif opcao == "5":
            listar_dependentes()
        elif opcao == "6":
            criar_dependente()
        elif opcao == "7":
            listar_departamentos()
        elif opcao == "8":
            cadastrar_departamento()
        elif opcao == "9":
            listar_pagamentos()
        elif opcao == "0":
            print("\nSistema encerrado. Até logo! 👋")
            break
        else:
            print("❌ Opção inválida! Escolha uma opção do menu.")
            pausar()


if __name__ == "__main__":
    menu_principal()
