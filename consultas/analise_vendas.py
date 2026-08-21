# Análise de Vendas Globais - Departamento de Vendas
# Equipe: Francisco Viana, Murilo Maciel, Felipe Oliveira
# Requisitos: Python 3 + pandas  (pip install pandas)

from pathlib import Path

import pandas as pd

pd.options.display.float_format = "{:,.2f}".format

# Caminhos ancorados neste arquivo, para o script rodar de qualquer pasta
DADOS = Path(__file__).resolve().parent.parent / "dados"

# ---------- Carga dos dados ----------
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
    print(f"\n{'=' * 70}\n{n}. {texto}\n{'=' * 70}")


# 1) 10 maiores clientes em vendas ($)
titulo(1, "10 maiores clientes em vendas ($)")
print(vendas.groupby("ClienteNome")["Vendas"].sum()
      .sort_values(ascending=False).head(10))

# 2) 3 maiores países em vendas ($)
titulo(2, "3 maiores países em vendas ($)")
print(vendas.groupby("ClientePaís")["Vendas"].sum()
      .sort_values(ascending=False).head(3))

# 3) Categorias com maior faturamento no Brasil
titulo(3, "Categorias com maior faturamento no Brasil")
brasil = vendas[vendas["ClientePaís"] == "Brazil"]
print(brasil.groupby("CategoriaNome")["Vendas"].sum()
      .sort_values(ascending=False))

# 4) Despesa com frete por transportadora
titulo(4, "Despesa com frete por transportadora")
print(vendas.groupby("TransportadoraNome")["Frete"].sum()
      .sort_values(ascending=False))

# 5) Principais clientes de Men's Footwear na Alemanha
titulo(5, "Principais clientes de Men's Footwear na Alemanha")
calcados_de = vendas[(vendas["CategoriaNome"] == "Men´s Footwear") &
                     (vendas["ClientePaís"] == "Germany")]
print(calcados_de.groupby("ClienteNome")["Vendas"].sum()
      .sort_values(ascending=False))

# 6) Vendedores que mais dão descontos nos EUA
titulo(6, "Vendedores que mais dão descontos nos EUA")
eua = vendas[vendas["ClientePaís"] == "USA"]
print(eua.groupby("VendedorNome")["Desconto"].sum()
      .sort_values(ascending=False))

# 7) Fornecedores com maior margem de lucro em Womens wear
titulo(7, "Fornecedores com maior margem ($) em Womens wear")
feminino = vendas[vendas["CategoriaNome"] == "Womens wear"]
print(feminino.groupby("FornecedorNome")["Margem Bruta"].sum()
      .sort_values(ascending=False).head(10))

# 8) Vendas em 2009 e evolução anual 2009-2012
titulo(8, "Vendas em 2009 e evolução anual 2009-2012")
anual = vendas.groupby("Ano")["Vendas"].sum()
print(anual)
print(f"\nVendido em 2009: $ {anual[2009]:,.2f}")
print("Variação ano a ano (%):")
print(anual.pct_change().mul(100).round(1))

# 9) Clientes de Men's Footwear em 2013 (e cidades)
titulo(9, "Clientes de Men's Footwear em 2013 (e cidades)")
calcados_2013 = vendas[(vendas["CategoriaNome"] == "Men´s Footwear") &
                       (vendas["Ano"] == 2013)]
if calcados_2013.empty:
    print("Não há vendas registradas em 2013 (a base cobre 2009 a 2012).")
else:
    print(calcados_2013.groupby(["ClienteNome", "ClienteCidade"])["Vendas"]
          .sum().sort_values(ascending=False))

# 10) Vendas por país na Europa
titulo(10, "Vendas por país na Europa")
europa = ["France", "Ireland", "UK", "Germany", "Sweden", "Belgium",
          "Spain", "Norway", "Portugal", "Austria", "Switzerland",
          "Finland", "Italy", "Poland", "Denmark"]
print(vendas[vendas["ClientePaís"].isin(europa)]
      .groupby("ClientePaís")["Vendas"].sum()
      .sort_values(ascending=False))
