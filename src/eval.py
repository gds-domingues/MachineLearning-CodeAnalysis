def vulnerable_eval(user_input):
    eval("result = " + user_input)  # Permite execução de código arbitrário
    print(result)

# Exemplo de uso
user_input = "__import__('os').system('echo hacked')"  # Exploração de entrada
vulnerable_eval(user_input)