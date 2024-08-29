print ("Bem vindo ao Banco X digital")

print("Escolha as opções abaixo:")

menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair

=> """

saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)

    if opcao == "1":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            saldo += valor
            extrato.append(f"Depósito: R$ {valor:.2f}")
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")

        else:
            print("Valor inválido para depósito.")

    elif opcao == "2":
        if numero_saques >= LIMITE_SAQUES:
            print("Número máximo (3) de saques diários excedido!")

        else:
            valor = float(input("Informe o valor do saque: "))
            excedeu_saldo = valor > saldo
            excedeu_limite = valor > limite

            if excedeu_saldo:
                print("Saldo insuficiente!")

            elif excedeu_limite:
                print("O valor do saque excede o limite permitido!")

            elif valor > 0:
                saldo -= valor
                extrato.append(f"Saque: R$ {valor:.2f}")
                numero_saques += 1
                print(f"Saque de R$ {valor:.2f} realizado com sucesso!")

            else:
                print("Valor inválido para saque.")

    elif opcao == "3":
        print("\n============== EXTRATO ==============")
        
        if not extrato:
            print("Não foram realizadas movimentações.")
            
        else:
            for movimento in extrato:
                print(movimento)
        print(f"\nSaldo atual: R$ {saldo:.2f}")
        print("=============================")

    elif opcao == "0":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada!")