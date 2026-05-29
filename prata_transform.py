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


def transform_pacientes():
    df = load_table("pacientes")
    df = standardize_columns(df)

    df["cpf"] = df["cpf"].str.strip()
    df["cpf"] = df["cpf"].str.replace(".", "")
    df["cpf"] = df["cpf"].str.replace("-", "")

    df["data_nascimento"] = df["data_de_nascimento"]
    df.drop(columns=["data_de_nascimento"], inplace=True)
    df["data_nascimento"] = pd.to_datetime(df["data_nascimento"])

    # df['idade'] = (pd.to_datetime('today') - pd.to_datetime(df['data_nascimento']))

    print(df)

    return df


def transform_pedidos():
    df = load_table("pedidos")
    df = standardize_columns(df)
    # Converte coluna de data (assumindo nome após padronização: 'datapedido' ou 'data_pedido')
    if "datapedido" in df.columns:
        df["datapedido"] = pd.to_datetime(df["datapedido"])
    elif "data_pedido" in df.columns:
        df["data_pedido"] = pd.to_datetime(df["data_pedido"])
    return df


def transform_detalhes():
    df = load_table("detalhes_pedidos")
    df = standardize_columns(df)
    # Calcula venda líquida usando os nomes padronizados
    df["venda_liquida"] = df["quantidade"] * df["precounitario"] * (1 - df["desconto"])
    return df


def transform_produtos():
    df = load_table("produtos")
    df = standardize_columns(df)
    # Garante que a coluna de custo unitário exista com nome padronizado
    # (se original era 'custounitario' ou 'custo_unitario')
    return df


def transform_fornecedores():
    df = load_table("fornecedores")
    df = standardize_columns(df)
    return df


def run():
    save_table(transform_pacientes(), "pacientes")
    # save_table(transform_pedidos(), "pedidos")
    # save_table(transform_detalhes(), "detalhes_pedidos")
    # save_table(transform_produtos(), "produtos")
    # save_table(transform_fornecedores(), "fornecedores")
    print("[PRATA] Transformações concluídas")


if __name__ == "__main__":
    run()
