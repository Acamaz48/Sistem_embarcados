#include <WiFi.h>
#include <PubSubClient.h>
#include <ultrasonic.h>

// Definição dos pinos
#define trigPin 2       // Pino TRIG do HC-SR04
#define echoPin 3       // Pino ECHO do HC-SR04
#define buzzerPin 5     // Pino do buzzer
#define ledPositivo 9   // LED positivo (distante)
#define ledNegativo 8   // LED negativo (perto)
#define chaveMestre 15  // Pino da chave mestre

// Variáveis
long duracao;
float distancia;
float capacidadeCheia = 20.0;  // Distância em cm quando o lixo está cheio
float limite80 = capacidadeCheia * 0.8;  // 80% da capacidade cheia
float limiteSilencio = 30.0;   // Limite para não emitir som

// Configurações Wi-Fi e MQTT
const char ssid[] = "Galaxy A55 Lukas";      // Nome da rede Wi-Fi
const char pass[] = "eduw8101";              // Senha da rede Wi-Fi

// Configuração do broker MQTT
const char broker[] = "172.16.6.26";         // IP do seu servidor Mosquitto
int port = 1883;    
WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
    delay(10);
    Serial.println();
    Serial.print("Conectando-se à rede ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("WiFi conectado.");
    Serial.println("Endereço IP: ");
    Serial.println(WiFi.localIP());
}

void reconnect() {
    // Loop até que a conexão seja restabelecida
    while (!client.connected()) {
        Serial.print("Tentando conexão MQTT...");
        if (client.connect("ESP32Client")) {
            Serial.println("conectado!");
        } else {
            Serial.print("falhou, rc=");
            Serial.print(client.state());
            Serial.println(" tentando novamente em 5 segundos");
            delay(5000);
        }
    }
}

void setup() {
    // Inicializa comunicação serial
    Serial.begin(9600);
    
    // Conectar ao Wi-Fi
    setup_wifi();
    
    // Configura MQTT
    client.setServer(mqtt_server, 1883);

    // Configura os pinos
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
    pinMode(buzzerPin, OUTPUT);
    pinMode(ledPositivo, OUTPUT);
    pinMode(ledNegativo, OUTPUT);
}

void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();
  
    // Envia o pulso TRIG
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    // Calcula o tempo do pulso ECHO
    duracao = pulseIn(echoPin, HIGH);

    // Calcula a distância (em cm)
    distancia = (duracao * 0.0343) / 2; // A velocidade do som é aproximadamente 343 m/s

    Serial.print("Distância: ");
    Serial.println(distancia);

    // Se a distância for maior que 15 cm, desliga o som e os LEDs
    if (distancia > limiteSilencio) {
        digitalWrite(ledPositivo, LOW);  // Apaga LED positivo
        digitalWrite(ledNegativo, LOW);  // Apaga LED negativo
        noTone(buzzerPin);               // Não emite som
        Serial.println("Distância maior que 15 cm. Nenhum LED aceso.");
    }
    // Se a distância for maior que 80% da capacidade cheia, mas menor que 15 cm
    else if (distancia > limite80 && distancia <= limiteSilencio) { 
        digitalWrite(ledPositivo, HIGH);  // Acende LED positivo (objeto distante)
        digitalWrite(ledNegativo, LOW);   // Apaga LED negativo
        tone(buzzerPin, 1000);            // Som fraco (1000 Hz)
        Serial.println("LED Positivo aceso (distante).");

        // Envia a mensagem MQTT ao broker
        client.publish("lixeira/status", "O lixo está a 80% da capacidade.");
    }
    // Se o objeto estiver perto (menor ou igual a 80% da capacidade cheia)
    else if (distancia <= limite80) { 
        digitalWrite(ledNegativo, HIGH);  // Acende LED negativo (objeto perto)
        digitalWrite(ledPositivo, LOW);   // Apaga LED positivo
        tone(buzzerPin, 500);             // Som forte (500 Hz)
        Serial.println("LED Negativo aceso (perto).");

        // Envia a mensagem MQTT ao broker
        client.publish("lixeira/status", "O lixo está cheio, precisa trocar.");
    }

    delay(1000);   // Mantém o som por 1 segundo
    noTone(buzzerPin); // Para o buzzer

    delay(500);    // Delay para estabilidade
}
