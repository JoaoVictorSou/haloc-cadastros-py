from cmath import e
from models.pessoa import Pessoa
from models.banco_dados import BancoDados
import datetime

class Administrador(Pessoa):
    def __init__(self, nome, cpf, data_nascimento, email, id, nivel, salario, senha, numero_celular, numero_telefone = "s/n"):
        super().__init__(nome, cpf, data_nascimento, email, numero_celular, numero_telefone)
        self.__id = id
        self.__senha = senha
        self.__nivel = nivel
        if Administrador.valida_salario(salario):
            self.__salario = salario
        else:
            raise ValueError("Salário inválido!")

    def cadastra_administrador(self):
        try:
            self.cnx.iniciar_conexao()
            
            sucesso = False
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
	            numeroCelular,
                numeroTelefone
            ) VALUES (
	            {self.id},
                "{self.cpf}",
                "{self.nome}",
                "{self.data_nascimento_formatada_internacional()}",
                "{self.email}",
                {self.nivel},
                "{self.senha}",
                {self.salario},
                "{self.numero_celular}",
                "{self.numero_telefone}"
            )
            """
            
            sucesso = self.cnx.query_post(query_base)
        finally:
            self.cnx.encerrar_conexao()
        
            return sucesso

    def atualiza_administrador(self, nome, data_nascimento, email, senha, salario, numero_celular, numero_telefone):
        try:
            self.cnx.iniciar_conexao()
            
            sucesso = False
            query_base = f"""
            UPDATE Administrador
	            SET nome = '{nome}',
                dataNascimento = '{data_nascimento}',
	            email = '{email}',
	            senha = '{senha}',
	            salario = {salario},
	            numeroCelular = '{numero_celular}',
                numeroTelefone = '{numero_telefone}'
            WHERE cpf = '{self.cpf}' AND id = {self.id}
            """
            print(query_base)
            sucesso = self.cnx.query_post(query_base)
        finally:
            self.cnx.encerrar_conexao()
        
            return sucesso

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

    @staticmethod
    def valida_salario(salario):
        salario_float = float(salario)

        return salario_float >= 0

    @staticmethod
    def carrega_administrador_pk(cpf = None, id = None):
        administrador = None
        if cpf or id:
            try:
                if cpf:
                    query_base = f"""
                    SELECT * 
                    FROM Administrador
                    WHERE cpf = '{cpf}'
                    """
                else:
                    query_base = f"""
                    SELECT * 
                    FROM Administrador
                    WHERE id = {id}
                    """
                
                cnx = BancoDados.informa_caminho_haloc()

                cnx.iniciar_conexao()

                resposta = cnx.query_get(query_base)
                
                # Atributos do administrador
                email = resposta[0][0]
                nome = resposta[0][1]
                data_nascimento = str(resposta[0][2]).replace("-", "/")
                numero_telefone = resposta[0][3]
                cpf_bd = resposta[0][4]
                nivel = resposta[0][5]
                salario = resposta[0][6]
                senha = resposta[0][7]
                id_db = resposta[0][8]
                numero_celular = resposta[0][9]

                administrador = Administrador(
                    nome, 
                    cpf_bd, 
                    data_nascimento, 
                    email, 
                    id_db, 
                    nivel, 
                    salario, 
                    senha, 
                    numero_celular, 
                    numero_telefone
                )
            finally:
                cnx.encerrar_conexao()
                return administrador
        else:
            raise ValueError("Deve-se informar ao menos uma PK. (CPF ou ID)")

    @staticmethod
    def carrega_lista_administradores():
        administradores = []
        try:
            cnx = BancoDados.informa_caminho_haloc()

            cnx.iniciar_conexao()

            query_base = f"""
            SELECT *
            FROM Administrador
            """

            resposta_lista = cnx.query_get(query_base)

            for resposta in resposta_lista:  
                # Atributos do administrador
                email = resposta[0]
                nome = resposta[1]
                data_nascimento = str(resposta[2]).replace("-", "/")
                # Primeiro o número de telefone deve ser limpo, para não pegar a da repetição interior
                numero_telefone = resposta[3]
                cpf_bd = resposta[4]
                nivel = resposta[5]
                salario = resposta[6]
                senha = resposta[7]
                id_db = resposta[8]
                numero_celular = resposta[9]
                
                administrador = Administrador(
                    nome, 
                    cpf_bd, 
                    data_nascimento, 
                    email, 
                    id_db, 
                    nivel, 
                    salario, 
                    senha, 
                    numero_celular, 
                    numero_telefone
                )
                
                administradores.append(administrador)
        finally:
            cnx.encerrar_conexao()
            return administradores
