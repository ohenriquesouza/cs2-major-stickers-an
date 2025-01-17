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
    df["Preco"] = pd.to_numeric(df["Preco"].astype(str).str.replace(",", ".", regex=False), errors="coerce")
    df["Quantidade"] = pd.to_numeric(df["Quantidade"], errors="coerce")
    df["Data_Scraping"] = pd.to_datetime(df["Data_Scraping"], errors="coerce")

    # Remover linhas com valores inválidos
    df = df.dropna(subset=["Preco", "Quantidade", "Data_Scraping"])
    dataframes.append(df)

# Garantir que temos pelo menos dois arquivos para análise
if len(dataframes) < 2:
    raise ValueError("É necessário pelo menos dois arquivos CSV para comparar os preços ao longo do tempo.")

# Selecionar o primeiro e o último DataFrame
df_primeiro = dataframes[0]
df_ultimo = dataframes[-1]

# Lista de nomes a serem ignorados (equipes e cápsulas)
nomes_a_ignorar = [
    "G2 Esports", "Natus Vincere", "Vitality", "Team Spirit", "MOUZ", "FaZe Clan", "HEROIC", "3DMAX",
    "The MongolZ", "Team Liquid", "GamerLegion", "FURIA", "paiN Gaming", "BIG", "MIBR", "Wildcard",
    "cápsula"
]

# Filtrar os dados para incluir apenas os jogadores com adesivos dourados
def filtrar_jogadores_dourados(df):
    df["Nome"] = df["Nome"].str.replace("Adesivo |", "", regex=False).str.strip()
    df["Tipo"] = df["Nome"].str.extract(r"\((.*?)\)")[0]
    df["Nome"] = df["Nome"].str.split("(").str[0].str.strip()
    return df[(~df["Nome"].isin(nomes_a_ignorar)) & (df["Tipo"] == "Dourado")]

df_primeiro = filtrar_jogadores_dourados(df_primeiro)
df_ultimo = filtrar_jogadores_dourados(df_ultimo)

# Obter os 10 jogadores mais relevantes (maiores preços)
df_primeiro_top10 = df_primeiro.groupby("Nome")["Preco"].mean().nlargest(10)
df_ultimo_top10 = df_ultimo.groupby("Nome")["Preco"].mean().nlargest(10)

# ----- FIGURA 1: Top 10 jogadores dourados no primeiro dia (barras horizontais) -----
plt.figure(figsize=(10, 8))
plt.barh(df_primeiro_top10.index, df_primeiro_top10.values, color="gold")
plt.xlabel("Preço (R$)")
plt.ylabel("Nome do Jogador")
plt.title("Top 10 Jogadores Dourados - Primeiro Dia")
plt.tight_layout()
plt.show()

# ----- FIGURA 2: Top 10 jogadores dourados no último dia (barras horizontais) -----
plt.figure(figsize=(10, 8))
plt.barh(df_ultimo_top10.index, df_ultimo_top10.values, color="darkgoldenrod")
plt.xlabel("Preço (R$)")
plt.ylabel("Nome do Jogador")
plt.title("Top 10 Jogadores Dourados - Último Dia")
plt.tight_layout()
plt.show()


## Normal stickers
# import os
# import pandas as pd
# import matplotlib.pyplot as plt

# # Caminho da pasta CSV
# pasta_csv = "CSVS"

# # Listar todos os arquivos CSV na pasta (ordenando para pegar o primeiro e o último)
# arquivos_csv = sorted([os.path.join(pasta_csv, arquivo) for arquivo in os.listdir(pasta_csv) if arquivo.endswith(".csv")])

# # Lista para armazenar os DataFrames
# dataframes = []

# # Leitura dos arquivos CSV, ignorando a primeira linha e tratando caracteres especiais
# for arquivo in arquivos_csv:
#     df = pd.read_csv(arquivo, skiprows=1, encoding='utf-8', delimiter=',')

#     # Renomear colunas para garantir compatibilidade
#     df.columns = ["Nome", "Preco", "Quantidade", "Tipo", "Data_Scraping"]

#     # Limpar valores e converter as colunas necessárias
#     df["Preco"] = pd.to_numeric(df["Preco"].astype(str).str.replace(",", ".", regex=False), errors="coerce")
#     df["Quantidade"] = pd.to_numeric(df["Quantidade"], errors="coerce")
#     df["Data_Scraping"] = pd.to_datetime(df["Data_Scraping"], errors="coerce")

#     # Remover linhas com valores inválidos
#     df = df.dropna(subset=["Preco", "Quantidade", "Data_Scraping"])
#     dataframes.append(df)

# # Garantir que temos pelo menos dois arquivos para análise
# if len(dataframes) < 2:
#     raise ValueError("É necessário pelo menos dois arquivos CSV para comparar os preços ao longo do tempo.")

# # Selecionar o primeiro e o último DataFrame
# df_primeiro = dataframes[0]
# df_ultimo = dataframes[-1]

# # Lista de nomes a serem ignorados (equipes e cápsulas)
# nomes_a_ignorar = [
#     "G2 Esports", "Natus Vincere", "Team Vitality", "Team Spirit", "MOUZ", "FaZe Clan", "HEROIC", "3DMAX",
#     "The MongolZ", "Team Liquid", "GamerLegion", "FURIA Esports", "paiN Gaming", "BIG", "MIBR", "Wildcard",
#     "cápsula"
# ]

# # Filtrar os dados para incluir apenas os jogadores
# def filtrar_jogadores(df):
#     df["Nome"] = df["Nome"].str.replace("Adesivo |", "", regex=False).str.split("(").str[0].str.strip()
#     return df[~df["Nome"].isin(nomes_a_ignorar)]

# df_primeiro = filtrar_jogadores(df_primeiro)
# df_ultimo = filtrar_jogadores(df_ultimo)

# # Obter os 10 jogadores mais relevantes (maiores preços)
# df_primeiro_top10 = df_primeiro.groupby("Nome")["Preco"].mean().nlargest(10)
# df_ultimo_top10 = df_ultimo.groupby("Nome")["Preco"].mean().nlargest(10)

# # ----- FIGURA 1: Top 10 jogadores no primeiro dia (barras horizontais) -----
# plt.figure(figsize=(10, 8))
# plt.barh(df_primeiro_top10.index, df_primeiro_top10.values, color="seagreen")
# plt.xlabel("Preço (R$)")
# plt.ylabel("Nome do Jogador")
# plt.title("Top 10 Jogadores - Primeiro Dia")
# plt.tight_layout()
# plt.show()

# # ----- FIGURA 2: Top 10 jogadores no último dia (barras horizontais) -----
# plt.figure(figsize=(10, 8))
# plt.barh(df_ultimo_top10.index, df_ultimo_top10.values, color="steelblue")
# plt.xlabel("Preço (R$)")
# plt.ylabel("Nome do Jogador")
# plt.title("Top 10 Jogadores - Último Dia")
# plt.tight_layout()
# plt.show()