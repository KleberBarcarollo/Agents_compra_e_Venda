class Produto:
    def __init__(self, nome, preco, quantidade):
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade

class Estoque:
    def __init__(self):
        self.produtos = {}  # chave: nome, valor: Produto

    def adicionar_produto(self, nome, quantidade, preco):
        if nome in self.produtos:
            self.produtos[nome].quantidade += quantidade
            self.produtos[nome].preco = preco
        else:
            self.produtos[nome] = Produto(nome, preco, quantidade)

    def tem_produto(self, nome, quantidade):
        produto = self.produtos.get(nome)
        if produto is None:
            return False
        return produto.quantidade >= quantidade

    def obter_preco(self, nome):
        produto = self.produtos.get(nome)
        return produto.preco if produto else None

    def vender(self, nome, quantidade):
        if self.tem_produto(nome, quantidade):
            self.produtos[nome].quantidade -= quantidade
            return True
        return False