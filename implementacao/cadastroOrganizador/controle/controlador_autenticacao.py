import sys
import os
import PySimpleGUI as sg
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from entidade.organizador import Organizador
from entidade.sessao import Sessao
from persistencia.organizador_dao import OrganizadorDAO
from limite.tela_sistema import TelaSistema
from validadores import validar_cpf

class ControladorAutenticacao:
    def __init__(self, tela_sistema: TelaSistema):
        self.organizador_dao = OrganizadorDAO()
        self.tela_sistema = tela_sistema
        self.sessao_ativa = None

    def fazer_login(self, cpf: str, senha: str) -> bool:
        """Realiza login do organizador"""
        if not cpf or not senha:
            self.tela_sistema.exibir_popup_erro('CPF e senha são obrigatórios!')
            return False
        
        if not validar_cpf(cpf):
            self.tela_sistema.exibir_popup_erro('CPF inválido!')
            return False
        
        organizador = self.organizador_dao.autenticar(cpf, senha)
        
        if organizador:
            self.sessao_ativa = Sessao(
                organizador_id=1,  # Seria o ID real do banco
                cpf=organizador.cpf,
                nome=organizador.nome
            )
            return True
        else:
            self.tela_sistema.exibir_popup_erro('CPF ou senha incorretos!')
            return False

    def fazer_logout(self):
        """Realiza logout do organizador"""
        if self.sessao_ativa:
            self.sessao_ativa.desativar()
            self.sessao_ativa = None

    def verificar_sessao_ativa(self) -> bool:
        """Verifica se há uma sessão ativa"""
        return self.sessao_ativa is not None and self.sessao_ativa.ativa

    def obter_organizador_logado(self) -> Organizador:
        """Retorna o organizador da sessão ativa"""
        if self.verificar_sessao_ativa():
            return self.organizador_dao.buscar_por_cpf(self.sessao_ativa.cpf)
        return None

    def obter_sessao_ativa(self) -> Sessao:
        """Retorna a sessão ativa"""
        return self.sessao_ativa

    def abrir_tela_login(self):
        """Abre a tela de login"""
        janela_login = self.tela_sistema.criar_janela_login()
        
        if janela_login is None:
            print("Error: Failed to create login window")
            return False
        
        while True:
            event, values = janela_login.read()
            
            if event in ('-VOLTAR-', sg.WIN_CLOSED):
                janela_login.close()
                return False
            
            elif event == '-ENTRAR-':
                cpf = values['-CPF_LOGIN-']
                senha = values['-SENHA_LOGIN-']
                
                if self.fazer_login(cpf, senha):
                    janela_login.close()
                    return True
            
            elif event == '-CADASTRAR-':
                janela_login.close()
                # Retornar para cadastro
                return 'cadastro'
        
        janela_login.close()
        return False
