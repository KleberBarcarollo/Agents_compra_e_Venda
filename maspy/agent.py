class Agent:
    def __init__(self, name):
        self.name = name
        self.environment = None
    
    def send_message(self, message):
        if self.environment:
            self.environment.deliver_message(message)
    
    def receber_mensagem(self, message):
        pass
    
    def deliberar(self):
        pass