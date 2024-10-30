# Importa os módulos criados
from identificacao_produto import identificar_produto
from leitura_peso import ler_peso, calibrar_sensor
from nota_fiscal import gerar_nota_fiscal

def main():
    # Inicializa lista de produtos
    lista_produtos = []

    # Calibração do sensor de peso
    print("Calibrando a balança...")
    offset, escala = calibrar_sensor()
    print("Calibração concluída.\n")

    while True:
        # Identificação do produto
        print("\nCapturando imagem para identificar o produto...")
        produto_id = identificar_produto()
        produto_nome = f"Produto {produto_id}"  # Nome fictício para o exemplo
        preco_por_kg = 15.0  # Preço fictício por kg

        # Leitura do peso
        print("Pesando o produto...")
        peso_bruto = ler_peso() - offset
        peso_real = peso_bruto * escala  # Conversão para unidade de peso com base na escala
        preco = (peso_real / 1000) * preco_por_kg  # Conversão do peso para kg e cálculo do preço

        # Exibe as informações para confirmação
        while True:
            print(f"\nProduto detectado: {produto_nome} - {peso_real:.0f} g - R${preco:.2f}")
            confirmacao = input("O seu produto está correto? (Sim/Não): ").strip().lower()
            
            if confirmacao == 'sim':
                # Adiciona o produto à lista
                lista_produtos.append((produto_nome, peso_real, preco))
                print(f"{produto_nome} adicionado com sucesso.\n")
                break
            elif confirmacao == 'não':
                print("Reidentificando o produto e recalculando o peso...\n")
                break  # Sai do loop para repetir a identificação e pesagem
            else:
                print("Por favor, responda com 'Sim' ou 'Não'.")

        # Pergunta se deseja continuar
        continuar = input("Deseja adicionar outro produto? (s/n): ").strip().lower()
        if continuar != 's':
            break

    # Gera e imprime a nota fiscal
    gerar_nota_fiscal(lista_produtos)
    print("\nOperação finalizada.")

# Executa o programa
if __name__ == "__main__":
    main()
