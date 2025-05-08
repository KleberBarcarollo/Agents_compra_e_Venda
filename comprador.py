from maspy.agent import Agent
from maspy.messages import Ask

class Comprador(Agent):
    def __init__(self, nome, item_desejado, quantidade_desejada, preco_maximo):
        super().__init__(nome)
        self.item_desejado = item_desejado
        self.quantidade_desejada = quantidade_desejada
        self.preco_maximo = preco_maximo
        self.negociacoes = {}

    def deliberar(self):
        """Envia mensagens de interesse a todos os vendedores disponíveis"""
        print(f"\n[{self.name}] Procurando {self.quantidade_desejada}x {self.item_desejado}:")
        for vendedor in self.environment.get_agents_by_type("Vendedor"):
            mensagem = Ask(
                sender=self.name,
                receiver=vendedor.name,
                content={
                    'tipo': 'interesse',
                    'item': self.item_desejado,
                    'quantidade': self.quantidade_desejada,
                    'preco_maximo': self.preco_maximo
                }
            )
            self.send_message(mensagem)

    def receber_mensagem(self, mensagem):
        """Processa todos os tipos de mensagens recebidas"""
        conteudo = mensagem.content
        tipo = conteudo.get('tipo')
        
        if tipo == 'oferta':
            self.processar_oferta(mensagem)
        elif tipo == 'venda_aprovada':
            print(f"[{self.name}] COMPRA CONCLUÍDA: {conteudo['quantidade']}x {conteudo['item']} por R${conteudo['preco_final']:.2f}")
        elif tipo == 'recusa':
            print(f"[{self.name}] COMPRA RECUSADA: {conteudo.get('motivo', 'sem motivo especificado')}")

    def processar_oferta(self, mensagem):
        """Processa ofertas recebidas e faz contra-ofertas quando viável"""
        conteudo = mensagem.content
        vendedor = mensagem.sender
        preco_total = conteudo['preco']
        preco_max_total = self.preco_maximo * self.quantidade_desejada
        
        print(f"[{self.name}] Oferta recebida de {vendedor}: R${preco_total:.2f}")
        print(f"[{self.name}] Preço máximo aceitável para {self.quantidade_desejada}x {self.item_desejado}: R${preco_max_total:.2f}")

        if preco_total <= preco_max_total:
            print(f"[{self.name}] ACEITOU oferta (R${preco_total:.2f} ≤ R${preco_max_total:.2f})")
            resposta = Ask(
                sender=self.name,
                receiver=vendedor,
                content={
                    'tipo': 'aceite',
                    'item': self.item_desejado,
                    'quantidade': self.quantidade_desejada
                }
            )
        else:
            # Obter margem do vendedor da mensagem
            margem_vendedor = conteudo.get('margem_negociacao', 0.15)  # Default 15% se não informado
            minimo_vendedor = preco_total * (1 - margem_vendedor)
            
            print(f"[{self.name}] Margem do vendedor: {margem_vendedor*100}% | Mínimo aceitável: R${minimo_vendedor:.2f}")

            if preco_max_total >= minimo_vendedor:
                # Faz contra-oferta com o preço máximo do comprador
                print(f"[{self.name}] Fazendo contra-oferta com preço máximo: R${preco_max_total:.2f}")
                resposta = Ask(
                    sender=self.name,
                    receiver=vendedor,
                    content={
                        'tipo': 'contra_oferta',
                        'item': self.item_desejado,
                        'quantidade': self.quantidade_desejada,
                        'preco': preco_max_total,
                        'preco_original': preco_total
                    }
                )
            else:
                print(f"[{self.name}] IMPOSSÍVEL NEGOCIAR: preço máximo (R${preco_max_total:.2f}) abaixo do mínimo do vendedor (R${minimo_vendedor:.2f})")
                resposta = Ask(
                    sender=self.name,
                    receiver=vendedor,
                    content={
                        'tipo': 'recusa',
                        'motivo': f'Preço máximo (R${preco_max_total:.2f}) abaixo do mínimo negociável (R${minimo_vendedor:.2f})'
                    }
                )
        self.send_message(resposta)