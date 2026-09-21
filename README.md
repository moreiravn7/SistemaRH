# Sistema RH - Versão 2.0 Aprimorada

Sistema de Recursos Humanos em Python com SQLite local (fallback automático para Supabase se disponível).

## ✅ Requisitos da Professora Atendidos

- **Tabela com 50+ registros**: `funcionarios` possui **55 funcionários** cadastrados
- Bugs corrigidos e sistema totalmente funcional

## 🏢 Estrutura do Banco

### 1. Departamentos (8 registros)
- Tecnologia da Informação (10 pessoas)
- Recursos Humanos (5)
- Financeiro (7)
- Marketing (7)
- Comercial / Vendas (10)
- Operações (8)
- Jurídico (4)
- Administrativo (4)

Cada departamento tem:
- ID, nome, descrição, orçamento, responsável
- Contagem de funcionários e folha salarial

### 2. Funcionários (55 registros)
Distribuição equilibrada com cargos e salários realistas do mercado brasileiro:

| Nível | Faixa Salarial | Exemplos |
|-------|---------------|----------|
| Estagiário | R$ 1.550 - 1.800 | TI, Financeiro, Marketing |
| Assistente/Auxiliar | R$ 2.300 - 3.400 | Todas as áreas |
| Analista Jr | R$ 3.100 - 4.500 | Suporte, Vendas, Marketing |
| Analista Pleno | R$ 4.700 - 6.800 | DevOps, QA, Financeiro, RH |
| Analista Sr | R$ 7.100 - 9.200 | Backend, Frontend, Contábil |
| Coordenador/Supervisor | R$ 8.800 - 11.000 | Todas as áreas |
| Gerente | R$ 12.800 - 16.000 | TI, RH, Financeiro, etc |
| Diretor | R$ 24.000 - 27.000 | TI, Financeiro, Comercial, Jurídico |

### 3. Dependentes (38 registros)
Agora mostra **de quem é filho** corretamente:
- Nome do dependente + parentesco
- Nome do funcionário responsável + cargo + departamento
- Data de nascimento com cálculo de idade

### 4. Pagamentos (55 registros + geração mensal)
- Salário base, descontos (INSS/IR simulado), bônus, líquido
- Mês de referência, status
- Join com funcionário e departamento

## 🐛 Bugs Corrigidos

### Antes (v1.0 com bugs):
```python
# listar_dependentes() só imprimia dict cru
print("ID:", d)  # bug: mostrava objeto inteiro, não nome do responsável

# listar_pagamentos() igual
print(p)

# Departamento só tinha 1
# Salários irreais
# IDs manuais causavam colisão
# Sem validação
```

### Depois (v2.0 corrigido):
- ✅ `listar_dependentes()` faz JOIN com `funcionarios` e `departamentos`, mostra nome do responsável, cargo, departamento e idade do dependente
- ✅ `listar_pagamentos()` mostra nome, departamento, base vs líquido
- ✅ `listar_funcionarios()` mostra departamento, email, telefone, status com ícone 🟢/🔴
- ✅ 8 departamentos em vez de 1
- ✅ Salários realistas baseados no mercado BR 2024/2025
- ✅ IDs autoincrement (sem colisão)
- ✅ Validação de CPF, salário, departamento existente
- ✅ Status Ativo/Inativo
- ✅ Sistema funciona offline (SQLite) + tenta Supabase

## 🚀 Funcionalidades Novas

### Menu Principal (15 opções):
1. **Dashboard** - Resumo geral com totais, folha, distribuição
2. **Listar departamentos** - Com contagem de funcionários e folha
3. **Listar funcionários** - Todos com departamento
4. **Listar apenas ativos** - Filtro
5. **Buscar funcionário** - Por nome, cargo ou ID
6. **Criar funcionário** - Com validação e criação automática de pagamento
7. **Editar funcionário** - Edição parcial
8. **Ativar/Desligar** - Muda status
9. **Listar dependentes** - Agrupado por responsável (bug corrigido!)
10. **Cadastrar dependente** - Valida funcionário existente
11. **Remover dependente**
12. **Ver folha de pagamentos** - Agrupada por mês com totais
13. **Gerar folha do mês** - Cria folha para todos ativos
14. **Relatório por departamento** - Média, mín, máx, total
15. **Sair**

## 💾 Como Executar

```bash
# Instalar dependências (opcional, para Supabase)
pip install supabase

# Rodar sistema
python main.py

# O banco SQLite rh.db é criado automaticamente na primeira execução
# com 55 funcionários, 8 departamentos, 38 dependentes, 55 pagamentos
```

### Estrutura de Arquivos:
- `banco.py` - Conexão híbrida + init + seed de 55 registros
- `main.py` - Sistema completo com menu
- `rh.db` - Banco SQLite local (gerado automaticamente)
- `README.md` - Esta documentação

## 📊 Exemplo de Saída - Dependentes (bug corrigido)

```
👤 Ana Silva - Diretora de TI (Tecnologia da Informação)
   2 dependente(s):
   - [1] Miguel Silva (Filho) - Nasc: 2018-05-10 - 7 anos
   - [2] Sofia Silva (Filha) - Nasc: 2020-09-12 - 5 anos

👤 Marcos Vinicius - Diretor Comercial (Comercial / Vendas)
   3 dependente(s):
   - [17] Arthur Vinicius (Filho) - Nasc: 2009-09-09 - 16 anos
   ...
```

## 🎯 Distribuição Equilibrada

- TI: 10 pessoas (18%) - 1 diretora, 1 gerente, 1 coord, 4 analistas, 2 jr, 1 estag
- Vendas: 10 pessoas (18%) - foco comercial
- Operações: 8 (14.5%)
- Financeiro: 7 (12.7%)
- Marketing: 7 (12.7%)
- RH: 5 (9%)
- Jurídico: 4 (7.3%)
- Administrativo: 4 (7.3%)

Salários totais: ~R$ 450k/mês em folha (realista para empresa média)

## 🔧 Tecnologias

- Python 3
- SQLite3 (nativo)
- Supabase (opcional, com fallback)
- Tabulação e formatação de moeda BRL

## 👨‍🏫 Para a Professora

Para comprovar os 50+ registros:
```python
from banco import get_connection
conn = get_connection()
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM funcionarios")
print(cur.fetchone()[0])  # 55
```

Ou simplesmente rodar opção 1 (Dashboard) no menu.

---
Desenvolvido como melhoria do projeto original - v2.0
