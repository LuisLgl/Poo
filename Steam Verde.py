from abc import ABC, abstractmethod

class FuncBase(ABC):

    @abstractmethod
    def editar_cliente(self, cpf, novo_nome=None, novo_saldo=None):
        pass

    @abstractmethod    
    def cadastrar_cliente(self, nome, cpf, saldo=0):
        pass

    @abstractmethod
    def excluir_cliente(self, cpf):
        pass

    @abstractmethod
    def listar_cliente(self):
        pass
    
    @abstractmethod
    def editar_empresa(self, cnpj, novo_nome=None):
        pass

    @abstractmethod    
    def cadastrar_empresa(self, nome, cnpj):
        pass

    @abstractmethod
    def excluir_empresa(self, cnpj):
        pass

    @abstractmethod
    def listar_empresa(self):
        pass

    @abstractmethod
    def editar_produto(self, cnpj_empresa, nome_produto, novo_nome=None, novo_preco=None, nova_plataforma=None, nova_categoria=None, nova_promocao=None):
        pass

    @abstractmethod    
    def cadastrar_produto(self, cnpj_empresa, nome_produto, preco, plataforma=None, categoria=None, tipo_promocao=None):
        pass

    @abstractmethod
    def excluir_produto(self, cnpj_empresa, nome_produto):
        pass
    
    @abstractmethod
    def listar_produto(self):
        pass
    
    @abstractmethod
    def executar(self):
        pass
    

# Interface para produtos
class ProdutoInterface(ABC):
    @abstractmethod
    def aplicar_promocao(self):
        pass

    @abstractmethod
    def aplicar_taxa_loja(self):
        pass

    @abstractmethod
    def definir_promocao(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

# Classe base para Entidades
class Entidade:
    def __init__(self, nome, chave):
        self._nome = nome
        self._chave = chave

    @property
    def nome(self):
        return self._nome

    @property
    def chave(self):
        return self._chave

    def __str__(self):
        return f'{self._nome} - {self._chave}'

# Classe Produto com interface
class Produto:
    def __init__(self, nome, preco, empresa=None):
        self._nome = nome
        self._preco = preco
        self._preco_original = preco
        self._empresa = empresa
        self._promocao = None  # Promoção inicial como None

    @property
    def nome(self):
        return self._nome

    def aplicar_taxa_loja(self, preco):
        return preco * 1.30

    def aplicar_promocao(self):
        preco_com_taxa = self.aplicar_taxa_loja(self._preco_original)
        if self._promocao == 'lançamento':
            return preco_com_taxa * 0.90  # 10% de desconto para lançamento
        elif self._promocao == 'fim de ano':
            return preco_com_taxa * 0.85  # 15% de desconto para fim de ano
        return preco_com_taxa

    def definir_promocao(self, tipo_promocao):
        self._promocao = tipo_promocao
        self._preco = self._preco_original  # Reverte para o preço original antes de aplicar nova promoção
        preco_com_taxa = self.aplicar_taxa_loja(self._preco)
        if tipo_promocao == 'lançamento':
            self._preco = preco_com_taxa * 0.90
        elif tipo_promocao == 'fim de ano':
            self._preco = preco_com_taxa * 0.85

    def __str__(self):
        preco_original = self._preco_original
        preco_com_taxa = self._aplicar_taxa_loja(preco_original)
        preco_final = self.aplicar_promocao()
        return (f'{self._nome} - Preço Original: R${preco_original:.2f}, '
                f'Preço com Taxa: R${preco_com_taxa:.2f}, '
                f'Preço com Promoção: R${preco_final:.2f} - Empresa: {self._empresa}')

# Classe Jogo que herda de Produto
class Jogo:
    def __init__(self, nome, preco_original, nome_empresa, plataforma=None, categoria=None):
        self._nome = nome
        self._preco_original = preco_original
        self._nome_empresa = nome_empresa
        self._plataforma = plataforma
        self._categoria = categoria
        self._promocao = None
        self._preco_com_taxa = self._aplicar_taxa_loja(preco_original)

    def _aplicar_taxa_loja(self, preco):
        return preco * 1.30  # Supondo uma taxa de 30%

    def definir_promocao(self, tipo_promocao):
        if tipo_promocao == 'lançamento':
            self._promocao = 0.10  # 10% de desconto
        elif tipo_promocao == 'fim de ano':
            self._promocao = 0.20  # 20% de desconto
        else:
            self._promocao = None

    def aplicar_promocao(self):
        preco_com_taxa = self._aplicar_taxa_loja(self._preco_original)
        if self._promocao:
            preco_final = preco_com_taxa * (1 - self._promocao)
        else:
            preco_final = preco_com_taxa
        return preco_final

    def get_nome(self):
        return self._nome
    
    def __str__(self):
        preco_com_taxa = self._aplicar_taxa_loja(self._preco_original)
        preco_final = self.aplicar_promocao()
        return (f'Nome: {self._nome}, Empresa: {self._nome_empresa}, '
                f'Plataforma: {self._plataforma or "N/A"}, Categoria: {self._categoria or "N/A"}, '
                f'Preço Original: R${self._preco_original:.2f}, '
                f'Preço com Taxa: R${preco_com_taxa:.2f}, '
                f'Preço com Taxa e Desconto: R${preco_final:.2f}')


# Classe Empresa
class Empresa(Entidade):
    def __init__(self, nome, cnpj):
        super().__init__(nome, cnpj)
        self._produtos = []

    def _adicionar_produto(self, produto):
        self._produtos.append(produto)

    def _remover_produto(self, nome_produto):
        self._produtos = [produto for produto in self._produtos if produto.nome != nome_produto]

    def listar_produtos(self):
        return [str(produto) for produto in self._produtos]

    def buscar_produto(self, nome_produto):
        for produto in self._produtos:
            if produto.get_nome() == nome_produto:
                return produto
        return None

    def __str__(self):
        return f'{self.nome} - CNPJ: {self.chave}'

# Classe Cliente
class Cliente:
    def __init__(self, nome, cpf, saldo=0):
        self._nome = nome
        self._cpf = cpf
        self._saldo = saldo
        self._jogos_comprados = set()  # Armazena os nomes dos jogos comprados

    @property
    def nome(self):
        return self._nome

    @property
    def chave(self):
        return self._cpf

    def adicionar_saldo(self, valor):
        self._saldo += valor

    def remover_saldo(self, valor):
        if self._saldo >= valor:
            self._saldo -= valor
            return True
        return False

    def comprar_jogo(self, nome_jogo):
        if nome_jogo in self._jogos_comprados:
            return False  # O cliente já comprou este jogo
        self._jogos_comprados.add(nome_jogo)
        return True

    def remover_jogo(self, nome_jogo):
        if nome_jogo in self._jogos_comprados:
            self._jogos_comprados.remove(nome_jogo)

    def listar_jogos(self):
        return self._jogos_comprados

    def __str__(self):
        return f'{self._nome} (CPF: {self._cpf}, Saldo: R${self._saldo:.2f})'


# Classe Loja
class Loja(FuncBase):
    def __init__(self):
        self._empresas = {}
        self._clientes = {}
        self._receita = 0
        self._lucro = 0
        self._historico = []  # Adiciona o atributo para o histórico

    def _adicionar_empresa(self, empresa):
        self._empresas[empresa.chave] = empresa

    def _adicionar_cliente(self, cliente):
        self._clientes[cliente.chave] = cliente

    def cadastrar_empresa(self, nome, cnpj):
        empresa = Empresa(nome, cnpj)
        self._adicionar_empresa(empresa)
        print(f'Empresa {nome} cadastrada com sucesso.')

    def excluir_empresa(self, cnpj):
        if cnpj in self._empresas:
            del self._empresas[cnpj]
            print('Empresa removida com sucesso.')
        else:
            print('Empresa não encontrada.')

    def listar_empresa(self):
        return [str(empresa) for empresa in self._empresas.values()]

    def editar_empresa(self, cnpj, novo_nome=None):
        empresa = self._empresas.get(cnpj)
        if empresa:
            if novo_nome:
                empresa._nome = novo_nome
            print('Empresa editada com sucesso.')
        else:
            print('Empresa não encontrada.')

    def cadastrar_cliente(self, nome, cpf, saldo=0):
        cliente = Cliente(nome, cpf, saldo)
        self._adicionar_cliente(cliente)
        print(f'Cliente {nome} cadastrado com sucesso.')

    def excluir_cliente(self, cpf):
        if cpf in self._clientes:
            del self._clientes[cpf]
            print('Cliente removido com sucesso.')
        else:
            print('Cliente não encontrado.')

    def listar_cliente(self):
        return [str(cliente) for cliente in self._clientes.values()]

    def editar_cliente(self, cpf, novo_nome=None, novo_saldo=None):
        cliente = self._clientes.get(cpf)
        if cliente:
            if novo_nome:
                cliente._nome = novo_nome
            if novo_saldo is not None:
                cliente._saldo = novo_saldo
            print('Cliente editado com sucesso.')
        else:
            print('Cliente não encontrado.')

    def cadastrar_produto(self, cnpj_empresa, nome_produto, preco, plataforma=None, categoria=None, tipo_promocao=None):
        empresa = self._empresas.get(cnpj_empresa)
        if empresa:
        
            novo_jogo = Jogo(nome_produto, preco, empresa._nome, plataforma, categoria)
            if tipo_promocao:
                novo_jogo.definir_promocao(tipo_promocao)
            empresa._adicionar_produto(novo_jogo)
            print(f'Produto {nome_produto} cadastrado com sucesso para a empresa {empresa._nome}.')
        else:
            print('Empresa não encontrada.')

    def excluir_produto(self, cnpj_empresa, nome_produto):
        empresa = self._empresas.get(cnpj_empresa)
        if empresa:
            empresa._remover_produto(nome_produto)
            print('Produto removido com sucesso.')
        else:
            print('Empresa não encontrada.')

    def listar_produto(self):
        produtos = []
        for empresa in self._empresas.values():
            produtos.extend(empresa.listar_produtos())
        return produtos

    def editar_produto(self, cnpj_empresa, nome_produto, novo_nome=None, novo_preco=None, nova_plataforma=None, nova_categoria=None, nova_promocao=None):
        empresa = self._empresas.get(cnpj_empresa)
        if empresa:
            produto = empresa.buscar_produto(nome_produto)
            if produto:
                if novo_nome:
                    produto._nome = novo_nome
                if novo_preco is not None:
                    produto._preco_original = novo_preco
                    produto._preco_com_taxa = produto._aplicar_taxa_loja(novo_preco)
                    produto.definir_promocao(produto._promocao)  # Reaplicar promoção com o novo preço
                if nova_plataforma:
                    produto._plataforma = nova_plataforma
                if nova_categoria:
                    produto._categoria = nova_categoria
                if nova_promocao is not None:
                    produto.definir_promocao(nova_promocao)
                    # Recalcula o preço com a nova promoção
                    produto._preco_com_taxa = produto._aplicar_taxa_loja(produto._preco_original)
                    produto._preco_final = produto.aplicar_promocao()
                    
                print('Produto editado com sucesso.')
            else:
                print('Produto não encontrado.')
        else:
            print('Empresa não encontrada.')


    
    def comprar_jogo(self, cpf_cliente, nome_produto):
        cliente = self._clientes.get(cpf_cliente)
        if not cliente:
            print('Cliente não encontrado.')
            return

        produto = None
        for empresa in self._empresas.values():
            produto = empresa.buscar_produto(nome_produto)
            if produto:
                break

        if produto:
            # Verifica se o cliente já comprou o jogo
            if nome_produto in cliente.listar_jogos():
                print(f'O cliente já comprou o jogo {nome_produto} anteriormente.')
                return

            preco_final = produto.aplicar_promocao()
            total_preco = preco_final

            if cliente.remover_saldo(total_preco):
                receita = total_preco
                lucro = total_preco * 0.30  # 30% de lucro para a loja

                self._receita += receita
                self._lucro += lucro
                self._historico.append((cliente.nome, nome_produto, preco_final))  # Adiciona a compra ao histórico

                print(f'Compra realizada com sucesso! Produto: {nome_produto}, Valor: R${preco_final:.2f}, Cliente: {cliente.nome}')
            else:
                print('Saldo insuficiente para realizar a compra.')
        else:
            print('Produto não encontrado.')
    
    def reembolsar_jogo(self, cpf_cliente, nome_jogo):
        cliente = self._clientes.get(cpf_cliente)
        if not cliente:
            print('Cliente não encontrado.')
            return False

        for empresa in self._empresas.values():
            produto = empresa.buscar_produto(nome_jogo)
            if produto and nome_jogo in cliente.listar_jogos():
                preco_final = produto.aplicar_promocao()
                cliente.adicionar_saldo(preco_final)
                cliente.remover_jogo(nome_jogo)
                self._receita -= preco_final
                self._lucro -= preco_final - produto._preco_original
                self._historico = [(c, j, p) for c, j, p in self._historico if not (c == cpf_cliente and j == nome_jogo)]
                print(f'Jogo {nome_jogo} reembolsado com sucesso para {cliente.nome}.')
                return True
        print(f'Jogo {nome_jogo} não encontrado para reembolso.')
        return False

    def exibir_historico_cliente(self, cpf_cliente):
        cliente = self._clientes.get(cpf_cliente)
        if cliente:
            compras_cliente = [compra for compra in self._historico if compra[0] == cliente.nome]
            if compras_cliente:
                print(f"Histórico de Compras do Cliente {cliente.nome}:")
                for compra in compras_cliente:
                    nome_cliente, nome_produto, preco_final = compra
                    acao = 'Comprado' if preco_final > 0 else 'Reembolsado'
                    valor_abs = abs(preco_final)
                    print(f'Produto: {nome_produto}, Valor: R${valor_abs:.2f}, Ação: {acao}')
            else:
                print(f'Nenhuma compra registrada para o cliente {cliente.nome}.')
        else:
            print('Cliente não encontrado.')


    def exibir_jogos_comprados(self, cpf_cliente):
        cliente = self._clientes.get(cpf_cliente)
        if not cliente:
            print('Cliente não encontrado.')
            return

        jogos_comprados = cliente.listar_jogos()
        if jogos_comprados:
            print(f'Jogos comprados por {cliente.nome}:')
            for jogo in jogos_comprados:
                print(jogo)
        else:
            print(f'O cliente {cliente.nome} ainda não comprou nenhum jogo.')


    def executar(self):
        while True:
            self.mostrar_menu_principal()
            opcao = input('Escolha uma opção: ')
            
            if opcao == '1':
                self.menu_clientes()
            elif opcao == '2':
                self.menu_empresas()
            elif opcao == '3':
                self.menu_produtos()
            elif opcao == '4':
                self.menu_compras()
            elif opcao == '5':
                break
            else:
                print('Opção inválida. Tente novamente.')

    def mostrar_menu_principal(self):
        print('\n1. Menu Clientes\n2. Menu Empresas\n3. Menu Produtos\n4. Menu Compras\n5. Sair\n')

    def menu_clientes(self):
        while True:
            print('\n1. Cadastrar Cliente\n2. Editar Cliente\n3. Excluir Cliente\n4. Listar Clientes\n5. Listar Jogos do Cliente\n6. Voltar\n')
            opcao = input('Escolha uma opção: ')
            
            if opcao == '1':
                nome = input('Nome do Cliente: ')
                cpf = input('CPF do Cliente: ')
                saldo = float(input('Saldo do Cliente: '))
                self.cadastrar_cliente(nome, cpf, saldo)
            elif opcao == '2':
                cpf = input('CPF do Cliente: ')
                novo_nome = input('Novo Nome do Cliente (deixe em branco para não alterar): ')
                novo_saldo = input('Novo Saldo do Cliente (deixe em branco para não alterar): ')
                novo_saldo = float(novo_saldo) if novo_saldo else None
                self.editar_cliente(cpf, novo_nome, novo_saldo)
            elif opcao == '3':
                cpf = input('CPF do Cliente: ')
                self.excluir_cliente(cpf)
            elif opcao == '4':
                for cliente in self.listar_cliente():
                    print(cliente)
            elif opcao == '5':
                cpf_cliente = input('CPF do Cliente: ')
                self.exibir_jogos_comprados(cpf_cliente)
            elif opcao == '6':
                break
            else:
                print('Opção inválida. Tente novamente.')

    def menu_empresas(self):
        while True:
            print('\n1. Cadastrar Empresa\n2. Editar Empresa\n3. Excluir Empresa\n4. Listar Empresas\n5. Voltar\n')
            opcao = input('Escolha uma opção: ')
            
            if opcao == '1':
                nome = input('Nome da Empresa: ')
                cnpj = input('CNPJ da Empresa: ')
                self.cadastrar_empresa(nome, cnpj)
            elif opcao == '2':
                cnpj = input('CNPJ da Empresa: ')
                novo_nome = input('Novo Nome da Empresa (deixe em branco para não alterar): ')
                self.editar_empresa(cnpj, novo_nome)
            elif opcao == '3':
                cnpj = input('CNPJ da Empresa: ')
                self.excluir_empresa(cnpj)
            elif opcao == '4':
                for empresa in self.listar_empresa():
                    print(empresa)
            elif opcao == '5':
                break
            else:
                print('Opção inválida. Tente novamente.')

    def menu_produtos(self):
        while True:
            print('\n1. Cadastrar Jogo\n2. Editar Jogo\n3. Excluir Jogo\n4. Listar Jogo\n5. Voltar\n')
            opcao = input('Escolha uma opção: ')
            
            if opcao == '1':
                cnpj_empresa = input('CNPJ da Empresa: ')
                nome_produto = input('Nome do Produto: ')
                preco = float(input('Preço do Produto: '))
                plataforma = input('Plataforma do Jogo: ')
                categoria = input('Categoria do Jogo: ')
                tipo_promocao = input('Tipo de Promoção (lançamento/fim de ano/deixe em branco para nenhuma): ')
                self.cadastrar_produto(cnpj_empresa, nome_produto, preco, plataforma, categoria, tipo_promocao)
            elif opcao == '2':
                cnpj_empresa = input('CNPJ da Empresa: ')
                nome_produto = input('Nome do Produto: ')
                novo_nome = input('Novo Nome do Produto (deixe em branco para não alterar): ')
                novo_preco = input('Novo Preço do Produto (deixe em branco para não alterar): ')
                novo_preco = float(novo_preco) if novo_preco else None
                nova_plataforma = input('Nova Plataforma do Produto (deixe em branco para não alterar): ')
                nova_categoria = input('Nova Categoria do Produto (deixe em branco para não alterar): ')
                nova_promocao = input('Nova Promoção do Produto (lançamento/fim de ano/deixe em branco para nenhuma): ')
                self.editar_produto(cnpj_empresa, nome_produto, novo_nome, novo_preco, nova_plataforma, nova_categoria, nova_promocao)
            elif opcao == '3':
                cnpj_empresa = input('CNPJ da Empresa: ')
                nome_produto = input('Nome do Produto: ')
                self.excluir_produto(cnpj_empresa, nome_produto)
            elif opcao == '4':
                for produto in self.listar_produto():
                    print(produto)
            elif opcao == '5':
                break
            else:
                print('Opção inválida. Tente novamente.')

    def menu_compras(self):
        while True:
            print('\n1. Comprar Jogo\n2. Reembolsar Jogo\n3. Exibir Histórico de Compras\n4. Voltar\n')
            opcao = input('Escolha uma opção: ')
            
            if opcao == '1':
                cpf_cliente = input("CPF do Cliente: ")
                nome_produto = input("Nome do Produto: ")
                self.comprar_jogo(cpf_cliente, nome_produto)
            elif opcao == '2':
                cpf_cliente = input('CPF do Cliente: ')
                nome_jogo = input('Nome do Jogo: ')
                self.reembolsar_jogo(cpf_cliente, nome_jogo)
            elif opcao == '3':
                cpf_cliente = input("CPF do Cliente: ")
                self.exibir_historico_cliente(cpf_cliente)
            elif opcao == '4':
                break
            else:
                print('Opção inválida. Tente novamente.')

# Exemplo de execução
loja = Loja()
loja.executar()