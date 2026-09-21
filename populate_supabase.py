"""
Script para popular Supabase com 55+ registros (quando Supabase voltar a ficar online)
Rode: python populate_supabase.py
"""
import sys
sys.path.insert(0, '.')

# Primeiro garante que SQLite está populado
from banco import get_connection, listar_todos_funcionarios, listar_todos_departamentos, listar_todos_dependentes, listar_todos_pagamentos

print("Lendo dados do SQLite local...")
funcs = listar_todos_funcionarios()
deps = listar_todos_departamentos()
dependentes = listar_todos_dependentes()
pagamentos = listar_todos_pagamentos()

print(f"SQLite: {len(deps)} deps, {len(funcs)} funcs, {len(dependentes)} dependentes, {len(pagamentos)} pagamentos")

# Tenta Supabase
try:
    from banco import supabase, USE_SUPABASE
    if not USE_SUPABASE or supabase is None:
        print("❌ Supabase offline (DNS não resolve). Use o SQLite local ou execute supabase_schema.sql manualmente no painel Supabase.")
        print("💡 O arquivo supabase_schema.sql tem o DDL pronto para colar no SQL Editor do Supabase.")
        sys.exit(0)

    print("Conectado ao Supabase, limpando e populando...")

    # Limpa
    supabase.table("pagamentos").delete().neq("id_pagamento", 0).execute()
    supabase.table("dependentes").delete().neq("id_dependente", 0).execute()
    supabase.table("funcionarios").delete().neq("id_funcionario", 0).execute()
    supabase.table("departamentos").delete().neq("id_departamento", 0).execute()

    # Insere departamentos
    for d in deps:
        supabase.table("departamentos").insert({
            "id_departamento": d["id_departamento"],
            "nome": d["nome"],
            "descricao": d["descricao"],
            "orcamento": d["orcamento"],
            "responsavel": d["responsavel"]
        }).execute()

    print(f"✅ {len(deps)} departamentos inseridos no Supabase")

    # Insere funcionários
    for f in funcs:
        supabase.table("funcionarios").insert({
            "id_funcionario": f["id_funcionario"],
            "id_departamento": f["id_departamento"],
            "nome": f["nome"],
            "cpf": f["cpf"],
            "cargo": f["cargo"],
            "salario": f["salario"],
            "status": f["status"]
        }).execute()

    print(f"✅ {len(funcs)} funcionários inseridos")

    # Dependentes
    for dep in dependentes:
        supabase.table("dependentes").insert({
            "id_funcionario": dep["id_funcionario"],
            "nome": dep["nome"],
            "parentesco": dep["parentesco"]
        }).execute()

    print(f"✅ {len(dependentes)} dependentes inseridos")
    print("🎉 Supabase populado com sucesso!")

except Exception as e:
    print(f"❌ Erro ao popular Supabase: {e}")
    print("Use o SQLite local (rh.db) que já tem 55+ registros.")
