import bronze_ingestao
import prata_transform


def main():
    bronze_ingestao.ingest()
    prata_transform.run()

if __name__ == "__main__":
    main()
