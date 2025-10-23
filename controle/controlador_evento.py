import PySimpleGUI as sg
from entidade.organizador import Organizador
from limite.tela_evento import TelaEvento
from entidade.evento import Evento
from entidade.kit_de_corrida import KitDeCorrida
from datetime import datetime
from persistencia.evento_dao import EventoDAO
from persistencia.usuario_dao import UsuarioDAO


class ControladorEvento:
    def __init__(self, controlador_sistema, evento_dao: EventoDAO, usuario_dao: UsuarioDAO):
        self.__controlador_sistema = controlador_sistema
        self.__tela_evento = TelaEvento()
        self.__evento_dao = evento_dao
        self.__usuario_dao = usuario_dao

    def abre_tela_novo_evento(self, organizador_logado: Organizador):

        janela_principal = self.__tela_evento.exibir_janela_novo_evento()
        kits_do_evento_obj = []

        while True:
            window, event, values = sg.read_all_windows()

            if window == janela_principal and event in (sg.WIN_CLOSED, '-CANCELAR-'):
                break

            if event == '-BOTAO_CALENDARIO_EVENTO-' or event == '-BOTAO_CALENDARIO_CANCEL-':
                meses = ('Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro',
                         'Outubro', 'Novembro', 'Dezembro')
                dias = ('Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb')

                data_tuple = sg.popup_get_date(
                    month_names=meses,
                    day_abbreviations=dias,
                    title="Selecione uma data"
                )

                if data_tuple:
                    mes, dia, ano = data_tuple
                    data_formatada = f"{dia:02d}/{mes:02d}/{ano}"

                    if event == '-BOTAO_CALENDARIO_EVENTO-':
                        janela_principal['-DATA_EVENTO-'].update(data_formatada)
                    else:
                        janela_principal['-DATA_CANCEL-'].update(data_formatada)

            if event == '-CADASTRAR_KITS-':
                janela_kits = self.__tela_evento.exibir_janela_cadastro_kit([str(k) for k in kits_do_evento_obj])

                while True:
                    event_kit, values_kit = janela_kits.read()
                    if event_kit in (sg.WIN_CLOSED, '-SALVAR_KITS-'):
                        break

                    if event_kit == '-ADICIONAR_KIT-':
                        nome = values_kit['-NOME_KIT-']
                        descricao = values_kit['-DESCRICAO-']
                        valor_str = values_kit['-VALOR-']

                        if nome and descricao and valor_str:
                            try:
                                valor = float(valor_str.replace(',', '.'))
                                novo_kit = KitDeCorrida(nome, descricao, valor)
                                kits_do_evento_obj.append(novo_kit)
                                janela_kits['-LISTA_KITS-'].update(values=[str(k) for k in kits_do_evento_obj])

                                janela_kits['-NOME_KIT-'].update('')
                                janela_kits['-DESCRICAO-'].update('')
                                janela_kits['-VALOR-'].update('')
                            except ValueError:
                                self.__controlador_sistema.exibir_popup_erro(
                                    'O valor do kit deve ser um número válido.')
                        else:
                            self.__controlador_sistema.exibir_popup_erro('Todos os campos do kit são obrigatórios.')

                    if event_kit == '-REMOVER_KIT-':
                        selecionados = values_kit['-LISTA_KITS-']
                        if selecionados:
                            kit_str_para_remover = selecionados[0]
                            kit_para_remover = next((k for k in kits_do_evento_obj if str(k) == kit_str_para_remover),
                                                    None)

                            if kit_para_remover:
                                kits_do_evento_obj.remove(kit_para_remover)
                                janela_kits['-LISTA_KITS-'].update(values=[str(k) for k in kits_do_evento_obj])

                janela_kits.close()
                janela_principal['-STATUS_KITS-'].update(f'{len(kits_do_evento_obj)} kit(s) cadastrado(s).',
                                                         text_color='lime')

            if event == '-SALVAR_EVENTO-':
                campos_obrigatorios = ['-NOME_EVENTO-', '-DATA_EVENTO-', '-DISTANCIA-', '-LOCAL-', '-HORAS-',
                                       '-MINUTOS-', '-DATA_CANCEL-']
                if any(not values[campo] for campo in campos_obrigatorios) or not kits_do_evento_obj:
                    self.__controlador_sistema.exibir_popup_erro(
                        'Por favor, preencha todos os campos e cadastre pelo menos um kit.')
                    continue

                try:
                    data_evento_str = values['-DATA_EVENTO-']
                    data_cancel_str = values['-DATA_CANCEL-']

                    data_evento_obj = datetime.strptime(data_evento_str, '%d/%m/%Y')
                    data_cancel_obj = datetime.strptime(data_cancel_str, '%d/%m/%Y')

                    if data_cancel_obj > data_evento_obj:
                        self.__controlador_sistema.exibir_popup_erro(
                            'A data limite para cancelamento não pode ser posterior à data do evento.')
                        continue
                    if data_evento_obj < datetime.now():
                        self.__controlador_sistema.exibir_popup_erro('A data do evento não pode ser no passado.')
                        continue

                except ValueError:
                    self.__controlador_sistema.exibir_popup_erro('As datas inseridas não são válidas.')
                    continue

                tempo_corte = f"{values['-HORAS-']}:{values['-MINUTOS-']}"
                distancia_str = values['-DISTANCIA-']

                evento = Evento(
                    nome=values['-NOME_EVENTO-'],
                    data=values['-DATA_EVENTO-'],
                    distancia=int(distancia_str),
                    local_largada=values['-LOCAL-'],
                    tempo_corte=tempo_corte,
                    data_limite_cred=values['-DATA_CANCEL-'],
                    organizador_cpf=organizador_logado.cpf
                )
                evento.kits = kits_do_evento_obj

                try:
                    self.__evento_dao.add_evento(evento)
                    self.__controlador_sistema.exibir_popup_sucesso('Evento criado e salvo no banco de dados.')
                    break
                except Exception as e:
                    self.__controlador_sistema.exibir_popup_erro(f'Erro ao salvar evento no banco de dados: {e}')

        janela_principal.close()