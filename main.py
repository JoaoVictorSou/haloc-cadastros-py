from models.banco_dados import BancoDados
from models.pessoa import Pessoa
from models.administrador import Administrador

administrador = Administrador("João", "415.305.570-03", "2002/04/01", "soulima.joao@gmail.com", "5584987553968")
print(administrador)
'''
banco_dados = BancoDados(
    usuario = "root",
    senha = "552210",
    host = "localhost",
    banco_dados = "world"
)

try: 
    banco_dados.iniciar_conexao()

    query_base = "SELECT * FROM City"
    resposta = banco_dados.query_get(query_base)

    for cidade in resposta:
        print(f"{cidade[1]}")

finally:
    banco_dados.encerrar_conexao()
'''