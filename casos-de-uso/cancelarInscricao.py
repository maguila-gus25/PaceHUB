import PySimpleGUI as sg
from datetime import datetime

def criar_janela_cancelar_inscricao():
    sg.theme('DarkBlue14')

    # Simulação de dados
    data_limite_str = "20/09/2025"
    data_limite = datetime.strptime(data_limite_str, "%d/%m/%Y")
    hoje = datetime.now()
    pode_cancelar = hoje < data_limite

    layout = [
        [sg.Text('Cancelar Inscrição', font=('Helvetica', 20))],
        [sg.Text('Evento: Maratona de Floripa')],
        [sg.Text(f'Data limite para cancelamento: {data_limite_str}')],
        [sg.Text('Você tem certeza que deseja cancelar sua inscrição?')],
        [sg.Button('Confirmar Cancelamento', key='-CONFIRMAR-', disabled=not pode_cancelar)],
        [sg.Button('Voltar', key='-VOLTAR-')]
    ]

    if not pode_cancelar:
        layout.insert(3, [sg.Text('O prazo para cancelamento já encerrou.', text_color='red')])

    return sg.Window('PaceHub - Cancelar Inscrição', layout, finalize=True)

if __name__ == '__main__':
    janela_cancelar = criar_janela_cancelar_inscricao()

    while True:
        event, values = janela_cancelar.read()
        if event in (sg.WIN_CLOSED, '-VOLTAR-'):
            break
        if event == '-CONFIRMAR-':
            sg.popup('Inscrição cancelada com sucesso.')
            break
            
    janela_cancelar.close()