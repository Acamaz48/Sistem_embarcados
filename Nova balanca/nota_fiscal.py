def gerar_nota_fiscal(produtos):
    nota_fiscal = "Nota Fiscal:\n"
    total = 0.0

    for produto in produtos:
        nota_fiscal += f"Produto: {produto['nome']}, Peso: {produto['peso']}kg, Valor: R${produto['valor']:.2f}\n"
        total += produto['valor']
    nota_fiscal += f"Total a pagar: R${total:.2f}"
    return nota_fiscal
