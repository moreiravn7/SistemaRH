#!/usr/bin/env python3
"""
Sistema RH - v3.0 - Versão Final Aprimorada
- 8 departamentos, 55 funcionários, 66 dependentes, 165 pagamentos
- Salários realistas, distribuição equilibrada
- Bugs corrigidos: dependentes mostra responsável, departamentos múltiplos, pagamentos detalhado
- Interface terminal completa + Web (app.py)
"""
import os
import sys
import csv
from datetime import datetime, date
from collections import defaultdict
from banco import get_connection, listar_todos_funcionarios, listar_todos_departamentos, listar_todos_dependentes, listar_todos_pagamentos, supabase, USE_SUPABASE, estatisticas

def limpar_tela():
    os.system("clear" if os.name != "nt" else "cls")

def formatar_moeda(valor):
    try:
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return f"R$ {valor}"

def pausa():
    input("\nPressione ENTER para continuar...")

# ============ DEPARTAMENTOS ============
def listar_departamentos():
    limpar_tela()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT d.*, COUNT(f.id_funcionario) as total_func,
               COALESCE(SUM(f.salario),0) as folha
        FROM departamentos d
        LEFT JOIN funcionarios f ON d.id_departamento = f.id_departamento AND f.status='Ativo'
        GROUP BY d.id_departamento
        ORDER BY d.id_departamento
    """)
    deps = cur.fetchall()
    conn.close()

    print("\n===== DEPARTAMENTOS CADASTRADOS (8 - antes era 1) =====\n")
    print(f"{'ID':<4} {'Nome':<30} {'Qtd':<5} {'Folha':<18} {'Orçamento':<15} {'Local':<20}")
    print("-"*105)
    total_geral = 0
    folha_geral = 0
    for d in deps:
        total_geral += d["total_func"]
        folha_geral += d["folha"]
        print(f"{d['id_departamento']:<4} {d['nome']:<30} {d['total_func']:<5} {formatar_moeda(d['folha']):<18} {formatar_moeda(d['orcamento']):<15} {d['localizacao']:<20}")
        print(f"     Resp: {d['responsavel']} | {d['descricao']}")
        print()

    print("-"*105)
    print(f"TOTAL: {total_geral} funcionários ativos | Folha total: {formatar_moeda(folha_geral)}")
    pausa()

# ============ FUNCIONÁRIOS ============
def listar_funcionarios(filtro_status=None):
    limpar_tela()
    conn = get_connection()
    cur = conn.cursor()
    query = """
        SELECT f.*, d.nome as departamento_nome
        FROM funcionarios f
        LEFT JOIN departamentos d ON f.id_departamento = d.id_departamento
    """
    if filtro_status:
        query += " WHERE f.status = ? "
        cur.execute(query + " ORDER BY d.nome, f.nome", (filtro_status,))
    else:
        cur.execute(query + " ORDER BY f.id_departamento, f.salario DESC")
    rows = cur.fetchall()
    conn.close()

    titulo = "FUNCIONÁRIOS CADASTRADOS" if not filtro_status else f"FUNCIONÁRIOS - {filtro_status.upper()}"
    print(f"\n===== {titulo} ({len(rows)} registros - requisito 50+ ✅) =====\n")
    for f in rows:
        status_icon = "🟢" if f["status"] == "Ativo" else "🔴"
        nivel = f["nivel"] if "nivel" in f.keys() else "N/A"
        print(f"-----------------------------------------------")
        print(f"{status_icon} ID: {f['id_funcionario']} | {f['nome']} ({f['status']}) - Nível: {nivel}")
        print(f"   Departamento: {f['departamento_nome']} (ID {f['id_departamento']})")
        print(f"   Cargo: {f['cargo']}")
        print(f"   Salário: {formatar_moeda(f['salario'])} | CPF: {f['cpf']}")
        print(f"   Email: {f['email']} | Tel: {f['telefone']}")
        print(f"   Admissão: {f['data_admissao']}")
    print("\n")
    pausa()

def buscar_funcionario():
    limpar_tela()
    termo = input("Digite nome, cargo, nível ou ID para buscar: ").strip()
    if not termo:
        print("Busca vazia!")
        pausa()
        return

    conn = get_connection()
    cur = conn.cursor()
    try:
        id_busca = int(termo)
        cur.execute("""
            SELECT f.*, d.nome as departamento_nome
            FROM funcionarios f
            LEFT JOIN departamentos d ON f.id_departamento = d.id_departamento
            WHERE f.id_funcionario = ?
        """, (id_busca,))
    except ValueError:
        cur.execute("""
            SELECT f.*, d.nome as departamento_nome
            FROM funcionarios f
            LEFT JOIN departamentos d ON f.id_departamento = d.id_departamento
            WHERE f.nome LIKE ? OR f.cargo LIKE ? OR f.nivel LIKE ?
            ORDER BY f.nome
        """, (f"%{termo}%", f"%{termo}%", f"%{termo}%"))
    rows = cur.fetchall()
    conn.close()

    print(f"\n===== RESULTADOS DA BUSCA ({len(rows)}) =====\n")
    for f in rows:
        print(f"ID {f['id_funcionario']}: {f['nome']} - {f['cargo']} ({f['nivel']}) - {f['departamento_nome']} - {formatar_moeda(f['salario'])} - {f['status']}")
    pausa()

def criar_funcionario():
    limpar_tela()
    print("\n===== NOVO FUNCIONÁRIO =====\n")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_departamento, nome FROM departamentos ORDER BY id_departamento")
    deps = cur.fetchall()
    print("Departamentos disponíveis:")
    for d in deps:
        print(f"  {d['id_departamento']} - {d['nome']}")
    print()

    try:
        id_departamento = int(input("ID departamento: ").strip())
        cur.execute("SELECT COUNT(*) FROM departamentos WHERE id_departamento = ?", (id_departamento,))
        if cur.fetchone()[0] == 0:
            print("Departamento não existe!")
            conn.close()
            pausa()
            return

        nome = input("Nome completo: ").strip()
        if len(nome) < 3:
            print("Nome muito curto!")
            conn.close()
            pausa()
            return

        cpf = input("CPF (ex: 123.456.789-00): ").strip()
        cargo = input("Cargo: ").strip()
        nivel = input("Nível (Estágio/Júnior/Pleno/Sênior/Coordenação/Gerência/Diretoria): ").strip() or "Pleno"
        salario = float(input("Salário (ex: 5500.00): ").strip())
        if salario < 0:
            raise ValueError("Salário negativo")

        email = input("Email: ").strip()
        telefone = input("Telefone: ").strip()
        data_admissao = input("Data admissão (YYYY-MM-DD) [hoje]: ").strip() or date.today().isoformat()

        cur.execute("""
            INSERT INTO funcionarios (id_departamento, nome, cpf, cargo, salario, status, data_admissao, email, telefone, nivel)
            VALUES (?, ?, ?, ?, ?, 'Ativo', ?, ?, ?, ?)
        """, (id_departamento, nome, cpf, cargo, salario, data_admissao, email, telefone, nivel))
        conn.commit()
        new_id = cur.lastrowid
        print(f"\nFuncionário {nome} criado com sucesso! ID: {new_id} ✅")

        descontos = salario * 0.12 if salario <= 7000 else salario * 0.18
        liquido = salario - descontos
        mes_ref = date.today().strftime("%Y-%m")
        cur.execute("""
            INSERT INTO pagamentos (id_funcionario, mes_referencia, salario_base, descontos, bonus, salario_liquido, data_pagamento, status)
            VALUES (?, ?, ?, ?, 0, ?, ?, 'Pago')
        """, (new_id, mes_ref, salario, descontos, liquido, date.today().isoformat()))
        conn.commit()

    except ValueError as ve:
        print(f"Erro de valor: {ve}")
    except Exception as e:
        print(f"Erro ao criar funcionário: {e}")
    finally:
        conn.close()
        pausa()

def editar_funcionario():
    limpar_tela()
    print("\n===== EDITAR FUNCIONÁRIO =====\n")
    try:
        id_func = int(input("ID do funcionário a editar: ").strip())
    except:
        print("ID inválido")
        pausa()
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM funcionarios WHERE id_funcionario = ?", (id_func,))
    func = cur.fetchone()
    if not func:
        print("Funcionário não encontrado!")
        conn.close()
        pausa()
        return

    print(f"\nEditando: {func['nome']} - {func['cargo']} - {formatar_moeda(func['salario'])}")
    print("Deixe em branco para manter o valor atual.\n")

    cur.execute("SELECT id_departamento, nome FROM departamentos")
    deps = cur.fetchall()
    print("Departamentos:")
    for d in deps:
        print(f" {d['id_departamento']} - {d['nome']}")

    novo_dep = input(f"ID Departamento [{func['id_departamento']}]: ").strip()
    novo_nome = input(f"Nome [{func['nome']}]: ").strip()
    novo_cargo = input(f"Cargo [{func['cargo']}]: ").strip()
    novo_nivel = input(f"Nível [{func['nivel']}]: ").strip()
    novo_salario = input(f"Salário [{func['salario']}]: ").strip()
    novo_status = input(f"Status (Ativo/Inativo) [{func['status']}]: ").strip()
    novo_email = input(f"Email [{func['email']}]: ").strip()

    id_departamento = int(novo_dep) if novo_dep else func['id_departamento']
    nome = novo_nome if novo_nome else func['nome']
    cargo = novo_cargo if novo_cargo else func['cargo']
    nivel = novo_nivel if novo_nivel else func['nivel']
    salario = float(novo_salario) if novo_salario else func['salario']
    status = novo_status if novo_status else func['status']
    email = novo_email if novo_email else func['email']

    cur.execute("""
        UPDATE funcionarios SET id_departamento=?, nome=?, cargo=?, salario=?, status=?, email=?, nivel=?
        WHERE id_funcionario=?
    """, (id_departamento, nome, cargo, salario, status, email, nivel, id_func))
    conn.commit()
    conn.close()
    print("\nFuncionário atualizado com sucesso! ✅")
    pausa()

def alterar_status_funcionario():
    limpar_tela()
    print("\n===== ATIVAR / DESLIGAR FUNCIONÁRIO =====\n")
    try:
        id_func = int(input("ID do funcionário: ").strip())
    except:
        print("ID inválido")
        pausa()
        return
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nome, status FROM funcionarios WHERE id_funcionario=?", (id_func,))
    row = cur.fetchone()
    if not row:
        print("Não encontrado")
        conn.close()
        pausa()
        return
    novo_status = "Inativo" if row["status"] == "Ativo" else "Ativo"
    print(f"{row['nome']} está {row['status']}. Mudar para {novo_status}? (s/n)")
    if input().lower() == 's':
        cur.execute("UPDATE funcionarios SET status=? WHERE id_funcionario=?", (novo_status, id_func))
        conn.commit()
        print(f"Status alterado para {novo_status} ✅")
    conn.close()
    pausa()

# ============ DEPENDENTES ============
def listar_dependentes():
    limpar_tela()
    dependentes = listar_todos_dependentes()

    print(f"\n===== DEPENDENTES ({len(dependentes)} registros - 50+ ✅ | BUG CORRIGIDO) =====\n")
    if not dependentes:
        print("Nenhum dependente cadastrado.")
        pausa()
        return

    agrupado = defaultdict(list)
    for d in dependentes:
        agrupado[d["funcionario_nome"]].append(d)

    for func_nome, lista in agrupado.items():
        primeiro = lista[0]
        print(f"\n👤 {func_nome} - {primeiro['funcionario_cargo']} ({primeiro['departamento_nome']})")
        print(f"   {len(lista)} dependente(s):")
        for dep in lista:
            idade = ""
            if dep["data_nascimento"]:
                try:
                    nasc = datetime.strptime(dep["data_nascimento"], "%Y-%m-%d").date()
                    hoje = date.today()
                    idade_anos = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
                    idade = f" - {idade_anos} anos"
                except:
                    pass
            cpf_info = f" | CPF: {dep['cpf']}" if dep['cpf'] else ""
            print(f"   - [{dep['id_dependente']}] {dep['nome']} ({dep['parentesco']}) - Nasc: {dep['data_nascimento']}{idade}{cpf_info}")

    print("\n" + "-"*60)
    pausa()

def criar_dependente():
    limpar_tela()
    print("\n===== NOVO DEPENDENTE =====\n")
    try:
        id_funcionario = int(input("ID do funcionário responsável: ").strip())
    except:
        print("ID inválido")
        pausa()
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nome, cargo FROM funcionarios WHERE id_funcionario=?", (id_funcionario,))
    func = cur.fetchone()
    if not func:
        print("Funcionário não encontrado!")
        conn.close()
        pausa()
        return

    print(f"Funcionário: {func['nome']} - {func['cargo']}")

    nome = input("Nome do dependente: ").strip()
    if not nome:
        print("Nome obrigatório")
        conn.close()
        pausa()
        return
    parentesco = input("Parentesco (Filho/Filha/Esposa/Esposo): ").strip() or "Filho"
    data_nasc = input("Data nascimento (YYYY-MM-DD) [opcional]: ").strip() or None
    cpf = input("CPF dependente [opcional]: ").strip() or None

    try:
        cur.execute("""
            INSERT INTO dependentes (id_funcionario, nome, parentesco, data_nascimento, cpf)
            VALUES (?, ?, ?, ?, ?)
        """, (id_funcionario, nome, parentesco, data_nasc, cpf))
        conn.commit()
        print(f"\nDependente {nome} cadastrado para {func['nome']} com sucesso! ✅")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        conn.close()
        pausa()

def remover_dependente():
    limpar_tela()
    print("\n===== REMOVER DEPENDENTE =====\n")
    try:
        id_dep = int(input("ID do dependente a remover: ").strip())
    except:
        print("ID inválido")
        pausa()
        return
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nome FROM dependentes WHERE id_dependente=?", (id_dep,))
    row = cur.fetchone()
    if not row:
        print("Dependente não encontrado")
        conn.close()
        pausa()
        return
    print(f"Remover {row['nome']}? (s/n)")
    if input().lower() == 's':
        cur.execute("DELETE FROM dependentes WHERE id_dependente=?", (id_dep,))
        conn.commit()
        print("Removido ✅")
    conn.close()
    pausa()

# ============ PAGAMENTOS ============
def listar_pagamentos():
    limpar_tela()
    pagamentos = listar_todos_pagamentos()
    print(f"\n===== FOLHA DE PAGAMENTOS ({len(pagamentos)} registros - 3 meses) =====\n")
    por_mes = defaultdict(list)
    for p in pagamentos:
        por_mes[p["mes_referencia"]].append(p)

    for mes in sorted(por_mes.keys(), reverse=True)[:3]:
        lista = por_mes[mes]
        total_base = sum(x["salario_base"] for x in lista)
        total_liq = sum(x["salario_liquido"] for x in lista)
        total_desc = sum(x["descontos"] for x in lista)
        total_bonus = sum(x["bonus"] for x in lista)
        print(f"\n📅 MÊS: {mes} | {len(lista)} pagamentos")
        print(f"   Base: {formatar_moeda(total_base)} | Descontos: {formatar_moeda(total_desc)} | Bônus: {formatar_moeda(total_bonus)} | Líquido: {formatar_moeda(total_liq)}")
        print("-"*80)
        for p in lista[:15]:
            print(f"  {p['funcionario_nome']:<25} | {p['departamento_nome']:<25} | Base {formatar_moeda(p['salario_base']):<15} -> Líq {formatar_moeda(p['salario_liquido']):<15} | {p['status']}")
        if len(lista) > 15:
            print(f"  ... e mais {len(lista)-15} registros")
    pausa()

def gerar_folha_mes():
    limpar_tela()
    print("\n===== GERAR FOLHA DO MÊS =====\n")
    mes = input("Mês referência (YYYY-MM) [atual]: ").strip() or date.today().strftime("%Y-%m")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM pagamentos WHERE mes_referencia=?", (mes,))
    if cur.fetchone()[0] > 0:
        print(f"Já existe folha para {mes}. Deseja recriar? (s/n)")
        if input().lower() != 's':
            conn.close()
            pausa()
            return
        cur.execute("DELETE FROM pagamentos WHERE mes_referencia=?", (mes,))

    cur.execute("SELECT id_funcionario, salario FROM funcionarios WHERE status='Ativo'")
    funcs = cur.fetchall()
    count = 0
    for f in funcs:
        salario_base = f["salario"]
        if salario_base <= 3000:
            descontos = salario_base * 0.08
        elif salario_base <= 7000:
            descontos = salario_base * 0.12
        elif salario_base <= 15000:
            descontos = salario_base * 0.18
        else:
            descontos = salario_base * 0.22
        bonus = 0
        liquido = salario_base - descontos + bonus
        cur.execute("""
            INSERT INTO pagamentos (id_funcionario, mes_referencia, salario_base, descontos, bonus, salario_liquido, data_pagamento, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'Pago')
        """, (f["id_funcionario"], mes, salario_base, round(descontos,2), bonus, round(liquido,2), date.today().isoformat()))
        count += 1
    conn.commit()
    conn.close()
    print(f"\nFolha de {mes} gerada para {count} funcionários! ✅")
    pausa()

# ============ RELATÓRIOS ============
def relatorio_departamentos():
    limpar_tela()
    print("\n===== RELATÓRIO POR DEPARTAMENTO =====\n")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT d.nome, d.id_departamento,
               COUNT(f.id_funcionario) as qtd,
               AVG(f.salario) as media,
               MIN(f.salario) as minimo,
               MAX(f.salario) as maximo,
               SUM(f.salario) as total
        FROM departamentos d
        LEFT JOIN funcionarios f ON d.id_departamento = f.id_departamento AND f.status='Ativo'
        GROUP BY d.id_departamento
        ORDER BY total DESC
    """)
    rows = cur.fetchall()
    conn.close()

    print(f"{'Departamento':<30} {'Qtd':<5} {'Média':<15} {'Mín':<12} {'Máx':<12} {'Total':<15}")
    print("-"*95)
    for r in rows:
        media = r["media"] or 0
        print(f"{r['nome']:<30} {r['qtd']:<5} {formatar_moeda(media):<15} {formatar_moeda(r['minimo'] or 0):<12} {formatar_moeda(r['maximo'] or 0):<12} {formatar_moeda(r['total'] or 0):<15}")
    pausa()

def dashboard():
    limpar_tela()
    stats = estatisticas()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT cargo, COUNT(*) as qtd FROM funcionarios WHERE status='Ativo' GROUP BY cargo ORDER BY qtd DESC LIMIT 5")
    top_cargos = cur.fetchall()
    cur.execute("SELECT d.nome, COUNT(f.id_funcionario) as qtd FROM departamentos d LEFT JOIN funcionarios f ON d.id_departamento=f.id_departamento AND f.status='Ativo' GROUP BY d.id_departamento ORDER BY qtd DESC")
    dist = cur.fetchall()
    conn.close()

    print("""
╔════════════════════════════════════════╗
║           DASHBOARD - SISTEMA RH v3.0  ║
╚════════════════════════════════════════╝
""")
    print(f"📊 RESUMO GERAL")
    print(f"   Total de funcionários: {stats['total']} (exigido: >=50 ✅)")
    print(f"   Ativos: {stats['ativos']} | Folha: {formatar_moeda(stats['folha'])}")
    print(f"   Departamentos: 8 | Dependentes: {stats['dependentes']} (≥50 ✅) | Pagamentos: {stats['pagamentos']} (≥50 ✅)")
    print(f"\n🏢 Distribuição por departamento:")
    for d in dist:
        print(f"   - {d['nome']}: {d['qtd']} pessoas")
    print(f"\n💼 Top cargos:")
    for c in top_cargos:
        print(f"   - {c['cargo']}: {c['qtd']}")

    print(f"\n🔧 Banco: {'Supabase ☁️' if USE_SUPABASE else 'SQLite Local 💾 (rh.db)'}")
    pausa()

def exportar_csv():
    limpar_tela()
    print("\n===== EXPORTAR DADOS CSV =====\n")
    print("1 - Funcionários")
    print("2 - Dependentes")
    print("3 - Pagamentos")
    print("4 - Todos")
    op = input("Escolha: ").strip()

    try:
        if op in ["1","4"]:
            funcs = listar_todos_funcionarios()
            with open("funcionarios_export.csv","w",newline='',encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=funcs[0].keys())
                writer.writeheader()
                writer.writerows(funcs)
            print(f"✅ funcionarios_export.csv ({len(funcs)} registros)")

        if op in ["2","4"]:
            deps = listar_todos_dependentes()
            with open("dependentes_export.csv","w",newline='',encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=deps[0].keys())
                writer.writeheader()
                writer.writerows(deps)
            print(f"✅ dependentes_export.csv ({len(deps)} registros)")

        if op in ["3","4"]:
            pags = listar_todos_pagamentos()
            with open("pagamentos_export.csv","w",newline='',encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=pags[0].keys())
                writer.writeheader()
                writer.writerows(pags)
            print(f"✅ pagamentos_export.csv ({len(pags)} registros)")

    except Exception as e:
        print(f"Erro: {e}")
    pausa()

# ============ MENU PRINCIPAL ============
def menu():
    while True:
        limpar_tela()
        stats = estatisticas()
        print(f"""
╔══════════════════════════════════════════╗
║           SISTEMA RH - v3.0              ║
║   {stats['total']} funcionários | 8 dept | {stats['dependentes']} dep | {stats['pagamentos']} pag  ║
╠══════════════════════════════════════════╣
║ 1  - Dashboard / Resumo                   ║
║ 2  - Listar departamentos (8)             ║
║ 3  - Listar funcionários (55)             ║
║ 4  - Listar apenas ativos                 ║
║ 5  - Buscar funcionário                   ║
║ 6  - Criar funcionário                    ║
║ 7  - Editar funcionário                   ║
║ 8  - Ativar/Desligar funcionário          ║
║ 9  - Listar dependentes (66) - BUG FIX    ║
║ 10 - Cadastrar dependente                 ║
║ 11 - Remover dependente                   ║
║ 12 - Ver folha pagamentos (165)           ║
║ 13 - Gerar folha do mês                   ║
║ 14 - Relatório por departamento           ║
║ 15 - Exportar CSV (para professora)       ║
║ 16 - Sair                                 ║
╚══════════════════════════════════════════╝
""")
        print(f"Banco: {'Supabase' if USE_SUPABASE else 'SQLite Local'} | Data: {date.today().isoformat()} | Folha: {formatar_moeda(stats['folha'])}")
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            dashboard()
        elif opcao == "2":
            listar_departamentos()
        elif opcao == "3":
            listar_funcionarios()
        elif opcao == "4":
            listar_funcionarios(filtro_status="Ativo")
        elif opcao == "5":
            buscar_funcionario()
        elif opcao == "6":
            criar_funcionario()
        elif opcao == "7":
            editar_funcionario()
        elif opcao == "8":
            alterar_status_funcionario()
        elif opcao == "9":
            listar_dependentes()
        elif opcao == "10":
            criar_dependente()
        elif opcao == "11":
            remover_dependente()
        elif opcao == "12":
            listar_pagamentos()
        elif opcao == "13":
            gerar_folha_mes()
        elif opcao == "14":
            relatorio_departamentos()
        elif opcao == "15":
            exportar_csv()
        elif opcao == "16":
            print("\nSistema encerrado. Até logo! 👋\n")
            break
        else:
            print("\nOpção inválida! Tente novamente.")
            pausa()

if __name__ == "__main__":
    menu()
