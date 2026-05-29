import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

files = ["fato_atendimentos", "dim_tempo"]


def load(spark, name):
    df = spark.read.parquet(f"datalake/ouro/{name}/{name}.parquet")
    df.createOrReplaceTempView(name)

    return df


def load_metrics(spark):
    df = spark.read.parquet("datalake/ouro/metricas.parquet")
    df.createOrReplaceTempView("metricas")

    return df


def atendimentos_por_dia(spark):
    df = spark.sql(
        "SELECT to_date(atendimento) atendimento, COUNT(*) num_atendimentos FROM fato_atendimentos WHERE atendimento IS NOT NULL GROUP BY to_date(atendimento)"
    )

    total_dias = df.count()

    total_atendimentos = df.select(
        F.sum("num_atendimentos").alias("total_atendimentos")
    ).first()["total_atendimentos"]

    media_atendimentos_por_dia = total_atendimentos / total_dias

    return media_atendimentos_por_dia

def relatorio_diagnosticos(spark):
    df = spark.sql("SELECT diagnostico, COUNT(*) num_atendimentos FROM fato_atendimentos WHERE diagnostico IS NOT NULL AND diagnostico != 'Normal' GROUP BY diagnostico ORDER BY num_atendimentos DESC")
    df_pandas = df.toPandas()
    df_pandas.to_parquet("datalake/ouro/relatorio_diagnosticos.parquet", index=False)

    df = spark.read.parquet("datalake/ouro/relatorio_diagnosticos.parquet")
    df.createOrReplaceTempView("relatorio_diagnosticos")
    

def analyze(spark):
    media_atendimentos_por_dia = atendimentos_por_dia(spark)

    df = spark.sql(
        "SELECT AVG(duracao_espera) media_tempo_espera FROM dim_tempo WHERE duracao_espera IS NOT NULL"
    )

    media_tempo_espera = df.first()["media_tempo_espera"]

    df = spark.sql(
        "SELECT AVG(duracao_consulta) media_tempo_consulta FROM dim_tempo WHERE duracao_consulta IS NOT NULL"
    )

    media_tempo_consulta = df.first()["media_tempo_consulta"]

    df = spark.sql(
        "SELECT AVG(duracao_total) media_tempo_total FROM dim_tempo WHERE duracao_total IS NOT NULL"
    )

    media_tempo_total = df.first()["media_tempo_total"]

    metrics = [
        ["media_atendimentos_por_dia", media_atendimentos_por_dia],
        ["media_tempo_espera", media_tempo_espera],
        ["media_tempo_consulta", media_tempo_consulta],
        ["media_tempo_total", media_tempo_total],
    ]

    metrics_df = pd.DataFrame(metrics, columns=["metrica", "valor"])
    metrics_df.to_parquet("datalake/ouro/metricas.parquet", index=False)

    load_metrics(spark)
    df_metrics = spark.sql("SELECT * FROM metricas")
    df_metrics.show()

    relatorio_diagnosticos(spark)

    df_relatorio = spark.sql("SELECT * FROM relatorio_diagnosticos")
    df_relatorio.show()


def run():
    spark = SparkSession.builder.appName("Analytics").getOrCreate()
    for name in files:
        load(spark, name)

    analyze(spark)


if __name__ == "__main__":
    run()
