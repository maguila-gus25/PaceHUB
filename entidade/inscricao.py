from datetime import datetime

class Inscricao:
    def __init__(self, atleta_cpf, evento_id, kit_id, status, data_inscricao, kit_entregue: int = 0):
        self.__atleta_cpf = atleta_cpf
        self.__evento_id = evento_id
        self.__kit_id = kit_id
        self.__status = status
        if data_inscricao:
            self.data_inscricao = datetime.strptime(data_inscricao, '%Y-%m-%d %H:%M:%S')
        else:
            self.data_inscricao = datetime.now()
        self.__kit_entregue = kit_entregue

    @property
    def data_inscricao_str(self):
        return self.data_inscricao.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def atleta_cpf_str(self):
        return self.__atleta_cpf

    @property
    def evento_id(self):
        return self.__evento_id

    @property
    def kit_id(self):
        return self.__kit_id

    @property
    def kit_entregue(self):
        return self.__kit_entregue

    @kit_entregue.setter
    def kit_entregue(self, kit_entregue):
        self.__kit_entregue = kit_entregue

    @property
    def status(self):
        return self.__status