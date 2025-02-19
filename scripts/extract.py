import requests
import gzip
import tarfile
import os

# Definir caminho correto para a pasta data (no nível do projeto)
output_folder = os.path.join("..", "data")  # Define a pasta "data" fora de "scripts"
os.makedirs(output_folder, exist_ok=True)  # Garante que a pasta "data" exista

# Função para baixar e descompactar arquivos gzip
def download_and_uncompress_gzip(url, output_filename):
    output_path = os.path.join(output_folder, output_filename)  # Caminho correto dentro de "data"
    compressed_file = f"{output_path}.gz"

    response = requests.get(url)
    
    with open(compressed_file, "wb") as file:
        file.write(response.content)
    
    with gzip.open(compressed_file, "rb") as f_in:
        with open(output_path, "wb") as f_out:
            f_out.write(f_in.read())
    
    print(f"{output_filename} baixado e salvo em '{output_folder}/'.")
    os.remove(compressed_file)  # Remove o arquivo .gz

# Função para baixar e descompactar arquivos tar.gz
def download_and_uncompress_tar(url, output_filename):
    tar_file = os.path.join(output_folder, "ab_test_ref.tar.gz")  # Caminho correto

    response = requests.get(url)
    
    with open(tar_file, "wb") as file:
        file.write(response.content)
    
    with tarfile.open(tar_file, "r:gz") as tar:
        tar.extractall(path=output_folder)
    
    print(f"Arquivos extraídos para a pasta '{output_folder}/'.")
    os.remove(tar_file)  # Remove o arquivo .tar.gz

# Baixar e descompactar arquivos na pasta correta (data/)
download_and_uncompress_gzip("https://data-architect-test-source.s3-sa-east-1.amazonaws.com/order.json.gz", "order.json")
download_and_uncompress_gzip("https://data-architect-test-source.s3-sa-east-1.amazonaws.com/consumer.csv.gz", "consumer.csv")
download_and_uncompress_gzip("https://data-architect-test-source.s3-sa-east-1.amazonaws.com/restaurant.csv.gz", "restaurant.csv")
download_and_uncompress_tar("https://data-architect-test-source.s3-sa-east-1.amazonaws.com/ab_test_ref.tar.gz", "ab_test_ref.csv")
