import cv2
import numpy as np
import imutils
import tensorflow as tf  # Corrigido para importar o tensorflow corretamente

# Carrega o modelo MobileNet pré-treinado
model = tf.keras.applications.MobileNetV2(weights="imagenet")

def preprocess_image(image):
    """
    Pré-processa a imagem capturada para o modelo de classificação.
    Redimensiona para o tamanho esperado e normaliza os valores dos pixels.
    """
    image_resized = cv2.resize(image, (224, 224))  # Redimensiona para 224x224
    image_array = np.array(image_resized, dtype=np.float32)
    image_array = np.expand_dims(image_array, axis=0)  # Adiciona uma dimensão para o lote
    image_array = tf.keras.applications.mobilenet_v2.preprocess_input(image_array)
    return image_array

def identificar_produto():
    """
    Captura uma imagem da câmera e identifica o produto.
    Retorna o rótulo do produto identificado.
    """
    # Inicia a captura de vídeo
    cap = cv2.VideoCapture(0)  # Abre a câmera padrão
    if not cap.isOpened():
        raise Exception("Não foi possível abrir a câmera.")

    print("Posicione o produto na câmera e pressione 'q' para capturar.")
    
    # Loop para exibir o vídeo até a captura ser confirmada
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar a imagem.")
            break

        frame = imutils.resize(frame, width=800)  # Redimensiona a imagem para visualização
        cv2.imshow("Captura de Produto", frame)

        # Pressione 'q' para capturar a imagem e realizar a identificação
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Imagem capturada para identificação.")
            break

    # Fecha a câmera e janela de captura
    cap.release()
    cv2.destroyAllWindows()

    # Pré-processa a imagem capturada
    image_array = preprocess_image(frame)

    # Realiza a previsão usando o modelo
    predictions = model.predict(image_array)
    decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=1)

    # Extrai o rótulo do produto identificado
    produto_id = decoded_predictions[0][0][1]  # Identificador do produto
    print(f"Produto identificado: {produto_id}")

    return produto_id

if __name__ == "__main__":
    produto = identificar_produto()
