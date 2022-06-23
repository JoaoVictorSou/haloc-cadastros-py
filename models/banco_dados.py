import mysql.connector as connector

class BancoDados:
    def __init__(self, usuario, senha, host, banco_dados):
        self.__usuario = usuario
        self.__senha = senha
        self.__host = host
        self.__banco_dados = banco_dados
        self.__cnx = None # Conexão
    
    def iniciar_conexao(self):
        try:
            self.__cnx = connector.connect(
                user = self.__usuario,
                password = self.__senha,
                host = self.__host,
                database = self.__banco_dados
            )
        except:
            self.__cnx.close()

    def encerrar_conexao(self):
        self.__cnx.close()
    
    def query_get(self, query_base):
        resposta = None
        
        try:
            cursor = self.__cnx.cursor()

            cursor.execute(query_base)
            resposta = cursor.fetchall()
        except:
            resposta = None
        finally:
            cursor.close()
        
        return resposta
    
    def query_post(self, query_base):
        try:
            cursor = self.__cnx

            cursor.execute(query_base)
            cursor.commit()

            linhas_afetadas = cursor.rowcount()
        except:
            linhas_afetadas = None
        finally:
            cursor.close()
        
        return linhas_afetadas
