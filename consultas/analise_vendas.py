# Análise de Vendas Globais - Departamento de Vendas
# Equipe: Francisco Viana, Murilo Maciel, Felipe Oliveira
# Requisitos: Python 3 + pandas  (pip install pandas)

import textwrap
from pathlib import Path

import pandas as pd

pd.options.display.float_format = "{:,.2f}".format

DADOS = Path(__file__).resolve().parent.parent / "dados"

vendas = pd.read_csv(DADOS / "Vendas-Globais.csv").dropna(how="all")
vendas["Data"] = pd.to_datetime(vendas["Data"], format="%m/%d/%Y")
vendas["Ano"] = vendas["Data"].dt.year

vendedores = pd.read_csv(DADOS / "vendedores.csv")
fornecedores = pd.read_csv(DADOS / "fornecedores.csv")
transportadoras = pd.read_csv(DADOS / "transportadoras.csv")

vendas = (vendas
          .merge(vendedores, on="VendedorID")
          .merge(fornecedores, on="FornecedorID")
          .merge(transportadoras, on="TransportadoraID"))


def titulo(n, texto):
    prefixo = f"{n}. "
    corpo = textwrap.fill(texto, width=78, initial_indent=prefixo,
                          subsequent_indent=" " * len(prefixo))
    print(f"\n{'=' * 78}\n{corpo}\n{'=' * 78}")


titulo(1, "Quem são os meus 10 maiores clientes, em termos de vendas ($)?")
print(vendas.groupby("ClienteNome")["Vendas"].sum()
      .sort_values(ascending=False).head(10))

titulo(2, "Quais os três maiores países, em termos de vendas ($)?")
print(vendas.groupby("ClientePaís")["Vendas"].sum()
      .sort_values(ascending=False).head(3))

titulo(3, "Quais as categorias de produtos que geram maior faturamento (vendas $) no Brasil?")
brasil = vendas[vendas["ClientePaís"] == "Brazil"]
print(brasil.groupby("CategoriaNome")["Vendas"].sum()
      .sort_values(ascending=False))

titulo(4, "Qual a despesa com frete envolvendo cada transportadora?")
print(vendas.groupby("TransportadoraNome")["Frete"].sum()
      .sort_values(ascending=False))

titulo(5, "Quais são os principais clientes (vendas $) do segmento “Calçados Masculinos” (Men´s Footwear) na Alemanha?")
calcados_de = vendas[(vendas["CategoriaNome"] == "Men´s Footwear") &
                     (vendas["ClientePaís"] == "Germany")]
print(calcados_de.groupby("ClienteNome")["Vendas"].sum()
      .sort_values(ascending=False))

titulo(6, "Quais os vendedores que mais dão descontos nos Estados Unidos?")
eua = vendas[vendas["ClientePaís"] == "USA"]
print(eua.groupby("VendedorNome")["Desconto"].sum()
      .sort_values(ascending=False))

titulo(7, "Quais os fornecedores que dão a maior margem de lucro ($) no segmento de “Vestuário Feminino” (Womens wear)?")
feminino = vendas[vendas["CategoriaNome"] == "Womens wear"]
print(feminino.groupby("FornecedorNome")["Margem Bruta"].sum()
      .sort_values(ascending=False).head(10))

titulo(8, "Quanto que foi vendido ($) no ano de 2009? Analisando as vendas anuais entre 2009 e 2012, podemos concluir que o faturamento vem crescendo, se mantendo estável ou decaindo?")
anual = vendas.groupby("Ano")["Vendas"].sum()
print(anual)
print(f"\nVendido em 2009: $ {anual[2009]:,.2f}")
print("Variação ano a ano (%):")
print(anual.pct_change().mul(100).round(1))

titulo(9, "Quais são os principais clientes (vendas $) do segmento “Calçados Masculinos” (Men´s Footwear) no ano de 2013. Para quais cidades houve venda e quanto?")
calcados_2013 = vendas[(vendas["CategoriaNome"] == "Men´s Footwear") &
                       (vendas["Ano"] == 2013)]
if calcados_2013.empty:
    print("Não há vendas registradas em 2013 (a base cobre 2009 a 2012).")
else:
    print(calcados_2013.groupby(["ClienteNome", "ClienteCidade"])["Vendas"]
          .sum().sort_values(ascending=False))

titulo(10, "Na Europa, quanto que se vende ($) para cada país?")
europa = ["France", "Ireland", "UK", "Germany", "Sweden", "Belgium",
          "Spain", "Norway", "Portugal", "Austria", "Switzerland",
          "Finland", "Italy", "Poland", "Denmark"]
print(vendas[vendas["ClientePaís"].isin(europa)]
      .groupby("ClientePaís")["Vendas"].sum()
      .sort_values(ascending=False))
