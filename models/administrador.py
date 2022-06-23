from models.pessoa import Pessoa

class Administrador(Pessoa):
    def __init__(self, nome, cpf, data_nascimento, email, numero_celular, numero_telefone = None):
        super().__init__(nome, cpf, data_nascimento, email, numero_celular, numero_telefone)