"""
PROJETO DE AGENTES INTELIGENTES - SISTEMA DE NEGOCIAÇÃO AUTÔNOMA
Autores:
# Alunos: Rodrigo Vieira, Kleber Barcarollo
# Instituição: UTFPR
# Curso: Mestrado em Ciência da Computação
# Disciplina: Inteligência Artificial - Mestrado UTFPR
# Professor: André Pinz Borges

ESTRATÉGIA DE NEGOCIAÇÃO IMPLEMENTADA:

1. ESTRATÉGIA DOS COMPRADORES:
   - Enviam uma mensagem de interesse (broadcast) para todos os vendedores disponíveis, especificando o produto, a quantidade desejada e o preço máximo por unidade.
   - Ao receberem uma oferta:
     • Se o preço total da oferta estiver dentro do limite (preço_unitário x quantidade ≤ preço_total_máximo), aceitam imediatamente.
     • Caso contrário, avaliam a margem de negociação informada pelo vendedor:
          -Se o preço máximo que o comprador aceita for ≥ preço mínimo aceito pelo vendedor (considerando sua margem), então enviam uma contra-oferta com esse preço máximo.
          -Se o preço máximo do comprador for inferior ao mínimo aceitável do vendedor, a proposta é rejeitada.
   - Não há memória de negociações anteriores — cada rodada é independente.

2. ESTRATÉGIA DOS VENDEDORES:
   - Respondem a mensagens de interesse com uma oferta direta a preço cheio (sem desconto).
   - Caso recebam uma contra-oferta:
     • Aceitam se o valor oferecido estiver dentro da margem de negociação definida individualmente:
         -Vendedor_1: aceita até 15% abaixo do valor original
         -Vendedor_2: aceita até 10% abaixo
         -Vendedor_3: aceita até 20% abaixo
     • Caso contrário, rejeitam com uma justificativa.
   - Em caso de aceite direto, vendem o produto ao preço original, desde que haja estoque disponível.

3. DINÂMICA GERAL DO SISTEMA:
   - As interações ocorrem em ciclos discretos (etapas), controladas pelo ambiente MASPY.
   - O ambiente apenas organiza os ciclos, não interfere nas decisões dos agentes.
   - Estoques dos vendedores são atualizados automaticamente após cada venda.
   - A cada etapa, os estoques são exibidos para acompanhamento do progresso das negociações.
"""

from maspy.environment import Environment
from comprador import Comprador
from vendedor import Vendedor

def mostrar_estoques(*vendedores, etapa=None):
    if etapa:
        print("\n" + "="*50)
        print("ESTOQUE APÓS ETAPA " + str(etapa) + ":")
    else:
        print("\nESTOQUE INICIAL:")
    
    for v in vendedores:
        print("\n" + v.name + ":")
        for nome, produto in v.estoque.produtos.items():
            print("  - " + str(produto.quantidade) + "x " + nome + " (R$" + f"{produto.preco:.2f}" + "/un)")

# Cria o ambiente
ambiente = Environment()

# Cria e registra vendedores com estoque
print("\n" + "="*50)
print("CRIANDO VENDEDORES...")
v1 = Vendedor("Vendedor_1", margem_negociacao=0.15)
v1.estoque.adicionar_produto("banana", 50, 3.50)

v2 = Vendedor("Vendedor_2", margem_negociacao=0.10)
v2.estoque.adicionar_produto("banana", 20, 3.80)

v3 = Vendedor("Vendedor_3", margem_negociacao=0.20)
v3.estoque.adicionar_produto("maçã", 90, 2.50)

# Realiza Registro de vendedores no ambiente
ambiente.register_agent(v1)
ambiente.register_agent(v2)
ambiente.register_agent(v3)

# Mostrar o estoque inicial
mostrar_estoques(v1, v2, v3)

# Cria e registra os compradores
print("\n" + "="*50)
print("CRIANDO COMPRADORES...")
c1 = Comprador("Comprador_Ana", item_desejado="banana", quantidade_desejada=10, preco_maximo=2.98)
c2 = Comprador("Comprador_João", item_desejado="maçã", quantidade_desejada=30, preco_maximo=2.50)

# Registra os compradores no ambiente
ambiente.register_agent(c1)
ambiente.register_agent(c2)

# Executa o ambiente com número de ciclos
print("\n" + "="*50)
print("INICIANDO SIMULAÇÕES...")

# Adiciona um hook para mostrar estoques posterior cada etapa
original_run = ambiente.run
def run_with_steps(steps, *args, **kwargs):
    for step in range(1, steps+1):
        print("\n" + "="*50)
        print("ETAPA " + str(step))
        original_run(1, *args, **kwargs)  # Executa apenas 1 step por vez
        mostrar_estoques(v1, v2, v3, etapa=step)
        
ambiente.run = run_with_steps
ambiente.run(steps=5)

# Exibe estoques finais com destaque
print("\n" + "="*50)
print("RESULTADO FINAL DA SIMULAÇÃO")
mostrar_estoques(v1, v2, v3)
print("\n" + "="*50)