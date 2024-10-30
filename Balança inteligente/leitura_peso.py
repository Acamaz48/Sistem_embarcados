from hx711 import HX711
import time

# Configura os pinos do HX711 (verifique os pinos conectados no seu ESP32 ou Arduino)
HX711_DT_PIN = 5  # Substitua pelo pino correto do seu setup
HX711_SCK_PIN = 6  # Substitua pelo pino correto do seu setup

# Inicializa o HX711
hx = HX711(dout_pin=HX711_DT_PIN, pd_sck_pin=HX711_SCK_PIN)

def calibrar_sensor():
    """
    Realiza a calibração do sensor de peso, retornando offset e escala.
    O offset é obtido com a balança vazia e a escala com um peso conhecido.
    """
    # Configura a balança com valores de calibração iniciais
    print("Posicione a balança vazia para calibração do offset.")
    time.sleep(2)  # Dá tempo para posicionar a balança 

    # Medida do offset com a balança vazia
    hx.zero()  # Ajusta o zero (offset)
    offset = hx.get_raw_data_mean()  # Captura o valor médio sem peso
    print(f"Offset (sem peso): {offset}")

    # Medida da escala com um peso conhecido
    peso_conhecido = 100  # Valor em gramas, ajuste para o peso conhecido disponível
    input(f"Coloque {peso_conhecido}g na balança e pressione Enter para continuar...")
    peso_leitura = hx.get_raw_data_mean() - offset  # Subtrai o offset do valor bruto

    # Calcula a escala
    escala = peso_leitura / peso_conhecido
    print(f"Escala calculada: {escala}")

    return offset, escala

def ler_peso():
    """
    Retorna o valor bruto lido pelo sensor, a ser ajustado com offset e escala.
    """
    peso_bruto = hx.get_raw_data_mean()
    return peso_bruto

