# PROCESSOS_README.md - Documentação para Diagramas UML

## Visão Geral do Sistema

O sistema de **Importação de Tempos de Participantes** do PaceHub implementa o caso de uso completo para importação de resultados de corrida via arquivo CSV e visualização de rankings por categoria. O sistema segue arquitetura UML com 4 camadas: Entidade, Limite, Controlador e Persistência.

## Arquitetura do Sistema

### Camadas UML Implementadas

1. **Entidade**: Classes de domínio (`Atleta`, `Resultado`, `Evento`)
2. **Limite**: Interfaces gráficas (`tela_importar_resultados.py`, `tela_visualizar_ranking.py`)
3. **Controlador**: Lógica de negócio (`controlador_importacao.py`, `controlador_ranking.py`)
4. **Persistência**: Acesso ao banco (`resultado_dao.py`)

### Regras de Negócio Implementadas

- **RN04**: Categoria do atleta é definida pela idade em 31/12 do ano do evento
- **RN06**: Classificação Geral = Top 5 de cada gênero
- **RN07**: Demais atletas classificados por faixa etária (Júnior ≤17, Adulto 18-49, Master ≥50)
- **PCD**: Atletas com deficiência competem em categoria separada

## Processos do Sistema

### 1. Processo: Importar Resultados

**Objetivo**: Importar tempos de atletas de um arquivo CSV e calcular rankings

**Atores Principais**:
- Organizador (usuário do sistema)
- Sistema (interfaces e controladores)
- Banco de Dados (SQLite)

**Fluxo Principal**:

1. **Organizador** acessa o painel do organizador
2. **Organizador** clica no botão "Imp. Tempos" de um evento concluído
3. **Sistema** abre a tela de importação com lista de eventos disponíveis
4. **Organizador** seleciona o evento desejado
5. **Organizador** clica em "Selecionar Arquivo" e escolhe arquivo CSV
6. **Organizador** clica em "Importar"
7. **Sistema** valida se o arquivo existe e tem formato correto
8. **ControladorImportacao** processa o arquivo CSV:
   - Lê linha por linha
   - Valida formato (CPF, Tempo)
   - Busca atleta no mockdata
   - Cria objetos Resultado
   - Calcula categoria baseada na RN04
9. **ControladorImportacao** calcula rankings:
   - Ordena resultados por tempo
   - Aplica RN06 (Top 5 geral por gênero)
   - Aplica RN07 (classificação por categoria)
10. **ResultadoDAO** salva resultados em lote no banco
11. **Sistema** exibe resumo da importação
12. **Sistema** fecha a tela de importação

**Fluxos de Exceção**:

- **Arquivo não encontrado**: Sistema exibe erro e solicita novo arquivo
- **CPF inválido**: Linha é ignorada, erro é registrado
- **Atleta não encontrado**: Linha é ignorada, erro é registrado
- **Tempo inválido**: Linha é ignorada, erro é registrado
- **Evento não permite importação**: Sistema exibe erro

**Pré-condições**:
- Evento deve estar com status "Concluído"
- Arquivo CSV deve existir e ser acessível
- Sistema deve ter mockdata de atletas carregado

**Pós-condições**:
- Resultados salvos no banco de dados
- Rankings calculados e classificações definidas
- Evento habilitado para visualização de resultados

### 2. Processo: Visualizar Rankings

**Objetivo**: Exibir rankings de um evento organizados por categoria

**Atores Principais**:
- Organizador
- Sistema
- Banco de Dados

**Fluxo Principal**:

1. **Organizador** clica no botão "Ver Resultados" de um evento
2. **Sistema** verifica se o evento possui resultados no banco
3. **ControladorRanking** busca todos os resultados do evento
4. **ControladorRanking** organiza resultados por categoria e gênero
5. **Sistema** cria janela com abas dinâmicas:
   - Aba Geral (sempre presente)
   - Abas por categoria (Júnior, Adulto, Master)
   - Aba PCD (só se houver atletas PCD)
6. **Sistema** popula tabelas com dados formatados
7. **Organizador** navega entre as abas
8. **Organizador** clica em "Voltar"
9. **Sistema** fecha a janela de rankings

**Fluxos de Exceção**:

- **Evento sem resultados**: Sistema exibe popup informativo
- **Erro ao buscar dados**: Sistema exibe erro e fecha janela

**Pré-condições**:
- Evento deve ter resultados importados
- Banco de dados deve estar acessível

**Pós-condições**:
- Rankings exibidos corretamente
- Organizador pode visualizar classificações

### 3. Processo: Buscar Atleta

**Objetivo**: Encontrar resultado específico de um atleta

**Fluxo Principal**:

1. **Organizador** clica em "Buscar Atleta"
2. **Sistema** lista eventos com resultados disponíveis
3. **Organizador** seleciona o evento
4. **Sistema** abre janela de busca
5. **Organizador** digita CPF do atleta
6. **Organizador** clica em "Buscar"
7. **ControladorRanking** busca resultado no banco
8. **Sistema** exibe informações do atleta:
   - Nome, tempo, categoria
   - Classificação geral (se top 5)
   - Classificação na categoria

## Diagrama de Atividades - Importar Resultados

### Atividades Principais:

1. **Iniciar Importação**
   - [Organizador] Acessa painel
   - [Organizador] Clica "Imp. Tempos"
   - [Sistema] Abre tela importação

2. **Selecionar Arquivo**
   - [Organizador] Seleciona evento
   - [Organizador] Escolhe arquivo CSV
   - [Sistema] Valida arquivo

3. **Processar CSV**
   - [ControladorImportacao] Lê arquivo
   - [Loop] Para cada linha:
     - [ControladorImportacao] Valida linha
     - [ControladorImportacao] Busca atleta
     - [Decisão] Atleta encontrado?
       - [Sim] Cria resultado
       - [Não] Registra erro
   - [ControladorImportacao] Calcula rankings

4. **Salvar Resultados**
   - [ResultadoDAO] Limpa resultados anteriores
   - [ResultadoDAO] Salva novos resultados
   - [Sistema] Exibe resumo

### Decisões e Loops:

- **Loop**: Processamento de cada linha do CSV
- **Decisão**: Atleta encontrado no mockdata?
- **Decisão**: Arquivo válido?
- **Decisão**: Evento permite importação?

### Pontos de Sincronização:

- Aguardar seleção de arquivo pelo usuário
- Aguardar confirmação de importação
- Sincronização com banco de dados

## Diagrama de Sequência - Importar Resultados

### Atores:
- Organizador
- TelaImportacao
- ControladorImportacao
- Atleta (mockdata)
- ResultadoDAO
- BancoDados

### Sequência de Mensagens:

1. Organizador → TelaImportacao: `clica_importar()`
2. TelaImportacao → ControladorImportacao: `processar_csv(arquivo, evento_id)`
3. ControladorImportacao → ControladorImportacao: `validar_arquivo_csv()`
4. ControladorImportacao → ControladorImportacao: `ler_csv()`
5. **[Loop para cada linha]**
   - ControladorImportacao → ControladorImportacao: `_processar_linha()`
   - ControladorImportacao → ControladorImportacao: `_validar_cpf()`
   - ControladorImportacao → ControladorImportacao: `_validar_formato_tempo()`
   - ControladorImportacao → Atleta: `obter_atleta_por_cpf(cpf)`
   - Atleta → ControladorImportacao: `retorna atleta`
   - ControladorImportacao → Atleta: `calcular_categoria(data_evento)`
   - Atleta → ControladorImportacao: `retorna categoria`
   - ControladorImportacao → ControladorImportacao: `criar_resultado_para_atleta()`
6. ControladorImportacao → ControladorImportacao: `calcular_rankings()`
7. ControladorImportacao → ResultadoDAO: `limpar_resultados_evento()`
8. ResultadoDAO → BancoDados: `DELETE FROM resultados WHERE evento_id = ?`
9. BancoDados → ResultadoDAO: `commit successful`
10. ControladorImportacao → ResultadoDAO: `salvar_lote_resultados()`
11. ResultadoDAO → BancoDados: `INSERT INTO resultados ...`
12. BancoDados → ResultadoDAO: `commit successful`
13. ResultadoDAO → ControladorImportacao: `retorna total_salvos`
14. ControladorImportacao → TelaImportacao: `retorna (total, erros)`
15. TelaImportacao → Organizador: `exibe_popup_resumo()`

### Cenários de Exceção:

**Cenário 1: CPF não encontrado**
- ControladorImportacao → Atleta: `obter_atleta_por_cpf(cpf)`
- Atleta → ControladorImportacao: `retorna None`
- ControladorImportacao → ControladorImportacao: `adiciona_erro()`

**Cenário 2: Arquivo inválido**
- ControladorImportacao → ControladorImportacao: `validar_arquivo_csv()`
- ControladorImportacao → TelaImportacao: `retorna False, mensagem_erro`
- TelaImportacao → Organizador: `exibe_popup_erro()`

## Estados dos Objetos

### Estado do Resultado:

1. **Criado**: Objeto criado sem classificações
2. **Com Categoria**: Categoria calculada baseada na RN04
3. **Com Rankings**: Classificações geral e por categoria definidas
4. **Salvo**: Persistido no banco de dados

### Estado do Evento:

1. **Planejado**: Evento criado, não permite importação
2. **Inscrições Abertas**: Permite visualização, não importação
3. **Concluído**: Permite importação e visualização

### Estado da Importação:

1. **Iniciada**: Arquivo selecionado
2. **Processando**: CSV sendo lido e validado
3. **Calculando**: Rankings sendo calculados
4. **Salvando**: Dados sendo persistidos
5. **Concluída**: Importação finalizada

## Dados de Entrada e Saída

### Entrada:
- **Arquivo CSV**: Formato `CPF,Tempo` (ex: `12345678901,01:30:45`)
- **ID do Evento**: Identificador do evento para importação

### Saída:
- **Resultados Importados**: Número de linhas processadas com sucesso
- **Lista de Erros**: Detalhes dos problemas encontrados
- **Rankings Calculados**: Classificações por categoria e geral

### Validações:
- **CPF**: Deve ter 11 dígitos numéricos
- **Tempo**: Formato HH:MM:SS válido
- **Atleta**: Deve existir no mockdata
- **Evento**: Deve permitir importação

## Considerações para Diagramas UML

### Para Diagrama de Atividades:
- Use símbolos de decisão (losango) para validações
- Use símbolos de loop para processamento de linhas
- Indique pontos de sincronização com usuário
- Mostre fluxos paralelos quando possível

### Para Diagrama de Sequência:
- Agrupe mensagens relacionadas em blocos
- Use notas para explicar regras de negócio
- Indique loops com frames de repetição
- Mostre cenários de exceção separadamente

### Elementos Visuais Recomendados:
- **Atividades**: Retângulos com cantos arredondados
- **Decisões**: Losangos
- **Início/Fim**: Círculos
- **Sincronização**: Barras grossas
- **Swimlanes**: Separação por ator/camada

Este documento fornece todas as informações necessárias para criar diagramas UML precisos e completos do sistema de importação de resultados do PaceHub.
