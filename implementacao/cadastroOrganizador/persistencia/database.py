# arquivo: persistencia/organizador_dao.py

import sqlite3
import re
from entidade.organizador import Organizador

class OrganizadorDAO:
    def __init__(self, db_file='banco.db'):
        self.db_file = db_file

    def _conectar(self):
        return sqlite3.connect(self.db_file)

    def salvar(self, organizador: Organizador):
        conexao = self._conectar()
        cursor = conexao.cursor()

        # Insere os dados básicos do usuário
        dados_usuario = (
            organizador.cpf,
            organizador.nome,
            organizador.email,
            organizador.senha_hash,
            organizador.perfil
        )
        sql_usuario = "INSERT INTO usuarios (cpf, nome, email, senha_hash, perfil) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(sql_usuario, dados_usuario)

        conexao.commit()
        conexao.close()

    def cpf_ja_existe(self, cpf: str) -> bool:
        conexao = self._conectar()
        cursor = conexao.cursor()
        
        cpf_limpo = ''.join(re.findall(r'\d', cpf))

        sql = "SELECT cpf FROM usuarios WHERE cpf = ?"
        cursor.execute(sql, (cpf_limpo,))
        resultado = cursor.fetchone()

        conexao.close()
        return resultado is not None