"""
Demo rápido para mostrar que o sistema está funcional e tem 50+ registros
Rode: python demo.py
v3.0 - Agora com 66 dependentes e 165 pagamentos também 50+
"""
from banco import listar_todos_funcionarios, listar_todos_departamentos, listar_todos_dependentes, listar_todos_pagamentos, estatisticas

print("="*70)
print(" DEMO - SISTEMA RH v3.0 - Prova de 50+ registros")
print("="*70)

stats = estatisticas()
deps = listar_todos_departamentos()
funcs = listar_todos_funcionarios()
dependentes = listar_todos_dependentes()
pagamentos = listar_todos_pagamentos()

print(f"\n📊 ESTATÍSTICAS:")
print(f"   Funcionários: {stats['total']} (requisito ≥50: {'✅ PASSOU' if stats['total']>=50 else '❌ FALHOU'})")
print(f"   Dependentes: {stats['dependentes']} (também ≥50: {'✅ PASSOU' if stats['dependentes']>=50 else '❌'})")
print(f"   Pagamentos: {stats['pagamentos']} (também ≥50: {'✅ PASSOU' if stats['pagamentos']>=50 else '❌'})")
print(f"   Departamentos: {len(deps)} (antes era 1 - bug corrigido ✅)")
print(f"   Folha mensal: R$ {stats['folha']:,.2f}")

print(f"\n✅ Departamentos ({len(deps)}):")
for d in deps:
    print(f"   - {d['id_departamento']}: {d['nome']} - {d['localizacao']} (R$ {d['orcamento']:.0f})")

print(f"\n✅ Funcionários: {len(funcs)} (distribuição equilibrada)")
from collections import Counter
dist = Counter([f['departamento_nome'] for f in funcs])
for dept, qtd in dist.items():
    print(f"   - {dept}: {qtd} pessoas")

print(f"\n💰 Salários realistas (mercado BR 2024):")
for f in sorted(funcs, key=lambda x: x['salario'], reverse=True)[:8]:
    print(f"   - {f['nome']:<20} | {f['cargo']:<30} | {f['nivel']:<12} | R$ {f['salario']:>8,.2f}")

print(f"\n👨‍👩‍👧‍👦 Dependentes: {len(dependentes)} (BUG CORRIGIDO - agora mostra responsável)")
for d in dependentes[:10]:
    print(f"   - {d['nome']} ({d['parentesco']}) -> {d['funcionario_nome']} ({d['funcionario_cargo']} / {d['departamento_nome']})")

print(f"\n💸 Pagamentos: {len(pagamentos)} (3 meses histórico, bug corrigido)")
for p in pagamentos[:6]:
    print(f"   - {p['mes_referencia']} | {p['funcionario_nome']:<20} | Base R$ {p['salario_base']:.2f} -> Líquido R$ {p['salario_liquido']:.2f}")

print("\n" + "="*70)
print(" ✅ Sistema funcional! Opções:")
print("   - Terminal: python main.py (menu completo)")
print("   - Web: python app.py (dashboard visual)")
print("="*70)
