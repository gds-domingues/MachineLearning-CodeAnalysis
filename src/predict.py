import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
import sys
import os

# Função para carregar o modelo com verificações de erro
def load_model_safe(model_path):
    try:
        print(f"Tentando carregar o modelo do caminho: {model_path}")
        model = tf.keras.models.load_model(model_path)
        print("Modelo carregado com sucesso.")
        return model
    except FileNotFoundError:
        print(f"Erro: O modelo não foi encontrado no caminho '{model_path}'.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao carregar o modelo: {e}")
        sys.exit(1)

# Função para carregar o tokenizer com verificações de erro
def load_tokenizer_safe(tokenizer_path):
    try:
        print(f"Tentando carregar o tokenizer do caminho: {tokenizer_path}")
        with open(tokenizer_path, "rb") as f:
            tokenizer = pickle.load(f)
        print("Tokenizer carregado com sucesso.")
        return tokenizer
    except FileNotFoundError:
        print(f"Erro: O tokenizer não foi encontrado no caminho '{tokenizer_path}'.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao carregar o tokenizer: {e}")
        sys.exit(1)

# Caminhos corrigidos para apontar para a pasta 'models' no diretório principal
model_path = os.path.abspath("../models/model_cnn_lstm.h5")
tokenizer_path = os.path.abspath("../models/tokenizer.pkl")
model = load_model_safe(model_path)
tokenizer = load_tokenizer_safe(tokenizer_path)

def preprocess_code_snippet(code_snippet, max_len=200):
    sequence = tokenizer.texts_to_sequences([code_snippet])
    padded_sequence = pad_sequences(sequence, maxlen=max_len, padding='post')
    return padded_sequence

def analyze_code_snippet(code_snippet):
    processed_code = preprocess_code_snippet(code_snippet)
    prediction = model.predict(processed_code)
    return "Provavelmente vulnerável" if prediction[0][0] > 0.5 else "Provavelmente seguro"

def read_code_from_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python predict.py <caminho_para_o_arquivo_de_codigo>")
        sys.exit(1)

    # Lê o arquivo de código fornecido como argumento
    file_path = sys.argv[1]
    code = read_code_from_file(file_path)

    # Analisa o código e exibe o resultado
    result = analyze_code_snippet(code)
    print(f"Resultado da análise: {result}")
