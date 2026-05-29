import bronze_ingestao
import prata_transform
import ouro_consumo
import analytics


def main():
    bronze_ingestao.ingest()
    prata_transform.run()
    ouro_consumo.run()
    analytics.run()
    

if __name__ == "__main__":
    main()
