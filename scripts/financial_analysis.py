import pandas as pd
import os

# Configuração da pasta de relatórios
output_folder = "../reports/"
os.makedirs(output_folder, exist_ok=True)

# Definição de parâmetros para análise financeira
custo_por_cupom = 5  # Hipótese de custo médio do cupom por usuário
quantidade_usuarios_target = 2145250
quantidade_usuarios_controle = 1525576

# Taxa de retenção por grupo
taxa_controle = 0.754614
retidos_controle = taxa_controle * quantidade_usuarios_controle

taxa_target = 0.802201
retidos_target = taxa_target * quantidade_usuarios_target

diferenca_retencao = retidos_target - retidos_controle

ticket_medio = 47.90  # Sem diferença estatística entre os grupos

# Receita incremental gerada pela retenção
receita_incremental = diferenca_retencao * ticket_medio

# Custo total da campanha
custo_total = quantidade_usuarios_target * custo_por_cupom

# Retorno sobre investimento (ROI)
roi = (receita_incremental - custo_total) / custo_total

# Resultados
resultado_df = pd.DataFrame({
    "Métrica": ["Usuários Retidos (Controle)", "Usuários Retidos (Target)", 
                "Diferença na Retenção", "Receita Incremental", 
                "Custo Total", "ROI"],
    "Valor": [retidos_controle, retidos_target, diferenca_retencao, 
              receita_incremental, custo_total, roi]
})

# Salvar os resultados
resultado_path = os.path.join(output_folder, "analise_financeira.csv")
resultado_df.to_csv(resultado_path, index=False)

# Exibição dos resultados no terminal
print("\n🚀 Análise Financeira da Campanha de Cupons 🚀")
print("\n🔍 Esta é uma previsão de impacto financeiro baseada nos dados do experimento. "
      "Os valores apresentados são **projeções estimadas** e podem variar conforme fatores externos.")
      
print(f"\n📌 Usuários Retidos no Grupo Controle: {retidos_controle:,.0f}")
print(f"📌 Usuários Retidos no Grupo Target: {retidos_target:,.0f}")
print(f"📌 Diferença na Retenção: {diferenca_retencao:,.0f}")

print("\n💰 Impacto Financeiro 💰")
print(f"🔹 Receita Incremental Estimada: R$ {receita_incremental:,.2f}")
print(f"🔹 Custo Total da Campanha: R$ {custo_total:,.2f}")

# Interpretação do ROI
print("\n📊 Retorno Sobre Investimento (ROI) 📊")
print(f"📈 ROI Estimado da Campanha: {roi:.2%}")

if roi > 0:
    print("\n✅ **Conclusão:** A campanha foi financeiramente viável, pois a projeção indica que a receita adicional "
          "foi superior ao custo dos cupons. Isso sugere que o incentivo pode ser mantido ou ajustado para maximizar resultados.")
else:
    print("\n⚠️ **Conclusão:** A projeção indica um retorno negativo, ou seja, os custos dos cupons superaram os ganhos adicionais. "
          "Seria recomendável testar ajustes na mecânica promocional para otimizar os resultados.")

print("\n📢 **Recomendação:** Para validar essa projeção, o iFood deve considerar:"
      "\n1️⃣ Acompanhamento contínuo do comportamento dos clientes retidos a longo prazo."
      "\n2️⃣ Testes adicionais com diferentes valores de cupons para avaliar impacto no ticket médio."
      "\n3️⃣ Personalização da oferta para diferentes segmentos de clientes, otimizando retenção e receita.")

print(f"\n📂 Resultados salvos em: {resultado_path}")
