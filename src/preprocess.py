import pandas as pd
import os
import json
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# Caminho do diretório base
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Caminhos absolutos para os arquivos
exploit_json_file = os.path.join(BASE_DIR, "data/compiled_exploits.json")  # Novo arquivo de exploits
safe_code_file = os.path.join(BASE_DIR, "data/safe_code_examples.json")

# Função para carregar e processar o novo arquivo JSON dos exploits
def load_exploit_data():
    with open(exploit_json_file, "r", encoding="utf-8") as f:
        exploit_data = json.load(f)
    
    exploit_records = []
    for item in exploit_data:
        description = item.get("code", "")  # Pega o código do exploit
        exploit_records.append({
            "description": description,
            "label": "vulnerável"
        })
    return pd.DataFrame(exploit_records)

# Função para carregar exemplos de código seguro do JSON
def load_safe_examples():
    with open(safe_code_file, "r", encoding="utf-8") as f:
        safe_data = json.load(f)
    safe_df = pd.DataFrame(safe_data)
    return safe_df

# Função principal de pré-processamento e tokenização
def preprocess_and_tokenize(max_len=200, vocab_size=10000):
    # Carregar dados vulneráveis e seguros
    exploit_data = load_exploit_data()  # Carrega a nova database de exploits
    safe_data = load_safe_examples()
    
    # Combina dados de vulnerabilidades e exemplos seguros
    combined_df = pd.concat([exploit_data[['description', 'label']], safe_data[['description', 'label']]], ignore_index=True)
    
    # Balanceamento de dados: iguala a quantidade de exemplos vulneráveis e seguros
    vulnerable_samples = combined_df[combined_df['label'] == "vulnerável"]
    safe_samples = combined_df[combined_df['label'] == "seguro"].sample(len(vulnerable_samples), replace=True)
    balanced_df = pd.concat([vulnerable_samples, safe_samples])

    # Tokenização dos textos
    tokenizer = Tokenizer(num_words=vocab_size, oov_token="<OOV>")
    tokenizer.fit_on_texts(balanced_df["description"])
    
    sequences = tokenizer.texts_to_sequences(balanced_df["description"])
    padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post')
    
    # Salvar o tokenizer para uso posterior
    tokenizer_path = os.path.join(BASE_DIR, "models/tokenizer.pkl")
    with open(tokenizer_path, "wb") as f:
        pickle.dump(tokenizer, f)

    return padded_sequences, balanced_df["label"]

if __name__ == "__main__":
    sequences, labels = preprocess_and_tokenize()
    print("Pré-processamento concluído.")
