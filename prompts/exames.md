# Tabela consultas, geração de dados fonte

Gerar um arquivo `Exames.csv` com dados de exames de pacientes.
Gere dados brutos sem formatação e sem processamento.
Gere registros de 4000 exames.

## Colunas

ID: numérico, incremental, ordenado
Chegada: data e hora em formato ISO padrão
Atendimento: data e hora em formato ISO padrão
Saída: data e hora em formato ISO padrão
Paciente ID: chave estrangeira de Pacientes (entre 1 e 1000)
Médico ID: chave estrangeria de Medicos (entre 1 e 20)
Nome do exame: Texto
Diagnóstico do exame: Texto

## Regras

5% dos registros são de pacientes de desistiram do atendimento e portanto não tem data/hora de atendimento e nem de saída.
