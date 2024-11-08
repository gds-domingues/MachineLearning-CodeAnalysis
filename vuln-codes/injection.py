import os

def vulnerable_command(user_input):
    os.system("echo " + user_input)

# Exemplo de uso
user_input = "malicious_code; rm -rf /"  # Entrada maliciosa de exemplo
vulnerable_command(user_input)
