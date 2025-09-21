import PySimpleGUI as sg
from organizador import Organizador
from validations import validar_nome_completo, validar_email, validar_cpf, verificar_cpf_existente

# Simulação de um banco de dados para a verificação de CPFs (RN12)
cpfs_cadastrados_org = []

def criar_janela_login():
    sg.theme('DarkBlue14')
    layout = [
        [sg.Text('PaceHub', font=('Helvetica', 25), justification='center', expand_x=True)],
        [sg.Text('Sua plataforma de gestão de corridas.', font=('Helvetica', 12), justification='center', expand_x=True)],
        [sg.VPush()],
        [sg.Text('CPF*'), sg.Input(key='-CPF_LOGIN-')],
        [sg.Text('Senha*'), sg.Input(key='-SENHA_LOGIN-', password_char='*')],
        [sg.Text('* Campos obrigatórios', text_color='red')],
        [sg.Button('Login', size=(10, 1), expand_x=True)],
        [sg.Text('_' * 40)],
        [sg.Text('Ainda não tem uma conta? Cadastre-se agora!')],
        [sg.Button('Cadastrar como Atleta', key='-CADASTRO_ATLETA-', expand_x=True)],
        [sg.Button('Cadastrar como Organizador', key='-CADASTRO_ORGANIZADOR-', expand_x=True)],
        [sg.VPush()],
    ]
    return sg.Window('PaceHub - Bem-vindo', layout, size=(400, 350), finalize=True)


def criar_janela_cadastro(perfil: str):
    sg.theme('DarkBlue14')
    layout_usuario = [
        [sg.Text(f'Cadastro de {perfil}', font=('Helvetica', 20))],
        [sg.Frame('Dados Pessoais', [
            [sg.Text('Nome Completo*', size=(15, 1)), sg.Input(key='-NOME-')],
            [sg.Text('CPF*', size=(15, 1)), sg.Input(key='-CPF-')],
            [sg.Text('Email*', size=(15,1)), sg.Input(key='-EMAIL-')],
            [sg.Text('Senha*', size=(15,1)), sg.Input(key='-SENHA-', password_char='*')],
        ])],
        [sg.Text('* Todos os campos são obrigatórios.', text_color='red')],
        [sg.Button('Cadastrar', key='-CADASTRAR-', size=(10, 1))],
        [sg.Button('Voltar', key='-VOLTAR-', size=(10, 1))]
    ]
    return sg.Window(f'PaceHub - Cadastro de {perfil}', [layout_usuario], finalize=True, resizable=True)


if __name__ == '__main__':
    janela_login = criar_janela_login()

    while True:
        window, event, values = sg.read_all_windows()

        if window == janela_login and event in (sg.WIN_CLOSED, 'Sair'):
            break

        if event == 'Login':
            sg.popup(f"Lógica de login a ser implementada para o CPF: {values['-CPF_LOGIN-']}")
        
        if event == '-CADASTRO_ORGANIZADOR-':
            janela_login.hide()
            janela_cadastro_org = criar_janela_cadastro('Organizador')

            while True:
                event_cad, values_cad = janela_cadastro_org.read()
                
                if event_cad in (sg.WIN_CLOSED, '-VOLTAR-'):
                    janela_cadastro_org.close()
                    janela_login.un_hide()
                    break
                
                if event_cad == '-CADASTRAR-':
                    # --- VALIDAÇÕES INTEGRADAS ---
                    nome = values_cad['-NOME-']
                    cpf = values_cad['-CPF-']
                    email = values_cad['-EMAIL-']
                    senha = values_cad['-SENHA-']

                    # 1. Verifica campos vazios
                    if not all([nome, cpf, email, senha]):
                        sg.popup_error('Todos os campos com * são obrigatórios!')
                        continue

                    # 2. Valida nome completo
                    if not validar_nome_completo(nome):
                        sg.popup_error('Por favor, insira seu nome completo (nome e sobrenome).')
                        continue

                    # 3. Valida formato do e-mail
                    if not validar_email(email):
                        sg.popup_error('O formato do e-mail inserido é inválido.')
                        continue
                    
                    # 4. Valida o CPF
                    if not validar_cpf(cpf):
                        sg.popup_error('O CPF inserido é inválido!')
                        continue
                    
                    # 5. Verifica se o CPF já existe (RN12)
                    if verificar_cpf_existente(cpf, cpfs_cadastrados_org):
                        sg.popup_error(f'O CPF {cpf} já está cadastrado no sistema.')
                        continue
                    
                    # Se todas as validações passaram:
                    organizador = Organizador(
                        nome=nome, cpf=cpf, email=email, senha=senha
                    )
                    cpfs_cadastrados_org.append(cpf) # Adiciona ao "banco de dados"
                    
                    sg.popup('Cadastro Realizado com Sucesso!', f"Dados cadastrados:\n\n{organizador}")
                    janela_cadastro_org.close()
                    janela_login.un_hide()
                    break

    janela_login.close()