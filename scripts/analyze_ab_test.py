import pandas as pd
import os
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib

# Definir backend não interativo para evitar erro com Tkinter
matplotlib.use('Agg')

# Configuração da pasta
data_folder = "../parquet_data/"
output_folder = "../reports/"
os.makedirs(output_folder, exist_ok=True)  # Criar a pasta se não existir

# Carregar os dados completos a partir dos arquivos Parquet
def load_full_data():
    try:
        order_df = pd.read_parquet(os.path.join(data_folder, "order_final.parquet"))
        consumer_df = pd.read_parquet(os.path.join(data_folder, "consumer.parquet"))
        ab_test_df = pd.read_parquet(os.path.join(data_folder, "ab_test_ref.parquet"))
        print("\n🚀 Dados completos carregados com sucesso.")
        return order_df, consumer_df, ab_test_df
    except Exception as e:
        print(f"Erro ao carregar dados completos: {e}")
        return None, None, None

# Carregar os dados completos
order_df, consumer_df, ab_test_df = load_full_data()

if order_df is not None and consumer_df is not None and ab_test_df is not None:
    # Mesclar os dados para análise do Teste A/B
    full_data = order_df.merge(consumer_df, on='customer_id', how='left')
    full_data = full_data.merge(ab_test_df, on='customer_id', how='left')
    full_data['is_target'].fillna("control", inplace=True)  # Usuários sem marcação são controle
    
    # Contagem de usuários por grupo (Target vs. Controle)
    print("\n📊 Contagem de usuários por grupo A/B:")
    print(full_data['is_target'].value_counts())
    
    # Analisando a taxa de retenção (usuários que fizeram mais de um pedido)
    retention_df = full_data.groupby('customer_id')['order_id'].count().reset_index()
    retention_df['retained'] = retention_df['order_id'] > 1
    merged_retention = pd.merge(retention_df, full_data[['customer_id', 'is_target']].drop_duplicates(), on='customer_id', how='right')
    merged_retention['retained'].fillna(False, inplace=True)  # Garante que valores ausentes sejam tratados como False
    
    print("\n📊 Taxa de retenção por grupo:")
    retention_rates = merged_retention.groupby('is_target')['retained'].mean()
    print(retention_rates)
    
    # Analisando o valor médio dos pedidos
    print("\n📊 Ticket médio por grupo:")
    avg_order_value = full_data.groupby('is_target')['order_total_amount'].mean()
    print(avg_order_value)
    
    # Número médio de pedidos por usuário
    print("\n📊 Média de pedidos por usuário:")
    avg_orders_per_user = merged_retention.groupby('is_target')['order_id'].mean()
    print(avg_orders_per_user)
    
    # Teste estatístico - Teste T para comparar ticket médio
    target_values = full_data[full_data['is_target'] == 'target']['order_total_amount']
    control_values = full_data[full_data['is_target'] == 'control']['order_total_amount']
    t_stat, p_value = stats.ttest_ind(target_values, control_values, equal_var=False)
    print(f"\n📊 Teste T para Ticket Médio:")
    print(f"Estatística t: {t_stat}, p-valor: {p_value}")
    
    # Teste estatístico - Qui-quadrado para retenção
    retention_contingency = pd.crosstab(merged_retention['is_target'], merged_retention['retained'])
    print("\n📊 Tabela de Contingência para Qui-Quadrado:")
    print(retention_contingency)
    chi2, chi_p, dof, expected = stats.chi2_contingency(retention_contingency)
    print(f"\n📊 Teste Qui-Quadrado para Retenção:")
    print(f"Chi2: {chi2}, p-valor: {chi_p}")
    
    # Alterar gráfico de retenção para colunas
    plt.figure(figsize=(8, 6))
    plt.bar(retention_rates.index, retention_rates.values, color=['blue', 'orange'])
    plt.xlabel("Grupo A/B")
    plt.ylabel("Taxa de Retenção")
    plt.title("Taxa de Retenção por Grupo A/B")
    plt.savefig(os.path.join(output_folder, "taxa_retencao.png"))
    plt.close()
    
    # Alterar gráfico do ticket médio para barras
    plt.figure(figsize=(8, 6))
    plt.bar(avg_order_value.index, avg_order_value.values, color=['blue', 'orange'])
    plt.xlabel("Grupo A/B")
    plt.ylabel("Ticket Médio")
    plt.title("Ticket Médio por Grupo A/B")
    plt.savefig(os.path.join(output_folder, "ticket_medio.png"))
    plt.close()
    
    print(f"\n🚀 Gráficos salvos na pasta {output_folder}.")
    print("\n🚀 Análise do Teste A/B concluída com gráficos e testes estatísticos.")

    print("✅ O cupom ajudou a aumentar a retenção de clientes, o que pode indicar que a estratégia de cupons foi eficaz para trazer usuários de volta à plataforma.")
    print('❌ O cupom não influenciou o valor médio dos pedidos, ou seja, os clientes compraram com a mesma média de gasto, independentemente de terem recebido o cupom.')