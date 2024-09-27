#include <WiFi.h>
#include <ArduinoMqttClient.h>

// Credenciais Wi-Fi
const char ssid[] = "Galaxy A55 Lukas";      // Nome da rede Wi-Fi
const char pass[] = "eduw8101";              // Senha da rede Wi-Fi

// Configuração do broker MQTT
const char broker[] = "172.16.6.26";         // IP do seu servidor Mosquitto
int port = 1883;                              // Porta padrão MQTT

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

void setup() {
  // Inicializa a serial para depuração
  Serial.begin(115200);
  
  // Conecta ao Wi-Fi
  connectWiFi();
  
  // Conecta ao broker MQTT
  connectMQTT();
}

void connectWiFi() {
  Serial.print("Conectando ao WiFi...");
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Conectado ao WiFi!");
}

void connectMQTT() {
  Serial.print("Conectando ao broker MQTT...");
  
  // Conecta ao broker Mosquitto
  if (!mqttClient.connect(broker, port)) {
    Serial.print("Falha na conexão com o broker. Código de erro: ");
    Serial.println(mqttClient.connectError());
    while (1);
  }
  
  Serial.println("Conectado ao broker MQTT!");
  
  // Subscreve ao tópico
  mqttClient.subscribe("test/topic");
}

void loop() {
  // Mantém a conexão MQTT
  mqttClient.poll();
  
  // Envia uma mensagem ao broker MQTT
  mqttClient.beginMessage("test/topic");
  mqttClient.print("Olá do Arduino!");
  mqttClient.endMessage();
  
  delay(1000);  // Espera 1 segundo antes de enviar outra mensagem
}
