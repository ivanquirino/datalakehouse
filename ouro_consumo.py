import pandas as pd
import os

PRATA = "datalake/prata"
OURO = "datalake/ouro"

def load(name):
    return pd.read_parquet(f"{PRATA}/{name}/{name}.parquet")

def save(df, name):
    path = f"{OURO}/{name}"
    os.makedirs(path, exist_ok=True)
    df.to_parquet(f"{path}/{name}.parquet", index=False)

def create_fato_atendimentos():
    pacientes = load("pacientes")
    medicos = load("medicos")
    consultas = load("consultas")
    exames = load("exames")

    consultas['tipo'] = 'consulta'
    exames['tipo'] = 'exame'

    fato = pd.concat([consultas, exames])
    
    print(fato)    

    return fato

def create_dim_cliente():
    return load("clientes")

def create_dim_produto():
    return load("produtos")

def run():
    save(create_fato_atendimentos(), "fato_atendimentos")
    # save(create_dim_cliente(), "dim_cliente")
    # save(create_dim_produto(), "dim_produto")
    print("[OURO] Camada analítica pronta")

if __name__ == "__main__":
    run()