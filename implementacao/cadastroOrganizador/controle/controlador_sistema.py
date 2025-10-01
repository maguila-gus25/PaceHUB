import PySimpleGUI as sg
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from limite.tela_sistema import TelaSistema
from controle.controlador_organizador import ControladorOrganizador

class ControladorSistema:
    def __init__(self):
        self.tela_sistema = TelaSistema()
        self.controlador_organizador = ControladorOrganizador(self.tela_sistema)

    def iniciar(self):
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