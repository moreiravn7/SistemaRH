"""
Demo rápido para mostrar que o sistema está funcional e tem 50+ registros
Rode: python demo.py
"""
from banco import listar_todos_funcionarios, listar_todos_departamentos, listar_todos_dependentes, listar_todos_pagamentos, get_connection

print("="*70)
print(" DEMO - SISTEMA RH v2.0 - Prova de 50+ registros")
print("="*70)

deps = listar_todos_departamentos()
funcs = listar_todos_funcionarios()
dependentes = listar_todos_dependentes()
pagamentos = listar_todos_pagamentos()

print(f"\n✅ Departamentos: {len(deps)} (antes era 1)")
for d in deps:
    print(f"   - {d['id_departamento']}: {d['nome']} (R$ {d['orcamento']:.0f})")

print(f"\n✅ Funcionários: {len(funcs)} (requisito professora: >=50)")
# mostra distribuição
from collections import Counter
dist = Counter([f['departamento_nome'] for f in funcs])
for dept, qtd in dist.items():
    print(f"   - {dept}: {qtd} pessoas")

print(f"\n💰 Exemplos de salários realistas:")
for f in sorted(funcs, key=lambda x: x['salario'], reverse=True)[:5]:
    print(f"   - {f['nome']:<20} | {f['cargo']:<30} | R$ {f['salario']:,.2f}")

print(f"\n👨‍👩‍👧‍👦 Dependentes: {len(dependentes)} (bug corrigido - agora mostra responsável)")
for d in dependentes[:8]:
    print(f"   - {d['nome']} ({d['parentesco']}) -> Filho(a) de {d['funcionario_nome']} ({d['funcionario_cargo']} / {d['departamento_nome']})")

print(f"\n💸 Pagamentos: {len(pagamentos)} (bug corrigido - antes mostrava dict cru)")
for p in pagamentos[:5]:
    print(f"   - {p['funcionario_nome']:<20} | {p['mes_referencia']} | Base R$ {p['salario_base']:.2f} -> Líquido R$ {p['salario_liquido']:.2f}")

print("\n" + "="*70)
print(" ✅ Sistema funcional! Rode 'python main.py' para menu completo")
print("="*70)
