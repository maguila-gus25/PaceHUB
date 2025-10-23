import PySimpleGUI as sg


class TelaInscricao:

    def __init__(self):
        pass

    def exibir_tela_gerenciar_kit(self, nome_evento: str):
        sg.theme('DarkBlue14')  # Mesmo tema da imagem

        layout_busca = [
            [sg.Text('Buscar por Nome ou CPF:'),
             sg.Input(key='-INPUT_BUSCA-', size=(30, 1)),
             sg.Button('Buscar', key='-BUSCAR-')]
        ]

        layout_dados = [
            [sg.Text('Nome do Atleta:', size=(15, 1)), sg.Text('[Nome do Atleta]', key='-NOME_ATLETA-')],
            [sg.Text('CPF:', size=(15, 1)), sg.Text('[CPF do Atleta]', key='-CPF_ATLETA-')],
            [sg.Checkbox('Kit Entregue', key='-KIT_ENTREGUE-', disabled=True)]
        ]

        layout = [
            [sg.Text(f'Gerenciar Entrega de Kits - {nome_evento}', font=('Helvetica', 20, 'bold'))],
            [sg.Frame('Buscar Inscrição', layout_busca)],
            [sg.Frame('Dados da Inscrição', layout_dados)],
            [sg.Button('Salvar', key='-SALVAR-', disabled=True), sg.Button('Voltar', key='-VOLTAR-')]
        ]

        return sg.Window('PaceHub - Gerenciar Kits', layout, finalize=True, modal=True)