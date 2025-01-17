import os
import pandas as pd
import matplotlib.pyplot as plt

# Caminho da pasta CSV
pasta_csv = "CSVS"

# Listar todos os arquivos CSV na pasta (ordenando para pegar o primeiro e o último)
arquivos_csv = sorted([os.path.join(pasta_csv, arquivo) for arquivo in os.listdir(pasta_csv) if arquivo.endswith(".csv")])

# Lista para armazenar os DataFrames
dataframes = []

# Leitura dos arquivos CSV, ignorando a primeira linha e tratando caracteres especiais
for arquivo in arquivos_csv:
    df = pd.read_csv(arquivo, skiprows=1, encoding='utf-8', delimiter=',')

    # Renomear colunas para garantir compatibilidade
    df.columns = ["Nome", "Preco", "Quantidade", "Tipo", "Data_Scraping"]

    # Limpar valores e converter as colunas necessárias
    df["Quantidade"] = pd.to_numeric(df["Quantidade"], errors="coerce")
    df["Data_Scraping"] = pd.to_datetime(df["Data_Scraping"], errors="coerce")

    # Remover linhas com valores inválidos
    df = df.dropna(subset=["Quantidade", "Data_Scraping"])
    dataframes.append(df)

# Garantir que temos pelo menos dois arquivos para análise
if len(dataframes) < 2:
    raise ValueError("É necessário pelo menos dois arquivos CSV para comparar as quantidades.")

# Selecionar o primeiro e o último DataFrame
df_primeiro = dataframes[0]
df_ultimo = dataframes[-1]

# Lista de equipes a serem consideradas
nomes_equipes = [
    "G2 Esports", "Natus Vincere", "Vitality", "Team Spirit", "MOUZ", "FaZe Clan", "HEROIC", "3DMAX",
    "The MongolZ", "Team Liquid", "GamerLegion", "FURIA", "paiN Gaming", "BIG", "MIBR", "Wildcard"
]

# Filtrar os dados para incluir apenas as equipes
def filtrar_equipes(df):
    df["Nome"] = df["Nome"].str.replace("Adesivo |", "", regex=False).str.split("(").str[0].str.strip()
    return df[df["Nome"].isin(nomes_equipes)]

df_primeiro = filtrar_equipes(df_primeiro)
df_ultimo = filtrar_equipes(df_ultimo)

# Obter as quantidades totais por equipe
quantidades_primeiro = df_primeiro.groupby("Nome")["Quantidade"].sum()
quantidades_ultimo = df_ultimo.groupby("Nome")["Quantidade"].sum()

# Criar um DataFrame combinado para plotagem
df_comparacao = pd.DataFrame({
    "Primeiro Dia": quantidades_primeiro,
    "Último Dia": quantidades_ultimo
}).fillna(0)

# ----- Gráfico de barras duplas -----
fig, ax = plt.subplots(figsize=(12, 8))
bar_width = 0.4
indice = range(len(df_comparacao))

ax.bar(indice, df_comparacao["Primeiro Dia"], bar_width, label="Primeiro Dia", color="royalblue")
ax.bar([i + bar_width for i in indice], df_comparacao["Último Dia"], bar_width, label="Último Dia", color="darkorange")

# Configurações do gráfico
ax.set_xlabel("Equipes")
ax.set_ylabel("Quantidade de Adesivos")
ax.set_title("Comparação de Quantidade de Adesivos: Primeiro Dia x Último Dia")
ax.set_xticks([i + bar_width / 2 for i in indice])
ax.set_xticklabels(df_comparacao.index, rotation=45, ha="right")
ax.legend()

plt.tight_layout()
plt.show()
