-- Sistema RH - Schema Supabase / PostgreSQL
-- Execute este script no SQL Editor do Supabase para criar as tabelas
-- Compatível com SQLite também

-- Limpa tabelas existentes (cuidado!)
DROP TABLE IF EXISTS pagamentos;
DROP TABLE IF EXISTS dependentes;
DROP TABLE IF EXISTS funcionarios;
DROP TABLE IF EXISTS departamentos;

-- Departamentos
CREATE TABLE departamentos (
    id_departamento SERIAL PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT,
    orcamento DECIMAL(12,2) DEFAULT 0,
    responsavel TEXT,
    localizacao TEXT DEFAULT 'Matriz - São Paulo'
);

-- Funcionários
CREATE TABLE funcionarios (
    id_funcionario SERIAL PRIMARY KEY,
    id_departamento INTEGER NOT NULL REFERENCES departamentos(id_departamento),
    nome TEXT NOT NULL,
    cpf TEXT UNIQUE,
    cargo TEXT NOT NULL,
    salario DECIMAL(10,2) NOT NULL,
    status TEXT DEFAULT 'Ativo',
    data_admissao DATE,
    email TEXT,
    telefone TEXT,
    nivel TEXT DEFAULT 'Pleno'
);

-- Dependentes
CREATE TABLE dependentes (
    id_dependente SERIAL PRIMARY KEY,
    id_funcionario INTEGER NOT NULL REFERENCES funcionarios(id_funcionario) ON DELETE CASCADE,
    nome TEXT NOT NULL,
    parentesco TEXT NOT NULL,
    data_nascimento DATE,
    cpf TEXT
);

-- Pagamentos
CREATE TABLE pagamentos (
    id_pagamento SERIAL PRIMARY KEY,
    id_funcionario INTEGER NOT NULL REFERENCES funcionarios(id_funcionario) ON DELETE CASCADE,
    mes_referencia TEXT NOT NULL,
    salario_base DECIMAL(10,2) NOT NULL,
    descontos DECIMAL(10,2) DEFAULT 0,
    bonus DECIMAL(10,2) DEFAULT 0,
    salario_liquido DECIMAL(10,2) NOT NULL,
    data_pagamento DATE,
    status TEXT DEFAULT 'Pago'
);

-- Índices para performance
CREATE INDEX idx_funcionarios_departamento ON funcionarios(id_departamento);
CREATE INDEX idx_dependentes_funcionario ON dependentes(id_funcionario);
CREATE INDEX idx_pagamentos_funcionario ON pagamentos(id_funcionario);
CREATE INDEX idx_pagamentos_mes ON pagamentos(mes_referencia);

-- Dados iniciais - 8 Departamentos
INSERT INTO departamentos (id_departamento, nome, descricao, orcamento, responsavel, localizacao) VALUES
(1, 'Tecnologia da Informação', 'Desenvolvimento, infraestrutura, suporte e segurança', 500000, 'Ana Silva', 'Prédio A - 3º andar'),
(2, 'Recursos Humanos', 'Gestão de pessoas, recrutamento e cultura', 150000, 'Sandra Regina', 'Prédio A - 2º andar'),
(3, 'Financeiro', 'Controladoria, contas a pagar/receber, planejamento', 300000, 'Eduardo Nogueira', 'Prédio A - 4º andar'),
(4, 'Marketing', 'Branding, campanhas, social media e design', 200000, 'Priscila Duarte', 'Prédio B - 1º andar'),
(5, 'Comercial / Vendas', 'Vendas, prospecção e relacionamento com clientes', 400000, 'Marcos Vinicius', 'Prédio B - 2º andar'),
(6, 'Operações', 'Logística, produção e cadeia de suprimentos', 350000, 'Jorge Amado', 'Galpão - Operações'),
(7, 'Jurídico', 'Assessoria legal, contratos e compliance', 180000, 'Helena Morais', 'Prédio A - 5º andar'),
(8, 'Administrativo', 'Rotinas administrativas e facilities', 120000, 'Cláudia Regina', 'Prédio A - Térreo');

-- 55 Funcionários (exemplo, lista completa no banco.py)
-- Para popular completo, rode: python -c "import banco"
-- Ou use o script populate_supabase.py

-- Verificação
SELECT 'departamentos' as tabela, COUNT(*) as total FROM departamentos
UNION ALL
SELECT 'funcionarios', COUNT(*) FROM funcionarios
UNION ALL
SELECT 'dependentes', COUNT(*) FROM dependentes
UNION ALL
SELECT 'pagamentos', COUNT(*) FROM pagamentos;
