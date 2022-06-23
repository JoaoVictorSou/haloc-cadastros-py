from models.pessoa import Pessoa
from models.banco_dados import BancoDados
import datetime

class Aluno(Pessoa):
    def __init__(self, nome, cpf, data_nascimento, email, id, status_aluno, tipo_plano, senha, numero_celular, numero_telefone = "s/n"):
        super().__init__(nome, cpf, data_nascimento, email, numero_celular, numero_telefone)
        self.__id = id
        self.__senha = senha
        self.__status_aluno = status_aluno
        if Aluno.valida_tipo_plano(tipo_plano):
            self.__tipo_plano = tipo_plano
        else:
            raise ValueError("Tipo de plano inválido!")
        
        self.calcula_mensalidade()

    def cadastra_aluno(self):
        try:
            self.cnx.iniciar_conexao()
            
            sucesso = False
            query_base = f"""
            INSERT INTO Aluno (
	            id,
	            cpf,
	            nome,
                dataNascimento,
	            email,
	            statusAluno,
	            senha,
	            tipoPlano,
                valorMensalidade,
	            numeroCelular,
                numeroTelefone
            ) VALUES (
	            {self.id},
                "{self.cpf}",
                "{self.nome}",
                "{self.data_nascimento_formatada_internacional()}",
                "{self.email}",
                {self.__status_aluno},
                "{self.senha}",
                {self.__tipo_plano},
                {self.mensalidade},
                "{self.numero_celular}",
                "{self.numero_telefone}"
            )
            """
            
            sucesso = self.cnx.query_post(query_base)
        finally:
            self.cnx.encerrar_conexao()
        
            return sucesso

    def atualiza_aluno(self, nome, data_nascimento, email, senha, tipo_plano, numero_celular, numero_telefone):
        try:
            self.cnx.iniciar_conexao()
            
            sucesso = False
            query_base = f"""
            UPDATE Aluno
	            SET nome = '{nome}',
                dataNascimento = '{data_nascimento}',
	            email = '{email}',
	            senha = '{senha}',
	            tipoPlano = {tipo_plano},
                valorMensalidade = {self.mensalidade},
	            numeroCelular = '{numero_celular}',
                numeroTelefone = '{numero_telefone}'
            WHERE cpf = '{self.cpf}' AND id = {self.id}
            """
            
            sucesso = self.cnx.query_post(query_base)
        finally:
            self.cnx.encerrar_conexao()
        
            return sucesso

    def deleta_aluno(self, id, cpf):
        sucesso = False
        try:
            if id == self.id and cpf == self.cpf:
                self.cnx.iniciar_conexao()

                query_base = f"""
                DELETE FROM Aluno
                WHERE id = {self.id} and cpf = '{self.cpf}' 
                """

                sucesso = self.cnx.query_post(query_base)
        finally:
            self.cnx.encerrar_conexao()
            return sucesso

    def calcula_mensalidade(self):
        self.__mensalidade = 0

        if self.__tipo_plano == 0:
            self.__mensalidade = 70
        elif self.__tipo_plano == 1:
            self.__mensalidade = 90
        elif self.__tipo_plano == 2:
            self.__mensalidade = 120
        else:
            raise ValueError("Mensalidade não pode ser calculada com o plano existente!")

    @property
    def id(self):
            return self.__id
        
    @property
    def senha(self):
        return self.__senha
    
    @property
    def status_aluno(self):
        return self.__status_aluno

    @property
    def tipo_plano(self):
        plano = None

        if self.__tipo_plano == 0:
            plano = "Básico - R$ 70,00"
        elif self.__tipo_plano == 1:
            plano = "Médio - R$ 90,00"
        elif self.__tipo_plano == 2:
            plano = "Completo - R$ 120,00"

        return plano
    
    @property
    def mensalidade(self):
        self.calcula_mensalidade()
        return self.__mensalidade

    @staticmethod
    def valida_tipo_plano(tipo_plano):
        if tipo_plano >= 0 and tipo_plano <= 2:
            return True
        
        return False

    @staticmethod
    def carrega_aluno_pk(cpf = None, id = None):
        aluno = None
        if cpf or id:
            try:
                if cpf:
                    query_base = f"""
                    SELECT * 
                    FROM Aluno
                    WHERE cpf = '{cpf}'
                    """
                else:
                    query_base = f"""
                    SELECT * 
                    FROM Aluno
                    WHERE id = {id}
                    """
                
                cnx = BancoDados.informa_caminho_haloc()

                cnx.iniciar_conexao()

                resposta = cnx.query_get(query_base)[0]
                
                # Atributos do aluno
                email = resposta[8]
                nome = resposta[5]
                data_nascimento = str(resposta[2]).replace("-", "/")
                numero_telefone = resposta[8]
                cpf_bd = resposta[1]
                status_aluno = resposta[6]
                tipo_plano = resposta[12]
                senha = resposta[4]
                id_db = resposta[0]
                numero_celular = resposta[9]
                
                aluno = Aluno(
                    nome, 
                    cpf_bd, 
                    data_nascimento, 
                    email, 
                    id_db, 
                    status_aluno, 
                    tipo_plano, 
                    senha, 
                    numero_celular, 
                    numero_telefone
                    )
            finally:
                cnx.encerrar_conexao()
                return aluno
        else:
            raise ValueError("Deve-se informar ao menos uma PK. (CPF ou ID)")

    @staticmethod
    def carrega_lista_aluno():
        alunos = []
        try:
            cnx = BancoDados.informa_caminho_haloc()

            cnx.iniciar_conexao()

            query_base = f"""
            SELECT *
            FROM Aluno
            """

            resposta_lista = cnx.query_get(query_base)

            for resposta in resposta_lista:  
                # Atributos do aluno
                email = resposta[5]
                nome = resposta[9]
                data_nascimento = str(resposta[2]).replace("-", "/")
                numero_telefone = resposta[0]
                cpf_bd = resposta[7]
                status_aluno = resposta[3]
                tipo_plano = resposta[4]
                senha = resposta[8]
                id_db = resposta[6]
                numero_celular = resposta[1]
                
                aluno = Aluno(
                    nome, 
                    cpf_bd, 
                    data_nascimento, 
                    email, 
                    id_db, 
                    status_aluno, 
                    tipo_plano, 
                    senha, 
                    numero_celular, 
                    numero_telefone
                    )
                
                alunos.append(aluno)
        finally:
            cnx.encerrar_conexao()
            return alunos
