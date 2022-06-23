from models.pessoa import Pessoa

class Administrador(Pessoa):
    def __init__(self, nome, cpf, data_nascimento, email, id, nivel, salario, senha, numero_celular, numero_telefone = None):
        super().__init__(nome, cpf, data_nascimento, email, numero_celular, numero_telefone)
        self.__id = id
        self.__senha = senha
        self.__nivel = nivel
        self.__salario = salario

    def cadastra_administrador(self):
        try:
            self.cnx.iniciar_conexao()
            
            query_base = f"""
            INSERT INTO Administrador (
	            id,
	            cpf,
	            nome,
                dataNascimento,
	            email,
	            nivel,
	            senha,
	            salario,
	            numeroCelular
            ) VALUES (
	            {self.id},
                "{self.cpf}",
                "{self.nome}",
                "{self.data_nascimento_formatada_internacional()}",
                "{self.email}",
                {self.nivel},
                "{self.senha}",
                {self.salario},
                "{self.numero_celular}"
            )
            """
            print(query_base)
            print(self.cnx.query_post(query_base))
        finally:
            self.cnx.encerrar_conexao()

    @property
    def id(self):
            return self.__id
        
    @property
    def senha(self):
        return self.__senha
    
    @property
    def nivel(self):
        return self.__nivel

    @property
    def salario(self):
        return self.__salario