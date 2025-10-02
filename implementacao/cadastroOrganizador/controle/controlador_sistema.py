import PySimpleGUI as sg
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from limite.tela_sistema import TelaSistema
from controle.controlador_organizador import ControladorOrganizador
from controle.controlador_autenticacao import ControladorAutenticacao
from controle.controlador_perfil import ControladorPerfil

class ControladorSistema:
    def __init__(self):
        self.tela_sistema = TelaSistema()
        self.controlador_organizador = ControladorOrganizador(self.tela_sistema)
        self.controlador_auth = ControladorAutenticacao(self.tela_sistema)
        self.controlador_perfil = ControladorPerfil(self.tela_sistema)

    def iniciar(self):
        """Inicia o sistema com tela de login"""
        self._exibir_tela_login()

    def _exibir_tela_login(self):
        """Exibe a tela de login"""
        while True:
            resultado = self.controlador_auth.abrir_tela_login()
            
            if resultado == True:
                # Login bem-sucedido
                self._exibir_painel_organizador()
                break
            elif resultado == 'cadastro':
                # Usuário quer se cadastrar
                if self.controlador_organizador.abrir_tela_cadastro():
                    # Cadastro realizado com sucesso, voltar para login
                    continue
                else:
                    # Cadastro cancelado, voltar para login
                    continue
            else:
                # Usuário cancelou ou fechou
                break

    def _exibir_painel_organizador(self):
        """Exibe o painel do organizador logado"""
        organizador = self.controlador_auth.obter_organizador_logado()
        
        if not organizador:
            self.tela_sistema.exibir_popup_erro('Erro: Sessão inválida!')
            return
        
        janela_painel = self.tela_sistema.criar_janela_painel_organizador(organizador)
        
        while True:
            evento, values = janela_painel.read()
            
            if evento in (sg.WIN_CLOSED, '-SAIR-'):
                self.controlador_auth.fazer_logout()
                break
            
            elif evento == '-SAIR_PERFIL-':
                # Sair do perfil e voltar para login
                janela_painel.close()
                self.controlador_auth.fazer_logout()
                self._exibir_tela_login()
                break
            
            elif evento == '-PERFIL-':
                janela_painel.hide()
                self.controlador_perfil.abrir_tela_perfil(organizador)
                # Atualizar dados do organizador após edição
                organizador = self.controlador_auth.obter_organizador_logado()
                janela_painel.un_hide()
            
            elif evento == '-EVENTOS-':
                self.tela_sistema.exibir_popup_erro('Funcionalidade de eventos ainda não implementada.')
            
            elif evento == '-RELATORIOS-':
                self.tela_sistema.exibir_popup_erro('Funcionalidade de relatórios ainda não implementada.')
        
        janela_painel.close()

    def _exibir_menu_principal(self):
        """Exibe o menu principal com opções CRUD (método legado)"""
        janela_menu = self.tela_sistema.criar_janela_menu_principal()

        while True:
            evento, values = janela_menu.read()

            if evento in (sg.WIN_CLOSED, '-SAIR-'):
                break
            
            elif evento == '-CADASTRAR-':
                janela_menu.hide()
                self.controlador_organizador.abrir_tela_cadastro()
                janela_menu.un_hide()
            
            elif evento == '-LISTAR-':
                janela_menu.hide()
                self.controlador_organizador.abrir_tela_listagem()
                janela_menu.un_hide()
            
            elif evento == '-BUSCAR-':
                janela_menu.hide()
                self.controlador_organizador.abrir_tela_busca()
                janela_menu.un_hide()

        janela_menu.close()

    def iniciar_login(self):
        """Método alternativo para iniciar com tela de login (compatibilidade)"""
        janela_login = self.tela_sistema.criar_janela_login()

        while True:
            evento, values = janela_login.read()

            if evento in (sg.WIN_CLOSED, 'Sair'):
                break
            
            if evento == '-CADASTRO_ORGANIZADOR-':
                janela_login.hide()
                self.controlador_organizador.abrir_tela_cadastro()
                janela_login.un_hide()
            
            elif evento == '-CADASTRO_ATLETA-':
                self.tela_sistema.exibir_popup_erro("Cadastro de Atleta ainda não implementado.")

            elif evento == 'Login':
                self.tela_sistema.exibir_popup_erro("Funcionalidade de Login ainda não implementada.")

        janela_login.close()