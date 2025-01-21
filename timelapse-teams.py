import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Configuração inicial
pasta_csv = "CSVS"
pasta_imgs = "imgs"  # Pasta com as logos das equipes
nomes_equipes = [
    "G2 Esports", "Natus Vincere", "Vitality", "Team Spirit", "MOUZ", "FaZe Clan", "HEROIC", "3DMAX",
    "The MongolZ", "Team Liquid", "GamerLegion", "FURIA", "paiN Gaming", "BIG", "MIBR", "Wildcard"
]

# Carregar arquivos CSV
arquivos_csv = sorted([os.path.join(pasta_csv, arquivo) for arquivo in os.listdir(pasta_csv) if arquivo.endswith(".csv")])
dataframes = []

for arquivo in arquivos_csv:
    df = pd.read_csv(arquivo, skiprows=0, encoding='utf-8', delimiter=',')
    df.columns = ["Nome", "Preco", "Quantidade", "Tipo", "Data_Scraping"]
    df["Preco"] = pd.to_numeric(df["Preco"].astype(str).str.replace(",", ".", regex=False), errors="coerce")
    df["Data_Scraping"] = pd.to_datetime(df["Data_Scraping"], errors="coerce")
    df = df.dropna(subset=["Preco", "Data_Scraping"])
    dataframes.append(df)

# Combinar os DataFrames
df_todos_dias = pd.concat(dataframes, ignore_index=True)

# Filtrar para considerar apenas os adesivos dourados
def filtrar_equipes_douradas(df):
    df["Nome"] = df["Nome"].str.replace("Adesivo |", "", regex=False).str.strip()
    df["Tipo"] = df["Nome"].str.extract(r"\((.*?)\)")[0]
    df["Nome"] = df["Nome"].str.split("(").str[0].str.strip()
    return df[(df["Nome"].isin(nomes_equipes)) & (df["Tipo"] == "Dourado")]

df_todos_dias = filtrar_equipes_douradas(df_todos_dias)

# Agrupar por Nome da Equipe e Data, e calcular o preço médio
df_todos_dias = df_todos_dias.groupby(["Nome", "Data_Scraping"])["Preco"].mean().reset_index()

# Obter todas as datas únicas e inicializar preços como 0
datas = sorted(df_todos_dias["Data_Scraping"].unique())
precos_inicial = {nome: 0 for nome in nomes_equipes}

# Preparar os dados para animação
data_animacao = []
for data in datas:
    precos_dia = precos_inicial.copy()
    df_dia = df_todos_dias[df_todos_dias["Data_Scraping"] == data]
    for _, row in df_dia.iterrows():
        precos_dia[row["Nome"]] = row["Preco"]
    precos_ordenados = dict(sorted(precos_dia.items(), key=lambda item: item[1], reverse=True))
    data_animacao.append((data, precos_ordenados))

# Função para adicionar logos
def adicionar_logos(ax, nomes, valores):
    for i, nome in enumerate(nomes):
        caminho_logo = os.path.join(pasta_imgs, f"{nome}.png")
        if os.path.exists(caminho_logo):
            img = plt.imread(caminho_logo)
            imagebox = OffsetImage(img, zoom=0.35)
            ab = AnnotationBbox(imagebox, (valores[i], i), frameon=False, xycoords="data", box_alignment=(0, 0.5))
            ax.add_artist(ab)

# Configuração da animação
fig, ax = plt.subplots(figsize=(12, 8))
barra = ax.barh(nomes_equipes, [0] * len(nomes_equipes), color="royalblue")

# Função de atualização
def atualizar(frame):
    data, precos = data_animacao[frame]
    ax.clear()
    nomes_ordenados = list(precos.keys())[::-1]  # Reverter ordem para ranking correto
    valores_ordenados = list(precos.values())[::-1]
    ax.barh(nomes_ordenados, valores_ordenados, color="royalblue")
    adicionar_logos(ax, nomes_ordenados, valores_ordenados)
    ax.set_xlim(0, max(valores_ordenados) * 1.1)
    ax.set_title(f"Ranking dos Preços dos Adesivos Dourados - {data.strftime('%Y-%m-%d')}", fontsize=16)
    ax.set_xlabel("Preço ($)", fontsize=12)
    ax.set_ylabel("Nome da Equipe", fontsize=12)
    ax.grid(axis="x", linestyle="--", alpha=0.7)

# Criar a animação
anim = FuncAnimation(fig, atualizar, frames=len(data_animacao), interval=800, repeat=False)

# Salvar ou exibir a animação
from matplotlib.animation import PillowWriter
anim.save("animacao_ranking_precos_dourados.gif", writer=PillowWriter(fps=2))

plt.show()
