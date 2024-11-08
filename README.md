# Vulnerability Detection in Code Using Machine Learning

Este projeto utiliza aprendizado de máquina para detectar vulnerabilidades em exemplos de código. Com uma combinação de redes neurais convolucionais (CNN) e redes LSTM, o modelo analisa descrições e exemplos de código para identificar padrões associados a vulnerabilidades comuns.

## Objetivo

O objetivo é fornecer uma ferramenta que auxilie na análise de segurança de códigos, detectando automaticamente potenciais vulnerabilidades. Este projeto pode ser aplicado a uma variedade de linguagens de programação e tipos de vulnerabilidade, sendo especialmente útil para desenvolvedores e analistas de segurança.

## Estrutura do Projeto

```
vulnhub/
├── data/
│   ├── files_exploits.csv          # Dados de exploits do Exploit-DB
│   ├── files_shellcodes.csv         # Dados de shellcodes do Exploit-DB
│   └── nvdcve-1.1-2024.json         # Arquivo JSON da CVE para treinamento
├── models/
│   ├── model_cnn_lstm.h5            # Arquivo do modelo treinado
│   └── tokenizer.pkl                # Tokenizer para preprocessamento de texto
├── vuln-codes/
│   ├── buffer-overflow.c            # Exemplo de código vulnerável para teste
│   └── safe_code.py                 # Exemplo de código seguro para teste
├── src/
│   ├── preprocess.py                # Script para preprocessamento dos dados
│   ├── train.py                     # Script para treinamento do modelo
│   └── predict.py                   # Script para predição em novos códigos
└── README.md                        # Descrição do projeto (este arquivo)
```

## Configuração do Ambiente

### Pré-requisitos

- **Python 3.8+**
- **Bibliotecas Python**:
  - TensorFlow
  - Pandas
  - NumPy
  - Scikit-learn
  - h5py

### Instalando as Dependências

Para instalar as dependências, crie e ative um ambiente virtual e, em seguida, instale os pacotes listados em `requirements.txt`:

```bash
python -m venv venv
source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

## Uso do Projeto

### 1. Pré-processamento dos Dados

O script `preprocess.py` processa os dados dos arquivos `files_exploits.csv`, `files_shellcodes.csv` e `nvdcve-1.1-2024.json`. Ele tokeniza as descrições e os exemplos de código, preparando-os para o treinamento do modelo.

```bash
python src/preprocess.py
```

### 2. Treinamento do Modelo

Após o preprocessamento, o script `train.py` treina o modelo CNN + LSTM usando os dados tokenizados.

```bash
python src/train.py
```

Isso irá salvar o modelo treinado em `models/model_cnn_lstm.h5`.

### 3. Predição em Novos Exemplos de Código

Para usar o modelo treinado em novos exemplos de código, execute `predict.py` passando o caminho para o arquivo de código como argumento.

```bash
python src/predict.py vuln-codes/safe_code.py
```

O script analisará o código e indicará se ele é "Provavelmente vulnerável" ou "Provavelmente seguro" com base nos padrões aprendidos durante o treinamento.

## Exemplo de Código Não Vulnerável para Teste

Aqui está um exemplo de código seguro em Python que pode ser usado para teste com o modelo:

```python
def greet_user(username):
    if username.isalnum():
        print(f"Olá, {username}!")
    else:
        print("Nome de usuário inválido.")

def calculate_sum(a, b):
    return a + b

def main():
    greet_user("Alice123")
    result = calculate_sum(10, 20)
    print(f"Resultado da soma: {result}")

if __name__ == "__main__":
    main()
```

Salve este código como `safe_code.py` e use o comando de predição para testá-lo:

```bash
python src/predict.py vuln-codes/safe_code.py
```

## Conclusão

Esse projeto fornece uma estrutura de machine learning para análise de vulnerabilidades em código. Ao incorporar dados de CVEs e exemplos de exploits, ele se torna uma ferramenta poderosa para auxiliar desenvolvedores e analistas de segurança na identificação de possíveis falhas de segurança em trechos de código.
