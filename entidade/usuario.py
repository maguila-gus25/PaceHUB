import re
from abc import ABC

import bcrypt


class Usuario(ABC):
    def __init__(self, cpf, nome, email, senha_hash, perfil):
        if self.validar_cpf(cpf):
            self.__cpf = cpf
        else:
            raise ValueError(f'O CPF {cpf} é inválido.')
        self.__nome = nome
        if self.validar_email(email):
            self.__email = email
        else:
            raise ValueError(f'O email {email} é inválido.')
        self.__senha_hash = senha_hash
        self.__perfil = perfil

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf):
        if self.validar_cpf(cpf):
            self.__cpf = cpf
        else:
            raise ValueError(f'O CPF {cpf} é inválido.')

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        if self.validar_email(email):
            self.__email = email
        else:
            raise ValueError(f'O email {email} é inválido')

    @property
    def perfil(self):
        return self.__perfil

    @perfil.setter
    def perfil(self, perfil):
        self.__perfil = perfil

    @property
    def senha_hash(self):
        return self.__senha_hash

    def set_senha_hash(self, senha_hash):
        self.__senha_hash = senha_hash

    def verifica_senha_hash(self, senha):
        senha_em_bytes= senha.encode('utf-8')
        hassh_em_bytes = self.__senha_hash.encode('utf-8')
        return bcrypt.checkpw(senha_em_bytes, hassh_em_bytes)

    @staticmethod
    def validar_cpf(cpf) -> bool:
        cpf_limpo = re.sub(r'[^0-9]', '', cpf)

        if len(cpf_limpo) != 11:
            return False

        if cpf_limpo == cpf_limpo[0] * 11:
            return False

        soma = 0
        for i in range(9):
            soma += int(cpf_limpo[i]) * (10 - i)

        resto = soma % 11
        digito_verificador_1 = 0 if resto < 2 else 11 - resto

        if int(cpf_limpo[9]) != digito_verificador_1:
            return False

        soma = 0
        for i in range(10):
            soma += int(cpf_limpo[i]) * (11 - i)

        resto = soma % 11
        digito_verificador_2 = 0 if resto < 2 else 11 - resto

        if int(cpf_limpo[10]) != digito_verificador_2:
            return False
        return True

    @staticmethod
    def validar_email(email) -> bool:
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if re.match(padrao, email):
            return True
        return False
