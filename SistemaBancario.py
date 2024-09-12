from datetime import datetime
import pytz

horario_local = pytz.timezone("America/Sao_Paulo")

class Transacao:
    def registrar(self, conta):
        raise NotImplementedError()


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor > 0:
            conta.saldo += self.valor
            data_hora = datetime.now(horario_local).strftime('%d/%m/%Y %H:%M:%S')
            conta.historico.adicionar_transacao(f"{data_hora} - Depósito: R$ {self.valor:.2f}")
            print(f"Depósito de R$ {self.valor:.2f} realizado com sucesso!")

        else:
            print("Valor inválido para depósito.")


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):

        if conta.numero_saques >= conta.limite_saques:
            print("Número máximo de saques diários excedido!")

        elif self.valor > conta.saldo:
            print("Saldo insuficiente!")

        elif self.valor > conta.limite:
            print("O valor do saque excede o limite permitido!")

        elif self.valor > 0:
            conta.saldo -= self.valor
            data_hora = datetime.now(horario_local).strftime('%d/%m/%Y %H:%M:%S')
            conta.historico.adicionar_transacao(f"{data_hora} - Saque: R$ {self.valor:.2f}")
            conta.numero_saques += 1
            print(f"Saque de R$ {self.valor:.2f} realizado com sucesso!")

        else:
            print("Valor inválido para saque.")


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)


class Conta:
    def __init__(self, cliente, numero):
        self.saldo = 0.0
        self.numero = numero
        self.limite = 500
        self.cliente = cliente
        self.historico = Historico()
        self.numero_saques = 0
        self.limite_saques = 3

    def sacar(self, valor):
        saque = Saque(valor)
        saque.registrar(self)

    def depositar(self, valor):
        deposito = Deposito(valor)
        deposito.registrar(self)

    def exibir_extrato(self):
        print("\n============== EXTRATO ==============")
        if not self.historico.transacoes:
            print("Não foram realizadas movimentações.")
        else:
            for transacao in self.historico.transacoes:
                print(transacao)
        print(f"\nSaldo atual: R$ {self.saldo:.2f}")
        print("=======================================")


class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite_saques = limite_saques


class Cliente:
    def __init__(self, nome, cpf, endereco):
        self.nome = nome
        self.cpf = cpf
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)


usuarios = []
contas = []
numero_conta = 1


def criar_usuario(nome, cpf, endereco):
    global usuarios

    for usuario in usuarios:
        if usuario.cpf == cpf:
            print("Usuário com este CPF já existe!")
            return

    novo_usuario = Cliente(nome, cpf, endereco)
    usuarios.append(novo_usuario)
    print("Usuário criado com sucesso!")


def criar_conta_corrente(cpf):
    global numero_conta

    for usuario in usuarios:
        if usuario.cpf == cpf:
            nova_conta = ContaCorrente(usuario, numero_conta)
            usuario.adicionar_conta(nova_conta)
            contas.append(nova_conta)
            numero_conta += 1
            print("Conta criada com sucesso!")
            return

    print("Usuário não encontrado!")


def listar_contas():
    if not contas:
        print("Não foram encontradas contas no sistema!")
    else:
        for conta in contas:
            print(f"Agência: 0001, Conta: {conta.numero}, Cliente: {conta.cliente.nome}")


def menu_principal():
    print("""
                
[1] Depositar
[2] Sacar
[3] Extrato
[4] Criar Usuário
[5] Criar Conta Corrente
[6] Listar Contas
[0] Sair

""")
    
    return input()

while True:
    opcao = menu_principal()

    if opcao == "1":
        valor = input("Informe o valor do depósito: ")
        conta_num = int(input("Informe o número da conta: "))

        for conta in contas:
            if conta.numero == conta_num:
                conta.depositar(float(valor))
                break
        else:
            print("Conta não encontrada!")

    elif opcao == "2":
        valor = input("Informe o valor do saque: ")
        conta_num = int(input("Informe o número da conta: "))
        for conta in contas:
            if conta.numero == conta_num:
                conta.sacar(float(valor))
                break
        else:
            print("Conta não encontrada!")

    elif opcao == "3":
        conta_num = int(input("Informe o número da conta: "))
        for conta in contas:
            if conta.numero == conta_num:
                conta.exibir_extrato()
                break
        else:
            print("Conta não encontrada!")

    elif opcao == "4":
        nome = input("Informe o nome do usuário: ")
        cpf = input("Informe o CPF (somente números): ")
        endereco = input("Informe o endereço: ")
        criar_usuario(nome, cpf, endereco)

    elif opcao == "5":
        cpf = input("Informe o CPF do usuário: ")
        criar_conta_corrente(cpf)

    elif opcao == "6":
        listar_contas()

    elif opcao == "0":
        break

    else:
        print("Opção inválida! Escolha novamente.")
