import os
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import numpy as np
import json

# Carregar modelo e tokenizer
model_path = os.path.join("models", "model_cnn_lstm.h5")
tokenizer_path = os.path.join("models", "tokenizer.pkl")

print(f"Tentando carregar o modelo do caminho: {model_path}")
model = load_model(model_path)
print("Modelo carregado com sucesso.")

print(f"Tentando carregar o tokenizer do caminho: {tokenizer_path}")
with open(tokenizer_path, "rb") as f:
    tokenizer = pickle.load(f)
print("Tokenizer carregado com sucesso.")

# Função para processar e prever código com threshold ajustado
def analyze_code_snippet(code_snippet, threshold=0.6):  # Defina o threshold
    # Tokenizar e processar o código
    sequence = tokenizer.texts_to_sequences([code_snippet])[0]
    sequence = [idx if idx < tokenizer.num_words else 1 for idx in sequence]  # Substitui OOV
    padded_sequence = pad_sequences([sequence], maxlen=200, padding='post')

    # Fazer a predição com threshold personalizado
    prediction = model.predict(padded_sequence)
    return "Vulnerável" if prediction >= threshold else "Seguro"

# Carregar e analisar o código de teste a partir da database compilada
with open("data/compiled_exploits.json", "r", encoding="utf-8") as f:
    exploit_data = json.load(f)
    code = exploit_data[0]["code"]  # Analisa o primeiro código como exemplo

# Realizar a análise
result = analyze_code_snippet(code)
print(f"Resultado da análise: {result}")
