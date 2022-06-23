from models.pessoa import Pessoa
from models.aluno import Aluno
from models.banco_dados import BancoDados
import datetime

class Convidado(Pessoa):
    def __init__(self, nome, cpf, aluno: Aluno, data_nascimento, email, numero_celular, numero_telefone = "s/n"):
        super().__init__(nome, cpf, data_nascimento, email, numero_celular, numero_telefone)
        if Aluno.carrega_aluno_pk(id = aluno.id):
            self.__aluno = aluno
        else:
            raise ValueError("Impossível ligar convidado a um aluno não cadastrado.")

    def cadastra_convidado(self):
        try:
            self.cnx.iniciar_conexao()
            
            sucesso = False
            query_base = f"""
            INSERT INTO Convidado (
	            cpf,
	            nome,
                dataNascimento,
	            email,
	            numeroCelular,
                numeroTelefone
            ) VALUES (
                "{self.cpf}",
                "{self.nome}",
                "{self.data_nascimento_formatada_internacional()}",
                "{self.email}",
                "{self.numero_celular}",
                "{self.numero_telefone}"
            )
            """

            sucesso = self.cnx.query_post(query_base)

            query_base2 = f"""
            INSERT INTO Comporta (
                fk_Aluno_id,
                fk_Aluno_cpf,
                fk_Convidado_cpf
            ) VALUES (
                {self.__aluno.id},
                '{self.__aluno.cpf}',
                '{self.cpf}'
            )
            """

            sucesso = sucesso and self.cnx.query_post(query_base2)
        finally:
            self.cnx.encerrar_conexao()
        
            return sucesso

    def atualiza_convidado(self, nome, data_nascimento, email, numero_celular, numero_telefone = "s/n"):
        try:
            self.cnx.iniciar_conexao()
            
            sucesso = False
            query_base = f"""
            UPDATE Convidado
	            SET nome = '{nome}',
                dataNascimento = '{data_nascimento}',
	            email = '{email}',
	            numeroCelular = '{numero_celular}',
                numeroTelefone = '{numero_telefone}'
            WHERE cpf = '{self.cpf}'
            """
            
            sucesso = self.cnx.query_post(query_base)
        finally:
            self.cnx.encerrar_conexao()
        
            return sucesso

    def deleta_convidado(self, cpf):
        sucesso = False
        try:
            if cpf == self.cpf:
                self.cnx.iniciar_conexao()

                query_base = f"""
                DELETE FROM Convidado
                WHERE cpf = '{self.cpf}' 
                """

                sucesso = self.cnx.query_post(query_base)
        finally:
            self.cnx.encerrar_conexao()
            return sucesso

    @staticmethod
    def carrega_convidado_pk(cpf = None):
        convidado = None
        if cpf:
            try:
                query_base = f"""
                SELECT * 
                FROM Convidado
                WHERE cpf = '{cpf}'
                """
                
                cnx = BancoDados.informa_caminho_haloc()

                cnx.iniciar_conexao()

                resposta = cnx.query_get(query_base)[0]
                
                # Atributos do convidado
                email = resposta[8]
                nome = resposta[5]
                data_nascimento = str(resposta[2]).replace("-", "/")
                numero_telefone = resposta[8]
                cpf_bd = resposta[1]
                numero_celular = resposta[9]
                
                convidado = Convidado(
                    nome, 
                    cpf_bd, 
                    data_nascimento, 
                    email, 
                    numero_celular, 
                    numero_telefone
                    )
            finally:
                cnx.encerrar_conexao()
                return convidado
        else:
            raise ValueError("Deve-se informar ao menos uma PK. (CPF)")

    @staticmethod
    def carrega_lista_convidado():
        convidados = []
        try:
            cnx = BancoDados.informa_caminho_haloc()

            cnx.iniciar_conexao()

            query_base = f"""
            SELECT *
            FROM Convidado
            """

            resposta_lista = cnx.query_get(query_base)

            for resposta in resposta_lista:  
                # Atributos do convidado
                email = resposta[8]
                nome = resposta[5]
                data_nascimento = str(resposta[2]).replace("-", "/")
                numero_telefone = resposta[8]
                cpf_bd = resposta[1]
                numero_celular = resposta[9]
                
                convidado = Convidado(
                    nome, 
                    cpf_bd, 
                    data_nascimento, 
                    email, 
                    numero_celular, 
                    numero_telefone
                    )
                
                convidados.append(convidado)
        finally:
            cnx.encerrar_conexao()
            return convidados
