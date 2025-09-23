import PySimpleGUI as sg
from controle.controlador_organizador import ControladorOrganizador
from limite.tela_principal import criar_janela_principal
from limite.tela_organizador import criar_janela_cadastro


class ControladorSistema:
	def __init__(self):
		self.ctrl_organizador = ControladorOrganizador()
		self.janela_principal = criar_janela_principal()
		self.janela_cadastro_organizador = None

	def run(self):
		while True:
			window, event, values = sg.read_all_windows()

			if window == self.janela_principal and event in (sg.WIN_CLOSED, 'Sair'):
				break

			if event == '-CADASTRO_ORGANIZADOR-':
				self.abrir_cadastro_organizador()

			if window == self.janela_cadastro_organizador:
				if event in (sg.WIN_CLOSED, '-VOLTAR-'):
					self.fechar_cadastro_organizador()
				elif event == '-CADASTRAR-':
					ok = self.ctrl_organizador.cadastrar_organizador(values)
					if ok:
						self.fechar_cadastro_organizador()

		self.janela_principal.close()

	def abrir_cadastro_organizador(self):
		self.janela_principal.hide()
		self.janela_cadastro_organizador = criar_janela_cadastro('Organizador')

	def fechar_cadastro_organizador(self):
		if self.janela_cadastro_organizador:
			self.janela_cadastro_organizador.close()
			self.janela_cadastro_organizador = None
		self.janela_principal.un_hide()
