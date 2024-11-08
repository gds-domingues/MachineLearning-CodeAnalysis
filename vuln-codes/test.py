def greet_user(username):
    # Garante que o nome é alfanumérico antes de usá-lo
    if username.isalnum():
        print(f"Olá, {username}!")
    else:
        print("Nome de usuário inválido.")

def calculate_sum(a, b):
    # Função simples para somar dois números
    return a + b

# Função principal para teste
def main():
    # Teste de saudação
    greet_user("Alice123")

    # Teste de soma
    result = calculate_sum(10, 20)
    print(f"Resultado da soma: {result}")

if __name__ == "__main__":
    main()
