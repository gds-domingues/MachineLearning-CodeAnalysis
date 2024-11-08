import os
import json

# Diretório onde está o repositório clonado
BASE_DIR = 'algorithms-python'
OUTPUT_FILE = 'data/safe_code_examples.json'

def extract_functions(file_path):
    functions = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    function_code = ""
    recording = False

    for line in lines:
        if line.strip().startswith("def "):  # Início de uma função
            if recording:
                functions.append(function_code.strip())
                function_code = ""
            recording = True
        if recording:
            function_code += line

    if function_code:  # Adiciona a última função capturada
        functions.append(function_code.strip())

    return functions

def collect_safe_codes():
    safe_code_examples = []

    # Percorre todos os arquivos no diretório do repositório clonado
    for root, _, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith('.py'):  # Apenas arquivos Python
                file_path = os.path.join(root, file)
                functions = extract_functions(file_path)
                for func in functions:
                    safe_code_examples.append({
                        "description": "Function from The Algorithms repository",
                        "code": func,
                        "label": "seguro"
                    })
    
    # Salvar como JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(safe_code_examples, f, indent=4)

    print(f"Arquivo de códigos seguros salvo em: {OUTPUT_FILE}")

if __name__ == "__main__":
    collect_safe_codes()
