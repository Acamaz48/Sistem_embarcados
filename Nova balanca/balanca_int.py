from identificacao_produto import identificar_produto
from leitura_peso import ler_peso
from nota_fiscal import gerar_nota_fiscal
from mosquitto import enviar_informacoes

def main():
    produtos = []
    max_produtos = 30

    while len(produtos) < max_produtos:
        produto_id = identificar_produto()
        peso = ler_peso()

        if produto_id and peso:
            valor = peso * 5
            produto_info = {
                "nome" : produto_id,
                "peso" : peso,
                "valor" : valor
            }

            produtos.append(produto_info)

            enviar_informacoes(produto_id,peso,valor)

            print(f"Produto: {produto_id}, Peso: {peso}kg, Valor total: R${valor: .2f}")
        else 
            print("Erro ao identificar produto ou peso")
        
        continuar = input("Adicionar outro produto? (s/n): ")
        if continuar.lower() != 's':
            break
        
    nota_fiscal = gerar_nota_fiscal(produtos)
    print(nota_fiscal)

if _name_ == "_main_":
    main()
    

