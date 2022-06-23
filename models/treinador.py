from models.pessoa import Pessoa
from models.banco_dados import BancoDados
import datetime

class Treinador(Pessoa):
    def __init__(self, nome, cpf, data_nascimento, email, id, status_treinador, salario, senha, numero_celular, numero_telefone = "s/n"):
        super().__init__(nome, cpf, data_nascimento, email, numero_celular, numero_telefone)
        self.__id = id
        self.__senha = senha
        self.__status_treinador = status_treinador
        if Treinador.valida_salario(salario):
            self.__salario = salario
        else:
            raise ValueError("Salário inválido!")

    def cadastra_treinador(self):
        try:
            self.cnx.iniciar_conexao()
            
            sucesso = False
            query_base = f"""
            INSERT INTO Treinador (
	            id,
	            cpf,
	            nome,
                dataNascimento,
	            email,
	            statusTreinador,
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
                {self.__status_treinador},
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

    def atualiza_treinador(self, nome, data_nascimento, email, senha, salario, numero_celular, numero_telefone = "s/n"):
        try:
            self.cnx.iniciar_conexao()
            
            sucesso = False
            query_base = f"""
            UPDATE Treinador
	            SET nome = '{nome}',
                dataNascimento = '{data_nascimento}',
	            email = '{email}',
	            senha = '{senha}',
	            salario = {salario},
	            numeroCelular = '{numero_celular}',
                numeroTelefone = '{numero_telefone}'
            WHERE cpf = '{self.cpf}' AND id = {self.id}
            """
            
            sucesso = self.cnx.query_post(query_base)
        finally:
            self.cnx.encerrar_conexao()
        
            return sucesso

    def deleta_treinador(self, id, cpf):
        sucesso = False
        try:
            if id == self.id and cpf == self.cpf:
                self.cnx.iniciar_conexao()

                query_base = f"""
                DELETE FROM Treinador
                WHERE id = {self.id} and cpf = '{self.cpf}' 
                """

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
    def status_treinador(self):
        return self.__status_treinador

    @property
    def salario(self):
        return self.__salario

    @staticmethod
    def valida_salario(salario):
        salario_float = float(salario)

        return salario_float >= 0

    @staticmethod
    def carrega_treinador_pk(cpf = None, id = None):
        treinador = None
        if cpf or id:
            try:
                if cpf:
                    query_base = f"""
                    SELECT * 
                    FROM Treinador
                    WHERE cpf = '{cpf}'
                    """
                else:
                    query_base = f"""
                    SELECT * 
                    FROM Treinador
                    WHERE id = {id}
                    """
                
                cnx = BancoDados.informa_caminho_haloc()

                cnx.iniciar_conexao()

                resposta = cnx.query_get(query_base)[0]
                
                # Atributos do treinador
                email = resposta[5]
                nome = resposta[9]
                data_nascimento = str(resposta[2]).replace("-", "/")
                numero_telefone = resposta[0]
                cpf_bd = resposta[7]
                status_treinador = resposta[3]
                salario = resposta[4]
                senha = resposta[8]
                id_db = resposta[6]
                numero_celular = resposta[1]
                
                treinador = Treinador(
                    nome, 
                    cpf_bd, 
                    data_nascimento, 
                    email, 
                    id_db, 
                    status_treinador, 
                    salario, 
                    senha, 
                    numero_celular, 
                    numero_telefone
                    )
            finally:
                cnx.encerrar_conexao()
                return treinador
        else:
            raise ValueError("Deve-se informar ao menos uma PK. (CPF ou ID)")

    @staticmethod
    def carrega_lista_treinador():
        treinadores = []
        try:
            cnx = BancoDados.informa_caminho_haloc()

            cnx.iniciar_conexao()

            query_base = f"""
            SELECT *
            FROM Treinador
            """

            resposta_lista = cnx.query_get(query_base)

            for resposta in resposta_lista:  
                # Atributos do treinador
                email = resposta[5]
                nome = resposta[9]
                data_nascimento = str(resposta[2]).replace("-", "/")
                numero_telefone = resposta[0]
                cpf_bd = resposta[7]
                status_treinador = resposta[3]
                salario = resposta[4]
                senha = resposta[8]
                id_db = resposta[6]
                numero_celular = resposta[1]
                
                treinador = Treinador(
                    nome, 
                    cpf_bd, 
                    data_nascimento, 
                    email, 
                    id_db, 
                    status_treinador, 
                    salario, 
                    senha, 
                    numero_celular, 
                    numero_telefone
                    )
                
                treinadores.append(treinador)
        finally:
            cnx.encerrar_conexao()
            return treinadores
