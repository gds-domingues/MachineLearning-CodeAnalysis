from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, MaxPooling1D, LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from preprocess import preprocess_and_tokenize
import numpy as np

# Ajustes de hiperparâmetros
vocab_size = 10000           # Tamanho do vocabulário ajustado
embedding_dim = 200          # Dimensão do embedding ajustada
max_len = 1000                # Comprimento máximo das sequências ajustado
batch_size = 64              # Tamanho do batch
epochs = 5                  # Número de épocas ajustado

# Carregar dados de treinamento
sequences, labels = preprocess_and_tokenize(max_len, vocab_size)

# Convertendo rótulos em binário (1 para vulnerável e 0 para seguro)
labels = np.array([1 if label == "vulnerável" else 0 for label in labels])

# Separar dados em treinamento e validação
train_size = int(0.8 * len(sequences))
X_train, X_val = sequences[:train_size], sequences[train_size:]
y_train, y_val = labels[:train_size], labels[train_size:]

# Construção do modelo CNN + LSTM com ajustes
model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=embedding_dim),
    Conv1D(128, 3, activation='relu'),
    MaxPooling1D(pool_size=2),
    LSTM(128, return_sequences=True),
    Dropout(0.3),
    LSTM(64),
    Dense(64, activation='relu'),
    Dropout(0.4),
    Dense(1, activation='sigmoid')
])

# Compilar o modelo
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Configuração de early stopping para evitar overfitting
early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

# Treinamento do modelo com early stopping
model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_val, y_val), callbacks=[early_stopping])

# Salvar o modelo treinado
model.save("models/model_cnn_lstm.h5")
print("Modelo treinado e salvo em 'models/model_cnn_lstm.h5'.")
