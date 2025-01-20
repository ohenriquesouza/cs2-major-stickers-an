import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Caminho da pasta CSV
pasta_csv = "CSVS"
pasta_imgs = "imgs"  # Nova pasta para logos

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

# Obter os preços médios das equipes
df_primeiro = df_primeiro.groupby("Nome")["Preco"].mean().sort_values()
df_ultimo = df_ultimo.groupby("Nome")["Preco"].mean().sort_values()

# Função para adicionar logos ao lado das barras
def adicionar_logos(ax, df, pasta_imgs):
    for i, (nome, preco) in enumerate(df.items()):
        caminho_logo = os.path.join(pasta_imgs, f"{nome}.png")
        if os.path.exists(caminho_logo):
            img = plt.imread(caminho_logo)
            imagebox = OffsetImage(img, zoom=0.35)  # Ajustar o zoom para imagens maiores
            ab = AnnotationBbox(
                imagebox, 
                (preco + (max(df.values) * 0.02), i),  # Adicionar deslocamento para evitar colisão
                frameon=False, 
                xycoords='data', 
                box_alignment=(0, 0.5)  # Alinhar com o final da barra
            )
            ax.add_artist(ab)

# ----- FIGURA 1: Preços no primeiro dia (barras horizontais) com logos -----
fig, ax = plt.subplots(figsize=(12, 8))  # Aumentar tamanho do gráfico
ax.barh(df_primeiro.index, df_primeiro.values, color="royalblue")
adicionar_logos(ax, df_primeiro, pasta_imgs)
plt.xlabel("Preço ($)")
plt.ylabel("Nome da Equipe")
plt.title("Preços no Primeiro Dia")
plt.subplots_adjust(left=0.3)  # Aumentar margem esquerda
plt.tight_layout()
plt.show()

# ----- FIGURA 2: Preços no último dia (barras horizontais) com logos -----
fig, ax = plt.subplots(figsize=(12, 8))  # Aumentar tamanho do gráfico
ax.barh(df_ultimo.index, df_ultimo.values, color="darkorange")
adicionar_logos(ax, df_ultimo, pasta_imgs)
plt.xlabel("Preço ($)")
plt.ylabel("Nome da Equipe")
plt.title("Preços no Último Dia")
plt.subplots_adjust(left=0.3)  # Aumentar margem esquerda
plt.tight_layout()
plt.show()

# Combinar todos os DataFrames em um único para análise temporal
df_todos_dias = pd.concat(dataframes, ignore_index=True)

# Filtrar para incluir apenas as equipes desejadas
df_todos_dias = filtrar_equipes(df_todos_dias)

# Agrupar por Nome da Equipe e Data, e calcular o preço médio
df_todos_dias = df_todos_dias.groupby(["Nome", "Data_Scraping"])["Preco"].mean().reset_index()

# ----- FIGURA 3: Preço dos adesivos ao longo dos dias para todas as equipes -----
fig, ax = plt.subplots(figsize=(14, 8))  # Tamanho maior para acomodar os dados

# Criar um gráfico de linha para cada equipe
for equipe in nomes_equipes:
    dados_equipe = df_todos_dias[df_todos_dias["Nome"] == equipe]
    if not dados_equipe.empty:  # Certificar que existem dados para a equipe
        ax.plot(dados_equipe["Data_Scraping"], dados_equipe["Preco"], label=equipe, marker="o", linewidth=2)

# Configurações do gráfico
plt.xlabel("Data", fontsize=12)
plt.ylabel("Preço ($)", fontsize=12)
plt.title("Variação dos Preços dos Adesivos ao Longo dos Dias", fontsize=14)
plt.legend(title="Equipes", bbox_to_anchor=(1.05, 1), loc="upper left")  # Legenda fora do gráfico
plt.grid(True, linestyle="--", alpha=0.7)
plt.tight_layout()  # Ajustar espaçamentos
plt.show()
