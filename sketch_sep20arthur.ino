#include <ultrasonic.h>

// Definição dos pinos
#define trigPin 33       // Pino TRIG do HC-SR04
#define echoPin 35       // Pino ECHO do HC-SR04
#define buzzerPin 25     // Pino do buzzer
#define ledPositivo 26   // LED positivo (distante)
#define ledNegativo 32   // LED negativo (perto)
#define chaveMestre 15  // Pino da chave mestre (não usado neste exemplo)

// Variáveis
long duracao;
float distancia;
float capacidadeCheia = 20.0; // Distância em cm quando o lixo está cheio
float limite80 = capacidadeCheia * 0.8; // 80% da capacidade cheia
float limiteSilencio = 15.0;   // Limite para não emitir som

void setup() {
    // Inicializa comunicação serial
    Serial.begin(9600);

    // Configura os pinos
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
    pinMode(buzzerPin, OUTPUT);
    pinMode(ledPositivo, OUTPUT);
    pinMode(ledNegativo, OUTPUT);
}

void loop() {
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
    Serial.print("Limite 80%: ");
    Serial.println(limite80);
    Serial.print("Limite Silêncio: ");
    Serial.println(limiteSilencio);

    // Se a distância for maior que 15 cm, desliga o som e os LEDs
    if (distancia > limiteSilencio) {
        digitalWrite(ledPositivo, LOW);  // Apaga LED positivo
        digitalWrite(ledNegativo, LOW);   // Apaga LED negativo
        noTone(buzzerPin);                // Não emite som
        Serial.println("Distância maior que 30 cm. Nenhum LED aceso.");
    }
    // Se a distância for maior que 80% da capacidade cheia, mas menor ou igual a 15 cm
    else if (distancia > limite80 && distancia <= limiteSilencio) { 
        digitalWrite(ledPositivo, HIGH);  // Acende LED positivo (objeto distante)
        digitalWrite(ledNegativo, LOW);    // Apaga LED negativo
        tone(buzzerPin, 1000);             // Som fraco (1000 Hz)
        Serial.println("LED Positivo aceso (distante).");
    }
    // Se o objeto estiver perto (menor ou igual a 80% da capacidade cheia)
    else if (distancia <= limite80) { 
        digitalWrite(ledNegativo, HIGH);   // Acende LED negativo (objeto perto)
        digitalWrite(ledPositivo, LOW);    // Apaga LED positivo
        tone(buzzerPin, 500);              // Som forte (500 Hz)
        Serial.println("LED Negativo aceso (perto).");
    }

    delay(1000);   // Mantém o som por 1 segundo
    noTone(buzzerPin); // Para o buzzer

    delay(500);    // Delay para estabilidade
}
