import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, MaxPooling1D, LSTM, Dense, Dropout
from preprocess import preprocess_and_tokenize
import numpy as np

# Configurações do modelo
vocab_size = 10000
embedding_dim = 128
max_len = 200

# Carregar os dados e pré-processar
sequences, labels = preprocess_and_tokenize(max_len, vocab_size)

# Convertendo os rótulos em binário (1 para vulnerável)
labels = np.array([1 if label == "vulnerável" else 0 for label in labels])

# Separar os dados em treinamento e validação
train_size = int(0.8 * len(sequences))
X_train, X_val = sequences[:train_size], sequences[train_size:]
y_train, y_val = labels[:train_size], labels[train_size:]

# Construção do modelo CNN + LSTM
model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_len),
    Conv1D(64, 5, activation='relu'),
    MaxPooling1D(pool_size=2),
    LSTM(64, return_sequences=True),
    Dropout(0.2),
    LSTM(32),
    Dense(32, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Treinamento do modelo com o novo conjunto de dados combinado
model.fit(X_train, y_train, epochs=5, batch_size=64, validation_data=(X_val, y_val))

# Salvar o modelo treinado
model.save("models/model_cnn_lstm.h5")
print("Modelo treinado e salvo em 'models/model_cnn_lstm.h5'.")
