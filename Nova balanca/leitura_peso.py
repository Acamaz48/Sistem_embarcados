import time
import random  # Usado para simulação, substitua pela leitura do HX711

def ler_peso():
    # Simulação de leitura de peso
    peso = random.uniform(0.1, 1)  # Simula um peso entre 0 e 1 kg
    time.sleep(1)  # Simula um atraso na leitura
    return round(peso, 2)  # Retorna o peso com duas casas decimais

