import requests
import gzip
import tarfile
import os
import pandas as pd

# Função para baixar e descompactar arquivos gzip
def download_and_uncompress_gzip(url, output_filename):
    response = requests.get(url)
    compressed_file = f"{output_filename}.gz"
    
    with open(compressed_file, "wb") as file:
        file.write(response.content)
    
    with gzip.open(compressed_file, "rb") as f_in:
        with open(output_filename, "wb") as f_out:
            f_out.write(f_in.read())
    
    print(f"{output_filename} baixado e descompactado com sucesso.")
    os.remove(compressed_file)  # Remove o arquivo .gz

# Função para baixar e descompactar arquivos tar.gz
def download_and_uncompress_tar(url, output_folder):
    response = requests.get(url)
    tar_file = "ab_test_ref.tar.gz"
    
    with open(tar_file, "wb") as file:
        file.write(response.content)
    
    with tarfile.open(tar_file, "r:gz") as tar:
        tar.extractall(path=output_folder)
    
    print(f"Arquivos extraídos para a pasta {output_folder}.")
    os.remove(tar_file)  # Remove o arquivo .tar.gz

# Baixar e descompactar cada arquivo
download_and_uncompress_gzip("https://data-architect-test-source.s3-sa-east-1.amazonaws.com/order.json.gz", "order.json")
download_and_uncompress_gzip("https://data-architect-test-source.s3-sa-east-1.amazonaws.com/consumer.csv.gz", "consumer.csv")
download_and_uncompress_gzip("https://data-architect-test-source.s3-sa-east-1.amazonaws.com/restaurant.csv.gz", "restaurant.csv")
download_and_uncompress_tar("https://data-architect-test-source.s3-sa-east-1.amazonaws.com/ab_test_ref.tar.gz", "ab_test_ref")
