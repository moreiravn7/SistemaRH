"""
Banco de dados RH - Suporte híbrido: tenta Supabase, fallback para SQLite local
"""
import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "rh.db")

# Tenta importar supabase, mas não quebra se falhar
supabase = None
USE_SUPABASE = False

try:
    from supabase import create_client
    URL = "https://lamiupfzrllaqkcgbluv.supabase.co"
    KEY = "sb_publishable_qWk-x1Ano4lrNEpg99kKzA_xeYUxXUL"
    _client = create_client(URL, KEY)
    # testa conexão rápida (sem DNS pode falhar)
    _client.table("funcionarios").select("*").limit(1).execute()
    supabase = _client
    USE_SUPABASE = True
    print("Conectado ao Supabase.")
except Exception as e:
    # Fallback silencioso para SQLite
    supabase = None
    USE_SUPABASE = False
    # print(f"Usando SQLite local (Supabase indisponível): {e}")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Departamentos
    cur.execute("""
    CREATE TABLE IF NOT EXISTS departamentos (
        id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        descricao TEXT,
        orcamento REAL DEFAULT 0,
        responsavel TEXT
    )
    """)

    # Funcionarios
    cur.execute("""
    CREATE TABLE IF NOT EXISTS funcionarios (
        id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
        id_departamento INTEGER NOT NULL,
        nome TEXT NOT NULL,
        cpf TEXT UNIQUE,
        cargo TEXT NOT NULL,
        salario REAL NOT NULL,
        status TEXT DEFAULT 'Ativo',
        data_admissao TEXT,
        email TEXT,
        telefone TEXT,
        FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento)
    )
    """)

    # Dependentes
    cur.execute("""
    CREATE TABLE IF NOT EXISTS dependentes (
        id_dependente INTEGER PRIMARY KEY AUTOINCREMENT,
        id_funcionario INTEGER NOT NULL,
        nome TEXT NOT NULL,
        parentesco TEXT NOT NULL,
        data_nascimento TEXT,
        FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario) ON DELETE CASCADE
    )
    """)

    # Pagamentos
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pagamentos (
        id_pagamento INTEGER PRIMARY KEY AUTOINCREMENT,
        id_funcionario INTEGER NOT NULL,
        mes_referencia TEXT NOT NULL,
        salario_base REAL NOT NULL,
        descontos REAL DEFAULT 0,
        bonus REAL DEFAULT 0,
        salario_liquido REAL NOT NULL,
        data_pagamento TEXT,
        status TEXT DEFAULT 'Pago',
        FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()

    # Seed se vazio
    seed_if_empty()

def seed_if_empty():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM departamentos")
    if cur.fetchone()[0] > 0:
        conn.close()
        return

    print("Populando banco com dados iniciais (55 funcionários, 8 departamentos)...")

    # Departamentos
    departamentos = [
        (1, "Tecnologia da Informação", "Desenvolvimento, infraestrutura, suporte e segurança", 500000, "Ana Silva"),
        (2, "Recursos Humanos", "Gestão de pessoas, recrutamento e cultura", 150000, "Sandra Regina"),
        (3, "Financeiro", "Controladoria, contas a pagar/receber, planejamento", 300000, "Eduardo Nogueira"),
        (4, "Marketing", "Branding, campanhas, social media e design", 200000, "Priscila Duarte"),
        (5, "Comercial / Vendas", "Vendas, prospecção e relacionamento com clientes", 400000, "Marcos Vinicius"),
        (6, "Operações", "Logística, produção e cadeia de suprimentos", 350000, "Jorge Amado"),
        (7, "Jurídico", "Assessoria legal, contratos e compliance", 180000, "Dra. Helena Morais"),
        (8, "Administrativo", "Rotinas administrativas e facilities", 120000, "Cláudia Regina"),
    ]
    cur.executemany("INSERT INTO departamentos (id_departamento, nome, descricao, orcamento, responsavel) VALUES (?, ?, ?, ?, ?)", departamentos)

    # Funcionários - 55 registros
    funcionarios = [
        # TI - 10
        (1, 1, "Ana Silva", "111.222.333-01", "Diretora de TI", 25000.00, "Ativo", "2019-03-15", "ana.silva@empresa.com", "(11) 99999-0001"),
        (2, 1, "Carlos Mendes", "111.222.333-02", "Gerente de TI", 16000.00, "Ativo", "2020-01-10", "carlos.mendes@empresa.com", "(11) 99999-0002"),
        (3, 1, "Juliana Costa", "111.222.333-03", "Coordenadora de Desenvolvimento", 11000.00, "Ativo", "2020-06-20", "juliana.costa@empresa.com", "(11) 99999-0003"),
        (4, 1, "Rafael Oliveira", "111.222.333-04", "Analista Sr Backend", 9200.00, "Ativo", "2021-02-11", "rafael.oliveira@empresa.com", "(11) 99999-0004"),
        (5, 1, "Fernanda Lima", "111.222.333-05", "Analista Sr Frontend", 8800.00, "Ativo", "2021-04-05", "fernanda.lima@empresa.com", "(11) 99999-0005"),
        (6, 1, "Bruno Santos", "111.222.333-06", "Analista Pleno DevOps", 6800.00, "Ativo", "2021-09-12", "bruno.santos@empresa.com", "(11) 99999-0006"),
        (7, 1, "Patrícia Almeida", "111.222.333-07", "Analista Pleno QA", 6200.00, "Ativo", "2022-03-01", "patricia.almeida@empresa.com", "(11) 99999-0007"),
        (8, 1, "Lucas Pereira", "111.222.333-08", "Analista Jr Suporte", 4200.00, "Ativo", "2023-01-15", "lucas.pereira@empresa.com", "(11) 99999-0008"),
        (9, 1, "Mariana Rocha", "111.222.333-09", "Desenvolvedora Jr", 4500.00, "Ativo", "2023-02-20", "mariana.rocha@empresa.com", "(11) 99999-0009"),
        (10, 1, "Thiago Martins", "111.222.333-10", "Estagiário TI", 1800.00, "Ativo", "2024-02-01", "thiago.martins@empresa.com", "(11) 99999-0010"),

        # RH - 5
        (11, 2, "Sandra Regina", "111.222.333-11", "Gerente de RH", 14500.00, "Ativo", "2019-05-10", "sandra.regina@empresa.com", "(11) 99999-0011"),
        (12, 2, "Roberto Alves", "111.222.333-12", "Coordenador de RH", 9500.00, "Ativo", "2020-08-15", "roberto.alves@empresa.com", "(11) 99999-0012"),
        (13, 2, "Camila Souza", "111.222.333-13", "Analista Sr RH", 7200.00, "Ativo", "2021-05-20", "camila.souza@empresa.com", "(11) 99999-0013"),
        (14, 2, "Diego Ferreira", "111.222.333-14", "Analista Pleno RH", 5200.00, "Ativo", "2022-07-10", "diego.ferreira@empresa.com", "(11) 99999-0014"),
        (15, 2, "Larissa Gomes", "111.222.333-15", "Assistente de RH", 3200.00, "Ativo", "2023-06-01", "larissa.gomes@empresa.com", "(11) 99999-0015"),

        # Financeiro - 7
        (16, 3, "Eduardo Nogueira", "111.222.333-16", "Diretor Financeiro", 27000.00, "Ativo", "2018-11-01", "eduardo.nogueira@empresa.com", "(11) 99999-0016"),
        (17, 3, "Beatriz Andrade", "111.222.333-17", "Gerente Financeiro", 15500.00, "Ativo", "2019-09-20", "beatriz.andrade@empresa.com", "(11) 99999-0017"),
        (18, 3, "Marcelo Dias", "111.222.333-18", "Coordenador Contábil", 10200.00, "Ativo", "2020-04-12", "marcelo.dias@empresa.com", "(11) 99999-0018"),
        (19, 3, "Aline Barbosa", "111.222.333-19", "Analista Sr Financeiro", 7800.00, "Ativo", "2021-03-18", "aline.barbosa@empresa.com", "(11) 99999-0019"),
        (20, 3, "Gustavo Ribeiro", "111.222.333-20", "Analista Pleno Financeiro", 5800.00, "Ativo", "2022-02-10", "gustavo.ribeiro@empresa.com", "(11) 99999-0020"),
        (21, 3, "Vanessa Lopes", "111.222.333-21", "Assistente Financeiro", 3400.00, "Ativo", "2023-03-05", "vanessa.lopes@empresa.com", "(11) 99999-0021"),
        (22, 3, "Felipe Cunha", "111.222.333-22", "Estagiário Financeiro", 1700.00, "Ativo", "2024-03-01", "felipe.cunha@empresa.com", "(11) 99999-0022"),

        # Marketing - 7
        (23, 4, "Priscila Duarte", "111.222.333-23", "Gerente de Marketing", 13800.00, "Ativo", "2020-02-15", "priscila.duarte@empresa.com", "(11) 99999-0023"),
        (24, 4, "Rodrigo Cardoso", "111.222.333-24", "Coordenador de Marketing", 9800.00, "Ativo", "2020-10-10", "rodrigo.cardoso@empresa.com", "(11) 99999-0024"),
        (25, 4, "Letícia Moreira", "111.222.333-25", "Analista Sr Marketing", 7500.00, "Ativo", "2021-07-22", "leticia.moreira@empresa.com", "(11) 99999-0025"),
        (26, 4, "André Luiz", "111.222.333-26", "Analista Pleno Social Media", 5400.00, "Ativo", "2022-05-15", "andre.luiz@empresa.com", "(11) 99999-0026"),
        (27, 4, "Isabela Freitas", "111.222.333-27", "Designer Gráfico Pleno", 5600.00, "Ativo", "2022-08-20", "isabela.freitas@empresa.com", "(11) 99999-0027"),
        (28, 4, "Caio Henrique", "111.222.333-28", "Assistente de Marketing", 3100.00, "Ativo", "2023-04-10", "caio.henrique@empresa.com", "(11) 99999-0028"),
        (29, 4, "Natália Vieira", "111.222.333-29", "Estagiária Marketing", 1650.00, "Ativo", "2024-01-15", "natalia.vieira@empresa.com", "(11) 99999-0029"),

        # Comercial - 10
        (30, 5, "Marcos Vinicius", "111.222.333-30", "Diretor Comercial", 26000.00, "Ativo", "2018-07-01", "marcos.vinicius@empresa.com", "(11) 99999-0030"),
        (31, 5, "Simone Oliveira", "111.222.333-31", "Gerente de Vendas", 14800.00, "Ativo", "2019-07-10", "simone.oliveira@empresa.com", "(11) 99999-0031"),
        (32, 5, "Leandro Teixeira", "111.222.333-32", "Coordenador de Vendas", 10500.00, "Ativo", "2020-11-05", "leandro.teixeira@empresa.com", "(11) 99999-0032"),
        (33, 5, "Juliana Rios", "111.222.333-33", "Vendedor Sr", 6500.00, "Ativo", "2021-08-10", "juliana.rios@empresa.com", "(11) 99999-0033"),
        (34, 5, "Ricardo Neves", "111.222.333-34", "Vendedor Pleno", 4800.00, "Ativo", "2022-01-20", "ricardo.neves@empresa.com", "(11) 99999-0034"),
        (35, 5, "Tatiane Melo", "111.222.333-35", "Vendedora Pleno", 4700.00, "Ativo", "2022-03-15", "tatiane.melo@empresa.com", "(11) 99999-0035"),
        (36, 5, "Paulo Sérgio", "111.222.333-36", "Vendedor Jr", 3200.00, "Ativo", "2023-05-01", "paulo.sergio@empresa.com", "(11) 99999-0036"),
        (37, 5, "Amanda Carvalho", "111.222.333-37", "Assistente Comercial", 3300.00, "Ativo", "2023-07-10", "amanda.carvalho@empresa.com", "(11) 99999-0037"),
        (38, 5, "Jefferson Lima", "111.222.333-38", "SDR Pleno", 4200.00, "Ativo", "2022-09-01", "jefferson.lima@empresa.com", "(11) 99999-0038"),
        (39, 5, "Carla Mendes", "111.222.333-39", "Estagiária Comercial", 1600.00, "Ativo", "2024-02-10", "carla.mendes@empresa.com", "(11) 99999-0039"),

        # Operações - 8
        (40, 6, "Jorge Amado", "111.222.333-40", "Gerente de Operações", 14200.00, "Ativo", "2019-02-20", "jorge.amado@empresa.com", "(11) 99999-0040"),
        (41, 6, "Sueli Aparecida", "111.222.333-41", "Coordenadora de Logística", 9700.00, "Ativo", "2020-03-10", "sueli.aparecida@empresa.com", "(11) 99999-0041"),
        (42, 6, "Wagner Silva", "111.222.333-42", "Analista Sr Operações", 7100.00, "Ativo", "2021-01-25", "wagner.silva@empresa.com", "(11) 99999-0042"),
        (43, 6, "Elaine Cristina", "111.222.333-43", "Analista Pleno Logística", 5300.00, "Ativo", "2022-04-12", "elaine.cristina@empresa.com", "(11) 99999-0043"),
        (44, 6, "Fabio Junior", "111.222.333-44", "Supervisor de Operações", 6200.00, "Ativo", "2021-11-10", "fabio.junior@empresa.com", "(11) 99999-0044"),
        (45, 6, "Renata Prado", "111.222.333-45", "Assistente Operacional", 3000.00, "Ativo", "2023-08-01", "renata.prado@empresa.com", "(11) 99999-0045"),
        (46, 6, "Cleber Santos", "111.222.333-46", "Auxiliar de Operações", 2400.00, "Ativo", "2023-09-15", "cleber.santos@empresa.com", "(11) 99999-0046"),
        (47, 6, "Douglas Costa", "111.222.333-47", "Estagiário Operações", 1550.00, "Ativo", "2024-03-10", "douglas.costa@empresa.com", "(11) 99999-0047"),

        # Jurídico - 4
        (48, 7, "Helena Morais", "111.222.333-48", "Diretora Jurídica", 24000.00, "Ativo", "2018-09-01", "helena.morais@empresa.com", "(11) 99999-0048"),
        (49, 7, "Marcelo Tavares", "111.222.333-49", "Advogado Sr", 11500.00, "Ativo", "2020-05-15", "marcelo.tavares@empresa.com", "(11) 99999-0049"),
        (50, 7, "Lúcia Helena", "111.222.333-50", "Advogada Plena", 8200.00, "Ativo", "2021-06-10", "lucia.helena@empresa.com", "(11) 99999-0050"),
        (51, 7, "Pedro Henrique", "111.222.333-51", "Assistente Jurídico", 3600.00, "Ativo", "2023-02-10", "pedro.henrique@empresa.com", "(11) 99999-0051"),

        # Administrativo - 4
        (52, 8, "Cláudia Regina", "111.222.333-52", "Gerente Administrativo", 12800.00, "Ativo", "2019-10-01", "claudia.regina@empresa.com", "(11) 99999-0052"),
        (53, 8, "José Carlos", "111.222.333-53", "Coordenador Administrativo", 8800.00, "Ativo", "2020-12-01", "jose.carlos@empresa.com", "(11) 99999-0053"),
        (54, 8, "Maria Eduarda", "111.222.333-54", "Assistente Administrativo", 3100.00, "Ativo", "2023-01-10", "maria.eduarda@empresa.com", "(11) 99999-0054"),
        (55, 8, "Antônio Silva", "111.222.333-55", "Auxiliar Administrativo", 2300.00, "Ativo", "2023-10-01", "antonio.silva@empresa.com", "(11) 99999-0055"),
    ]

    cur.executemany("""
        INSERT INTO funcionarios (id_funcionario, id_departamento, nome, cpf, cargo, salario, status, data_admissao, email, telefone)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, funcionarios)

    # Dependentes - 38 registros
    dependentes = [
        (1, "Miguel Silva", "Filho", "2018-05-10"),
        (1, "Sofia Silva", "Filha", "2020-09-12"),
        (2, "Laura Mendes", "Filha", "2015-03-22"),
        (3, "Enzo Costa", "Filho", "2019-11-03"),
        (4, "Valentina Oliveira", "Filha", "2021-01-15"),
        (6, "Theo Santos", "Filho", "2017-07-19"),
        (11, "Helena Regina", "Filha", "2012-04-10"),
        (11, "Bernardo Alves", "Filho", "2014-08-25"),
        (13, "Isabella Souza", "Filha", "2020-02-14"),
        (16, "Davi Nogueira", "Filho", "2010-10-05"),
        (16, "Lara Nogueira", "Filha", "2013-06-18"),
        (17, "Gabriel Andrade", "Filho", "2016-12-01"),
        (18, "Manuela Dias", "Filha", "2019-03-30"),
        (23, "Lucas Duarte", "Filho", "2018-08-08"),
        (24, "Alice Cardoso", "Filha", "2022-04-22"),
        (26, "Yasmin Luiz", "Filha", "2021-07-07"),
        (30, "Arthur Vinicius", "Filho", "2009-09-09"),
        (30, "Beatriz Vinicius", "Filha", "2012-11-11"),
        (30, "Cecília Vinicius", "Filha", "2015-02-02"),
        (31, "Heitor Oliveira", "Filho", "2017-01-20"),
        (33, "Melissa Rios", "Filha", "2020-10-10"),
        (34, "Benício Neves", "Filho", "2019-05-05"),
        (35, "Luna Melo", "Filha", "2021-03-03"),
        (40, "Samuel Amado", "Filho", "2011-06-06"),
        (40, "Sophia Amado", "Filha", "2014-07-07"),
        (41, "Henrique Aparecida", "Filho", "2013-03-13"),
        (42, "Elisa Silva", "Filha", "2018-12-12"),
        (44, "Pietro Junior", "Filho", "2020-06-06"),
        (48, "Olívia Morais", "Filha", "2008-08-08"),
        (48, "Augusto Morais", "Filho", "2010-10-10"),
        (49, "Rebeca Tavares", "Filha", "2019-09-19"),
        (52, "Lucca Regina", "Filho", "2015-05-15"),
        (53, "Maria Flor Carlos", "Filha", "2017-11-11"),
        (3, "Maria Costa", "Esposa", "1988-04-14"),
        (16, "Patricia Nogueira", "Esposa", "1985-02-20"),
        (30, "Fernanda Vinicius", "Esposa", "1986-03-10"),
        (40, "Marcia Amado", "Esposa", "1987-01-30"),
        (48, "Ricardo Morais", "Esposo", "1979-12-12"),
    ]
    # map to id_funcionario
    dep_data = []
    for id_func, nome, parentesco, nasc in dependentes:
        dep_data.append((id_func, nome, parentesco, nasc))

    cur.executemany("INSERT INTO dependentes (id_funcionario, nome, parentesco, data_nascimento) VALUES (?, ?, ?, ?)", dep_data)

    # Pagamentos - último mês para todos
    from datetime import date
    hoje = date.today()
    mes_ref = hoje.strftime("%Y-%m")
    data_pag = hoje.strftime("%Y-%m-%d")

    pagamentos = []
    for f in funcionarios:
        id_func = f[0]
        salario_base = f[5]
        # descontos simulados: 8% INSS + IR variável
        if salario_base <= 3000:
            descontos = salario_base * 0.08
        elif salario_base <= 7000:
            descontos = salario_base * 0.12
        elif salario_base <= 15000:
            descontos = salario_base * 0.18
        else:
            descontos = salario_base * 0.22

        # bonus para alguns
        bonus = 0
        if id_func in [4,5,33,34,35]: # destaques
            bonus = salario_base * 0.10
        if id_func in [1,16,30,48]: # diretores
            bonus = salario_base * 0.15

        liquido = salario_base - descontos + bonus
        pagamentos.append((id_func, mes_ref, salario_base, round(descontos,2), round(bonus,2), round(liquido,2), data_pag, "Pago"))

    cur.executemany("""
        INSERT INTO pagamentos (id_funcionario, mes_referencia, salario_base, descontos, bonus, salario_liquido, data_pagamento, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, pagamentos)

    conn.commit()
    conn.close()
    print("Banco populado com sucesso!")

# Inicializa ao importar
init_db()

# Funções utilitárias para compatibilidade com código antigo
def listar_todos_funcionarios():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT f.*, d.nome as departamento_nome
        FROM funcionarios f
        LEFT JOIN departamentos d ON f.id_departamento = d.id_departamento
        ORDER BY f.id_funcionario
    """)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def listar_todos_departamentos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM departamentos ORDER BY id_departamento")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def listar_todos_dependentes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT dep.*, func.nome as funcionario_nome, func.cargo as funcionario_cargo, dept.nome as departamento_nome
        FROM dependentes dep
        JOIN funcionarios func ON dep.id_funcionario = func.id_funcionario
        LEFT JOIN departamentos dept ON func.id_departamento = dept.id_departamento
        ORDER BY func.nome, dep.nome
    """)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def listar_todos_pagamentos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT pag.*, func.nome as funcionario_nome, func.cargo as funcionario_cargo, dept.nome as departamento_nome
        FROM pagamentos pag
        JOIN funcionarios func ON pag.id_funcionario = func.id_funcionario
        LEFT JOIN departamentos dept ON func.id_departamento = dept.id_departamento
        ORDER BY pag.mes_referencia DESC, func.nome
    """)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows
