import PySimpleGUI as sg

def criar_janela_visualizar_estatisticas():
    sg.theme('DarkBlue14')

    layout = [
        [sg.Text('Estatísticas do Evento - [Nome do Evento]', font=('Helvetica', 20))],
        [sg.Text('Total de Inscritos: 2855')],
        [sg.HorizontalSeparator()],
        [sg.Text('Distribuição por Gênero:', font=('Helvetica', 15))],
        # Aqui poderia ser inserido um gráfico
        [sg.Text('Masculino: 60%')],
        [sg.Text('Feminino: 40%')],
        [sg.HorizontalSeparator()],
        [sg.Text('Distribuição por Faixa Etária:', font=('Helvetica', 15))],
        # Aqui poderia ser inserido um gráfico
        [sg.Text('Júnior (até 17): 10%')],
        [sg.Text('Adulto (18-49): 70%')],
        [sg.Text('Master (50+): 20%')],
        [sg.Button('Voltar', key='-VOLTAR-')]
    ]

    return sg.Window('PaceHub - Estatísticas do Evento', layout, size=(500, 400), finalize=True)

if __name__ == '__main__':
    janela_visualizar_estatisticas = criar_janela_visualizar_estatisticas()

    while True:
        event, values = janela_visualizar_estatisticas.read()
        if event in (sg.WIN_CLOSED, '-VOLTAR-'):
            break

    janela_visualizar_estatisticas.close()