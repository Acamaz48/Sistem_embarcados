import paho.mqtt.client as mqtt

# Função chamada quando a conexão for bem-sucedida
def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker MQTT com código de resultado: " + str(rc))
    client.subscribe("test/topic")

# Função chamada quando uma mensagem é recebida
def on_message(client, userdata, msg):
    print("Mensagem recebida no tópico " + msg.topic + ": " + str(msg.payload.decode()))

# Criar um cliente MQTT
client = mqtt.Client()

# Associar as funções de conexão e mensagem
client.on_connect = on_connect
client.on_message = on_message

# Conectar ao broker Mosquitto (localhost)
client.connect("localhost", 1883, 60)

# Iniciar o loop do cliente
client.loop_start()

# Função para enviar informações do produto
def enviar_informacoes(produto, peso, valor):
    mensagem = f"Produto: {produto}, Peso: {peso}kg, Valor: R${valor:.2f}"
    client.publish("test/topic", mensagem)
    print(f"Enviando mensagem: {mensagem}")

# Exemplo de uso (substitua pelos valores reais que você tiver)
produto = "banana"
peso = 0.5  # peso em kg
valor = peso * 5  # supondo R$5 por kg

# Enviar as informações do produto
enviar_informacoes(produto, peso, valor)

# Manter o script ativo para receber mensagens
input("Pressione Enter para sair...\n")
