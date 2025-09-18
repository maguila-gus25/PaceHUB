import PySimpleGUI as sg

def criar_janela_cadastro_kit():
    """
    Cria uma janela para o organizador cadastrar um novo kit para um evento.
    """
    sg.theme('DarkBlue14')

    layout = [
        [sg.Text('Cadastro de Kit de Corrida', font=('Helvetica', 20))],
        [sg.Text('Nome do Kit*', size=(12, 1)), sg.Input(key='-NOME_KIT-')],
        [sg.Text('Descrição*', size=(12, 1)), sg.Multiline(key='-DESCRICAO-', size=(45, 5), no_scrollbar=True)],
        [sg.Text('Valor (R$)*', size=(12, 1)), sg.Input(key='-VALOR-', size=(15,1))],
        [sg.Text('* Campos obrigatórios.', text_color='red')],
        [sg.Button('Cadastrar Kit', key='-CADASTRAR_KIT-'), sg.Button('Cancelar', key='-CANCELAR-')]
    ]

    return sg.Window('PaceHub - Cadastrar Kit', layout, finalize=True)

# --- LÓGICA PRINCIPAL ---
if __name__ == '__main__':
    janela_kit = criar_janela_cadastro_kit()

    while True:
        event, values = janela_kit.read()
        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            break

        if event == '-CADASTRAR_KIT-':
            # Validação simples para campos vazios
            nome_kit = values['-NOME_KIT-']
            descricao = values['-DESCRICAO-']
            valor = values['-VALOR-']

            if not nome_kit or not descricao or not valor:
                sg.popup_error('Todos os campos são obrigatórios. Por favor, preencha-os.')
                continue # Mantém a janela aberta para correção

            # Simulação do cadastro
            dados_kit = f"""Kit cadastrado com sucesso!
-----------------------------------
Nome: {nome_kit}
Descrição: {descricao}
Valor: R$ {valor}
"""
            sg.popup(dados_kit)
            break # Fecha a janela após o sucesso

    janela_kit.close()