import pandas as pd
import os

# Configuração das pastas
data_folder = "../parquet_data/"

# Função para carregar e explorar os dados
def load_and_explore(file_name):
    file_path = os.path.join(data_folder, file_name)
    try:
        df = pd.read_parquet(file_path)
        print(f"\n Análise inicial de {file_name}")
        print("Informações gerais:")
        print(df.info())
        print("\nEstatísticas descritivas:")
        print(df.describe(include='all'))
        print("\nVisualização das primeiras linhas:")
        print(df.head())
        return df
    except Exception as e:
        print(f"Erro ao carregar {file_name}: {e}")
        return None

# Carregar e explorar cada base
order_df = load_and_explore("order_final.parquet")
consumer_df = load_and_explore("consumer.parquet")
restaurant_df = load_and_explore("restaurant.parquet")
ab_test_ref_df = load_and_explore("ab_test_ref.parquet")

# Verificação de chaves e preparação para relacionar as bases
print("\n Verificando chaves para relacionar as bases.")
if order_df is not None and consumer_df is not None:
    print("\nVerificando chaves comuns entre order_df e consumer_df...")
    common_keys_order_consumer = set(order_df.columns).intersection(set(consumer_df.columns))
    print(f"Chaves comuns: {common_keys_order_consumer}")

if order_df is not None and restaurant_df is not None:
    print("\nVerificando chaves comuns entre order_df e restaurant_df...")
    common_keys_order_restaurant = set(order_df.columns).intersection(set(restaurant_df.columns))
    print(f"Chaves comuns: {common_keys_order_restaurant}")

if ab_test_ref_df is not None and consumer_df is not None:
    print("\nVerificando chaves comuns entre ab_test_ref_df e consumer_df...")
    common_keys_abtest_consumer = set(ab_test_ref_df.columns).intersection(set(consumer_df.columns))
    print(f"Chaves comuns: {common_keys_abtest_consumer}")

print("\n Preparação para relacionar as bases concluída.")

# Junção das bases
print("\n🚀 Iniciando a junção das bases.")
try:
    if order_df is not None and consumer_df is not None:
        merged_order_consumer = pd.merge(order_df, consumer_df, on="customer_id", how="left")
        print("Junção entre order_df e consumer_df concluída.")
    
    if merged_order_consumer is not None and restaurant_df is not None:
        consolidated_df = pd.merge(merged_order_consumer, restaurant_df, left_on="merchant_id", right_on="id", how="left")
        print("Junção entre merged_order_consumer e restaurant_df concluída.")
    
    if consolidated_df is not None and ab_test_ref_df is not None:
        consolidated_df = pd.merge(consolidated_df, ab_test_ref_df, on="customer_id", how="left")
        print("Junção com ab_test_ref_df concluída.")
    
    # Salvar uma amostra de 1000 linhas em CSV
    sample_df = consolidated_df.sample(1000, random_state=42)
    sample_df.to_csv("../parquet_data/consolidated_sample.csv", index=False)
    print("\n🚀 Amostra de 1000 linhas salva como 'consolidated_sample.csv' na pasta 'parquet_data/'.")
except Exception as e:
    print(f"Erro durante a junção das bases: {e}")
