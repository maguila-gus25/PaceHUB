from entidade.usuario import Usuario
from datetime import datetime

class Atleta(Usuario):
    def __init__(self, nome, cpf, email, senha_hash, data_nascimento, genero, pcd):
        super().__init__(cpf, nome, email, senha_hash, perfil = 'Atleta')
        data_convertida = None
        try:
            data_convertida = datetime.strptime(data_nascimento, "%d/%m/%Y")
        except ValueError:
            try:
                data_convertida = datetime.strptime(data_nascimento, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"O formato da data '{data_nascimento}' é inválido. Use dd/mm/yyyy.")
        if data_convertida > datetime.now():
            raise ValueError("A data de nascimento não pode ser uma data futura.")
        self.__data_nascimento = data_convertida
        self.__genero = genero
        self.__pcd = pcd

    @property
    def data_nascimento(self):
        return self.__data_nascimento

    @property
    def genero(self):
        return self.__genero

    @genero.setter
    def genero(self, genero):
        self.__genero = genero

    @property
    def pcd(self):
        return self.__pcd

    @pcd.setter
    def pcd(self, pcd):
        self.__pcd = pcd

    @property
    def data_nascimento_str(self):
        return self.__data_nascimento.strftime('%Y-%m-%d')

    def calcula_idade(self, ano_evento):
        idade = ano_evento - self.__data_nascimento.year
        return idade
