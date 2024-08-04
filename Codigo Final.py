from abc import ABC, abstractmethod

class LojaInterface(ABC):
    
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
    def editar_empresa(self, cnpj, novo_nome=None):
        pass
    
    @abstractmethod
    def cadastrar_cliente(self, nome, cpf, idade):
        pass
    
    @abstractmethod
    def excluir_cliente(self, cpf):
        pass
    
    @abstractmethod
    def listar_cliente(self):
        pass
    
    @abstractmethod
    def editar_cliente(self, cpf, novo_nome=None, nova_idade=None):
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
    def editar_produto(self, cnpj_empresa, nome_produto, novo_nome=None, novo_preco=None, nova_plataforma=None, nova_categoria=None, nova_promocao=None):
        pass
    
    @abstractmethod
    def comprar_jogo(self, cpf_cliente, nome_produto):
        pass
    
    @abstractmethod
    def exibir_historico_cliente(self, cpf_cliente):
        pass
    
    @abstractmethod
    def exibir_jogos_comprados(self, cpf_cliente):
        pass
    
    @abstractmethod
    def exibir_relatorio_financeiro(self):
        pass
    
    @abstractmethod
    def executar(self):
        pass
    
class ProdutoInterface(ABC):
    
    @abstractmethod
    def nome(self):
        pass
    
    @abstractmethod
    def aplicar_taxa_loja(self, preco):
        pass
    
    @abstractmethod
    def aplicar_promocao(self):
        pass
    
    @abstractmethod
    def definir_promocao(self, tipo_promocao):
        pass

    @abstractmethod
    def __str__(self):
        pass

class Base:
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
    
class Jogo(Base,ProdutoInterface):
    def __init__(self, nome, preco_original, chave, plataforma=None, categoria=None):
        super().__init__(nome, chave)
        self._preco_original = preco_original
        self._plataforma = plataforma
        self._categoria = categoria
        self._promocao = None
        self._preco_com_taxa = self.aplicar_taxa_loja(preco_original)

    def aplicar_taxa_loja(self, preco):
        return preco * 1.30  # Supondo uma taxa de 30%

    def definir_promocao(self, tipo_promocao):
        if tipo_promocao == 'lançamento':
            self._promocao = 0.10  # 10% de desconto
        elif tipo_promocao == 'fim de ano':
            self._promocao = 0.20  # 20% de desconto
        else:
            self._promocao = None

    def aplicar_promocao(self):
        preco_com_taxa = self.aplicar_taxa_loja(self._preco_original)
        if self._promocao:
            preco_final = preco_com_taxa * (1 - self._promocao)
        else:
            preco_final = preco_com_taxa
        return preco_final

    def get_nome(self):
        return self._nome
    
    def __str__(self):
        preco_com_taxa = self.aplicar_taxa_loja(self._preco_original)
        preco_final = self.aplicar_promocao()
        return (f'Nome: {self._nome}, Empresa: {self._chave}, '
                f'Plataforma: {self._plataforma or "N/A"}, Categoria: {self._categoria or "N/A"}, '
                f'Preço Original: R${self._preco_original:.2f}, '
                f'Preço com Taxa: R${preco_com_taxa:.2f}, '
                f'Preço com Taxa e Desconto: R${preco_final:.2f}')

class Empresa(Base):
    def __init__(self, nome, chave):
        super().__init__(nome, chave)
        self._produtos = []

    @property
    def produtos(self):
        return self._produtos

    def adicionar_produto(self, produto):
        self._produtos.append(produto)

    def remover_produto(self, nome_produto):
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

class Cliente(Base):
    def __init__(self, nome, chave, idade):
        super().__init__(nome, chave)
        self._idade = idade
        self._saldo = 0
        self._jogos_comprados = []

    @property
    def nome(self):
        return self._nome

    @property
    def chave(self):
        return self._chave
    
    @property
    def jogos_comprados(self):
        return self._jogos_comprados

    def adicionar_saldo(self, valor):
        self._saldo += valor

    def remover_saldo(self, valor):
        if self._saldo >= valor:
            self._saldo -= valor
            return True
        return False
    
    def remover_jogo(self, nome_jogo):
        if nome_jogo in self._jogos_comprados:
            self._jogos_comprados.remove(nome_jogo)

    def listar_jogos(self):
        return self._jogos_comprados

    def __str__(self):
        return f'{self._nome} (CPF: {self._chave}, Idade: {self._idade}, Saldo: R${self._saldo:.2f})'

class Loja(LojaInterface):
    def __init__(self):
        self._empresas = {}
        self._clientes = {}
        self._receita = 0
        self._lucro = 0
        self._historico = []  # Adiciona o atributo para o histórico

    def adicionar_empresa(self, empresa):
        self._empresas[empresa.chave] = empresa

    def adicionar_cliente(self, cliente):
        self._clientes[cliente.chave] = cliente

    def cadastrar_empresa(self, nome, cnpj):
        if any(empresa.chave == cnpj for empresa in self._empresas.values()):  
            print(f'Já existe uma empresa cadastrada com o CNPJ {cnpj}.')
            return
        if any(empresa.nome == nome for empresa in self._empresas.values()): 
            print(f'Já existe uma empresa cadastrada com o nome {nome}.')
            return

        empresa = Empresa(nome, cnpj)
        self.adicionar_empresa(empresa)
        print(f'Empresa {nome} cadastrada com sucesso.')

    def excluir_empresa(self, cnpj):
        empresa = self._empresas[cnpj]

        if not empresa:
            print('Empresa não encontrada.')
            return
        
        
        del self._empresas[cnpj]
        print('Empresa removida com sucesso.')

    def listar_empresa(self):
        empresas = [str(empresa) for empresa in self._empresas.values()]
        
        if not empresas:
            print('Não existe nenhum cadastro ainda.')
            return []  
        
        return empresas

    def editar_empresa(self, cnpj, novo_nome=None):
        empresa = self._empresas.get(cnpj)
        if empresa:
            if novo_nome:
                empresa._nome = novo_nome
            print('Empresa editada com sucesso.')
        else:
            print('Empresa não encontrada.')

    def cadastrar_cliente(self, nome, cpf, idade):
        # Verificar se o CPF já está cadastrado
        if cpf in self._clientes:
            print(f'CPF {cpf} já cadastrado .')
            return
        
        if idade < 18:
            print(f'Cliente {nome} não pode ser cadastrado, idade menor que 18 anos.')
            return
        
        cliente = Cliente(nome, cpf, idade)
        self.adicionar_cliente(cliente)
        print(f'Cliente {nome} cadastrado com sucesso.')

    def excluir_cliente(self, cpf):
        cliente = self._clientes.get(cpf)
        if cliente:
            if cliente._jogos_comprados:
                print('Cliente não pode ser removido porque possui jogos comprados.')
            else:
                del self._clientes[cpf]
                print('Cliente removido com sucesso.')
        else:
            print('Cliente não encontrado.')

    def listar_cliente(self):
        clientes = [str(cliente) for cliente in self._clientes.values()]
        
        if not clientes:
            print('Ainda não foi cadastrado nenhum cliente')
            return []  # Retorne uma lista vazia para evitar o erro de iteração
        
        return clientes
    
    def editar_cliente(self, cpf, novo_nome=None, nova_idade=None):
        cliente = self._clientes.get(cpf)
    
        if cliente:
            if novo_nome is not None:
                cliente._nome = novo_nome
            
            if nova_idade is not None:
                if isinstance(nova_idade, int) and nova_idade >= 17:
                    cliente._idade = nova_idade
                else:
                    print('Idade deve ser 18 anos ou mais')
                    return  
            
            print(f'Cliente com CPF {cpf} atualizado com sucesso.')
        else:
            print(f'Cliente com CPF {cpf} não encontrado.')
            
    def cadastrar_produto(self, cnpj_empresa, nome_produto, preco, plataforma=None, categoria=None, tipo_promocao=None):
        empresa = self._empresas.get(cnpj_empresa)
        if empresa:
            # Verificar se o produto já está cadastrado
            if empresa.buscar_produto(nome_produto):
                print(f'O produto {nome_produto} já está cadastrado para a empresa {empresa._nome}.')
                return

            novo_jogo = Jogo(nome_produto, preco, empresa._nome, plataforma, categoria)
            if tipo_promocao:
                novo_jogo.definir_promocao(tipo_promocao)
            empresa.adicionar_produto(novo_jogo)
            print(f'Produto {nome_produto} cadastrado com sucesso para a empresa {empresa._nome}.')
        else:
            print('Empresa não encontrada.')
   
    def excluir_produto(self, cnpj_empresa, nome_produto):
        
        empresa = self._empresas.get(cnpj_empresa)
        if not empresa:
            print('Empresa não encontrada.')
            return

        
        produto_existe = False
        for cliente in self._clientes.values():
            if nome_produto in cliente._jogos_comprados:
                print('Não é possível excluir o produto, pois ele foi comprado por um cliente.')
                return

       
        produto_existe = empresa.remover_produto(nome_produto)
        if produto_existe:
            print('Produto removido com sucesso.')
        else:
            print('Produto não encontrado.')

    def listar_produto(self):
        produtos = []
        for empresa in self._empresas.values():
            produtos.extend(empresa.listar_produtos())
        
        if not produtos:
            print('Não possui produto cadastrado ainda.')
            return []  # Retorne uma lista vazia para evitar o erro de iteração
        
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
                    produto._preco_com_taxa = produto.aplicar_taxa_loja(novo_preco)
                    produto.definir_promocao(produto._promocao)  # Reaplicar promoção com o novo preço
                if nova_plataforma:
                    produto._plataforma = nova_plataforma
                if nova_categoria:
                    produto._categoria = nova_categoria
                if nova_promocao is not None:
                    produto.definir_promocao(nova_promocao)
                    # Recalcula o preço com a nova promoção
                    produto._preco_com_taxa = produto.aplicar_taxa_loja(produto._preco_original)
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

                # Registra o jogo como comprado pelo cliente
                cliente._jogos_comprados.append(nome_produto)

                print(f'Compra realizada com sucesso! Produto: {nome_produto}, Valor: R${preco_final:.2f}, Cliente: {cliente.nome}')
            else:
                print('Saldo insuficiente para realizar a compra.')
        else:
            print('Produto não encontrado.')

    def exibir_historico_cliente(self, cpf_cliente):
        cliente = self._clientes.get(cpf_cliente)
        if cliente:
            # Filtra o histórico para mostrar apenas compras, excluindo reembolsos
            compras_cliente = [compra for compra in self._historico if compra[0] == cliente.nome and compra[2] > 0]
            if compras_cliente:
                print(f"Histórico de Compras do Cliente {cliente.nome}:")
                for compra in compras_cliente:
                    nome_cliente, nome_produto, preco_final = compra
                    print(f'Produto: {nome_produto}, Valor: R${preco_final:.2f}, Ação: Comprado')
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

    def exibir_relatorio_financeiro(self):
        print(f'\nRelatório Financeiro:')
        print(f'Receita Total: R${self._receita:.2f}')
        print(f'Lucro Total: R${self._lucro:.2f}')

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
                self.exibir_relatorio_financeiro()
            elif opcao == '6':
                print('Saindo do sistema...')
                break
            else:
                print('Opção inválida. Tente novamente.')


    def mostrar_menu_principal(self):
        print('\n1. Menu Clientes\n2. Menu Empresas\n3. Menu Produtos\n4. Menu Compras\n5. Exibir Relatório Financeiro\n6. Sair\n')

    def menu_clientes(self):
        while True:
            print('\n1. Cadastrar Cliente\n2. Editar Cliente\n3. Excluir Cliente\n4. Listar Clientes\n5. Listar Jogos do Cliente\n6. Adicionar Saldo\n7. Remover Saldo\n8. Voltar\n')
            opcao = input('Escolha uma opção: ')
            
            if opcao == '1':
                nome = input('Nome do Cliente: ')
                cpf = input('CPF do Cliente: ')
                
                while True:
                    try:
                        idade = int(input('Idade do Cliente: '))
                        if idade < 0:
                            print('Idade deve ser um número positivo.')
                        else:
                            break
                    except ValueError:
                        print('Idade deve ser um número inteiro. Tente novamente.')
                        
                self.cadastrar_cliente(nome, cpf, idade)
                
            elif opcao == '2':
                cpf = input('CPF do Cliente: ')
                novo_nome = input('Novo Nome do Cliente (deixe em branco para não alterar): ')
                
                while True:
                    nova_idade = input('Nova Idade do Cliente (deixe em branco para não alterar): ')
                    if nova_idade == '':
                        nova_idade = None
                        break
                    try:
                        nova_idade = int(nova_idade)
                        if nova_idade < 0:
                            print('Idade deve ser um número positivo.')
                        else:
                            break
                    except ValueError:
                        print('Idade deve ser um número inteiro. Tente novamente.')


                        
                self.editar_cliente(cpf, novo_nome, nova_idade)
                
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
                cpf_cliente = input('CPF do Cliente: ')
                cliente = self._clientes.get(cpf_cliente)
                if cliente:
                    while True:
                        try:
                            valor = float(input("Digite o valor que deseja adicionar à sua Carteira Steam Verde: "))
                            if valor < 0:
                                print("O valor deve ser positivo.")
                            else:
                                cliente.adicionar_saldo(valor)
                                print(f"Saldo adicionado com sucesso. Novo saldo: R${cliente._saldo:.2f}")
                                break
                        except ValueError:
                            print("Digite um valor numérico válido.")
                else:
                    print("Cliente não encontrado.")
                    
            elif opcao == '7':
                cpf_cliente = input('CPF do Cliente: ')
                cliente = self._clientes.get(cpf_cliente)
                if cliente:
                    while True:
                        try:
                            valor = float(input("Digite o valor que deseja remover da sua Carteira Steam Verde: "))
                            if valor < 0:
                                print("O valor deve ser positivo.")
                            elif cliente.remover_saldo(valor):
                                print(f"Saldo removido com sucesso. Novo saldo: R${cliente._saldo:.2f}")
                                break
                            else:
                                print("Saldo insuficiente para a remoção.")
                                break
                        except ValueError:
                            print("Digite um valor numérico válido.")
                else:
                    print("Cliente não encontrado.")
                    
            elif opcao == '8':
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
                nome_produto = input('Nome do Jogo: ')
                
                while True:
                    try:
                        preco = float(input('Preço do Jogo: '))
                        if preco < 0:
                            print('O preço deve ser um valor positivo.')
                        else:
                            break
                    except ValueError:
                        print('Preço deve ser um número válido. Tente novamente.')
                        
                plataforma = input('Plataforma do Jogo: ')
                categoria = input('Categoria do Jogo: ')
                tipo_promocao = input('Tipo de Promoção (lançamento/fim de ano/deixe em branco para nenhuma): ')
                self.cadastrar_produto(cnpj_empresa, nome_produto, preco, plataforma, categoria, tipo_promocao)
            
            elif opcao == '2':
                cnpj_empresa = input('CNPJ da Empresa: ')
                nome_produto = input('Nome do Jogo: ')
                novo_nome = input('Novo Nome do Jogo (deixe em branco para não alterar): ')
                
                while True:
                    novo_preco = input('Novo Preço do Jogo (deixe em branco para não alterar): ')
                    if novo_preco == '':
                        novo_preco = None
                        break
                    try:
                        novo_preco = float(novo_preco)
                        if novo_preco < 0:
                            print('O preço deve ser um valor positivo.')
                        else:
                            break
                    except ValueError:
                        print('Preço deve ser um número válido. Tente novamente.')
                        
                nova_plataforma = input('Nova Plataforma do Jogo (deixe em branco para não alterar): ')
                nova_categoria = input('Nova Categoria do Jogo (deixe em branco para não alterar): ')
                nova_promocao = input('Nova Promoção do Jogo (lançamento/fim de ano/deixe em branco para nenhuma): ')
                self.editar_produto(cnpj_empresa, nome_produto, novo_nome, novo_preco, nova_plataforma, nova_categoria, nova_promocao)
            
            elif opcao == '3':
                cnpj_empresa = input('CNPJ da Empresa: ')
                nome_produto = input('Nome do Jogo: ')
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
            print('\n1. Comprar Jogo\n2. Exibir Histórico de Compras\n3. Voltar\n')
            opcao = input('Escolha uma opção: ')
            
            if opcao == '1':
                cpf_cliente = input("CPF do Cliente: ")
                nome_produto = input("Nome do Jogo: ")
                self.comprar_jogo(cpf_cliente, nome_produto)
            elif opcao == '2':
                cpf_cliente = input("CPF do Cliente: ")
                self.exibir_historico_cliente(cpf_cliente)
            elif opcao == '3':
                break
            else:
                print('Opção inválida. Tente novamente.')


loja = Loja()
loja.executar()

