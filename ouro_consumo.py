import os

import pandas as pd

PRATA = "datalake/prata"
OURO = "datalake/ouro"


def load(name):
    return pd.read_parquet(f"{PRATA}/{name}/{name}.parquet")


def save(df, name):
    path = f"{OURO}/{name}"
    os.makedirs(path, exist_ok=True)
    df.to_parquet(f"{path}/{name}.parquet", index=False)


def create_fato_atendimentos():
    consultas = load("consultas")
    exames = load("exames")

    consultas["tipo"] = "consulta"
    exames["tipo"] = "exame"

    fato = pd.concat([consultas, exames], ignore_index=True)
    fato["id"] = range(len(fato))

    return fato


def create_dim_paciente():
    return load("pacientes")


def create_dim_medico():
    return load("medicos")


def create_dim_tempo(fato):
    df = pd.DataFrame()

    df["atendimento_id"] = fato["id"]
    df["duracao_espera"] = (fato["atendimento"] - fato["chegada"]) / pd.Timedelta(
        minutes=1
    )
    df["duracao_consulta"] = (fato["saida"] - fato["atendimento"]) / pd.Timedelta(
        minutes=1
    )
    df["duracao_total"] = (fato["saida"] - fato["chegada"]) / pd.Timedelta(minutes=1)

    return df


def run():
    fato_atendimentos = create_fato_atendimentos()

    save(fato_atendimentos, "fato_atendimentos")
    save(create_dim_tempo(fato_atendimentos), "dim_tempo")
    save(create_dim_paciente(), "dim_paciente")
    save(create_dim_medico(), "dim_medico")

    print("[OURO] Camada analítica pronta")


if __name__ == "__main__":
    run()
