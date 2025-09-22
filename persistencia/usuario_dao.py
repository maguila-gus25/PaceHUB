import sqlite3
from entidade.atleta import Atleta


class UsuarioDAO:

    def __init__(self, db_path='banco.db'):
        self.__db_path = db_path

    def __conectar(self):
        return sqlite3.connect(self.__db_path)

    def add(self, usuario):
        conexao = self.__conectar()
        cursor = conexao.cursor()


        if isinstance(usuario, Atleta):
            dados = (
                usuario.cpf,
                usuario.nome,
                usuario.email,
                usuario.senha_hash,
                usuario.perfil,
                usuario.data_nascimento_str,
                usuario.genero,
                int(usuario.pcd)
            )

            sql = """
            INSERT INTO usuarios (cpf, nome, email, senha_hash, perfil, data_nascimento, genero, pcd)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """

            cursor.execute(sql, dados)
            conexao.commit()
            conexao.close()

    def get(self, cpf):
        conexao = self.__conectar()
        cursor = conexao.cursor()

        sql = "SELECT * FROM usuarios WHERE cpf = ?;"
        cursor.execute(sql, (cpf,))
        dados_tupla = cursor.fetchone()
        conexao.close()

        if not dados_tupla:
            return None

        if dados_tupla[4] == 'Atleta':
            data_nascimento_str_banco = dados_tupla[5]
            atleta = Atleta(
                nome = dados_tupla[1],
                cpf=dados_tupla[0],
                email=dados_tupla[2],
                senha_hash=dados_tupla[3],
                data_nascimento = data_nascimento_str_banco.split(' ')[0],
                genero=dados_tupla[6],
                pcd=bool(dados_tupla[7])
            )
            return atleta
        return None

    def get_all(self):
        conexao = self.__conectar()
        cursor = conexao.cursor()

        sql = "SELECT * FROM usuarios"
        cursor.execute(sql)
        lista_dados = cursor.fetchall()
        conexao.close()

        usuarios = []
        for dados_tupla in lista_dados:
            if(dados_tupla[4] == 'Atleta'):
                atleta = Atleta(
                    nome=dados_tupla[1],
                    cpf=dados_tupla[0],
                    email=dados_tupla[2],
                    senha_hash=dados_tupla[3],
                    data_nascimento=dados_tupla[5],
                    genero=dados_tupla[6],
                    pcd=bool(dados_tupla[7])
                )
                usuarios.append(atleta)
        return usuarios

    def update(self, cpf, usuario):
        conexao = self.__conectar()
        cursor = conexao.cursor()

        if isinstance(usuario, Atleta):
            dados = (
                usuario.nome,
                usuario.email,
                usuario.senha_hash,
                usuario.perfil,
                usuario.genero,
                int(usuario.pcd),
                usuario.cpf
            )
            sql = """UPDATE usuarios SET 
            NOME = ?,
            EMAIL = ?,
            SENHA_HASH = ?,
            PERFIL = ?,
            GENERO = ?,
            pcd = ?
            WHERE cpf = ?; """
            cursor.execute(sql, dados)
            conexao.commit()
            conexao.close()
        return False


    def remove(self, cpf):
        conexao = self.__conectar()
        cursor = conexao.cursor()

        sql = "DELETE FROM usuarios WHERE cpf = ?;"
        cursor.execute(sql, [cpf])

        conexao.commit()
        conexao.close()
