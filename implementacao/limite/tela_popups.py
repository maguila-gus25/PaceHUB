import PySimpleGUI as sg

def exibir_popup_erro(mensagem: str):
    sg.popup_error(mensagem)

def exibir_popup_sucesso(mensagem: str, dados: str):
    sg.popup(mensagem, dados)