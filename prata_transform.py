import os

import pandas as pd

BRONZE = "datalake/bronze"
PRATA = "datalake/prata"


def load_table(name):
    return pd.read_parquet(f"{BRONZE}/{name}/{name}.parquet")


def save_table(df, name):
    path = f"{PRATA}/{name}"
    os.makedirs(path, exist_ok=True)
    df.to_parquet(f"{path}/{name}.parquet", index=False)


def standardize_columns(df):
    """Converte todos os nomes de colunas para snake_case (minúsculas)"""
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(" ", "_")

    return df


def limpa_cpf(df):
    df["cpf"] = df["cpf"].str.strip()
    df["cpf"] = df["cpf"].str.replace(".", "")
    df["cpf"] = df["cpf"].str.replace("-", "")

    return df


def transform_pacientes():
    df = load_table("pacientes")
    df = standardize_columns(df)

    df["nome"] = df["nome"].str.strip()

    df = limpa_cpf(df)

    df = df.drop_duplicates(subset=["cpf"])

    df["data_nascimento"] = df["data_de_nascimento"]
    df.drop(columns=["data_de_nascimento"], inplace=True)

    df["data_nascimento"] = pd.to_datetime(
        df["data_nascimento"], errors="coerce", format="mixed", dayfirst=True
    )
    df["idade"] = (pd.Timestamp.now() - df["data_nascimento"]).dt.days // 365
    df["idade"] = df["idade"].astype("Int64")

    df["sexo"] = df["sexo"].str.strip()
    df["sexo"] = df["sexo"]

    return df


def transform_medicos():
    df = load_table("medicos")
    df = standardize_columns(df)

    df = limpa_cpf(df)

    df["nome"] = df["nome"].str.strip()
    df["nome"] = df["nome"].str.replace("Dr. ", "")
    df["nome"] = df["nome"].str.replace("Dra. ", "")

    df["data_nascimento"] = pd.to_datetime(df["data_de_nascimento"], errors="coerce")
    df.drop(columns=["data_de_nascimento"], inplace=True)

    return df


def transform_consultas():
    df = load_table("consultas")
    df = standardize_columns(df)

    df["chegada"] = pd.to_datetime(
        df["chegada"], errors="coerce", format="mixed", dayfirst=True
    )
    df["atendimento"] = pd.to_datetime(
        df["atendimento"], errors="coerce", format="mixed", dayfirst=True
    )
    df["saida"] = pd.to_datetime(
        df["saida"], errors="coerce", format="mixed", dayfirst=True
    )

    df.loc[df["atendimento"].isna(), "diagnostico"] = None

    return df


def transform_exames():
    df = load_table("exames")
    df = standardize_columns(df)

    df["chegada"] = pd.to_datetime(
        df["chegada"], errors="coerce", format="mixed", dayfirst=True
    )
    df["atendimento"] = pd.to_datetime(
        df["atendimento"], errors="coerce", format="mixed", dayfirst=True
    )
    df["saida"] = pd.to_datetime(
        df["saida"], errors="coerce", format="mixed", dayfirst=True
    )

    df.loc[df["atendimento"].isna(), "diagnostico_do_exame"] = None

    df["nome_exame"] = df["nome_do_exame"]
    df.drop(columns=["nome_do_exame"], inplace=True)

    df["diagnostico_exame"] = df["diagnostico_do_exame"]
    df.drop(columns=["diagnostico_do_exame"], inplace=True)

    return df


def run():
    save_table(transform_pacientes(), "pacientes")
    save_table(transform_medicos(), "medicos")
    save_table(transform_consultas(), "consultas")
    save_table(transform_exames(), "exames")

    print("[PRATA] Transformações concluídas")


if __name__ == "__main__":
    run()
