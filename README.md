# Vulnerability Detection in Code Using Machine Learning

This project uses machine learning to detect vulnerabilities in code samples. With a combination of Convolutional Neural Networks (CNN) and LSTM networks, the model analyzes descriptions and code examples to identify patterns associated with common vulnerabilities.

## Objective

The goal is to provide a tool that assists in code security analysis by automatically detecting potential vulnerabilities. This project can be applied to a variety of programming languages and vulnerability types, making it especially useful for developers and security analysts.

## Project Structure

```
vulnhub/
├── data/
│   ├── files_exploits.csv          # Exploit data from Exploit-DB
│   ├── files_shellcodes.csv         # Shellcode data from Exploit-DB
│   └── nvdcve-1.1-2024.json         # CVE JSON file for training
├── models/
│   ├── model_cnn_lstm.h5            # Trained model file
│   └── tokenizer.pkl                # Tokenizer for text preprocessing
├── vuln-codes/
│   ├── buffer-overflow.c            # Vulnerable code example for testing
│   └── safe_code.py                 # Safe code example for testing
├── src/
│   ├── preprocess.py                # Script for data preprocessing
│   ├── train.py                     # Script for model training
│   └── predict.py                   # Script for prediction on new code
└── README.md                        # Project description (this file)
```

## Environment Setup

### Prerequisites

- **Python 3.8+**
- **Python Libraries**:
  - TensorFlow
  - Pandas
  - NumPy
  - Scikit-learn
  - h5py

### Installing Dependencies

To install dependencies, create and activate a virtual environment and then install the packages listed in `requirements.txt`:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

## Project Usage

### 1. Data Preprocessing

The `preprocess.py` script processes data from the `files_exploits.csv`, `files_shellcodes.csv`, and `nvdcve-1.1-2024.json` files. It tokenizes the descriptions and code examples, preparing them for model training.

```bash
python src/preprocess.py
```

### 2. Model Training

After preprocessing, the `train.py` script trains the CNN + LSTM model using the tokenized data.

```bash
python src/train.py
```

This will save the trained model in `models/model_cnn_lstm.h5`.

### 3. Prediction on New Code Examples

To use the trained model on new code examples, run `predict.py`, passing the path to the code file as an argument.

```bash
python src/predict.py vuln-codes/safe_code.py
```

The script will analyze the code and indicate whether it is "Probably Vulnerable" or "Probably Safe" based on the patterns learned during training.

## Example of Non-Vulnerable Code for Testing

Here is an example of safe Python code that can be used for testing with the model:

```python
def greet_user(username):
    if username.isalnum():
        print(f"Hello, {username}!")
    else:
        print("Invalid username.")

def calculate_sum(a, b):
    return a + b

def main():
    greet_user("Alice123")
    result = calculate_sum(10, 20)
    print(f"Sum result: {result}")

if __name__ == "__main__":
    main()
```

Save this code as `safe_code.py` and use the prediction command to test it:

```bash
python src/predict.py vuln-codes/safe_code.py
```

## Conclusion

This project provides a machine learning framework for vulnerability analysis in code. By incorporating CVE data and exploit examples, it becomes a powerful tool to help developers and security analysts identify potential security flaws in code snippets.
