def calcularValorSugerido(custoPreparacao,perImposto,perLucro):

    imposto = custoPreparacao * (perImposto / 100)

    lucro = (custoPreparacao - imposto) * (perLucro / 100)

    valorSugerido = custoPreparacao+imposto+lucro
    return valorSugerido
