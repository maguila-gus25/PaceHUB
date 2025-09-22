from limite.tela_principal import TelaPrincipal
from controle.controlador_atleta import ControladorAtleta
from persistencia.usuario_dao import UsuarioDAO


class ControladorSistema:
    def __init__(self):
        self.__tela_principal = TelaPrincipal()
        self.__usuario_dao = UsuarioDAO()
        self.__controlador_atleta = ControladorAtleta(self, self.__tela_principal, self.__usuario_dao)

    def iniciar(self):
        while True:
            evento, valores = self.__tela_principal.exibir_janela_login()
            if evento is None:
                break
            if evento == '-CADASTRO_ATLETA-':
                self.__controlador_atleta.abre_tela_cadastro()
            elif evento == '-CADASTRO_ORGANIZADOR-':
                self.exibir_popup_erro('Cadastro de Organizador ainda não implementado.')
            elif evento == 'Login':
                self.exibir_popup_erro('Funcionalidade de Login ainda não implementada.')
            elif evento == '-LISTAR_ATLETAS-':
                self.__controlador_atleta.listar_atletas()

        self.__tela_principal.root.destroy()

    def exibir_popup_erro(self, mensagem: str):
        self.__tela_principal.exibir_popup_erro(mensagem)

    def exibir_popup_sucesso(self, mensagem: str):
        self.__tela_principal.exibir_popup_sucesso(mensagem)