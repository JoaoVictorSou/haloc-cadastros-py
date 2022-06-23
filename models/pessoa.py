from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta, timezone
from models.banco_dados import BancoDados

class Pessoa(metaclass = ABCMeta):
    def __init__(self, nome, cpf, data_nascimento, email, numero_celular, numero_telefone = None):
        self.__nome = nome
        self.__dia_nascimento = int(data_nascimento[8:])
        self.__mes_nascimento = int(data_nascimento[5:7])
        self.__ano_nascimento = int(data_nascimento[:4])
        self.__email = email
        self.__numero_celular = numero_celular
        self.__numero_telefone = numero_telefone
        self.cnx = BancoDados.informa_caminho_haloc()

        if Pessoa.valida_nascimento(datetime(year = self.__ano_nascimento, month = self.__mes_nascimento, day = self.__dia_nascimento)):
            self.__data_nascimento = datetime(year = self.__ano_nascimento, month = self.__mes_nascimento, day = self.__dia_nascimento)
        else:
            raise ValueError("Data de nascimento é inválida!")

        if (Pessoa.valida_cpf(cpf)):
            self.__cpf = cpf
        else:
            raise ValueError("CPF inválido!")

    def __str__(self):
        return "cpf: {} | nome: {} | idade: {}".format(
            self.cpf,
            self.nome,
            self.idade
        )

    def data_nascimento_formatada_internacional(self):
        return self.__data_nascimento.strftime("%Y/%m/%d")

    # 5 dígitos | único para qualquer nível
    def implementa_id(self):
        pass

    @property
    def idade(self):
        return Pessoa.__calcula_idade(self.__data_nascimento)
    
    @property
    def data_nascimento(self):
        return self.__data_nascimento.strftime("%d/%m/%Y")
    
    @property
    def cpf(self):
        return Pessoa.monta_mascara(self.__cpf)

    @property
    def nome(self):
        return self.__nome
    
    @property
    def email(self):
        return self.__email

    @property
    def numero_celular(self):
        return self.__numero_celular
    
    @property
    def numero_telefone(self):
        return self.__numero_telefone

    @staticmethod
    def __calcula_idade(data_nascimento):
        diferenca_utc_brasil = timedelta(hours = -3)
        utc_brasil = timezone(diferenca_utc_brasil)

        data_atual = datetime.today()
        data_atual.astimezone(utc_brasil)

        diferenca_anos = data_atual.year - data_nascimento.year
        relacao_mes_dia = (data_atual.month >= data_nascimento.month) and (data_atual.day >= data_nascimento.day)

        return diferenca_anos if relacao_mes_dia else (diferenca_anos - 1)

    @staticmethod
    def valida_nascimento(data_nascimento):
        idade = Pessoa.__calcula_idade(data_nascimento)

        if idade >= 0 and idade <= 100:
            return True
        else:
            return False
    
    @staticmethod
    def valida_cpf(cpf):
        cpf_str = Pessoa.retira_mascara(cpf)

        # Possui a quantidade de dígitos exatas para ser um CPF
        if len(cpf_str) == 11:
            # Todos os dígitos são identicos
            primeiro_digito = cpf_str[0]
            digitos_diferentes = cpf_str.count(primeiro_digito) != 11 

            if digitos_diferentes:
                # Teste do primeiro dígito verificador 
                soma = 0
                c = 0

                for i in reversed(range(2, 11)):
                    digito = int(cpf_str[c])
                    soma += digito * i

                    c += 1
                
                resto_divisao = ((soma * 10) % 11)
                resto_divisao_filtrado = resto_divisao if resto_divisao != 10 else 0

                verificador_e_valido = resto_divisao_filtrado == int(cpf_str[9])

                if verificador_e_valido:
                    # Teste do segundo dígito verificador
                    soma = 0
                    c = 0

                    for i in reversed(range(2, 12)):
                        digito = int(cpf_str[c])
                        soma += digito * i

                        c += 1

                    resto_divisao = ((soma * 10) % 11)
                    resto_divisao_filtrado = resto_divisao if resto_divisao != 10 else 0

                    verificador_e_valido = resto_divisao_filtrado == int(cpf_str[10])

                    return verificador_e_valido
        
        # Retornará caso não passe em uma das validações
        return False
    
    @staticmethod
    def monta_mascara(cpf: str):
        if Pessoa.valida_cpf(cpf):
            str_cpf = Pessoa.retira_mascara(cpf)
            # Cortando o CPF com base em 000.000.000-00
            return f"{str_cpf[:3]}.{str_cpf[3:6]}.{str_cpf[6:9]}-{str_cpf[9:]}"

    @staticmethod
    def retira_mascara(cpf):
        cpf_str = str(cpf)

        cpf_sem_mascara = cpf_str.replace(".", "")
        cpf_sem_mascara = cpf_sem_mascara.replace("-", "")

        return cpf_sem_mascara
