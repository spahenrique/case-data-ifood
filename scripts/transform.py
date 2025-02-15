import pandas as pd
import os
import json
import traceback

# Configuração das pastas
data_folder = "../data/"
parquet_folder = "../parquet_data/"
os.makedirs(parquet_folder, exist_ok=True)

# Função para converter JSON grande em chunks para Parquet
def convert_large_json_to_parquet(json_file, parquet_base_file, chunksize=100000):
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = []
            chunk_num = 1
            for i, line in enumerate(f):
                data.append(json.loads(line))
                if (i + 1) % chunksize == 0:
                    chunk_df = pd.DataFrame(data)
                    chunk_file = f"{parquet_base_file}_chunk_{chunk_num}.parquet"
                    chunk_df.to_parquet(chunk_file, engine="pyarrow")
                    print(f"Chunk {chunk_num} salvo como {chunk_file}.")
                    data = []  # Limpa a lista para o próximo chunk
                    chunk_num += 1
            if data:  # Salva os dados restantes
                chunk_df = pd.DataFrame(data)
                chunk_file = f"{parquet_base_file}_chunk_{chunk_num}.parquet"
                chunk_df.to_parquet(chunk_file, engine="pyarrow")
                print(f"Chunk {chunk_num} salvo como {chunk_file}.")
        print(f"{json_file} processado com sucesso em múltiplos chunks.")
    except Exception as e:
        print(f"Erro ao converter {json_file}: {e}")

# Função para converter arquivos comuns (CSV ou JSON pequenos) para Parquet
def convert_to_parquet(file_name, file_type="csv"):
    file_path = os.path.join(data_folder, file_name)
    parquet_path = os.path.join(parquet_folder, file_name.replace(file_type, "parquet"))

    try:
        if file_type == "json":
            df = pd.read_json(file_path, lines=True)  # Para JSONs pequenos ou linha por linha
        elif file_type == "csv":
            df = pd.read_csv(file_path)

        df.to_parquet(parquet_path, engine="pyarrow")
        print(f"{file_name} convertido para {parquet_path}.")
    except Exception as e:
        print(f"Erro ao converter {file_name}:")
        traceback.print_exc()

# Lista de arquivos e seu tipo
file_list = [
    ("order.json", "json"),
    ("consumer.csv", "csv"),
    ("restaurant.csv", "csv"),
    ("ab_test_ref.csv", "csv")
]

# Processo de conversão
for file_name, file_type in file_list:
    file_path = os.path.join(data_folder, file_name)
    parquet_path = os.path.join(parquet_folder, file_name.replace(file_type, "parquet"))

    if file_name == "order.json":
        convert_large_json_to_parquet(file_path, parquet_path.replace(".parquet", ""))
    else:
        convert_to_parquet(file_name, file_type)

print("Conversão de todos os arquivos finalizada.")
