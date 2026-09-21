# Sistema RH - v3.0 Final

Sistema de RH completo, 100% funcional, com **55 funcionários, 8 departamentos, 66 dependentes, 165 pagamentos**.

## ✅ Requisitos Professora - TODOS ATENDIDOS

| Requisito | Status | Prova |
|-----------|--------|-------|
| Tabela com 50+ registros | ✅ | `funcionarios` = 55, `dependentes` = 66, `pagamentos` = 165 |
| Bugs corrigidos | ✅ | Dependentes mostra responsável, departamentos múltiplos |
| Departamentos diferentes | ✅ | 8 departamentos equilibrados |
| Funções diferentes | ✅ | 15+ cargos diferentes |
| Salários realistas | ✅ | R$1.550 a R$27.000 baseado mercado BR |

## 🚀 Como Rodar

### Terminal (menu completo - 16 opções)
```bash
python main.py
```

### Web (dashboard visual - para impressionar professora)
```bash
pip install flask
python app.py
# Acesse http://localhost:5000
```

### Demo rápida (prova 50+)
```bash
python demo.py
```

## 📊 Dados

### Departamentos (8 - antes era 1!)
1. **TI** - 10 pessoas - Prédio A 3º andar - R$500k - Resp: Ana Silva
2. **RH** - 5 pessoas - Prédio A 2º andar - R$150k
3. **Financeiro** - 7 pessoas - Prédio A 4º andar - R$300k
4. **Marketing** - 7 pessoas - Prédio B 1º andar - R$200k
5. **Comercial/Vendas** - 10 pessoas - Prédio B 2º andar - R$400k
6. **Operações** - 8 pessoas - Galpão - R$350k
7. **Jurídico** - 4 pessoas - Prédio A 5º andar - R$180k
8. **Administrativo** - 4 pessoas - Térreo - R$120k

### Funcionários (55)
Distribuição por nível:
- Diretoria: 4 (R$24k-27k)
- Gerência: 8 (R$12.8k-16k)
- Coordenação: 7 (R$8.8k-11k)
- Sênior: 10 (R$6.5k-11.5k)
- Pleno: 12 (R$4.2k-6.8k)
- Júnior/Assistente/Auxiliar: 10 (R$2.3k-4.5k)
- Estágio: 4 (R$1.55k-1.8k)

Exemplos:
- Eduardo Nogueira - Diretor Financeiro - R$27.000
- Ana Silva - Diretora de TI - R$25.000
- Carlos Mendes - Gerente TI - R$16.000
- Rafael Oliveira - Analista Sr Backend - R$9.200
- Lucas Pereira - Analista Jr Suporte - R$4.200
- Thiago Martins - Estagiário TI - R$1.800

### Dependentes (66 - BUG CORRIGIDO!)
Antes: `print(d)` mostrava dict cru
Agora:
```
👤 Ana Silva - Diretora de TI (TI)
   - Miguel Silva (Filho) - 7 anos - CPF: 529.111.222-01
   - Sofia Silva (Filha) - 5 anos
```

Cada dependente mostra:
- Nome + parentesco + idade + CPF
- Nome do funcionário responsável + cargo + departamento

### Pagamentos (165 - 3 meses histórico)
Antes: `print(p)` dict cru
Agora: Base, descontos (8-22% INSS/IR), bônus, líquido, mês, status

## 🐛 Bugs Corrigidos - Detalhes

1. **Dependentes**: JOIN com funcionarios e departamentos, agrupado, idade calculada
2. **Departamentos**: 1 → 8, com localização, orçamento, responsável
3. **Pagamentos**: dict cru → tabela formatada com totais por mês
4. **Funcionários**: sem dept → com dept, email, telefone, nível, status ícone
5. **IDs**: manual (colisão) → AUTOINCREMENT
6. **Supabase offline**: agora fallback SQLite local automático

## 📁 Arquivos

- `banco.py` - Conexão híbrida + seed 55/66/165 registros
- `main.py` - Menu terminal 16 opções (v3.0)
- `app.py` - Dashboard web Flask (novo!)
- `demo.py` - Prova rápida 50+ para professora
- `rh.db` - Banco SQLite 40KB já populado
- `supabase_schema.sql` - DDL para Supabase
- `populate_supabase.py` - Script para popular Supabase quando voltar
- `requirements.txt` - Dependências
- `README.md` + `ALTERACOES.md` - Documentação

## 🎯 Menu Terminal (16 opções)

1. Dashboard
2. Listar departamentos (8)
3. Listar funcionários (55)
4. Listar só ativos
5. Buscar funcionário
6. Criar funcionário
7. Editar funcionário
8. Ativar/Desligar
9. Listar dependentes (66) - BUG FIX
10. Cadastrar dependente
11. Remover dependente
12. Ver folha pagamentos (165)
13. Gerar folha do mês
14. Relatório por departamento
15. Exportar CSV (para entregar para professora)
16. Sair

## 💾 Exportar para Professora

No menu opção 15 exporta:
- `funcionarios_export.csv` (55 linhas)
- `dependentes_export.csv` (66 linhas)
- `pagamentos_export.csv` (165 linhas)

## 🔧 Tecnologias

- Python 3.11
- SQLite3 + Supabase (fallback)
- Flask (web opcional)
- HTML/CSS moderno (dashboard)

## 📸 Screenshots Web

Dashboard mostra:
- Cards: 55 funcionários ✅, 66 dependentes ✅, 165 pagamentos ✅
- Distribuição por departamento com barras
- Top 5 cargos
- Tabelas com salários formatados BRL

---

**v3.0 - Sistema pronto para apresentação!** 🎉
