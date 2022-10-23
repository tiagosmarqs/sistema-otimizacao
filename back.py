from pulp import *
import pandas as pd

def implementacao(ano):

    produtos = pd.read_csv("Tabela Produtos.csv", sep = ";")

    if ano==1:
        vendas = pd.read_csv("Tabela Vendas - 2007.csv", sep = ";")
    elif ano==2:
        vendas = pd.read_csv("Tabela Vendas - 2008.csv", sep = ";")
    elif ano==3:
        vendas = pd.read_csv("Tabela Vendas - 2009.csv", sep = ";")


    prob = LpProblem("ProblemaContotoso", LpMaximize)

    #variaveis

    x = []
    for i in range(0, 2517):
        x.append(LpVariable(f"{produtos.iloc[i]['NomeProduto']}", lowBound = 0)) 

    #função objetivo
    prob += lpSum(x) 

    #restrição 1
    taxa2010 = 0.0691 
    prob += lpSum([((produtos.loc[produtos['ChaveDoProduto']==i, 'PrecoUnitario'] + (taxa2010 * produtos.loc[produtos['ChaveDoProduto']==i, 'PrecoUnitario'])) * lpSum(vendas.loc[vendas['ChaveDoProduto']==i, 'QuantidadeDeVendas'])) - lpSum(vendas.loc[vendas['ChaveDoProduto']==i, 'CustoTotal']) - x[i-1] for i in range(1, 2518)]) >= (lpSum(vendas['TotalDeVendas']) - lpSum(vendas['CustoTotal'])) + ((lpSum(vendas['TotalDeVendas']) - lpSum(vendas['CustoTotal'])) * taxa2010)

    #restrição 2
    prob += lpSum([x[i] for i in range(0, 2517)]) <= lpSum(vendas['ValorDoDesconto']) + (0.01 * (lpSum(vendas['TotalDeVendas']) - lpSum(vendas['CustoTotal'])))

    #restrição 3
    listaR3eR4 = []

    lucroProdutoD = (vendas.groupby('ChaveDoProduto')['TotalDeVendas'].sum() - vendas.groupby('ChaveDoProduto')['CustoTotal'].sum()).sort_values(ascending=False) #lucro líquido total por produto, ordenado de forma decrescente
    descontoProduto = (vendas.groupby('ChaveDoProduto')['ValorDoDesconto'].sum()) #desconto total por produto

    for i in range(0, 15):
        prob += x[lucroProdutoD.index[i]-1] == descontoProduto[lucroProdutoD.index[i]]
        listaR3eR4.append(lucroProdutoD.index[i])


    #restrição 4
    lucroProdutoC = (vendas.groupby('ChaveDoProduto')['TotalDeVendas'].sum() - vendas.groupby('ChaveDoProduto')['CustoTotal'].sum()).sort_values() #lucro líquido total por produto, ordenado de forma crescente

    for i in range(0, 40):
        prob += x[lucroProdutoC.index[i]-1] == descontoProduto[lucroProdutoC.index[i]] * 1.1
        listaR3eR4.append(lucroProdutoC.index[i])


    #restrição 5 e 6

    numeroVendas = vendas.groupby('ChaveDoProduto')['QuantidadeDeVendas'].sum()

    lista = []
    for i in range(0, len(numeroVendas)):
        lista.append(numeroVendas.index[i])


    listaFiltrada = [item for item in lista if item not in listaR3eR4]


    for i in listaFiltrada:

        if numeroVendas[i] >= 100000:

            prob += x[i-1] >= descontoProduto[i] * 1.05   
        else:

            prob += x[i-1] >= descontoProduto[i] * 1.025
        

    status = prob.solve()

    print (LpStatus[status])

    lista_resul = []
    for v in prob.variables():
        
        lista_resul.append(f'{v.name} = ${v.varValue:.2f}')

    return lista_resul


def anoselecionado(ano):
    produtos = pd.read_csv("Tabela Produtos.csv", sep = ";")

    if ano==1:
        vendas = pd.read_csv("Tabela Vendas - 2007.csv", sep = ";")
    elif ano==2:
        vendas = pd.read_csv("Tabela Vendas - 2008.csv", sep = ";")
    elif ano==3:
        vendas = pd.read_csv("Tabela Vendas - 2009.csv", sep = ";")

    desconto_ano = vendas.groupby('ChaveDoProduto')['ValorDoDesconto'].sum()

    nome_produtos = produtos['NomeProduto']

    

    lista_resul = []

    for i in range(0, 2517):
        try:
            lista_resul.append(f'{nome_produtos.iloc[i]} = ${desconto_ano[i+1]:.2f}')
        except KeyError:
            lista_resul.append(f'{nome_produtos.iloc[i]} = $0.0')

    return sorted(lista_resul)
