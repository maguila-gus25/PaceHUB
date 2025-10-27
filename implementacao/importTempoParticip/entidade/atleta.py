from datetime import datetime
from typing import Optional

class Atleta:
    """
    Classe que representa um atleta no sistema PaceHub.
    Contém informações pessoais e métodos para cálculo de categoria.
    """
    
    def __init__(self, cpf: str, nome: str, data_nascimento: str, genero: str, pcd: bool = False):
        """
        Inicializa um atleta.
        
        Args:
            cpf: CPF do atleta (apenas números)
            nome: Nome completo do atleta
            data_nascimento: Data de nascimento no formato DD/MM/YYYY
            genero: Gênero ('Masculino' ou 'Feminino')
            pcd: Se o atleta é pessoa com deficiência
        """
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento  # formato DD/MM/YYYY
        self.genero = genero  # 'Masculino' ou 'Feminino'
        self.pcd = pcd  # bool
    
    def calcular_idade(self, data_referencia: str) -> int:
        """
        Calcula a idade do atleta na data de referência.
        
        Args:
            data_referencia: Data no formato DD/MM/YYYY
            
        Returns:
            Idade em anos
        """
        try:
            # Converter strings para objetos datetime
            nascimento = datetime.strptime(self.data_nascimento, '%d/%m/%Y')
            referencia = datetime.strptime(data_referencia, '%d/%m/%Y')
            
            # Calcular idade
            idade = referencia.year - nascimento.year
            
            # Ajustar se ainda não fez aniversário no ano de referência
            if (referencia.month, referencia.day) < (nascimento.month, nascimento.day):
                idade -= 1
                
            return idade
        except ValueError:
            raise ValueError(f"Formato de data inválido: {self.data_nascimento} ou {data_referencia}")
    
    def calcular_categoria(self, data_evento: str) -> str:
        """
        Calcula a categoria do atleta baseada na RN04.
        RN04: A categoria do atleta é definida pela idade que ele terá em 31 de dezembro do ano do evento.
        
        Args:
            data_evento: Data do evento no formato DD/MM/YYYY
            
        Returns:
            Categoria: 'PCD', 'Júnior', 'Adulto' ou 'Master'
        """
        # Se é PCD, sempre compete na categoria PCD
        if self.pcd:
            return 'PCD'
        
        # Calcular idade em 31/12 do ano do evento
        try:
            ano_evento = datetime.strptime(data_evento, '%d/%m/%Y').year
            data_31_dezembro = f"31/12/{ano_evento}"
            idade = self.calcular_idade(data_31_dezembro)
            
            # RN07: Classificação por faixas etárias
            if idade <= 17:
                return 'Júnior'
            elif idade <= 49:
                return 'Adulto'
            else:  # 50+ anos
                return 'Master'
                
        except ValueError:
            raise ValueError(f"Formato de data inválido: {data_evento}")
    
    def __str__(self):
        return f"Atleta: {self.nome} (CPF: {self.cpf}, {self.genero}, PCD: {self.pcd})"
    
    def __repr__(self):
        return f"Atleta(cpf='{self.cpf}', nome='{self.nome}', genero='{self.genero}', pcd={self.pcd})"


# Mockdata: 50+ atletas com distribuição realista
ATLETAS_MOCK = [
    # Júnior Masculino (15 atletas)
    Atleta("11111111111", "Lucas Ferraz", "15/03/2008", "Masculino"),
    Atleta("11111111112", "Pedro Santos", "22/07/2007", "Masculino"),
    Atleta("11111111113", "Gabriel Oliveira", "10/12/2006", "Masculino"),
    Atleta("11111111114", "Rafael Costa", "05/05/2008", "Masculino"),
    Atleta("11111111115", "Felipe Silva", "18/09/2007", "Masculino"),
    Atleta("11111111116", "Bruno Lima", "03/01/2006", "Masculino"),
    Atleta("11111111117", "Diego Souza", "28/11/2008", "Masculino"),
    Atleta("11111111118", "Thiago Alves", "14/06/2007", "Masculino"),
    Atleta("11111111119", "Marcos Pereira", "07/04/2006", "Masculino"),
    Atleta("11111111120", "André Rocha", "25/08/2008", "Masculino"),
    Atleta("11111111121", "Carlos Mendes", "12/02/2007", "Masculino"),
    Atleta("11111111122", "João Pedro", "19/10/2006", "Masculino"),
    Atleta("11111111123", "Vitor Hugo", "31/12/2008", "Masculino"),
    Atleta("11111111124", "Eduardo Nunes", "16/07/2007", "Masculino"),
    Atleta("11111111125", "Henrique Dias", "08/03/2006", "Masculino"),
    
    # Júnior Feminino (15 atletas)
    Atleta("22222222221", "Clara Martins", "20/04/2008", "Feminino"),
    Atleta("22222222222", "Ana Beatriz", "13/08/2007", "Feminino"),
    Atleta("22222222223", "Maria Eduarda", "27/11/2006", "Feminino"),
    Atleta("22222222224", "Larissa Silva", "09/06/2008", "Feminino"),
    Atleta("22222222225", "Beatriz Costa", "15/01/2007", "Feminino"),
    Atleta("22222222226", "Isabella Santos", "03/09/2006", "Feminino"),
    Atleta("22222222227", "Gabriela Lima", "22/05/2008", "Feminino"),
    Atleta("22222222228", "Camila Souza", "11/12/2007", "Feminino"),
    Atleta("22222222229", "Julia Oliveira", "28/07/2006", "Feminino"),
    Atleta("22222222230", "Livia Alves", "06/03/2008", "Feminino"),
    Atleta("22222222231", "Sophia Pereira", "19/10/2007", "Feminino"),
    Atleta("22222222232", "Valentina Rocha", "14/08/2006", "Feminino"),
    Atleta("22222222233", "Helena Mendes", "25/04/2008", "Feminino"),
    Atleta("22222222234", "Alice Dias", "17/11/2007", "Feminino"),
    Atleta("22222222235", "Laura Nunes", "02/06/2006", "Feminino"),
    
    # Adulto Masculino (15 atletas)
    Atleta("33333333331", "Fernando Gomes", "15/03/1990", "Masculino"),
    Atleta("33333333332", "Thiago Nunes", "22/07/1985", "Masculino"),
    Atleta("33333333333", "Ricardo Lima", "10/12/1992", "Masculino"),
    Atleta("33333333334", "Paulo Costa", "05/05/1988", "Masculino"),
    Atleta("33333333335", "Roberto Silva", "18/09/1995", "Masculino"),
    Atleta("33333333336", "Marcelo Santos", "03/01/1987", "Masculino"),
    Atleta("33333333337", "Antonio Souza", "28/11/1993", "Masculino"),
    Atleta("33333333338", "José Pereira", "14/06/1989", "Masculino"),
    Atleta("33333333339", "Carlos Andrade", "07/04/1991", "Masculino"),
    Atleta("33333333340", "João Silva", "25/08/1986", "Masculino"),
    Atleta("33333333341", "Francisco Mendes", "12/02/1994", "Masculino"),
    Atleta("33333333342", "Manuel Dias", "19/10/1988", "Masculino"),
    Atleta("33333333343", "Sebastião Rocha", "31/12/1992", "Masculino"),
    Atleta("33333333344", "Raimundo Alves", "16/07/1987", "Masculino"),
    Atleta("33333333345", "Pedro Henrique", "08/03/1990", "Masculino"),
    
    # Adulto Feminino (15 atletas)
    Atleta("44444444441", "Ana Beatriz", "20/04/1990", "Feminino"),
    Atleta("44444444442", "Carla Dias", "13/08/1985", "Feminino"),
    Atleta("44444444443", "Mariana Silva", "27/11/1992", "Feminino"),
    Atleta("44444444444", "Patricia Costa", "09/06/1988", "Feminino"),
    Atleta("44444444445", "Juliana Santos", "15/01/1995", "Feminino"),
    Atleta("44444444446", "Fernanda Lima", "03/09/1987", "Feminino"),
    Atleta("44444444447", "Cristina Souza", "22/05/1993", "Feminino"),
    Atleta("44444444448", "Sandra Oliveira", "11/12/1989", "Feminino"),
    Atleta("44444444449", "Denise Alves", "28/07/1991", "Feminino"),
    Atleta("44444444450", "Monica Pereira", "06/03/1986", "Feminino"),
    Atleta("44444444451", "Adriana Rocha", "19/10/1994", "Feminino"),
    Atleta("44444444452", "Silvia Mendes", "14/08/1988", "Feminino"),
    Atleta("44444444453", "Regina Dias", "25/04/1992", "Feminino"),
    Atleta("44444444454", "Eliane Nunes", "17/11/1987", "Feminino"),
    Atleta("44444444455", "Rosana Gomes", "02/06/1990", "Feminino"),
    
    # Master Masculino (8 atletas)
    Atleta("55555555551", "Roberto Assis", "15/03/1970", "Masculino"),
    Atleta("55555555552", "Jose Carlos", "22/07/1965", "Masculino"),
    Atleta("55555555553", "Antonio Silva", "10/12/1972", "Masculino"),
    Atleta("55555555554", "Francisco Costa", "05/05/1968", "Masculino"),
    Atleta("55555555555", "Manuel Santos", "18/09/1975", "Masculino"),
    Atleta("55555555556", "Sebastião Lima", "03/01/1967", "Masculino"),
    Atleta("55555555557", "Raimundo Souza", "28/11/1973", "Masculino"),
    Atleta("55555555558", "Pedro Oliveira", "14/06/1969", "Masculino"),
    
    # Master Feminino (8 atletas)
    Atleta("66666666661", "Sônia Braga", "20/04/1970", "Feminino"),
    Atleta("66666666662", "Maria Silva", "13/08/1965", "Feminino"),
    Atleta("66666666663", "Ana Costa", "27/11/1972", "Feminino"),
    Atleta("66666666664", "Lucia Santos", "09/06/1968", "Feminino"),
    Atleta("66666666665", "Rosa Lima", "15/01/1975", "Feminino"),
    Atleta("66666666666", "Teresa Souza", "03/09/1967", "Feminino"),
    Atleta("66666666667", "Carmen Oliveira", "22/05/1973", "Feminino"),
    Atleta("66666666668", "Isabel Alves", "11/12/1969", "Feminino"),
    
    # PCD Masculino (2 atletas)
    Atleta("77777777771", "João Silva", "15/03/1985", "Masculino", pcd=True),
    Atleta("77777777772", "Pedro Santos", "22/07/1990", "Masculino", pcd=True),
    
    # PCD Feminino (2 atletas)
    Atleta("88888888881", "Maria Oliveira", "20/04/1988", "Feminino", pcd=True),
    Atleta("88888888882", "Ana Costa", "13/08/1992", "Feminino", pcd=True),
]


def obter_atleta_por_cpf(cpf: str) -> Optional[Atleta]:
    """
    Busca um atleta no mockdata pelo CPF.
    
    Args:
        cpf: CPF do atleta (apenas números)
        
    Returns:
        Objeto Atleta se encontrado, None caso contrário
    """
    # Limpar CPF (remover pontos, traços, espaços)
    cpf_limpo = ''.join(filter(str.isdigit, cpf))
    
    for atleta in ATLETAS_MOCK:
        if atleta.cpf == cpf_limpo:
            return atleta
    
    return None


def listar_atletas_por_categoria(categoria: str, genero: str = None) -> list:
    """
    Lista atletas de uma categoria específica.
    
    Args:
        categoria: Categoria ('Júnior', 'Adulto', 'Master', 'PCD')
        genero: Gênero opcional ('Masculino' ou 'Feminino')
        
    Returns:
        Lista de atletas da categoria
    """
    atletas_categoria = []
    
    for atleta in ATLETAS_MOCK:
        if atleta.pcd and categoria == 'PCD':
            if genero is None or atleta.genero == genero:
                atletas_categoria.append(atleta)
        elif not atleta.pcd:
            # Calcular categoria para evento de exemplo (2025)
            try:
                cat_atleta = atleta.calcular_categoria("01/01/2025")
                if cat_atleta == categoria:
                    if genero is None or atleta.genero == genero:
                        atletas_categoria.append(atleta)
            except ValueError:
                continue
    
    return atletas_categoria


def contar_atletas() -> dict:
    """
    Conta atletas por categoria e gênero.
    
    Returns:
        Dicionário com contadores
    """
    contadores = {
        'total': len(ATLETAS_MOCK),
        'masculino': 0,
        'feminino': 0,
        'pcd': 0,
        'junior': 0,
        'adulto': 0,
        'master': 0
    }
    
    for atleta in ATLETAS_MOCK:
        if atleta.genero == 'Masculino':
            contadores['masculino'] += 1
        else:
            contadores['feminino'] += 1
            
        if atleta.pcd:
            contadores['pcd'] += 1
        else:
            try:
                categoria = atleta.calcular_categoria("01/01/2025")
                contadores[categoria.lower()] += 1
            except ValueError:
                continue
    
    return contadores


if __name__ == "__main__":
    # Teste das funções
    print("=== Teste da Classe Atleta ===")
    
    # Teste de busca por CPF
    atleta = obter_atleta_por_cpf("11111111111")
    if atleta:
        print(f"Atleta encontrado: {atleta}")
        print(f"Categoria para evento 2025: {atleta.calcular_categoria('01/01/2025')}")
    
    # Teste de contagem
    contadores = contar_atletas()
    print(f"\nContadores: {contadores}")
    
    # Teste de listagem por categoria
    juniores = listar_atletas_por_categoria('Júnior', 'Masculino')
    print(f"\nJúniores Masculinos: {len(juniores)}")
    
    pcds = listar_atletas_por_categoria('PCD')
    print(f"PCDs: {len(pcds)}")
