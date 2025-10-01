import sqlite3
import re
import os
from entidade.organizador import Organizador

class OrganizadorDAO:
    def __init__(self, db_file=None):
        if db_file is None:
            # Use the main database in implementacao directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            main_implementacao_dir = os.path.join(current_dir, '..', '..')
            self.db_file = os.path.join(main_implementacao_dir, 'banco.db')
        else:
            self.db_file = db_file

    def _conectar(self):
        return sqlite3.connect(self.db_file)

    def salvar(self, organizador: Organizador):
        conexao = self._conectar()
        cursor = conexao.cursor()

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