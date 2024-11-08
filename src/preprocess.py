import pandas as pd
import os
import json
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# Caminho dos arquivos
exploit_file = "data/files_exploits.csv"
shellcode_file = "data/files_shellcodes.csv"
cve_json_file = "data/nvdcve-1.1-2024.json"

# Função para carregar e combinar dados dos CSVs de exploits e shellcodes
def load_csv_data():
    exploits_df = pd.read_csv(exploit_file)
    shellcodes_df = pd.read_csv(shellcode_file)
    
    combined_df = pd.concat([
        exploits_df[['description', 'platform', 'file']],
        shellcodes_df[['description', 'platform', 'file']]
    ], ignore_index=True)
    
    return combined_df

# Função para carregar o conteúdo de arquivos CSV com vulnerabilidades
def load_code_snippet(row):
    file_path = os.path.join("exploitdb", row["file"])  # Verifique se o caminho está correto
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            return file.read()
    except FileNotFoundError:
        return "Arquivo não encontrado."

# Função para carregar e extrair dados do JSON de CVE
def load_cve_data():
    with open(cve_json_file, "r", encoding="utf-8") as f:
        cve_data = json.load(f)
    
    cve_records = []
    for item in cve_data['CVE_Items']:
        description = item['cve']['description']['description_data'][0]['value']
        cve_records.append({
            "description": description,
            "platform": "general",  # Pode ser ajustado se tiver detalhes específicos
            "file": None  # Não há arquivos associados aos dados CVE
        })
    return pd.DataFrame(cve_records)

# Pré-processar os dados de exploits, shellcodes e CVE
def preprocess_and_tokenize(max_len=200, vocab_size=10000):
    # Carregar dados dos arquivos CSV e JSON de CVE
    csv_data = load_csv_data()
    cve_data = load_cve_data()
    
    # Extrair conteúdo dos exploits e shellcodes
    csv_data["code_snippet"] = csv_data.apply(load_code_snippet, axis=1)
    
    # Combinar todos os dados
    combined_df = pd.concat([csv_data[['description', 'code_snippet']], cve_data[['description']]], ignore_index=True)
    combined_df['label'] = "vulnerável"  # Definimos todas as descrições como vulneráveis
    
    # Tokenizar os textos
    tokenizer = Tokenizer(num_words=vocab_size, oov_token="<OOV>")
    tokenizer.fit_on_texts(combined_df["description"])

    # Transformar as descrições em sequências
    sequences = tokenizer.texts_to_sequences(combined_df["description"])
    padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post')

    # Salvar o tokenizer para uso futuro
    with open("models/tokenizer.pkl", "wb") as f:
        pickle.dump(tokenizer, f)

    return padded_sequences, combined_df["label"]

if __name__ == "__main__":
    sequences, labels = preprocess_and_tokenize()
    print("Pré-processamento concluído.")
