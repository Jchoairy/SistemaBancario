from datetime import datetime
import pytz
import re

print("Bem vindo ao Banco X digital")

print("1-Para Depositar, 2-Para Sacar, 3-Para Extrato, 4-Para Criar Usuário, 5-Para Criar Conta Corrente, 6-Para Listar as Contas e 0-Para Sair")
print("Escolha as opções abaixo:")

menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[4] Criar Usuário
[5] Criar Conta Corrente
[6] Listar Contas
[0] Sair

=> """

saldo = 0
limite = 500
extrato = []
numero_saques = 0
numero_transacoes = 0

LIMITE_SAQUES = 3
LIMITE_TRANSACOES = 10

usuarios = []
contas = []
numero_conta = 1

horario_local = pytz.timezone("America/Sao_Paulo")

def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    try:
        valor = float(valor)
        
        if numero_saques >= limite_saques:
            print("Número máximo de saques diários excedido!")
        
        elif valor > saldo:
            print("Saldo insuficiente!")
        
        elif valor > limite:
            print("O valor do saque excede o limite permitido!")
        
        elif valor > 0:
            saldo -= valor
            data_hora = datetime.now(horario_local).strftime('%d/%m/%Y %H:%M:%S')
            extrato.append(f"{data_hora} - Saque: R$ {valor:.2f}")
            numero_saques += 1
            print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
        
        else:
            print("Valor inválido para saque.")

    except ValueError:
        print("Por favor, insira um valor numérico.")

    return saldo, extrato

def deposito(saldo, valor, extrato):
    try:
        valor = float(valor)
        
        if valor > 0:
            saldo += valor
            data_hora = datetime.now(horario_local).strftime('%d/%m/%Y %H:%M:%S')
            extrato.append(f"{data_hora} - Depósito: R$ {valor:.2f}")
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
        
        else:
            print("Valor inválido para depósito.")

    except ValueError:
        print("Por favor, insira um valor numérico.")

    return saldo, extrato

def exibir_extrato(saldo, *, extrato):
    print("\n============== EXTRATO ==============")
    
    if not extrato:
        print("Não foram realizadas movimentações.")
    
    else:
        for movimento in extrato:
            print(movimento)
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("=======================================")

def criar_usuario(nome, data_nascimento, cpf, endereco):
    
    for usuario in usuarios:
        
        if usuario['cpf'] == cpf:
            print("Usuário com este CPF já existe!")
            return
        
    usuario = {
        'nome': nome,
        'data_nascimento': data_nascimento,
        'cpf': cpf,
        'endereco': endereco
    }
    
    usuarios.append(usuario)
    print("Usuário criado com sucesso!")

def criar_conta_corrente(cpf):
    global numero_conta
    
    for usuario in usuarios:
        
        if usuario['cpf'] == cpf:
            conta = {
                'agencia': '0001',
                'numero_conta': numero_conta,
                'usuario': usuario
            }

            contas.append(conta)
            numero_conta += 1
            print("Conta criada com sucesso!")
            return
        
    print("Usuário não encontrado!")

def listar_contas():
    
    for conta in contas:
        print(f"Agência: {conta['agencia']}, Conta: {conta['numero_conta']}, Usuário: {conta['usuario']['nome']}")

def validar_nome(nome):
    
    return nome.isalpha()

def validar_cpf(cpf):
    
    return cpf.isdigit() and len(cpf) == 11

def validar_data(data):
    
    try:
        datetime.strptime(data, '%d/%m/%Y')
        return True
    
    except ValueError:
        return False

while True:
    opcao = input(menu)

    if opcao == "1":
        
        if numero_transacoes >= LIMITE_TRANSACOES:
            print("Número máximo (10) de transações diárias excedido!")
        
        else:
            valor = input("Informe o valor do depósito: ")
            saldo, extrato = deposito(saldo, valor, extrato)
            numero_transacoes += 1

    elif opcao == "2":

        if numero_transacoes >= LIMITE_TRANSACOES:
            print("Número máximo (10) de transações diárias excedido!")

        else:
            valor = input("Informe o valor do saque: ")
            saldo, extrato = saque(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)
            numero_transacoes += 1
            numero_saques += 1

    elif opcao == "3":
        exibir_extrato(saldo, extrato=extrato)

    elif opcao == "4":
        nome = input("Informe o seu nome do usuário: ")
        
        while not validar_nome(nome):
            print("Nome inválido! Por favor, insira apenas letras.")
            nome = input("Informe o seu nome do usuário: ")

        data_nascimento = input("Informe a sua data de nascimento (dd/mm/yyyy): ")
        
        while not validar_data(data_nascimento):
            print("Data de nascimento inválida! Por favor, use o formato dd/mm/yyyy.")
            data_nascimento = input("Informe a sua data de nascimento (dd/mm/yyyy): ")

        cpf = input("Informe o seu CPF (somente números): ")
        
        while not validar_cpf(cpf):
            print("CPF inválido! Por favor, insira apenas números e com 11 dígitos.")
            cpf = input("Informe o seu CPF (somente números): ")

        endereco = input("Informe o endereço (logradouro, N - bairro - cidade/sigla estado): ")

        criar_usuario(nome, data_nascimento, cpf, endereco)

    elif opcao == "5":
        cpf = input("Informe o CPF do usuário: ")
        criar_conta_corrente(cpf)

    elif opcao == "6":
        listar_contas()

    elif opcao == "0":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada!")

