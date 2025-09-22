# PaceHub

> Um software sob encomenda para organizadores de eventos esportivos e clubes de corrida que precisam de uma plataforma eficiente para gerenciar todas as etapas de uma corrida, desde a divulgação até a publicação dos resultados.

O PaceHub se diferencia por oferecer uma solução unificada e robusta para a gestão integral do evento, em contraste com alternativas que exigem o uso de múltiplas planilhas e plataformas descentralizadas.

## 📋 Tabela de Conteúdos
1. [Visão Geral](#-visão-geral)
2. [Público-Alvo](#-público-alvo)
3. [Funcionalidades Principais](#-funcionalidades-principais)
4. [Regras de Negócio](#-regras-de-negócio)
5. [Arquitetura do Sistema](#-arquitetura-do-sistema)
6. [Tecnologias Utilizadas](#-tecnologias-utilizadas)
7. [Como Executar o Projeto](#-como-executar-o-projeto)

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
* **RF02:** Permite que um novo usuário se cadastre na plataforma com o perfil "Organizador".
* **UC01.03:** Autenticação de usuários para acesso ao sistema.
* **UC01.04:** Gerenciamento do próprio perfil após o cadastro.

### Gerenciamento de Eventos (Visão do Organizador - PCT02)
* **RF03:** Permite ao organizador criar um novo evento de corrida.
* **RF04:** Permite ao organizador visualizar uma lista de todos os atletas inscritos no seu evento.
* **RF05:** Permite ao organizador gerenciar a entrega de kits de corrida aos atletas.
* **RF09:** Permite aos organizadores importar uma lista de participantes e seus tempos de corrida.
* **RF12:** Exibe para o organizador um painel com estatísticas do evento, como total de inscritos e distribuição por gênero e faixa etária.

### Jornada do Atleta (PCT03)
* **RF06:** Exibe aos usuários uma lista com os eventos de corrida disponíveis para inscrição.
* **RF07:** Permite aos atletas se inscreverem em um evento disponível.
* **RF11:** Permite que os atletas cancelem sua própria inscrição em uma corrida, respeitando o prazo.
* **UC03.04 & UC03.05:** Exige o preenchimento da Ficha Médica e o aceite do Termo de Responsabilidade como parte obrigatória da inscrição.

### Resultados e Rankings (PCT04)
* **RF09:** Publica em uma página do evento os rankings de classificação geral e por categoria.
* **RF10:** Permite que os atletas pesquisem e visualizem seus próprios resultados e históricos de desempenho.

## 📜 Regras de Negócio

O sistema opera sob um conjunto de regras de domínio específicas para o universo das corridas de rua:

* **RN01:** A inscrição é permitida apenas para atletas que atendam à idade mínima para cada distância (5km: 14 anos, 10km: 16 anos, 21km: 18 anos, 42km: 20 anos).
* **RN04:** A categoria do atleta é definida pela idade que ele terá em 31 de dezembro do ano do evento.
* **RN05:** Para efetivar a inscrição, é obrigatório o preenchimento da ficha médica e o aceite do termo de responsabilidade.
* **RN06:** A "Classificação Geral" é composta pelos 5 primeiros colocados de cada gênero.
* **RN07:** Atletas não classificados no top 5 geral são classificados por faixas etárias: Júnior (até 17 anos), Adulto (18-49 anos) e Master (50+ anos).
* **RN08/RN10:** O cancelamento da inscrição só é permitido até a data limite definida pelo organizador.
* **RN11/RN12:** Não é permitido o cadastro de atletas ou organizadores com CPFs duplicados.
* **RNF05:** Todas as senhas de usuários devem ser armazenadas de forma segura, utilizando um algoritmo de hashing com salt.

## 🏗️ Arquitetura do Sistema

O projeto é estruturado seguindo o padrão arquitetural **Model-View-Controller (MVC)**, que promove a separação de responsabilidades e facilita a manutenção do código.

* **Model (`modelo.py`):** Representa a camada de dados e lógica de negócio. Contém as classes de domínio (`Usuario`, `Organizador`, `Evento`), as funções de validação (ex: `validar_cpf`) e o gerenciador de dados (`OrganizadorModel`). É totalmente independente da interface.
* **View (`visao.py`):** É a camada de apresentação. Responsável por construir as janelas e elementos da interface gráfica com `PySimpleGUI`. Não contém nenhuma lógica de negócio.
* **Controller (`controlador.py`):** Atua como o intermediário que conecta o Model e a View. Ele recebe as ações do usuário da View, utiliza o Model para processar a lógica e as regras de negócio, e por fim, atualiza a View com os resultados.

### Modelo de Domínio
O sistema é modelado através de um conjunto de classes inter-relacionadas:
* **Usuario:** Classe abstrata com os atributos comuns a todos os usuários, como `cpf`, `nome` e `email`.
* **Atleta e Organizador:** Classes que herdam de `Usuario` e representam os papéis específicos no sistema.
* **Evento:** Centraliza todas as informações de uma corrida, como `distancia`, `data` e `tempoCorte`. Um organizador pode gerenciar múltiplos eventos (1:N).
* **Inscricao:** Modela o processo de inscrição, ligando um `Atleta` a um `Evento` e controlando o status da ficha médica e do termo de responsabilidade.

## 💻 Tecnologias Utilizadas

* **Linguagem:** Python
* **Interface Gráfica:** PySimpleGUI==4.60.5

## 🚀 Como Executar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-seu-repositorio>
    cd <diretorio-do-projeto>
    ```

2.  **Instale as dependências:**
    Certifique-se de que você tem o arquivo `requirements.txt` com o conteúdo abaixo.
    ```
    PySimpleGUI==5.0.10
    ```
    Execute o comando de instalação:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute a aplicação:**
    O ponto de entrada do sistema é o arquivo `controlador.py`.
    ```bash
    python controlador.py
    ```

4.  **Uso:**
    * Na tela inicial, você pode fazer o login ou se cadastrar.
    * Escolha entre "Cadastrar como Atleta" ou "Cadastrar como Organizador".
    * Preencha o formulário e utilize as funcionalidades disponíveis para o seu perfil.

