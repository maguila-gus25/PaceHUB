import PySimpleGUI as sg

def criar_janela_importar_resultados():
    sg.theme('DarkBlue14')

    layout = [
        [sg.Text('Importar Resultados', font=('Helvetica', 20))],
        [sg.Text('Selecione o arquivo de resultados (.csv):')],
        [sg.Input(key='-ARQUIVO-', readonly=True), sg.FileBrowse('Selecionar Arquivo')],
        [sg.Button('Importar', key='-IMPORTAR-'), sg.Button('Cancelar', key='-CANCELAR-')]
    ]

    return sg.Window('PaceHub - Importar Resultados', layout, finalize=True)

if __name__ == '__main__':
    janela_importar_resultados = criar_janela_importar_resultados()

    while True:
        event, values = janela_importar_resultados.read()
        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            break
        if event == '-IMPORTAR-':
            if values['-ARQUIVO-']:
                sg.popup('Resultados importados com sucesso!')
                break
            else:
                sg.popup_error('Por favor, selecione um arquivo.')

    janela_importar_resultados.close()