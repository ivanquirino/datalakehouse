import pandas as pd
import os

BASE_PATH = "datalake/bronze"

# Arquivos fonte (todos .xlsx conforme ambiente)
files = {
    "pacientes": "fontes/Pacientes.xlsx",
    "medicos": "fontes/Medicos.xlsx",
    "consultas": "fontes/Consultas.xlsx",    
    "exames": "fontes/Exames.csv",
}

def ingest():
    for name, file in files.items():
        # Lê o arquivo Excel (funciona tanto para .xls quanto .xlsx)
        if file.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        path = f"{BASE_PATH}/{name}"
        os.makedirs(path, exist_ok=True)

        df.to_parquet(f"{path}/{name}.parquet", index=False)
        print(f"[BRONZE] {name} carregado")

if __name__ == "__main__":
    ingest()