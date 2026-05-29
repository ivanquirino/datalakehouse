from pyspark.sql import SparkSession

def run():
    spark = SparkSession.builder.appName("ReadAnalytics").getOrCreate()

    df = spark.read.parquet("datalake/ouro/metricas.parquet")
    df.createOrReplaceTempView("metricas")
    
    df = spark.read.parquet("datalake/ouro/relatorio_diagnosticos.parquet")
    df.createOrReplaceTempView("relatorio_diagnosticos")
    
    df = spark.sql("SELECT * FROM metricas")
    df.show()

    df = spark.sql("SELECT * FROM relatorio_diagnosticos")
    df.show()

if __name__ == "__main__":
    run()