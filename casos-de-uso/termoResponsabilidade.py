import PySimpleGUI as sg

def criar_janela_termo():
    sg.theme('DarkBlue14')

    termo_responsabilidade = """
Declaro que participo deste evento por livre e espontânea vontade,
isentando de qualquer responsabilidade os organizadores, patrocinadores
e realizadores, em meu nome e de meus sucessores. Declaro estar em
boas condições de saúde e ter treinado apropriadamente para a prova.
"""

    layout = [
        [sg.Text('Termo de Responsabilidade', font=('Helvetica', 20))],
        [sg.Multiline(default_text=termo_responsabilidade, disabled=True, size=(60, 10), autoscroll=True)],
        [sg.Checkbox('Li e aceito os termos de responsabilidade e isenção de riscos.', key='-TERMO_ACEITO-')],
        [sg.Button('Confirmar', key='-CONFIRMAR-'), sg.Button('Voltar', key='-VOLTAR-')]
    ]

    return sg.Window('PaceHub - Termo de Responsabilidade', layout, size=(500, 350), finalize=True)

if __name__ == '__main__':
    janela_termo = criar_janela_termo()

    while True:
        event, values = janela_termo.read()
        if event in (sg.WIN_CLOSED, '-VOLTAR-'):
            break
        if event == '-CONFIRMAR-':
            if values['-TERMO_ACEITO-']:
                sg.popup('Termo aceito com sucesso!')
                break
            else:
                sg.popup_error('Você precisa aceitar os termos para continuar.')
                
    janela_termo.close()