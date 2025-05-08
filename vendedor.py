from maspy.agent import Agent
from maspy.messages import Tell
from produtos import Estoque

class Vendedor(Agent):
    def __init__(self, nome, margem_negociacao=0.15):
        super().__init__(nome)
        self.estoque = Estoque()
        self.margem = margem_negociacao

    def receber_mensagem(self, mensagem):
        """Processa todos os tipos de mensagens recebidas"""
        conteudo = mensagem.content
        tipo = conteudo.get('tipo')

        print(f"\n[DEBUG] {self.name} recebeu mensagem de {mensagem.sender}: {conteudo}")

        if tipo == 'interesse':
            self.processar_interesse(mensagem)
        elif tipo == 'contra_oferta':
            self.processar_contra_oferta(mensagem)
        elif tipo == 'aceite':
            self.processar_aceite(mensagem)

    def processar_interesse(self, mensagem):
        """Processa mensagem de interesse e envia oferta inicial"""
        conteudo = mensagem.content
        item = conteudo['item']
        quantidade = conteudo['quantidade']
        
        if self.estoque.tem_produto(item, quantidade):
            preco_unitario = self.estoque.obter_preco(item)
            preco_total = preco_unitario * quantidade

            print(f"[{self.name}] oferta: {quantidade}x {item} por R${preco_total:.2f}")

            resposta = Tell(
                sender=self.name,
                receiver=mensagem.sender,
                content={
                    'tipo': 'oferta',
                    'item': item,
                    'quantidade': quantidade,
                    'preco': preco_total,
                    'preco_unitario': preco_unitario,
                    'margem_negociacao': self.margem  # Adicionado informação da margem
                }
            )
            self.send_message(resposta)
        else:
            print(f"[{self.name}] estoque insuficiente: {item}")

    def processar_contra_oferta(self, mensagem):
        """Processa contra-ofertas dos compradores"""
        conteudo = mensagem.content
        item = conteudo['item']
        quantidade = conteudo['quantidade']
        preco_oferecido = conteudo['preco']
        preco_original = conteudo['preco_original']

        minimo_aceito = preco_original * (1 - self.margem)
        print(f"[{self.name}] Margem de negociação: {self.margem*100}% | Mínimo aceitável: R${minimo_aceito:.2f}")

        if preco_oferecido >= minimo_aceito:
            print(f"[{self.name}] ACEITOU contra-oferta: R${preco_oferecido:.2f}")
            if self.estoque.vender(item, quantidade):
                print(f"[{self.name}] VENDA CONCLUÍDA: {quantidade}x {item} para {mensagem.sender} por R${preco_oferecido:.2f}")
                resposta = Tell(
                    sender=self.name,
                    receiver=mensagem.sender,
                    content={
                        'tipo': 'venda_aprovada',
                        'item': item,
                        'quantidade': quantidade,
                        'preco_final': preco_oferecido
                    }
                )
            else:
                print(f"[{self.name}] FALHA: estoque insuficiente após contra-oferta")
                resposta = Tell(
                    sender=self.name,
                    receiver=mensagem.sender,
                    content={
                        'tipo': 'recusa',
                        'motivo': 'estoque insuficiente'
                    }
                )
        else:
            print(f"[{self.name}] RECUSOU contra-oferta: R${preco_oferecido:.2f} < R${minimo_aceito:.2f}")
            resposta = Tell(
                sender=self.name,
                receiver=mensagem.sender,
                content={
                    'tipo': 'recusa',
                    'motivo': f'preço abaixo do mínimo (R${minimo_aceito:.2f})'
                }
            )
        self.send_message(resposta)

    def processar_aceite(self, mensagem):
        """Processa aceite direto do comprador (sem contra-oferta)"""
        conteudo = mensagem.content
        item = conteudo['item']
        quantidade = conteudo['quantidade']

        preco_original = self.estoque.obter_preco(item) * quantidade
        
        if self.estoque.vender(item, quantidade):
            print(f"[{self.name}] VENDA CONCLUÍDA: {quantidade}x {item} para {mensagem.sender} por R${preco_original:.2f}")
            resposta = Tell(
                sender=self.name,
                receiver=mensagem.sender,
                content={
                    'tipo': 'venda_aprovada',
                    'item': item,
                    'quantidade': quantidade,
                    'preco_final': preco_original
                }
            )
        else:
            print(f"[{self.name}] FALHA NA VENDA: estoque insuficiente de {item}")
            resposta = Tell(
                sender=self.name,
                receiver=mensagem.sender,
                content={
                    'tipo': 'recusa',
                    'motivo': 'estoque insuficiente'
                }
            )
        self.send_message(resposta)