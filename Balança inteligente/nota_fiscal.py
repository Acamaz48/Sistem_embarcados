import os

def gerar_nota_fiscal(produto_nome, peso, preco_por_kg):
    """
    Gera o texto da nota fiscal para o produto.
    
    Args:
    - produto_nome (str): Nome do produto.
    - peso (float): Peso do produto em gramas.
    - preco_por_kg (float): Preço por kg do produto.
    
    Returns:
    - str: Texto formatado da nota fiscal.
    """
    # Converte o peso de gramas para kg
    peso_kg = peso / 1000
    
    # Calcula o preço total
    preco_total = peso_kg * preco_por_kg
    
    # Formata a nota fiscal
    nota_fiscal_texto = (
        f"--- Nota Fiscal ---\n"
        f"Produto: {produto_nome}\n"
        f"Peso: {peso:.2f} g ({peso_kg:.2f} kg)\n"
        f"Preço por kg: R${preco_por_kg:.2f}\n"
        f"Preço total: R${preco_total:.2f}\n"
        f"--------------------\n"
    )
    return nota_fiscal_texto

def imprimir_nota_fiscal(produto_nome, peso, preco_por_kg):
    """
    Imprime a nota fiscal na tela e pede confirmação ao usuário.
    
    Args:
    - produto_nome (str): Nome do produto.
    - peso (float): Peso do produto em gramas.
    - preco_por_kg (float): Preço por kg do produto.
    
    Returns:
    - bool: True se o usuário confirmar a nota, False caso contrário.
    """
    nota_fiscal_texto = gerar_nota_fiscal(produto_nome, peso, preco_por_kg)
    
    # Imprime a nota fiscal
    print(nota_fiscal_texto)
    
    # Pergunta se o usuário confirma
    confirmacao = input("O seu produto está correto? (Sim/Não): ")
    
    return confirmacao.strip().lower() == 'sim'

# Exemplo de uso
if __name__ == "__main__":
    produto_nome = "banana prata"
    peso = 100  # em gramas
    preco_por_kg = 15.00  # em reais por kg

    # Imprime e confirma a nota fiscal
    if imprimir_nota_fiscal(produto_nome, peso, preco_por_kg):
        print("Nota fiscal confirmada.")
    else:
        print("Por favor, ajuste o produto ou os dados e tente novamente.")
