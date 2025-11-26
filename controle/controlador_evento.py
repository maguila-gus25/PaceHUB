import FreeSimpleGUI as sg
from entidade.organizador import Organizador
from limite.tela_evento import TelaEvento
from entidade.evento import Evento
from entidade.kit_de_corrida import KitDeCorrida
from datetime import datetime
from persistencia.evento_dao import EventoDAO
from persistencia.usuario_dao import UsuarioDAO
from typing import List, Tuple, Optional


class ControladorEvento:
    def __init__(self, controlador_sistema, evento_dao: EventoDAO, usuario_dao: UsuarioDAO):
        self.__controlador_sistema = controlador_sistema
        self.__tela_evento = TelaEvento()
        self.__evento_dao = evento_dao
        self.__usuario_dao = usuario_dao

    
    def criar_evento(self, nome: str, data: str, distancia: int, local_largada: str, 
                     tempo_corte: str, data_limite_cred: str, organizador_cpf: str, 
                     kits: List[KitDeCorrida]) -> Evento:
        """Cria um novo objeto Evento com os dados fornecidos."""
        evento = Evento(
            nome=nome,
            data=data,
            distancia=distancia,
            local_largada=local_largada,
            tempo_corte=tempo_corte,
            data_limite_cred=data_limite_cred,
            organizador_cpf=organizador_cpf
        )
        evento.kits = kits
        return evento
    
    def salvar_evento_no_banco(self, evento: Evento) -> bool:
        """Salva um evento no banco de dados."""
        try:
            self.__evento_dao.add_evento(evento)
            self.__controlador_sistema.exibir_popup_sucesso(self.MSG_SUCESSO_EVENTO_CRIADO)
            return True
        except Exception as e:
            self.__controlador_sistema.exibir_popup_erro(f'{self.MSG_ERRO_SALVAR_BANCO} {str(e)}')
            return False
    
    def atualizar_evento_no_banco(self, evento: Evento) -> bool:
        """Atualiza um evento existente no banco de dados."""
        try:
            self.__evento_dao.update_evento(evento)
            self.__controlador_sistema.exibir_popup_sucesso(self.MSG_SUCESSO_EVENTO_ATUALIZADO)
            return True
        except Exception as e:
            self.__controlador_sistema.exibir_popup_erro(f'{self.MSG_ERRO_ATUALIZAR_BANCO} {str(e)}')
            return False
    
    def atualizar_dados_evento(self, evento: Evento, nome: str, data: str, distancia: int, 
                               local_largada: str, tempo_corte: str, data_limite_cred: str, 
                               kits: List[KitDeCorrida]) -> None:
        """Atualiza os dados de um evento existente."""
        evento.nome = nome
        evento.data = data
        evento.distancia = distancia
        evento.local_largada = local_largada
        evento.tempo_corte = tempo_corte
        evento.data_limite_cred = data_limite_cred
        evento.kits = kits
    
    def validar_dados_evento(self, values: dict, kits_do_evento: List[KitDeCorrida], 
                             validar_data_passado: bool = True) -> Tuple[bool, Optional[str]]:
        """Valida os dados do evento. Retorna (sucesso, mensagem_erro)."""
        campos_obrigatorios = ['-NOME_EVENTO-', '-DATA_EVENTO-', '-DISTANCIA-', '-LOCAL-', '-HORAS-', '-MINUTOS-', '-DATA_CANCEL-']
        
        if any(not values.get(campo) for campo in campos_obrigatorios):
            return False, self.MSG_ERRO_CAMPOS_OBRIGATORIOS
        
        if not kits_do_evento:
            return False, self.MSG_ERRO_CADASTRO_KIT_MINIMO
        
        try:
            data_evento_str = values['-DATA_EVENTO-']
            data_cancel_str = values['-DATA_CANCEL-']
            
            data_evento_obj = datetime.strptime(data_evento_str, '%d/%m/%Y')
            data_cancel_obj = datetime.strptime(data_cancel_str, '%d/%m/%Y')
            
            if data_cancel_obj > data_evento_obj:
                return False, self.MSG_ERRO_DATA_LIMITE_POSTERIOR
            
            if validar_data_passado and data_evento_obj < datetime.now():
                return False, self.MSG_ERRO_DATA_PASSADO
        
        except ValueError:
            return False, self.MSG_ERRO_DATA_INVALIDA
        
        try:
            horas_int = int(values['-HORAS-'])
            minutos_int = int(values['-MINUTOS-'])
            
            if not (0 <= horas_int <= 24) or not (0 <= minutos_int <= 59):
                return False, self.MSG_ERRO_TEMPO_CORTE_INTERVALO
            
            if horas_int == 24 and minutos_int > 0:
                return False, self.MSG_ERRO_TEMPO_CORTE_EXCEDE_MAX
        
        except ValueError:
            return False, self.MSG_ERRO_TEMPO_CORTE_INVALIDO
        
        return True, None
    
    def processar_selecao_data(self, event: str, janela) -> None:
        """Processa a seleção de data do calendário."""
        meses = ('Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 
                 'Setembro', 'Outubro', 'Novembro', 'Dezembro')
        dias = ('Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb')
        
        data_tuple = sg.popup_get_date(
            month_names=meses,
            day_abbreviations=dias,
            title=self.MSG_TITULO_SELECIONAR_DATA
        )
        
        if data_tuple:
            mes, dia, ano = data_tuple
            data_formatada = f"{dia:02d}/{mes:02d}/{ano}"
            
            if event == '-BOTAO_CALENDARIO_EVENTO-':
                janela['-DATA_EVENTO-'].update(data_formatada)
            else:
                janela['-DATA_CANCEL-'].update(data_formatada)
    
    
    def validar_dados_kit(self, nome: str, descricao: str, valor_str: str) -> Tuple[bool, Optional[float], Optional[str]]:
        """Valida os dados do kit. Retorna (sucesso, valor_float, mensagem_erro)."""
        if not (nome and descricao and valor_str):
            return False, None, self.MSG_ERRO_CAMPOS_KIT_OBRIGATORIOS
        
        try:
            valor = float(valor_str.replace(',', '.'))
            if valor < 0:
                return False, None, self.MSG_ERRO_VALOR_NEGATIVO
            return True, valor, None
        except ValueError:
            return False, None, self.MSG_ERRO_VALOR_NUMERICO_INVALIDO
    
    def criar_kit(self, nome: str, descricao: str, valor: float) -> KitDeCorrida:
        """Cria um novo objeto KitDeCorrida."""
        return KitDeCorrida(nome, descricao, valor)
    
    def adicionar_kit(self, kits_lista: List[KitDeCorrida], nome: str, descricao: str, valor: float) -> bool:
        """Adiciona um kit à lista de kits."""
        try:
            novo_kit = self.criar_kit(nome, descricao, valor)
            kits_lista.append(novo_kit)
            return True
        except Exception as e:
            self.__controlador_sistema.exibir_popup_erro(f'{self.MSG_ERRO_ADICIONAR_KIT} {str(e)}')
            return False
    
    def remover_kit(self, kits_lista: List[KitDeCorrida], kit_para_remover: KitDeCorrida) -> bool:
        """Remove um kit da lista de kits."""
        try:
            if kit_para_remover in kits_lista:
                kits_lista.remove(kit_para_remover)
                return True
            return False
        except Exception as e:
            self.__controlador_sistema.exibir_popup_erro(f'{self.MSG_ERRO_REMOVER_KIT} {str(e)}')
            return False
    
    def buscar_kit_por_string(self, kits_lista: List[KitDeCorrida], kit_str: str) -> Optional[KitDeCorrida]:
        """Busca um kit na lista pelo seu string representation."""
        return next((k for k in kits_lista if str(k) == kit_str), None)
    
    def atualizar_kit(self, kit: KitDeCorrida, nome: str, descricao: str, valor: float) -> None:
        """Atualiza os dados de um kit existente."""
        kit.nome = nome
        kit.descricao = descricao
        kit.valor = valor
    
    def listar_kits(self, kits_lista: List[KitDeCorrida]) -> List[str]:
        """Retorna uma lista de strings representando os kits."""
        return [str(k) for k in kits_lista]
    
    def preparar_edicao_kit(self, janela_kits, kit: KitDeCorrida) -> None:
        """Prepara a interface para edição de um kit."""
        janela_kits['-NOME_KIT-'].update(kit.nome)
        janela_kits['-DESCRICAO-'].update(kit.descricao)
        valor_formatado = f'{kit.valor:.2f}'.replace('.', ',')
        janela_kits['-VALOR-'].update(valor_formatado)
        
        janela_kits['-ADICIONAR_KIT-'].update(visible=False)
        janela_kits['-SALVAR_EDICAO-'].update(visible=True)
        janela_kits['-CANCELAR_EDICAO-'].update(visible=True)
        janela_kits['-EDITAR_KIT-'].update(disabled=True)
        janela_kits['-REMOVER_KIT-'].update(disabled=True)
    
    def cancelar_edicao_kit(self, janela_kits) -> None:
        """Cancela a edição de um kit e restaura a interface."""
        janela_kits['-NOME_KIT-'].update('')
        janela_kits['-DESCRICAO-'].update('')
        janela_kits['-VALOR-'].update('')
        
        janela_kits['-ADICIONAR_KIT-'].update(visible=True)
        janela_kits['-SALVAR_EDICAO-'].update(visible=False)
        janela_kits['-CANCELAR_EDICAO-'].update(visible=False)
        janela_kits['-EDITAR_KIT-'].update(disabled=False)
        janela_kits['-REMOVER_KIT-'].update(disabled=False)
    
    def limpar_campos_kit(self, janela_kits) -> None:
        """Limpa os campos do formulário de kit."""
        janela_kits['-NOME_KIT-'].update('')
        janela_kits['-DESCRICAO-'].update('')
        janela_kits['-VALOR-'].update('')
    
    def atualizar_lista_kits_na_interface(self, janela_kits, kits_lista: List[KitDeCorrida]) -> None:
        """Atualiza a lista de kits na interface."""
        janela_kits['-LISTA_KITS-'].update(values=self.listar_kits(kits_lista))
    
    def atualizar_status_kits_na_interface(self, janela_principal, kits_lista: List[KitDeCorrida]) -> None:
        """Atualiza o status de kits na interface principal."""
        janela_principal['-STATUS_KITS-'].update(
            self.MSG_STATUS_KITS.format(len(kits_lista)),
            text_color='lime'
        )
    
    def abrir_janela_gerenciar_kits(self, kits_do_evento_obj: List[KitDeCorrida]) -> List[KitDeCorrida]:
        """Abre a janela de gerenciamento de kits e retorna a lista atualizada."""
        janela_kits = self.__tela_evento.exibir_janela_cadastro_kit(self.listar_kits(kits_do_evento_obj))
        kit_sendo_editado: Optional[KitDeCorrida] = None
        
        while True:
            event_kit, values_kit = janela_kits.read()
            
            if event_kit in (sg.WIN_CLOSED, '-SALVAR_KITS-'):
                break
            
            if event_kit == '-ADICIONAR_KIT-':
                nome = values_kit['-NOME_KIT-']
                descricao = values_kit['-DESCRICAO-']
                valor_str = values_kit['-VALOR-']
                
                sucesso, valor, mensagem_erro = self.validar_dados_kit(nome, descricao, valor_str)
                
                if sucesso and valor is not None:
                    if self.adicionar_kit(kits_do_evento_obj, nome, descricao, valor):
                        self.atualizar_lista_kits_na_interface(janela_kits, kits_do_evento_obj)
                        self.limpar_campos_kit(janela_kits)
                else:
                    self.__controlador_sistema.exibir_popup_erro(mensagem_erro or self.MSG_ERRO_ADICIONAR_KIT)
            
            if event_kit == '-REMOVER_KIT-':
                selecionados = values_kit['-LISTA_KITS-']
                if selecionados:
                    kit_str_para_remover = selecionados[0]
                    kit_para_remover = self.buscar_kit_por_string(kits_do_evento_obj, kit_str_para_remover)
                    
                    if kit_para_remover:
                        self.remover_kit(kits_do_evento_obj, kit_para_remover)
                        self.atualizar_lista_kits_na_interface(janela_kits, kits_do_evento_obj)
            
            if event_kit == '-EDITAR_KIT-':
                selecionados = values_kit['-LISTA_KITS-']
                if not selecionados:
                    self.__controlador_sistema.exibir_popup_erro(self.MSG_ERRO_KIT_NAO_SELECIONADO)
                    continue
                
                kit_str_para_editar = selecionados[0]
                kit_para_editar = self.buscar_kit_por_string(kits_do_evento_obj, kit_str_para_editar)
                
                if kit_para_editar:
                    kit_sendo_editado = kit_para_editar
                    self.preparar_edicao_kit(janela_kits, kit_sendo_editado)
            
            if event_kit == '-SALVAR_EDICAO-':
                nome = values_kit['-NOME_KIT-']
                descricao = values_kit['-DESCRICAO-']
                valor_str = values_kit['-VALOR-']
                
                sucesso, valor, mensagem_erro = self.validar_dados_kit(nome, descricao, valor_str)
                
                if sucesso and valor is not None and kit_sendo_editado:
                    self.atualizar_kit(kit_sendo_editado, nome, descricao, valor)
                    kit_sendo_editado = None
                    self.atualizar_lista_kits_na_interface(janela_kits, kits_do_evento_obj)
                    self.limpar_campos_kit(janela_kits)
                    self.cancelar_edicao_kit(janela_kits)
                else:
                    self.__controlador_sistema.exibir_popup_erro(mensagem_erro or self.MSG_ERRO_SALVAR_EDICAO_KIT)
            
            if event_kit == '-CANCELAR_EDICAO-':
                kit_sendo_editado = None
                self.limpar_campos_kit(janela_kits)
                self.cancelar_edicao_kit(janela_kits)
        
        janela_kits.close()
        return kits_do_evento_obj

    def abre_tela_novo_evento(self, organizador_logado: Organizador):
        """Abre a tela para cadastrar um novo evento."""
        janela_principal = self.__tela_evento.exibir_janela_novo_evento()
        kits_do_evento_obj = []

        while True:
            window, event, values = sg.read_all_windows()

            if window == janela_principal and event in (sg.WIN_CLOSED, '-CANCELAR-'):
                break

            if event == '-BOTAO_CALENDARIO_EVENTO-' or event == '-BOTAO_CALENDARIO_CANCEL-':
                self.processar_selecao_data(event, janela_principal)

            if event == '-CADASTRAR_KITS-':
                kits_do_evento_obj = self.abrir_janela_gerenciar_kits(kits_do_evento_obj)
                self.atualizar_status_kits_na_interface(janela_principal, kits_do_evento_obj)

            if event == '-SALVAR_EVENTO-':
                sucesso, mensagem_erro = self.validar_dados_evento(values, kits_do_evento_obj, validar_data_passado=True)
                
                if not sucesso:
                    self.__controlador_sistema.exibir_popup_erro(mensagem_erro or self.MSG_ERRO_VALIDACAO_DADOS)
                    continue

                horas_int = int(values['-HORAS-'])
                minutos_int = int(values['-MINUTOS-'])
                tempo_corte = f"{horas_int}:{minutos_int}"
                distancia_str = values['-DISTANCIA-']

                evento = self.criar_evento(
                    nome=values['-NOME_EVENTO-'],
                    data=values['-DATA_EVENTO-'],
                    distancia=int(distancia_str),
                    local_largada=values['-LOCAL-'],
                    tempo_corte=tempo_corte,
                    data_limite_cred=values['-DATA_CANCEL-'],
                    organizador_cpf=organizador_logado.cpf,
                    kits=kits_do_evento_obj
                )

                if self.salvar_evento_no_banco(evento):
                    break

        janela_principal.close()

    def carregar_dados_evento_na_interface(self, janela_principal, evento: Evento) -> None:
        """Carrega os dados de um evento na interface."""
        janela_principal['-NOME_EVENTO-'].update(evento.nome)
        janela_principal['-DATA_EVENTO-'].update(evento.data)
        janela_principal['-DISTANCIA-'].update(evento.distancia)
        janela_principal['-LOCAL-'].update(evento.local_largada)
        
        try:
            horas, minutos = evento.tempo_corte.split(':')
        except ValueError:
            horas, minutos = '6', '0'
        
        janela_principal['-HORAS-'].update(horas)
        janela_principal['-MINUTOS-'].update(minutos)
        janela_principal['-DATA_CANCEL-'].update(evento.data_limite_cred)
    
    def abre_tela_editar_evento(self, evento_para_editar: Evento, organizador_logado: Organizador):
        """Abre a tela para editar um evento existente."""
        kits_do_evento_obj = self.__evento_dao.get_kits_by_evento_id(evento_para_editar.id)
        evento_para_editar.kits = kits_do_evento_obj

        janela_principal = self.__tela_evento.exibir_janela_novo_evento()
        self.carregar_dados_evento_na_interface(janela_principal, evento_para_editar)
        self.atualizar_status_kits_na_interface(janela_principal, kits_do_evento_obj)

        while True:
            window, event, values = sg.read_all_windows()

            if window == janela_principal and event in (sg.WIN_CLOSED, '-CANCELAR-'):
                break

            if event == '-BOTAO_CALENDARIO_EVENTO-' or event == '-BOTAO_CALENDARIO_CANCEL-':
                self.processar_selecao_data(event, janela_principal)

            if event == '-CADASTRAR_KITS-':
                kits_do_evento_obj = self.abrir_janela_gerenciar_kits(kits_do_evento_obj)
                self.atualizar_status_kits_na_interface(janela_principal, kits_do_evento_obj)

            if event == '-SALVAR_EVENTO-':
                sucesso, mensagem_erro = self.validar_dados_evento(values, kits_do_evento_obj, validar_data_passado=False)
                
                if not sucesso:
                    self.__controlador_sistema.exibir_popup_erro(mensagem_erro or self.MSG_ERRO_VALIDACAO_DADOS)
                    continue

                horas_int = int(values['-HORAS-'])
                minutos_int = int(values['-MINUTOS-'])
                tempo_corte = f"{horas_int}:{minutos_int}"
                distancia_str = values['-DISTANCIA-']

                self.atualizar_dados_evento(
                    evento=evento_para_editar,
                    nome=values['-NOME_EVENTO-'],
                    data=values['-DATA_EVENTO-'],
                    distancia=int(distancia_str),
                    local_largada=values['-LOCAL-'],
                    tempo_corte=tempo_corte,
                    data_limite_cred=values['-DATA_CANCEL-'],
                    kits=kits_do_evento_obj
                )

                if self.atualizar_evento_no_banco(evento_para_editar):
                    break

        janela_principal.close()

    # ========== MENSAGENS ==========
    MSG_ERRO_CAMPOS_OBRIGATORIOS = 'Por favor, preencha todos os campos obrigatórios.'
    MSG_ERRO_CAMPOS_KIT_OBRIGATORIOS = 'Todos os campos do kit são obrigatórios.'
    MSG_ERRO_VALOR_NUMERICO_INVALIDO = 'O valor informado deve ser um número válido.'
    MSG_ERRO_VALOR_NEGATIVO = 'O valor informado não pode ser negativo.'
    MSG_ERRO_DATA_INVALIDA = 'As datas inseridas não são válidas.'
    MSG_ERRO_DATA_PASSADO = 'A data do evento não pode ser no passado.'
    MSG_ERRO_DATA_LIMITE_POSTERIOR = 'A data limite para cancelamento não pode ser posterior à data do evento.'
    MSG_ERRO_TEMPO_CORTE_INTERVALO = 'O tempo de corte deve estar entre 0h00 e 24h00.'
    MSG_ERRO_TEMPO_CORTE_EXCEDE_MAX = 'O tempo máximo não pode exceder 24h00.'
    MSG_ERRO_TEMPO_CORTE_INVALIDO = 'O tempo de corte (horas e minutos) deve ser um número válido.'
    MSG_ERRO_KIT_NAO_SELECIONADO = 'Por favor, selecione um kit da lista para editar.'
    MSG_ERRO_VALIDACAO_DADOS = 'Erro na validação dos dados.'
    MSG_ERRO_SALVAR_BANCO = 'Erro ao salvar no banco de dados.'
    MSG_ERRO_ATUALIZAR_BANCO = 'Erro ao atualizar no banco de dados.'
    MSG_ERRO_ADICIONAR_KIT = 'Erro ao adicionar kit.'
    MSG_ERRO_REMOVER_KIT = 'Erro ao remover kit.'
    MSG_ERRO_SALVAR_EDICAO_KIT = 'Erro ao salvar edição do kit.'
    MSG_ERRO_CADASTRO_KIT_MINIMO = 'Por favor, cadastre pelo menos um kit.'
    MSG_SUCESSO_EVENTO_CRIADO = 'Evento criado e salvo no banco de dados.'
    MSG_SUCESSO_EVENTO_ATUALIZADO = 'Evento ATUALIZADO no banco de dados.'
    MSG_TITULO_SELECIONAR_DATA = 'Selecione uma data'
    MSG_STATUS_KITS = '{0} kit(s) cadastrado(s).'