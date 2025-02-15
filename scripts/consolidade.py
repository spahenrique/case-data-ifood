import pandas as pd
import os

# Configuração das pastas
parquet_folder = "../parquet_data/"

# Listar todos os arquivos Parquet que começam com "order_chunk_"
chunk_files = [os.path.join(parquet_folder, f) for f in os.listdir(parquet_folder) if f.startswith("order_chunk_")]

# Verificar se existem arquivos para consolidar
if not chunk_files:
    print("Nenhum chunk encontrado para consolidar.")
else:
    print(f"Encontrados {len(chunk_files)} chunks para consolidar.")

    # Carregar e concatenar todos os chunks em um único DataFrame
    order_df = pd.concat([pd.read_parquet(chunk) for chunk in chunk_files], ignore_index=True)

    # Exibir informações gerais sobre o DataFrame consolidado
    print("Informações do DataFrame consolidado:")
    print(order_df.info())

    # Salvar o DataFrame consolidado em um único arquivo Parquet
    final_file = os.path.join(parquet_folder, "order_final.parquet")
    order_df.to_parquet(final_file, engine="pyarrow")
    print(f"Todos os chunks foram consolidados em {final_file}.")
