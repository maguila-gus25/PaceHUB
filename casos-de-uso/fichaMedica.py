import PySimpleGUI as sg

def criar_janela_ficha_medica():
    sg.theme('DarkBlue14')

    layout = [
        [sg.Text('Ficha Médica', font=('Helvetica', 20))],
        [sg.Text('Possui alguma alergia? Se sim, qual?*'), sg.Input(key='-ALERGIA-')],
        [sg.Text('Usa algum medicamento controlado?*'), sg.Input(key='-MEDICAMENTO-')],
        [sg.Text('Contato de Emergência (Nome e Telefone)*'), sg.Input(key='-CONTATO_EMERGENCIA-')],
        [sg.Checkbox('Atesto que estou em condições de saúde aptas para a prática da atividade física.', key='-SAUDE_OK-')],
        [sg.Text('* Campos obrigatórios', text_color='red')],
        [sg.Button('Salvar', key='-SALVAR-'), sg.Button('Voltar', key='-VOLTAR-')]
    ]

    return sg.Window('PaceHub - Ficha Médica', layout, finalize=True)

if __name__ == '__main__':
    janela_ficha = criar_janela_ficha_medica()

    while True:
        event, values = janela_ficha.read()
        if event in (sg.WIN_CLOSED, '-VOLTAR-'):
            break
        if event == '-SALVAR-':
            if values['-SAUDE_OK-']:
                sg.popup('Ficha médica salva com sucesso!')
                break
            else:
                sg.popup_error('Você precisa atestar sua condição de saúde.')
            
    janela_ficha.close()