"""
====================================================================
SEED - Carga inicial do banco de dados do SistemaRH
====================================================================
Popula o banco (SQLite local OU Supabase remoto - usa a mesma
conexao do banco.py automaticamente) com:

  *  8 departamentos
  * 50 funcionarios distribuidos por departamento/cargo
  * 36 dependentes vinculados aos responsaveis
  * 50 lancamentos de folha de pagamento (mes de referencia)

Uso:
    python seed.py            -> popula se o banco estiver vazio
    python seed.py --force    -> apaga tudo e popula novamente
====================================================================
"""

import sys

from banco import supabase

MES_REFERENCIA = "2026-09"
DATA_PAGAMENTO = "2026-09-05"

# ------------------------------------------------------------------
# DADOS
# ------------------------------------------------------------------
DEPARTAMENTOS = [
    {"id_departamento": 1, "nome": "Financeiro", "descricao": "Gestão financeira, contas e contabilidade"},
    {"id_departamento": 2, "nome": "Recursos Humanos", "descricao": "Gestão de pessoas, recrutamento e benefícios"},
    {"id_departamento": 3, "nome": "Tecnologia da Informação", "descricao": "Sistemas, suporte e infraestrutura"},
    {"id_departamento": 4, "nome": "Marketing", "descricao": "Publicidade, redes sociais e branding"},
    {"id_departamento": 5, "nome": "Comercial", "descricao": "Vendas e relacionamento com clientes"},
    {"id_departamento": 6, "nome": "Operações", "descricao": "Logística, estoque e produção"},
    {"id_departamento": 7, "nome": "Jurídico", "descricao": "Contratos e assessoria legal"},
    {"id_departamento": 8, "nome": "Administração", "descricao": "Secretaria, recepção e serviços gerais"},
]

# (id, id_dep, nome, cpf, cargo, salario, status)
_FUNCIONARIOS_TUPLAS = [
    # --- Financeiro (7) ---
    (1, 1, "Carlos Mendes", "111.222.333-01", "Gerente Financeiro", 12000.00, "Ativo"),
    (2, 1, "Patrícia Lima", "111.222.333-02", "Analista Financeiro", 6500.00, "Ativo"),
    (3, 1, "João Pedro Santos", "111.222.333-03", "Analista Financeiro", 6500.00, "Ativo"),
    (4, 1, "Fernanda Costa", "111.222.333-04", "Contador", 7500.00, "Ativo"),
    (5, 1, "Lucas Oliveira", "111.222.333-05", "Assistente Financeiro", 3200.00, "Ativo"),
    (6, 1, "Mariana Souza", "111.222.333-06", "Assistente Financeiro", 3200.00, "Ativo"),
    (7, 1, "Roberto Almeida", "111.222.333-07", "Analista Financeiro", 6600.00, "Ativo"),
    # --- Recursos Humanos (6) ---
    (8, 2, "Ana Beatriz Rocha", "222.333.444-01", "Gerente de RH", 11000.00, "Ativo"),
    (9, 2, "Thiago Martins", "222.333.444-02", "Analista de RH", 5500.00, "Ativo"),
    (10, 2, "Camila Ferreira", "222.333.444-03", "Recrutador", 4200.00, "Ativo"),
    (11, 2, "Juliana Castro", "222.333.444-04", "Analista de RH", 5600.00, "Ativo"),
    (12, 2, "Pedro Henrique Dias", "222.333.444-05", "Recrutador", 4200.00, "Ativo"),
    (13, 2, "Larissa Barbosa", "222.333.444-06", "Recrutador", 4300.00, "Férias"),
    # --- TI (9) ---
    (14, 3, "Rafael Teixeira", "333.444.555-01", "Gerente de TI", 13500.00, "Ativo"),
    (15, 3, "Bruno Carvalho", "333.444.555-02", "Desenvolvedor Sênior", 10500.00, "Ativo"),
    (16, 3, "Diego Nogueira", "333.444.555-03", "Desenvolvedor Sênior", 10800.00, "Ativo"),
    (17, 3, "Aline Pinto", "333.444.555-04", "Desenvolvedor Júnior", 4800.00, "Ativo"),
    (18, 3, "Gustavo Ribeiro", "333.444.555-05", "Desenvolvedor Júnior", 4800.00, "Ativo"),
    (19, 3, "Felipe Moreira", "333.444.555-06", "Desenvolvedor Júnior", 4900.00, "Ativo"),
    (20, 3, "Vanessa Cardoso", "333.444.555-07", "Analista de Suporte", 3900.00, "Ativo"),
    (21, 3, "Eduardo Correia", "333.444.555-08", "Analista de Suporte", 4000.00, "Ativo"),
    (22, 3, "Priscila Moraes", "333.444.555-09", "Analista de Suporte", 3900.00, "Ativo"),
    # --- Marketing (5) ---
    (23, 4, "Beatriz Fonseca", "444.555.666-01", "Gerente de Marketing", 10500.00, "Ativo"),
    (24, 4, "Igor Santana", "444.555.666-02", "Social Media", 4500.00, "Ativo"),
    (25, 4, "Tatiane Reis", "444.555.666-03", "Social Media", 4500.00, "Ativo"),
    (26, 4, "André Luiz Peixoto", "444.555.666-04", "Designer Gráfico", 5200.00, "Ativo"),
    (27, 4, "Renata Vieira", "444.555.666-05", "Designer Gráfico", 5300.00, "Licença"),
    # --- Comercial (8) ---
    (28, 5, "Marcos Vinícius Leal", "555.666.777-01", "Gerente Comercial", 11500.00, "Ativo"),
    (29, 5, "Paula Azevedo", "555.666.777-02", "Vendedor", 3500.00, "Ativo"),
    (30, 5, "Rodrigo Freitas", "555.666.777-03", "Vendedor", 3500.00, "Ativo"),
    (31, 5, "Daniela Pires", "555.666.777-04", "Vendedor", 3600.00, "Ativo"),
    (32, 5, "Leonardo Barros", "555.666.777-05", "Vendedor", 3500.00, "Ativo"),
    (33, 5, "Sandra Ramos", "555.666.777-06", "Representante Comercial", 4800.00, "Ativo"),
    (34, 5, "Otávio Cunha", "555.666.777-07", "Representante Comercial", 4900.00, "Ativo"),
    (35, 5, "Mônica Duarte", "555.666.777-08", "Vendedor", 3500.00, "Ativo"),
    # --- Operações (6) ---
    (36, 6, "Sérgio Tavares", "666.777.888-01", "Gerente de Operações", 10800.00, "Ativo"),
    (37, 6, "Cláudio Nunes", "666.777.888-02", "Almoxarife", 3100.00, "Ativo"),
    (38, 6, "João Batista Melo", "666.777.888-03", "Almoxarife", 3200.00, "Ativo"),
    (39, 6, "Cristina Xavier", "666.777.888-04", "Auxiliar de Logística", 2800.00, "Ativo"),
    (40, 6, "Anderson Prado", "666.777.888-05", "Auxiliar de Logística", 2800.00, "Ativo"),
    (41, 6, "Simone Aguiar", "666.777.888-06", "Auxiliar de Logística", 2900.00, "Férias"),
    # --- Jurídico (3) ---
    (42, 7, "Paulo Sampaio", "777.888.999-01", "Advogado", 9000.00, "Ativo"),
    (43, 7, "Helena Braga", "777.888.999-02", "Advogado", 9200.00, "Ativo"),
    (44, 7, "Natália Queiroz", "777.888.999-03", "Assistente Jurídico", 3800.00, "Ativo"),
    # --- Administração (6) ---
    (45, 8, "Rosana Campos", "888.999.000-01", "Secretária Executiva", 4200.00, "Ativo"),
    (46, 8, "Kátia Silveira", "888.999.000-02", "Auxiliar Administrativo", 2600.00, "Ativo"),
    (47, 8, "Fabiano Lins", "888.999.000-03", "Auxiliar Administrativo", 2600.00, "Ativo"),
    (48, 8, "Débora Farias", "888.999.000-04", "Recepcionista", 2400.00, "Ativo"),
    (49, 8, "Willian Antunes", "888.999.000-05", "Auxiliar Administrativo", 2600.00, "Ativo"),
    (50, 8, "Eliane Vasconcelos", "888.999.000-06", "Recepcionista", 2500.00, "Ativo"),
]

FUNCIONARIOS = [
    {"id_funcionario": i, "id_departamento": d, "nome": n, "cpf": c,
     "cargo": cargo, "salario": s, "status": st}
    for (i, d, n, c, cargo, s, st) in _FUNCIONARIOS_TUPLAS
]

# (id_funcionario, nome, parentesco, data_nascimento)
_DEPENDENTES_TUPLAS = [
    (1, "Maria Mendes", "Cônjuge", "1980-02-14"),
    (1, "Pedro Mendes", "Filho", "2010-06-20"),
    (2, "Lucas Lima", "Filho", "2015-03-11"),
    (4, "José Costa", "Cônjuge", "1980-09-09"),
    (4, "Ana Costa", "Filha", "2012-12-01"),
    (8, "Carlos Rocha", "Cônjuge", "1981-07-19"),
    (8, "Bia Rocha", "Filha", "2011-04-25"),
    (9, "Fernanda Martins", "Cônjuge", "1990-01-05"),
    (11, "Ricardo Castro", "Cônjuge", "1988-03-30"),
    (11, "Gabi Castro", "Filha", "2018-09-14"),
    (13, "Laura Barbosa", "Filha", "2020-05-05"),
    (14, "Sônia Teixeira", "Cônjuge", "1983-11-11"),
    (14, "Vitor Teixeira", "Filho", "2009-08-08"),
    (16, "Paula Nogueira", "Cônjuge", "1991-02-02"),
    (20, "Marcos Cardoso", "Cônjuge", "1989-12-12"),
    (21, "Lúcia Correia", "Cônjuge", "1988-06-06"),
    (21, "Davi Correia", "Filho", "2016-10-10"),
    (23, "Paulo Fonseca", "Cônjuge", "1982-05-05"),
    (26, "Alice Peixoto", "Filha", "2019-01-23"),
    (27, "Fábio Vieira", "Cônjuge", "1988-04-17"),
    (28, "Teresa Leal", "Cônjuge", "1981-03-03"),
    (28, "Caio Leal", "Filho", "2008-07-07"),
    (28, "Elisa Leal", "Filha", "2013-02-28"),
    (29, "Bruno Azevedo", "Cônjuge", "1984-09-19"),
    (31, "Miguel Pires", "Filho", "2017-11-30"),
    (34, "Jorge Cunha", "Filho", "2021-06-15"),
    (36, "Fátima Tavares", "Cônjuge", "1978-08-08"),
    (37, "Rita Nunes", "Cônjuge", "1986-10-10"),
    (38, "Clara Melo", "Filha", "2014-04-04"),
    (41, "Lívia Melo", "Filha", "2022-12-25"),
    (42, "Mauro Sampaio Jr.", "Filho", "2005-05-15"),
    (43, "Otto Braga", "Cônjuge", "1979-01-01"),
    (45, "Hélio Campos", "Cônjuge", "1980-06-06"),
    (47, "Célia Lins", "Cônjuge", "1993-03-03"),
    (49, "Noah Antunes", "Filho", "2020-09-09"),
    (50, "Rui Vasconcelos", "Cônjuge", "1983-12-12"),
]

DEPENDENTES = [
    {"id_funcionario": fid, "nome": n, "parentesco": p, "data_nascimento": dn}
    for (fid, n, p, dn) in _DEPENDENTES_TUPLAS
]


def nome_backend():
    """Diz se estamos gravando no Supabase remoto ou no SQLite local."""
    return "SQLite local (rh.db)" if type(supabase).__name__ == "LocalSupabaseClient" else "Supabase remoto"


def contar(tabela):
    return len(supabase.table(tabela).select("*").execute().data)


def limpar_tudo():
    """Apaga todos os dados (ordem respeita as chaves estrangeiras)."""
    print("Limpando dados existentes...")
    # deleta linha a linha (funciona no SQLite local e no Supabase remoto)
    for tabela, pk in [("pagamentos", "id_pagamento"),
                       ("dependentes", "id_dependente"),
                       ("funcionarios", "id_funcionario"),
                       ("departamentos", "id_departamento")]:
        linhas = supabase.table(tabela).select("*").execute().data
        for linha in linhas:
            supabase.table(tabela).delete().eq(pk, linha[pk]).execute()
        print(f"  - {tabela}: {len(linhas)} registro(s) removido(s)")


def popular():
    print(f"Backend em uso: {nome_backend()}")
    print("Inserindo departamentos...")
    supabase.table("departamentos").insert(DEPARTAMENTOS).execute()

    print("Inserindo funcionarios (50)...")
    supabase.table("funcionarios").insert(FUNCIONARIOS).execute()

    print("Inserindo dependentes (36)...")
    supabase.table("dependentes").insert(DEPENDENTES).execute()

    print(f"Gerando folha de pagamento ({MES_REFERENCIA})...")
    pagamentos = []
    for f in FUNCIONARIOS:
        base = f["salario"]
        descontos = round(base * 0.11, 2)
        beneficios = 500.00
        pagamentos.append({
            "id_funcionario": f["id_funcionario"],
            "mes_referencia": MES_REFERENCIA,
            "salario_base": base,
            "descontos": descontos,
            "beneficios": beneficios,
            "valor_liquido": round(base - descontos + beneficios, 2),
            "data_pagamento": DATA_PAGAMENTO,
        })
    supabase.table("pagamentos").insert(pagamentos).execute()

    print()
    print("=" * 55)
    print("  ✅ CARGA CONCLUÍDA COM SUCESSO!")
    print("=" * 55)
    print(f"  Departamentos : {contar('departamentos')}")
    print(f"  Funcionários  : {contar('funcionarios')}")
    print(f"  Dependentes   : {contar('dependentes')}")
    print(f"  Pagamentos    : {contar('pagamentos')}")
    print("=" * 55)


def main():
    force = "--force" in sys.argv
    print("=" * 55)
    print("  SistemaRH - Carga inicial do banco de dados")
    print("=" * 55)

    existentes = contar("funcionarios")
    if existentes > 0 and not force:
        print(f"⚠️  O banco já possui {existentes} funcionário(s).")
        print("Nada foi alterado. Para apagar tudo e popular novamente, rode:")
        print("    python seed.py --force")
        return

    if force and (existentes > 0 or contar("departamentos") > 0):
        limpar_tudo()
        print()

    popular()


if __name__ == "__main__":
    main()
