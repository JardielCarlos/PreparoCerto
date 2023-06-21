

def calcularValorSugerido(custoPreparacao,perImposto,perLucro):
    imposto = custoPreparacao/perImposto
    lucro = custoPreparacao/perLucro
    
    valorSugerido = custoPreparacao+imposto+lucro
    return valorSugerido