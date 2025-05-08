class Environment:
    def __init__(self):
        self.agents = {}
    
    def register_agent(self, agent):
        self.agents[agent.name] = agent
        agent.environment = self
    
    def get_agents_by_type(self, agent_type):
        return [agent for agent in self.agents.values() 
                if agent.__class__.__name__ == agent_type]
    
    def deliver_message(self, message):
        if hasattr(message, 'receiver') and message.receiver in self.agents:
            self.agents[message.receiver].receber_mensagem(message)
        else:
            print(f"[ENV] Mensagem não entregue para {getattr(message, 'receiver', 'DESCONHECIDO')}")
    
    def run(self, steps=1):
        for _ in range(steps):
            for agent in self.agents.values():
                agent.deliberar()