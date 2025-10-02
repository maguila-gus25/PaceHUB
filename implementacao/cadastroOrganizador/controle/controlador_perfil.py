import sys
import os
import PySimpleGUI as sg
import bcrypt
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from entidade.organizador import Organizador
from persistencia.organizador_dao import OrganizadorDAO
from limite.tela_sistema import TelaSistema
from validadores import validar_nome_completo, validar_email

class ControladorPerfil:
    def __init__(self, tela_sistema: TelaSistema):
        self.organizador_dao = OrganizadorDAO()
        self.tela_sistema = tela_sistema
        self.janela_perfil = None

    def _hash_senha(self, senha: str) -> str:
        """Gera hash da senha usando bcrypt"""
        senha_bytes = senha.encode('utf-8')
        salt = bcrypt.gensalt()
        hash_bytes = bcrypt.hashpw(senha_bytes, salt)
        return hash_bytes.decode('utf-8')

    def abrir_tela_perfil(self, organizador: Organizador):
        """Abre a tela de perfil do organizador"""
        self.janela_perfil = self.tela_sistema.criar_janela_perfil_organizador(organizador)
        
        if self.janela_perfil is None:
            print("Error: Failed to create profile window")
            return
        
        while True:
            event, values = self.janela_perfil.read()
            
            if event in ('-VOLTAR-', sg.WIN_CLOSED):
                break
            
            elif event == '-SALVAR-':
                if self._salvar_alteracoes_perfil(organizador, values):
                    break
        
        self.fechar_tela_perfil()

    def fechar_tela_perfil(self):
        """Fecha a tela de perfil"""
        if self.janela_perfil:
            self.janela_perfil.close()
            self.janela_perfil = None

    def _salvar_alteracoes_perfil(self, organizador: Organizador, values) -> bool:
        """Salva as alterações do perfil"""
        nome = values['-NOME-']
        email = values['-EMAIL-']
        senha_atual = values['-SENHA_ATUAL-']
        nova_senha = values['-NOVA_SENHA-']
        confirmar_senha = values['-CONFIRMAR_SENHA-']
        
        # Validações básicas
        if not all([nome, email]):
            self.tela_sistema.exibir_popup_erro('Nome e email são obrigatórios!')
            return False
        
        if not validar_nome_completo(nome):
            self.tela_sistema.exibir_popup_erro('Por favor, insira um nome completo (nome e sobrenome).')
            return False
        
        if not validar_email(email):
            self.tela_sistema.exibir_popup_erro('O formato do e-mail inserido é inválido.')
            return False
        
        # Verificar se quer alterar senha
        alterar_senha = any([senha_atual, nova_senha, confirmar_senha])
        
        if alterar_senha:
            if not all([senha_atual, nova_senha, confirmar_senha]):
                self.tela_sistema.exibir_popup_erro('Para alterar a senha, preencha todos os campos de senha!')
                return False
            
            if nova_senha != confirmar_senha:
                self.tela_sistema.exibir_popup_erro('Nova senha e confirmação não coincidem!')
                return False
            
            if len(nova_senha) < 6:
                self.tela_sistema.exibir_popup_erro('A nova senha deve ter pelo menos 6 caracteres!')
                return False
            
            # Verificar senha atual
            if not self._verificar_senha_atual(organizador, senha_atual):
                self.tela_sistema.exibir_popup_erro('Senha atual incorreta!')
                return False
        
        # Atualizar dados
        organizador.atualizar_dados(nome=nome, email=email)
        
        # Atualizar senha se necessário
        if alterar_senha:
            nova_senha_hash = self._hash_senha(nova_senha)
            organizador.atualizar_dados(senha_hash=nova_senha_hash)
        
        # Salvar no banco
        if self.organizador_dao.atualizar(organizador):
            self.tela_sistema.exibir_popup_sucesso('Perfil atualizado com sucesso!')
            return True
        else:
            self.tela_sistema.exibir_popup_erro('Erro ao atualizar perfil!')
            return False

    def _verificar_senha_atual(self, organizador: Organizador, senha_atual: str) -> bool:
        """Verifica se a senha atual está correta"""
        try:
            senha_bytes = senha_atual.encode('utf-8')
            hash_bytes = organizador.senha_hash.encode('utf-8')
            return bcrypt.checkpw(senha_bytes, hash_bytes)
        except Exception:
            return False
