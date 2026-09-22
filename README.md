# SistemaRH 🏢

Sistema de Recursos Humanos em Python com menu interativo no terminal.
Funciona com **Supabase (remoto)** ou **SQLite local** (automático quando o Supabase não está acessível).

## 📁 Estrutura

| Arquivo | Descrição |
|---|---|
| `main.py` | Menu principal do sistema (listar, cadastrar, atualizar, folha, busca, relatórios) |
| `banco.py` | Conexão com o banco (Supabase remoto ou SQLite local `rh.db`) |
| `seed.py` | Carga inicial: 8 departamentos, 50 funcionários, 36 dependentes e folha de pagamento |
| `requirements.txt` | Dependência opcional (`supabase`) — sem ela, o sistema usa o SQLite local |

## 🚀 Como rodar

```bash
# 1. (Opcional) Instalar o cliente do Supabase para usar o banco remoto
pip install -r requirements.txt

# 2. Popular o banco com os dados iniciais (só precisa rodar 1 vez)
python seed.py

# 3. Abrir o sistema
python main.py
```

> Sem o pacote `supabase` instalado (ou sem internet), o sistema cria e usa
> automaticamente o arquivo `rh.db` (SQLite) na mesma pasta. Nada mais é preciso.

Para apagar tudo e popular novamente:

```bash
python seed.py --force
```

## 📊 Dados da carga inicial (`seed.py`)

- **8 departamentos:** Financeiro, Recursos Humanos, TI, Marketing, Comercial, Operações, Jurídico e Administração
- **50 funcionários** distribuídos por departamento e cargo
- **36 dependentes** vinculados aos responsáveis
- **Folha de pagamento** do mês de referência gerada para os 50 funcionários

## 🧭 Opções do menu

1. Listar funcionários (Quadro Geral)
2. Listar funcionários por departamento
3. Cadastrar novo funcionário
4. Atualizar funcionário (cargo, departamento, salário)
5. Listar dependentes (**com nome do responsável** + departamento)
6. Cadastrar dependente
7. Listar departamentos
8. Cadastrar departamento
9. Ver folha de pagamentos
10. Buscar funcionário por nome
11. Relatório por departamento (quantidade + folha salarial)
0. Sair
