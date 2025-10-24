import sqlite3
import re
import os
import bcrypt
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

    def _criar_organizador_do_banco(self, dados):
        """Cria um objeto Organizador a partir dos dados do banco"""
        organizador = Organizador(
            nome=dados[1],  # nome
            cpf=dados[0],   # cpf
            email=dados[2]  # email
        )
        organizador.senha_hash = dados[3]  # senha_hash
        return organizador

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

    def buscar_por_id(self, id_usuario: int) -> Organizador:
        """Busca organizador por ID"""
        conexao = self._conectar()
        cursor = conexao.cursor()
        
        sql = "SELECT cpf, nome, email, senha_hash FROM usuarios WHERE id = ? AND perfil = 'Organizador'"
        cursor.execute(sql, (id_usuario,))
        resultado = cursor.fetchone()
        
        conexao.close()
        
        if resultado:
            return self._criar_organizador_do_banco(resultado)
        return None

    def buscar_por_cpf(self, cpf: str) -> Organizador:
        """Busca organizador por CPF"""
        conexao = self._conectar()
        cursor = conexao.cursor()
        
        cpf_limpo = ''.join(re.findall(r'\d', cpf))
        
        sql = "SELECT cpf, nome, email, senha_hash FROM usuarios WHERE cpf = ? AND perfil = 'Organizador'"
        cursor.execute(sql, (cpf_limpo,))
        resultado = cursor.fetchone()
        
        conexao.close()
        
        if resultado:
            return self._criar_organizador_do_banco(resultado)
        return None

    def listar_todos(self) -> list:
        """Lista todos os organizadores"""
        conexao = self._conectar()
        cursor = conexao.cursor()
        
        sql = "SELECT cpf, nome, email, senha_hash FROM usuarios WHERE perfil = 'Organizador' ORDER BY nome"
        cursor.execute(sql)
        resultados = cursor.fetchall()
        
        conexao.close()
        
        organizadores = []
        for resultado in resultados:
            organizadores.append(self._criar_organizador_do_banco(resultado))
        
        return organizadores

    def buscar_por_nome(self, nome: str) -> list:
        """Busca organizadores por nome (busca parcial)"""
        conexao = self._conectar()
        cursor = conexao.cursor()
        
        sql = "SELECT cpf, nome, email, senha_hash FROM usuarios WHERE perfil = 'Organizador' AND nome LIKE ? ORDER BY nome"
        cursor.execute(sql, (f'%{nome}%',))
        resultados = cursor.fetchall()
        
        conexao.close()
        
        organizadores = []
        for resultado in resultados:
            organizadores.append(self._criar_organizador_do_banco(resultado))
        
        return organizadores

    def atualizar(self, organizador: Organizador) -> bool:
        """Atualiza dados do organizador"""
        conexao = self._conectar()
        cursor = conexao.cursor()
        
        try:
            sql = """UPDATE usuarios 
                     SET nome = ?, email = ?, senha_hash = ? 
                     WHERE cpf = ? AND perfil = 'Organizador'"""
            cursor.execute(sql, (
                organizador.nome,
                organizador.email,
                organizador.senha_hash,
                organizador.cpf
            ))
            
            conexao.commit()
            conexao.close()
            return cursor.rowcount > 0
        except Exception as e:
            conexao.close()
            return False

    def deletar(self, cpf: str) -> bool:
        """Deleta organizador por CPF"""
        conexao = self._conectar()
        cursor = conexao.cursor()
        
        try:
            cpf_limpo = ''.join(re.findall(r'\d', cpf))
            
            sql = "DELETE FROM usuarios WHERE cpf = ? AND perfil = 'Organizador'"
            cursor.execute(sql, (cpf_limpo,))
            
            conexao.commit()
            conexao.close()
            return cursor.rowcount > 0
        except Exception as e:
            conexao.close()
            return False

    def cpf_ja_existe(self, cpf: str) -> bool:
        conexao = self._conectar()
        cursor = conexao.cursor()
        
        cpf_limpo = ''.join(re.findall(r'\d', cpf))

        sql = "SELECT cpf FROM usuarios WHERE cpf = ?"
        cursor.execute(sql, (cpf_limpo,))
        resultado = cursor.fetchone()

        conexao.close()
        return resultado is not None

    def contar_organizadores(self) -> int:
        """Conta total de organizadores cadastrados"""
        conexao = self._conectar()
        cursor = conexao.cursor()
        
        sql = "SELECT COUNT(*) FROM usuarios WHERE perfil = 'Organizador'"
        cursor.execute(sql)
        resultado = cursor.fetchone()
        
        conexao.close()
        return resultado[0] if resultado else 0

    def autenticar(self, cpf: str, senha: str) -> Organizador:
        """Autentica organizador por CPF e senha"""
        conexao = self._conectar()
        cursor = conexao.cursor()
        
        cpf_limpo = ''.join(re.findall(r'\d', cpf))
        
        sql = "SELECT cpf, nome, email, senha_hash FROM usuarios WHERE cpf = ? AND perfil = 'Organizador'"
        cursor.execute(sql, (cpf_limpo,))
        resultado = cursor.fetchone()
        
        conexao.close()
        
        if resultado:
            organizador = self._criar_organizador_do_banco(resultado)
            # Verificar senha com bcrypt
            if self._verificar_senha(senha, organizador.senha_hash):
                return organizador
        
        return None

    def _verificar_senha(self, senha_plana: str, senha_hash: str) -> bool:
        """Verifica se a senha está correta usando bcrypt"""
        try:
            senha_bytes = senha_plana.encode('utf-8')
            hash_bytes = senha_hash.encode('utf-8')
            return bcrypt.checkpw(senha_bytes, hash_bytes)
        except Exception:
            return False