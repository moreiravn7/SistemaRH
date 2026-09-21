"""
Banco de dados RH - Suporte híbrido: tenta Supabase, fallback para SQLite local
v3.0 - 55 funcionários, 8 departamentos, 65 dependentes, 165 pagamentos
"""
import os
import sqlite3
from datetime import datetime, date

DB_PATH = os.path.join(os.path.dirname(__file__), "rh.db")

# Tenta importar supabase, mas não quebra se falhar
supabase = None
USE_SUPABASE = False

try:
    from supabase import create_client
    URL = "https://lamiupfzrllaqkcgbluv.supabase.co"
    KEY = "sb_publishable_qWk-x1Ano4lrNEpg99kKzA_xeYUxXUL"
    _client = create_client(URL, KEY)
    _client.table("funcionarios").select("*").limit(1).execute()
    supabase = _client
    USE_SUPABASE = True
    print("Conectado ao Supabase.")
except Exception:
    supabase = None
    USE_SUPABASE = False

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS departamentos (
        id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        descricao TEXT,
        orcamento REAL DEFAULT 0,
        responsavel TEXT,
        localizacao TEXT DEFAULT 'Matriz - São Paulo'
    )
    """)

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
        nivel TEXT DEFAULT 'Pleno',
        FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS dependentes (
        id_dependente INTEGER PRIMARY KEY AUTOINCREMENT,
        id_funcionario INTEGER NOT NULL,
        nome TEXT NOT NULL,
        parentesco TEXT NOT NULL,
        data_nascimento TEXT,
        cpf TEXT,
        FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario) ON DELETE CASCADE
    )
    """)

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
    seed_if_empty()

def seed_if_empty():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM departamentos")
    if cur.fetchone()[0] > 0:
        conn.close()
        return

    print("Populando banco com dados iniciais (55 funcionários, 8 departamentos, 65+ dependentes, 165 pagamentos)...")

    departamentos = [
        (1, "Tecnologia da Informação", "Desenvolvimento, infraestrutura, suporte e segurança", 500000, "Ana Silva", "Prédio A - 3º andar"),
        (2, "Recursos Humanos", "Gestão de pessoas, recrutamento e cultura", 150000, "Sandra Regina", "Prédio A - 2º andar"),
        (3, "Financeiro", "Controladoria, contas a pagar/receber, planejamento", 300000, "Eduardo Nogueira", "Prédio A - 4º andar"),
        (4, "Marketing", "Branding, campanhas, social media e design", 200000, "Priscila Duarte", "Prédio B - 1º andar"),
        (5, "Comercial / Vendas", "Vendas, prospecção e relacionamento com clientes", 400000, "Marcos Vinicius", "Prédio B - 2º andar"),
        (6, "Operações", "Logística, produção e cadeia de suprimentos", 350000, "Jorge Amado", "Galpão - Operações"),
        (7, "Jurídico", "Assessoria legal, contratos e compliance", 180000, "Helena Morais", "Prédio A - 5º andar"),
        (8, "Administrativo", "Rotinas administrativas e facilities", 120000, "Cláudia Regina", "Prédio A - Térreo"),
    ]
    cur.executemany("INSERT INTO departamentos (id_departamento, nome, descricao, orcamento, responsavel, localizacao) VALUES (?, ?, ?, ?, ?, ?)", departamentos)

    funcionarios = [
        (1, 1, "Ana Silva", "111.222.333-01", "Diretora de TI", 25000.00, "Ativo", "2019-03-15", "ana.silva@empresa.com", "(11) 99999-0001", "Diretoria"),
        (2, 1, "Carlos Mendes", "111.222.333-02", "Gerente de TI", 16000.00, "Ativo", "2020-01-10", "carlos.mendes@empresa.com", "(11) 99999-0002", "Gerência"),
        (3, 1, "Juliana Costa", "111.222.333-03", "Coordenadora de Desenvolvimento", 11000.00, "Ativo", "2020-06-20", "juliana.costa@empresa.com", "(11) 99999-0003", "Coordenação"),
        (4, 1, "Rafael Oliveira", "111.222.333-04", "Analista Sr Backend", 9200.00, "Ativo", "2021-02-11", "rafael.oliveira@empresa.com", "(11) 99999-0004", "Sênior"),
        (5, 1, "Fernanda Lima", "111.222.333-05", "Analista Sr Frontend", 8800.00, "Ativo", "2021-04-05", "fernanda.lima@empresa.com", "(11) 99999-0005", "Sênior"),
        (6, 1, "Bruno Santos", "111.222.333-06", "Analista Pleno DevOps", 6800.00, "Ativo", "2021-09-12", "bruno.santos@empresa.com", "(11) 99999-0006", "Pleno"),
        (7, 1, "Patrícia Almeida", "111.222.333-07", "Analista Pleno QA", 6200.00, "Ativo", "2022-03-01", "patricia.almeida@empresa.com", "(11) 99999-0007", "Pleno"),
        (8, 1, "Lucas Pereira", "111.222.333-08", "Analista Jr Suporte", 4200.00, "Ativo", "2023-01-15", "lucas.pereira@empresa.com", "(11) 99999-0008", "Júnior"),
        (9, 1, "Mariana Rocha", "111.222.333-09", "Desenvolvedora Jr", 4500.00, "Ativo", "2023-02-20", "mariana.rocha@empresa.com", "(11) 99999-0009", "Júnior"),
        (10, 1, "Thiago Martins", "111.222.333-10", "Estagiário TI", 1800.00, "Ativo", "2024-02-01", "thiago.martins@empresa.com", "(11) 99999-0010", "Estágio"),

        (11, 2, "Sandra Regina", "111.222.333-11", "Gerente de RH", 14500.00, "Ativo", "2019-05-10", "sandra.regina@empresa.com", "(11) 99999-0011", "Gerência"),
        (12, 2, "Roberto Alves", "111.222.333-12", "Coordenador de RH", 9500.00, "Ativo", "2020-08-15", "roberto.alves@empresa.com", "(11) 99999-0012", "Coordenação"),
        (13, 2, "Camila Souza", "111.222.333-13", "Analista Sr RH", 7200.00, "Ativo", "2021-05-20", "camila.souza@empresa.com", "(11) 99999-0013", "Sênior"),
        (14, 2, "Diego Ferreira", "111.222.333-14", "Analista Pleno RH", 5200.00, "Ativo", "2022-07-10", "diego.ferreira@empresa.com", "(11) 99999-0014", "Pleno"),
        (15, 2, "Larissa Gomes", "111.222.333-15", "Assistente de RH", 3200.00, "Ativo", "2023-06-01", "larissa.gomes@empresa.com", "(11) 99999-0015", "Assistente"),

        (16, 3, "Eduardo Nogueira", "111.222.333-16", "Diretor Financeiro", 27000.00, "Ativo", "2018-11-01", "eduardo.nogueira@empresa.com", "(11) 99999-0016", "Diretoria"),
        (17, 3, "Beatriz Andrade", "111.222.333-17", "Gerente Financeiro", 15500.00, "Ativo", "2019-09-20", "beatriz.andrade@empresa.com", "(11) 99999-0017", "Gerência"),
        (18, 3, "Marcelo Dias", "111.222.333-18", "Coordenador Contábil", 10200.00, "Ativo", "2020-04-12", "marcelo.dias@empresa.com", "(11) 99999-0018", "Coordenação"),
        (19, 3, "Aline Barbosa", "111.222.333-19", "Analista Sr Financeiro", 7800.00, "Ativo", "2021-03-18", "aline.barbosa@empresa.com", "(11) 99999-0019", "Sênior"),
        (20, 3, "Gustavo Ribeiro", "111.222.333-20", "Analista Pleno Financeiro", 5800.00, "Ativo", "2022-02-10", "gustavo.ribeiro@empresa.com", "(11) 99999-0020", "Pleno"),
        (21, 3, "Vanessa Lopes", "111.222.333-21", "Assistente Financeiro", 3400.00, "Ativo", "2023-03-05", "vanessa.lopes@empresa.com", "(11) 99999-0021", "Assistente"),
        (22, 3, "Felipe Cunha", "111.222.333-22", "Estagiário Financeiro", 1700.00, "Ativo", "2024-03-01", "felipe.cunha@empresa.com", "(11) 99999-0022", "Estágio"),

        (23, 4, "Priscila Duarte", "111.222.333-23", "Gerente de Marketing", 13800.00, "Ativo", "2020-02-15", "priscila.duarte@empresa.com", "(11) 99999-0023", "Gerência"),
        (24, 4, "Rodrigo Cardoso", "111.222.333-24", "Coordenador de Marketing", 9800.00, "Ativo", "2020-10-10", "rodrigo.cardoso@empresa.com", "(11) 99999-0024", "Coordenação"),
        (25, 4, "Letícia Moreira", "111.222.333-25", "Analista Sr Marketing", 7500.00, "Ativo", "2021-07-22", "leticia.moreira@empresa.com", "(11) 99999-0025", "Sênior"),
        (26, 4, "André Luiz", "111.222.333-26", "Analista Pleno Social Media", 5400.00, "Ativo", "2022-05-15", "andre.luiz@empresa.com", "(11) 99999-0026", "Pleno"),
        (27, 4, "Isabela Freitas", "111.222.333-27", "Designer Gráfico Pleno", 5600.00, "Ativo", "2022-08-20", "isabela.freitas@empresa.com", "(11) 99999-0027", "Pleno"),
        (28, 4, "Caio Henrique", "111.222.333-28", "Assistente de Marketing", 3100.00, "Ativo", "2023-04-10", "caio.henrique@empresa.com", "(11) 99999-0028", "Assistente"),
        (29, 4, "Natália Vieira", "111.222.333-29", "Estagiária Marketing", 1650.00, "Ativo", "2024-01-15", "natalia.vieira@empresa.com", "(11) 99999-0029", "Estágio"),

        (30, 5, "Marcos Vinicius", "111.222.333-30", "Diretor Comercial", 26000.00, "Ativo", "2018-07-01", "marcos.vinicius@empresa.com", "(11) 99999-0030", "Diretoria"),
        (31, 5, "Simone Oliveira", "111.222.333-31", "Gerente de Vendas", 14800.00, "Ativo", "2019-07-10", "simone.oliveira@empresa.com", "(11) 99999-0031", "Gerência"),
        (32, 5, "Leandro Teixeira", "111.222.333-32", "Coordenador de Vendas", 10500.00, "Ativo", "2020-11-05", "leandro.teixeira@empresa.com", "(11) 99999-0032", "Coordenação"),
        (33, 5, "Juliana Rios", "111.222.333-33", "Vendedor Sr", 6500.00, "Ativo", "2021-08-10", "juliana.rios@empresa.com", "(11) 99999-0033", "Sênior"),
        (34, 5, "Ricardo Neves", "111.222.333-34", "Vendedor Pleno", 4800.00, "Ativo", "2022-01-20", "ricardo.neves@empresa.com", "(11) 99999-0034", "Pleno"),
        (35, 5, "Tatiane Melo", "111.222.333-35", "Vendedora Pleno", 4700.00, "Ativo", "2022-03-15", "tatiane.melo@empresa.com", "(11) 99999-0035", "Pleno"),
        (36, 5, "Paulo Sérgio", "111.222.333-36", "Vendedor Jr", 3200.00, "Ativo", "2023-05-01", "paulo.sergio@empresa.com", "(11) 99999-0036", "Júnior"),
        (37, 5, "Amanda Carvalho", "111.222.333-37", "Assistente Comercial", 3300.00, "Ativo", "2023-07-10", "amanda.carvalho@empresa.com", "(11) 99999-0037", "Assistente"),
        (38, 5, "Jefferson Lima", "111.222.333-38", "SDR Pleno", 4200.00, "Ativo", "2022-09-01", "jefferson.lima@empresa.com", "(11) 99999-0038", "Pleno"),
        (39, 5, "Carla Mendes", "111.222.333-39", "Estagiária Comercial", 1600.00, "Ativo", "2024-02-10", "carla.mendes@empresa.com", "(11) 99999-0039", "Estágio"),

        (40, 6, "Jorge Amado", "111.222.333-40", "Gerente de Operações", 14200.00, "Ativo", "2019-02-20", "jorge.amado@empresa.com", "(11) 99999-0040", "Gerência"),
        (41, 6, "Sueli Aparecida", "111.222.333-41", "Coordenadora de Logística", 9700.00, "Ativo", "2020-03-10", "sueli.aparecida@empresa.com", "(11) 99999-0041", "Coordenação"),
        (42, 6, "Wagner Silva", "111.222.333-42", "Analista Sr Operações", 7100.00, "Ativo", "2021-01-25", "wagner.silva@empresa.com", "(11) 99999-0042", "Sênior"),
        (43, 6, "Elaine Cristina", "111.222.333-43", "Analista Pleno Logística", 5300.00, "Ativo", "2022-04-12", "elaine.cristina@empresa.com", "(11) 99999-0043", "Pleno"),
        (44, 6, "Fabio Junior", "111.222.333-44", "Supervisor de Operações", 6200.00, "Ativo", "2021-11-10", "fabio.junior@empresa.com", "(11) 99999-0044", "Coordenação"),
        (45, 6, "Renata Prado", "111.222.333-45", "Assistente Operacional", 3000.00, "Ativo", "2023-08-01", "renata.prado@empresa.com", "(11) 99999-0045", "Assistente"),
        (46, 6, "Cleber Santos", "111.222.333-46", "Auxiliar de Operações", 2400.00, "Ativo", "2023-09-15", "cleber.santos@empresa.com", "(11) 99999-0046", "Auxiliar"),
        (47, 6, "Douglas Costa", "111.222.333-47", "Estagiário Operações", 1550.00, "Ativo", "2024-03-10", "douglas.costa@empresa.com", "(11) 99999-0047", "Estágio"),

        (48, 7, "Helena Morais", "111.222.333-48", "Diretora Jurídica", 24000.00, "Ativo", "2018-09-01", "helena.morais@empresa.com", "(11) 99999-0048", "Diretoria"),
        (49, 7, "Marcelo Tavares", "111.222.333-49", "Advogado Sr", 11500.00, "Ativo", "2020-05-15", "marcelo.tavares@empresa.com", "(11) 99999-0049", "Sênior"),
        (50, 7, "Lúcia Helena", "111.222.333-50", "Advogada Plena", 8200.00, "Ativo", "2021-06-10", "lucia.helena@empresa.com", "(11) 99999-0050", "Pleno"),
        (51, 7, "Pedro Henrique", "111.222.333-51", "Assistente Jurídico", 3600.00, "Ativo", "2023-02-10", "pedro.henrique@empresa.com", "(11) 99999-0051", "Assistente"),

        (52, 8, "Cláudia Regina", "111.222.333-52", "Gerente Administrativo", 12800.00, "Ativo", "2019-10-01", "claudia.regina@empresa.com", "(11) 99999-0052", "Gerência"),
        (53, 8, "José Carlos", "111.222.333-53", "Coordenador Administrativo", 8800.00, "Ativo", "2020-12-01", "jose.carlos@empresa.com", "(11) 99999-0053", "Coordenação"),
        (54, 8, "Maria Eduarda", "111.222.333-54", "Assistente Administrativo", 3100.00, "Ativo", "2023-01-10", "maria.eduarda@empresa.com", "(11) 99999-0054", "Assistente"),
        (55, 8, "Antônio Silva", "111.222.333-55", "Auxiliar Administrativo", 2300.00, "Ativo", "2023-10-01", "antonio.silva@empresa.com", "(11) 99999-0055", "Auxiliar"),
    ]

    cur.executemany("""
        INSERT INTO funcionarios (id_funcionario, id_departamento, nome, cpf, cargo, salario, status, data_admissao, email, telefone, nivel)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, funcionarios)

    # Dependentes - 65 registros (agora >50 também)
    dependentes = [
        (1, "Miguel Silva", "Filho", "2018-05-10", "529.111.222-01"),
        (1, "Sofia Silva", "Filha", "2020-09-12", "529.111.222-02"),
        (2, "Laura Mendes", "Filha", "2015-03-22", "529.111.222-03"),
        (2, "Pedro Mendes", "Filho", "2017-08-14", "529.111.222-04"),
        (3, "Enzo Costa", "Filho", "2019-11-03", "529.111.222-05"),
        (3, "Maria Costa", "Esposa", "1988-04-14", "529.111.222-06"),
        (4, "Valentina Oliveira", "Filha", "2021-01-15", "529.111.222-07"),
        (4, "Júlia Oliveira", "Esposa", "1990-06-20", "529.111.222-08"),
        (5, "Lorenzo Lima", "Filho", "2022-03-10", "529.111.222-09"),
        (6, "Theo Santos", "Filho", "2017-07-19", "529.111.222-10"),
        (6, "Alice Santos", "Filha", "2019-02-25", "529.111.222-11"),
        (7, "Helena Almeida", "Filha", "2020-11-11", "529.111.222-12"),
        (8, "Davi Pereira", "Filho", "2023-04-05", "529.111.222-13"),
        (11, "Helena Regina", "Filha", "2012-04-10", "529.111.222-14"),
        (11, "Bernardo Alves", "Filho", "2014-08-25", "529.111.222-15"),
        (11, "Carlos Regina", "Esposo", "1975-03-15", "529.111.222-16"),
        (12, "Isabela Alves", "Filha", "2018-09-30", "529.111.222-17"),
        (13, "Isabella Souza", "Filha", "2020-02-14", "529.111.222-18"),
        (13, "Lucas Souza", "Filho", "2022-07-19", "529.111.222-19"),
        (14, "Matheus Ferreira", "Filho", "2021-12-12", "529.111.222-20"),
        (16, "Davi Nogueira", "Filho", "2010-10-05", "529.111.222-21"),
        (16, "Lara Nogueira", "Filha", "2013-06-18", "529.111.222-22"),
        (16, "Patricia Nogueira", "Esposa", "1985-02-20", "529.111.222-23"),
        (17, "Gabriel Andrade", "Filho", "2016-12-01", "529.111.222-24"),
        (17, "Sophia Andrade", "Filha", "2019-05-22", "529.111.222-25"),
        (18, "Manuela Dias", "Filha", "2019-03-30", "529.111.222-26"),
        (18, "Rafaela Dias", "Esposa", "1987-11-11", "529.111.222-27"),
        (19, "Felipe Barbosa", "Filho", "2020-08-08", "529.111.222-28"),
        (20, "Luiz Ribeiro", "Filho", "2022-01-01", "529.111.222-29"),
        (21, "Beatriz Lopes", "Filha", "2023-02-14", "529.111.222-30"),
        (23, "Lucas Duarte", "Filho", "2018-08-08", "529.111.222-31"),
        (23, "Fernanda Duarte", "Esposa", "1989-09-09", "529.111.222-32"),
        (24, "Alice Cardoso", "Filha", "2022-04-22", "529.111.222-33"),
        (25, "Heitor Moreira", "Filho", "2021-06-06", "529.111.222-34"),
        (26, "Yasmin Luiz", "Filha", "2021-07-07", "529.111.222-35"),
        (26, "Camila Luiz", "Esposa", "1992-02-02", "529.111.222-36"),
        (27, "Oliver Freitas", "Filho", "2023-03-03", "529.111.222-37"),
        (30, "Arthur Vinicius", "Filho", "2009-09-09", "529.111.222-38"),
        (30, "Beatriz Vinicius", "Filha", "2012-11-11", "529.111.222-39"),
        (30, "Cecília Vinicius", "Filha", "2015-02-02", "529.111.222-40"),
        (30, "Fernanda Vinicius", "Esposa", "1986-03-10", "529.111.222-41"),
        (31, "Heitor Oliveira", "Filho", "2017-01-20", "529.111.222-42"),
        (31, "Lívia Oliveira", "Filha", "2020-02-02", "529.111.222-43"),
        (32, "Gustavo Teixeira", "Filho", "2016-04-04", "529.111.222-44"),
        (33, "Melissa Rios", "Filha", "2020-10-10", "529.111.222-45"),
        (34, "Benício Neves", "Filho", "2019-05-05", "529.111.222-46"),
        (34, "Clara Neves", "Esposa", "1991-01-01", "529.111.222-47"),
        (35, "Luna Melo", "Filha", "2021-03-03", "529.111.222-48"),
        (36, "Noah Sérgio", "Filho", "2022-11-11", "529.111.222-49"),
        (38, "Elisa Lima", "Filha", "2023-05-05", "529.111.222-50"),
        (40, "Samuel Amado", "Filho", "2011-06-06", "529.111.222-51"),
        (40, "Sophia Amado", "Filha", "2014-07-07", "529.111.222-52"),
        (40, "Marcia Amado", "Esposa", "1987-01-30", "529.111.222-53"),
        (41, "Henrique Aparecida", "Filho", "2013-03-13", "529.111.222-54"),
        (41, "Laura Aparecida", "Filha", "2015-09-09", "529.111.222-55"),
        (42, "Elisa Silva", "Filha", "2018-12-12", "529.111.222-56"),
        (42, "Mateus Silva", "Filho", "2020-06-06", "529.111.222-57"),
        (43, "Isadora Cristina", "Filha", "2021-09-09", "529.111.222-58"),
        (44, "Pietro Junior", "Filho", "2020-06-06", "529.111.222-59"),
        (44, "Bianca Junior", "Esposa", "1993-03-03", "529.111.222-60"),
        (48, "Olívia Morais", "Filha", "2008-08-08", "529.111.222-61"),
        (48, "Augusto Morais", "Filho", "2010-10-10", "529.111.222-62"),
        (48, "Ricardo Morais", "Esposo", "1979-12-12", "529.111.222-63"),
        (49, "Rebeca Tavares", "Filha", "2019-09-19", "529.111.222-64"),
        (52, "Lucca Regina", "Filho", "2015-05-15", "529.111.222-65"),
        (53, "Maria Flor Carlos", "Filha", "2017-11-11", "529.111.222-66"),
    ]

    cur.executemany("INSERT INTO dependentes (id_funcionario, nome, parentesco, data_nascimento, cpf) VALUES (?, ?, ?, ?, ?)", dependentes)

    # Pagamentos - 3 meses de histórico para cada funcionário = 165 registros
    import calendar
    # fallback sem dateutil
    try:
        from dateutil.relativedelta import relativedelta
        has_dateutil = True
    except:
        has_dateutil = False

    hoje = date.today()
    meses = []
    for i in range(3):
        if has_dateutil:
            d = hoje - relativedelta(months=i)
        else:
            # simples: subtrai meses manualmente
            month = hoje.month - i
            year = hoje.year
            while month <= 0:
                month += 12
                year -= 1
            d = date(year, month, 1)
        meses.append(d.strftime("%Y-%m"))

    pagamentos = []
    for mes_ref in meses:
        year, month = map(int, mes_ref.split("-"))
        last_day = calendar.monthrange(year, month)[1]
        data_pag = f"{mes_ref}-{last_day:02d}"

        for f in funcionarios:
            id_func = f[0]
            salario_base = f[5]

            if salario_base <= 3000:
                descontos = salario_base * 0.08
            elif salario_base <= 7000:
                descontos = salario_base * 0.12
            elif salario_base <= 15000:
                descontos = salario_base * 0.18
            else:
                descontos = salario_base * 0.22

            bonus = 0
            if id_func in [4,5,33,34,35]:
                bonus = salario_base * 0.10
            if id_func in [1,16,30,48]:
                bonus = salario_base * 0.15
            # bonus extra aleatório para simular variação
            if mes_ref == meses[0] and id_func % 7 == 0:
                bonus += 500

            liquido = salario_base - descontos + bonus
            pagamentos.append((id_func, mes_ref, salario_base, round(descontos,2), round(bonus,2), round(liquido,2), data_pag, "Pago"))

    cur.executemany("""
        INSERT INTO pagamentos (id_funcionario, mes_referencia, salario_base, descontos, bonus, salario_liquido, data_pagamento, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, pagamentos)

    conn.commit()
    conn.close()
    print(f"Banco populado: {len(funcionarios)} funcionários, {len(departamentos)} departamentos, {len(dependentes)} dependentes, {len(pagamentos)} pagamentos!")

init_db()

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

def estatisticas():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as total FROM funcionarios")
    total = cur.fetchone()["total"]
    cur.execute("SELECT COUNT(*) as total FROM funcionarios WHERE status='Ativo'")
    ativos = cur.fetchone()["total"]
    cur.execute("SELECT COUNT(*) as total FROM dependentes")
    dep = cur.fetchone()["total"]
    cur.execute("SELECT COUNT(*) as total FROM pagamentos")
    pag = cur.fetchone()["total"]
    cur.execute("SELECT SUM(salario) as folha FROM funcionarios WHERE status='Ativo'")
    folha = cur.fetchone()["folha"]
    conn.close()
    return {"total": total, "ativos": ativos, "dependentes": dep, "pagamentos": pag, "folha": folha}
