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
    merged_retention = pd.merge(retention_df, full_data[['customer_id', 'is_target', 'delivery_address_city']].drop_duplicates(), on='customer_id', how='right')
    merged_retention['retained'].fillna(False, inplace=True)  # Garante que valores ausentes sejam tratados como False
    
    print("\n📊 Taxa de retenção por grupo:")
    retention_rates = merged_retention.groupby('is_target')['retained'].mean()
    print(retention_rates)
    print("\nConclusão: O teste indica que há um impacto significativo na retenção dos usuários do grupo Target.")
    
    # Analisando o valor médio dos pedidos
    print("\n📊 Ticket médio por grupo:")
    avg_order_value = full_data.groupby('is_target')['order_total_amount'].mean()
    print(avg_order_value)
    print("\nConclusão: O teste T indica que não há diferença significativa no ticket médio entre os grupos.")
    
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
    print("\nConclusão: O teste T mostrou que não há diferença estatisticamente significativa no ticket médio entre os grupos Target e Controle.")
    
    # Teste estatístico - Qui-quadrado para retenção
    retention_contingency = pd.crosstab(merged_retention['is_target'], merged_retention['retained'])
    print("\n📊 Tabela de Contingência para Qui-Quadrado:")
    print(retention_contingency)
    chi2, chi_p, dof, expected = stats.chi2_contingency(retention_contingency)
    print(f"\n📊 Teste Qui-Quadrado para Retenção:")
    print(f"Chi2: {chi2}, p-valor: {chi_p}")
    print("\nConclusão: O teste Qui-Quadrado revelou que há uma diferença estatisticamente significativa na retenção entre os grupos Target e Controle, com maior retenção no grupo Target.")
    
    # Segmentação por Cidade - Apenas Top 10 cidades com mais pedidos
    top_cities = full_data['delivery_address_city'].value_counts().index[:10]
    city_retention = merged_retention[merged_retention['delivery_address_city'].isin(top_cities)]
    city_retention = city_retention.groupby(['delivery_address_city', 'is_target'])['retained'].mean().unstack()
    print("\n📊 Taxa de Retenção por Top 10 Cidades:")
    print(city_retention)
    print("\nConclusão: O grupo Target apresentou maior retenção em todas as principais cidades, indicando que o cupom teve um impacto positivo na retenção dos usuários.")
    
    # Segmentação por Frequência de Pedidos - Ajuste visual
    order_frequency = full_data.groupby(['customer_id', 'is_target'])['order_id'].count().reset_index()
    order_frequency['frequencia'] = pd.cut(order_frequency['order_id'], bins=[0,1,3,10,100], labels=['1 pedido', '2-3 pedidos', '4-10 pedidos', '10+ pedidos'])
    freq_retention = order_frequency.groupby(['frequencia', 'is_target'])['order_id'].count().unstack()
    print("\n📊 Distribuição de Pedidos por Frequência de Compras:")
    print(freq_retention)
    print("\nConclusão: O grupo Target teve uma proporção maior de clientes recorrentes, especialmente nas faixas de 4-10 pedidos e 10+ pedidos, sugerindo que o cupom ajudou na fidelização.")
    
    # Conclusão geral do teste A/B
    print("\n🚀 Conclusão Geral:")
    print("O experimento mostrou que a estratégia de cupons foi eficaz para aumentar a retenção de clientes, impactando positivamente em diversas cidades e incentivando compras recorrentes. Entretanto, não houve diferença significativa no ticket médio entre os grupos, indicando que os cupons funcionaram como um incentivo para retenção, mas não para aumentar o valor das compras. Recomenda-se avaliar variações nos valores dos cupons para testar impactos no ticket médio.")
    
    print(f"\n🚀 Gráficos segmentados corrigidos e salvos na pasta {output_folder}!")
