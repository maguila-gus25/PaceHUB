# PaceHub

> Um software sob encomenda para organizadores de eventos esportivos e clubes de corrida que precisam de uma plataforma eficiente para gerenciar todas as etapas de uma corrida, desde a divulgação até a publicação dos resultados.

O PaceHub se diferencia por oferecer uma solução unificada e robusta para a gestão integral do evento, em contraste com alternativas que exigem o uso de múltiplas planilhas e plataformas descentralizadas.

## 📋 Tabela de Conteúdos

1. [Visão Geral](#-visão-geral)
2. [Público-Alvo](#-público-alvo)
3. [Funcionalidades Principais](#-funcionalidades-principais)
4. [Regras de Negócio](#-regras-de-negócio)
5. [Arquitetura do Sistema](#-arquitetura-do-sistema)
6. [Banco de Dados](#-banco-de-dados)
7. [Tecnologias Utilizadas](#-tecnologias-utilizadas)
8. [Como Executar o Projeto](#-como-executar-o-projeto)
9. [Testes](#-testes)

## 🎯 Visão Geral

O projeto ataca o problema da gestão manual de corridas de rua, que resulta na ausência de informações precisas, falta de controle automatizado de inscrições e dificuldade na comunicação com os atletas. A solução automatiza o processo de inscrição, o controle de percursos e a disponibilização de resultados em tempo real.

**Benefícios:**

* Redução do tempo gasto em tarefas administrativas manuais.
* Diminuição de custos operacionais com a automação de processos.
* Melhoria na comunicação e transparência entre organizadores e atletas.
* Fornecimento de dados e análises precisas para apoiar a tomada de decisões.

## 👥 Público-Alvo

O sistema é projetado para dois tipos principais de usuários:

* **Organizadores de Eventos:** Responsáveis por gerenciar o ciclo de vida completo da corrida, desde o planejamento até a análise pós-evento. O conhecimento em informática pode variar de básico a avançado.

* **Atletas:** Usuários com interesse principal no acompanhamento da corrida, inscrição e consulta de resultados. Geralmente possuem conhecimento básico em informática.

## ✨ Funcionalidades Principais

As funcionalidades do sistema são divididas em quatro áreas principais, cobrindo toda a jornada de gestão de um evento de corrida.

### Gestão de Contas e Perfis (PCT01)

* **RF01:** Permite que um novo usuário se cadastre na plataforma com o perfil "Atleta".
  - Validação de CPF (formato e dígitos verificadores)
  - Validação de email
  - Criptografia de senha usando bcrypt
  - Campos obrigatórios: Nome, CPF, Email, Data de Nascimento, Gênero, Senha
  - Suporte para atletas PCD (Pessoa com Deficiência)

* **RF02:** Permite que um novo usuário se cadastre na plataforma com o perfil "Organizador".
  - Validação de CPF e email
  - Criptografia de senha

* **UC01.03:** Autenticação de usuários para acesso ao sistema.
  - Autenticação por CPF e senha
  - Redirecionamento para painel específico (Atleta ou Organizador)
  - Validação de credenciais

* **UC01.04:** Gerenciamento do próprio perfil após o cadastro.

### Gerenciamento de Eventos (Visão do Organizador - PCT02)

* **RF03:** Permite ao organizador criar um novo evento de corrida.
  - Campos: Nome, Data, Distância, Local de Largada, Tempo de Corte, Data Limite para Crédito
  - Associação automática ao organizador logado
  - Validação de datas

* **RF04:** Permite ao organizador visualizar uma lista de todos os atletas inscritos no seu evento.
  - Listagem de eventos do organizador
  - Exibição de informações: Nome, Data, Número de Inscritos, Status
  - Status automático baseado na data do evento (Concluído/Futuro)

* **RF05:** Permite ao organizador gerenciar a entrega de kits de corrida aos atletas.
  - Criação de kits de corrida para eventos (Nome, Descrição, Valor)
  - Busca de inscrições por CPF ou nome do atleta
  - Atualização do status de entrega do kit (Entregue/Não Entregue)
  - Visualização de informações da inscrição

* **RF09:** Permite aos organizadores importar uma lista de participantes e seus tempos de corrida.
  - Importação em lote de resultados de atletas via CSV
  - Formato CSV: `CPF,Tempo` (sem cabeçalho)
  - Validações implementadas:
    - **CPF inválido**: Validação de formato e dígitos verificadores
    - **Atleta não cadastrado**: Verificação de existência no banco
    - **Atleta não inscrito**: Validação de inscrição no evento
    - **Tempo inválido**: Validação de formato HH:MM:SS
    - **Formato de arquivo**: Validação de estrutura do CSV
  - Relatório detalhado de erros linha por linha
  - Substituição automática de resultados anteriores
  - Importação permitida apenas para eventos com data no passado

* **RF12:** Exibe para o organizador um painel com estatísticas do evento, como total de inscritos e distribuição por gênero e faixa etária.

### Jornada do Atleta (PCT03)

* **RF06:** Exibe aos usuários uma lista com os eventos de corrida disponíveis para inscrição.

* **RF07:** Permite aos atletas se inscreverem em um evento disponível.
  - Seleção de kit de corrida
  - Validação de atleta existente
  - Status de inscrição (Pendente/Paga)

* **RF11:** Permite que os atletas cancelem sua própria inscrição em uma corrida, respeitando o prazo.

* **UC03.04 & UC03.05:** Exige o preenchimento da Ficha Médica e o aceite do Termo de Responsabilidade como parte obrigatória da inscrição.

### Resultados e Rankings (PCT04)

* **RF09:** Publica em uma página do evento os rankings de classificação geral e por categoria.
  - **Classificação Geral (RN06)**: Top 5 de cada gênero (Masculino/Feminino)
  - **Classificação por Categoria (RN07)**: 
    - Júnior (até 17 anos)
    - Adulto (18-49 anos)
    - Master (50+ anos)
    - PCD (competem separadamente)
  - Cálculo baseado na idade do atleta em 31/12 do ano do evento
  - Ordenação automática por tempo

* **RF10:** Permite que os atletas pesquisem e visualizem seus próprios resultados e históricos de desempenho.
  - Busca de inscrições por atleta
  - Visualização de detalhes da inscrição
  - Informações do evento e kit selecionado

## 📜 Regras de Negócio

O sistema opera sob um conjunto de regras de domínio específicas para o universo das corridas de rua:

* **RN01:** A inscrição é permitida apenas para atletas que atendam à idade mínima para cada distância (5km: 14 anos, 10km: 16 anos, 21km: 18 anos, 42km: 20 anos).

* **RN04:** A categoria do atleta é definida pela idade que ele terá em 31 de dezembro do ano do evento.
  - **Júnior**: ≤ 17 anos
  - **Adulto**: 18-49 anos
  - **Master**: ≥ 50 anos
  - **PCD**: Sempre categoria PCD, independente da idade

* **RN05:** Para efetivar a inscrição, é obrigatório o preenchimento da ficha médica e o aceite do termo de responsabilidade.

* **RN06:** A "Classificação Geral" é composta pelos 5 primeiros colocados de cada gênero.

* **RN07:** Atletas não classificados no top 5 geral são classificados por faixas etárias: Júnior (até 17 anos), Adulto (18-49 anos) e Master (50+ anos).

* **RN08/RN10:** O cancelamento da inscrição só é permitido até a data limite definida pelo organizador.

* **RN11/RN12:** Não é permitido o cadastro de atletas ou organizadores com CPFs duplicados.

* **RNF05:** Todas as senhas de usuários devem ser armazenadas de forma segura, utilizando um algoritmo de hashing com salt (bcrypt).

* **Validação de CPF**: Formato e dígitos verificadores

* **Validação de Evento**: Importação apenas para eventos concluídos

* **Validação de Inscrição**: Atleta deve estar inscrito para ter resultado importado

## 🏗️ Arquitetura do Sistema

O projeto é estruturado seguindo o padrão arquitetural **Model-View-Controller (MVC)**, que promove a separação de responsabilidades e facilita a manutenção do código.

* **Entidade (`entidade/`):** Representa a camada de dados e lógica de negócio. Contém as classes de domínio (`Usuario`, `Atleta`, `Organizador`, `Evento`, `Inscricao`, `Resultado`, `KitDeCorrida`), as funções de validação e as regras de negócio. É totalmente independente da interface.

* **Persistência (`persistencia/`):** Data Access Objects (DAOs) responsáveis pelas operações de banco de dados, abstraindo o acesso aos dados.

* **Limite (`limite/`):** É a camada de apresentação. Responsável por construir as janelas e elementos da interface gráfica com `FreeSimpleGUI`. Não contém nenhuma lógica de negócio.

* **Controle (`controle/`):** Atua como o intermediário que conecta a Entidade/Persistência e a Limite. Ele recebe as ações do usuário da Limite, utiliza a Entidade e Persistência para processar a lógica e as regras de negócio, e por fim, atualiza a Limite com os resultados.

### Modelo de Domínio

O sistema é modelado através de um conjunto de classes inter-relacionadas:

* **Usuario:** Classe abstrata com os atributos comuns a todos os usuários, como `cpf`, `nome` e `email`.

* **Atleta e Organizador:** Classes que herdam de `Usuario` e representam os papéis específicos no sistema.

* **Evento:** Centraliza todas as informações de uma corrida, como `distancia`, `data` e `tempoCorte`. Um organizador pode gerenciar múltiplos eventos (1:N).

* **Inscricao:** Modela o processo de inscrição, ligando um `Atleta` a um `Evento` e controlando o status da ficha médica e do termo de responsabilidade.

* **Resultado:** Armazena os tempos e classificações dos atletas nos eventos.

* **KitDeCorrida:** Representa os kits disponíveis para cada evento.

## 🗄️ Banco de Dados

O sistema utiliza SQLite como banco de dados relacional, com as seguintes tabelas principais:

* `usuarios`: Armazena atletas e organizadores
* `Eventos`: Informações dos eventos de corrida
* `inscricoes`: Relacionamento entre atletas e eventos
* `KitsDeCorrida`: Kits disponíveis para cada evento
* `Resultados`: Resultados dos atletas nos eventos
* `FichasMedicas`: Informações médicas dos atletas

## 💻 Tecnologias Utilizadas

* **Linguagem:** Python 3.13
* **Interface Gráfica:** FreeSimpleGUI 5.2.0
* **Banco de Dados:** SQLite
* **Criptografia:** bcrypt 5.0.0
* **Processamento de Dados:** csv (biblioteca padrão)

## 🚀 Como Executar o Projeto

### Pré-requisitos

* Python 3.13 ou superior

### Instalação

1. **Clone o repositório:**

```bash
git clone https://github.com/maguila-gus25/PaceHUB
cd PaceHUB
```

2. **Instale as dependências:**

Certifique-se de que você tem o arquivo `requirements.txt` com as dependências necessárias:

```
freesimplegui==5.2.0.post1
bcrypt==5.0.0
```

Execute o comando de instalação:

```bash
pip install -r requirements.txt
```

3. **Crie o banco de dados:**

```bash
python cria_banco.py
```

4. **Popule o banco com dados iniciais (opcional):**

```bash
python popula_banco.py
```

5. **Execute a aplicação:**

O ponto de entrada do sistema é o arquivo `main.py`.

```bash
python main.py
```

### Uso

* Na tela inicial, você pode fazer o login ou se cadastrar.
* Escolha entre "Cadastrar como Atleta" ou "Cadastrar como Organizador".
* Preencha o formulário e utilize as funcionalidades disponíveis para o seu perfil.

## 🧪 Testes

O projeto inclui scripts para geração de dados de teste:

* `gerar_evento_teste.py`: Gera evento, inscrições e arquivos CSV de teste
* Arquivos CSV de teste com diferentes tipos de erros para validação:
  * `resultados_teste.csv`: CSV válido
  * `resultados_erro_cpf_invalido.csv`: CPFs inválidos
  * `resultados_erro_atleta_nao_cadastrado.csv`: Atletas não cadastrados
  * `resultados_erro_tempo_nao_informado.csv`: Tempos vazios
  * `resultados_erro_tempo_invalido.csv`: Tempos em formato inválido
  * `resultados_erro_formato_invalido.csv`: Formato de arquivo incorreto
  * `resultados_erro_atleta_nao_inscrito.csv`: Atletas não inscritos
  * `resultados_erro_multiplos_erros.csv`: Múltiplos erros misturados

## 📦 Estrutura de Arquivos

```
PaceHub/
├── controle/              # Controladores (lógica de negócio)
│   ├── controlador_atleta.py
│   ├── controlador_evento.py
│   ├── controlador_importacao.py
│   ├── controlador_inscricao.py
│   ├── controlador_organizador.py
│   └── controlador_sistema.py
├── entidade/              # Entidades do domínio
│   ├── atleta.py
│   ├── evento.py
│   ├── ficha_medica.py
│   ├── inscricao.py
│   ├── kit_de_corrida.py
│   ├── organizador.py
│   ├── resultado.py
│   └── usuario.py
├── limite/                # Interfaces gráficas
│   ├── tela_atleta.py
│   ├── tela_cadastro.py
│   ├── tela_evento.py
│   ├── tela_ficha_medica.py
│   ├── tela_importar_resultados.py
│   ├── tela_inscricao.py
│   ├── tela_organizador.py
│   ├── tela_principal.py
│   └── tela_resultados.py
├── persistencia/          # Data Access Objects
│   ├── evento_dao.py
│   ├── ficha_medica_dao.py
│   ├── inscricao_dao.py
│   ├── resultado_dao.py
│   └── usuario_dao.py
├── csv/                   # Arquivos CSV de teste
├── cria_banco.py          # Script de criação do banco
├── popula_banco.py        # Script de população inicial
├── gerar_evento_teste.py  # Script para gerar dados de teste
├── main.py                # Ponto de entrada da aplicação
└── requirements.txt       # Dependências do projeto
```

## 👥 Autores

* Lucas Dutra de Ávila
* Gustavo Henrique Costa Ramos
* Pedro Heuser
* Ruan Lucas 

## 📄 Licença

Este projeto está sob licença MIT.

## 🔗 Repositório

[GitHub - PaceHub](https://github.com/maguila-gus25/PaceHUB)
