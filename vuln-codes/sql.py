import os
import sqlite3

# Função segura para executar comandos do sistema
def safe_command(user_input):
    # Verifica se a entrada é segura antes de usá-la
    if user_input.isalnum():  # Apenas caracteres alfanuméricos são permitidos
        os.system(f"echo {user_input}")
    else:
        print("Entrada inválida.")

# Função segura para consulta SQL
def safe_sql_query(user_input):
    # Usa query parametrizada para evitar SQL Injection
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = ?", (user_input,))
    results = cursor.fetchall()
    conn.close()
    return results

# Função para leitura de arquivos com controle de segurança
def safe_read_file(filename):
    # Garante que o arquivo está em um diretório específico
    base_path = "/safe_directory/"
    filepath = os.path.join(base_path, filename)

    # Verifica se o caminho do arquivo está dentro do diretório seguro
    if os.path.commonpath([base_path, os.path.abspath(filepath)]) == base_path:
        try:
            with open(filepath, 'r') as file:
                data = file.read()
                print(data)
        except FileNotFoundError:
            print("Arquivo não encontrado.")
    else:
        print("Acesso ao arquivo não permitido.")

# Função principal para testar
def main():
    # Exemplo seguro para a execução de comandos
    user_input = "safeInput123"
    safe_command(user_input)

    # Exemplo seguro para consulta SQL
    user_input = "admin"
    print(safe_sql_query(user_input))

    # Exemplo seguro para leitura de arquivos
    filename = "safe_file.txt"
    safe_read_file(filename)

if __name__ == "__main__":
    main()
