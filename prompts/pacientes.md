# Tabela pacientes, geração de dados fonte

Objetivo: gerar um arquivo `Pacientes.xls` com dados de pacientes de um sistema de saúde.
Gere registros de 1000 pacientes. Gere dados em formato bruto, sem formatação e sem nenhum tipo de processamento.


## Colunas

ID: numérico, incremental, ordenado
Nome: string
CPF: string
Data de nascimento: string (formato: 2026-05-29)
Idade: numéro
Sexo: string (M ou F)

## Dados inconsistentes

15% dos registros deverá ter inconsistências dentre as seguintes possibilidades:
* Idade e/ou sexo em branco/nulo. Pode ser apenas idade, ou apenas sexo, ou ambos faltando.
* Datas em formato diferente. Exemplo: 29/05/2026
* Registros duplicados de pacientes por CPF. Exemplo: dois registros de pacientes com mesmo CPF.