# Projeto 3 de Teoria e Aplicação de Grafos - Escalação de Jogos para Campeonato de Futebol

## Introdução
Este projeto utiliza técnicas de coloração de grafos para resolver um problema de escalação de jogos em um campeonato de futebol. A ideia central é representar cada jogo entre dois times como um nó de um grafo, onde arestas conectam jogos que não podem ocorrer na mesma rodada – seja por compartilharem um time ou por restrições específicas (como regras de mandante e rodadas proibidas). Utilizando um algoritmo de backtracking, o programa atribui rodadas (representadas por cores) aos jogos de forma que todas as restrições sejam satisfeitas, permitindo a geração de um cronograma eficiente e a visualização do grafo com a distribuição dos jogos por rodada.

## Requisitos
Este projeto foi desenvolvido em Python 3.9.6 e utiliza as seguintes bibliotecas:
- `networkx`: para a construção e manipulação do grafo.
- `matplotlib`: para a visualização do grafo com cores que representam as rodadas.
- `itertools` e `collections`: para a criação de combinações de jogos e manipulação de contadores.
- `matplotlib.patches`: para a criação de legendas na visualização.

## Como Executar o Projeto

### 1. Abrir o Projeto
Abra o terminal e navegue até a pasta onde o projeto está localizado:

    ```
    cd /caminho/para/o/projeto
    ```

### 2. Configurar e **Ativar o Ambiente Virtual**

O projeto utiliza um ambiente virtual para garantir que as dependências e pacotes necessários estejam isolados e não interfiram em outros projetos.

### Criar o Ambiente Virtual:

- Para criar o ambiente virtual, execute o seguinte comando no terminal:
    
    ```
    python3 -m venv venv
    ```
    
Esse comando cria uma pasta chamada `venv` com todos os arquivos necessários para o ambiente virtual.
    

### No macOS ou Linux:

- Ative o ambiente virtual com o seguinte comando:
    
    ```
    source venv/bin/activate
    ```
    

### No Windows:

- Ative o ambiente virtual com o comando:
    
    ```
    venv\Scripts\activate
    ```
    

Após executar o comando de ativação, o nome do seu ambiente virtual (normalmente `venv`) aparecerá entre parênteses no terminal, indicando que o ambiente virtual está ativo.

### 3. **Instalar as Dependências**

Se você nunca instalou as dependências do projeto, ou se está começando a configurar o ambiente, basta rodar o seguinte comando:

    pip install -r requirements.txt
    
Isso irá instalar todas as bibliotecas e pacotes necessários para o projeto.

### 4. **Executar o Projeto**

Com o ambiente virtual ativado e as dependências instaladas, execute o seu código Python com:

    python projeto3.py

Isso irá rodar o programa conforme o que está no arquivo `projeto3.py` e criará uma visualização do grafo.

### 5. **Fechar o Ambiente Virtual**

Após terminar de trabalhar com o projeto, você pode desativar o ambiente virtual com o comando:

    deactivate

Isso irá sair do ambiente virtual e retornar ao terminal normal.

## Conclusão
Este projeto demonstra a aplicação prática de algoritmos de coloração de grafos para resolver problemas reais de escalonamento esportivo. Entre os principais resultados, destacam-se:
1. Construção do Grafo: Representação dos jogos e das restrições de forma estruturada.
2. Algoritmo de Backtracking: Atribuição de rodadas aos jogos respeitando as restrições, evitando que um time jogue mais de uma vez na mesma rodada.
3. Visualização: Exibição gráfica do grafo com nós renomeados no formato "Time1 X Time2" e cores que representam as rodadas, além de uma legenda detalhada.
4. Cronograma de Jogos: Impressão organizada do cronograma no terminal, facilitando a verificação e análise dos resultados.
Através deste projeto, é possível explorar técnicas avançadas de grafos e backtracking, aplicadas a problemas de otimização e escalonamento, oferecendo uma ferramenta útil para a gestão de campeonatos esportivos.