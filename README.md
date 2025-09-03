# Monitoramento de CPU: Dashboard Interativo com Streamlit

## Visão Geral do Projeto

Este projeto implementa um pipeline **ETL (Extract, Transform, Load)** completo para monitorar dados de telemetria da CPU (dados extraídos via log do [Coretemp](https://www.alcpu.com/CoreTemp/)), incluindo **temperatura dos núcleos**, **velocidade de clock** e **consumo de energia**. Os dados são coletados, limpos, transformados, e carregados em um banco de dados **PostgreSQL**. Posteriormente, um dashboard interativo é desenvolvido utilizando **Streamlit** para visualizar e analisar essas métricas importantes da CPU. O objetivo é fornecer uma ferramenta para acompanhar o desempenho e o comportamento térmico e energético do processador.

## Funcionalidades Principais

*   **Processamento de Dados Automatizado**: Um script Python (`pipeline.py`) para automatizar a limpeza e organização de arquivos CSV brutos.
*   **Armazenamento de Dados Robustos**: Carregamento seguro dos dados processados em um banco de dados **PostgreSQL**, com tratamento de transações para garantir a integridade dos dados. (Como a pipeline produz arquivos csv, os arquivos csv podem ser diretamente conectados ao dashboard, evitando o uso de banco de dados)
*   **Dashboard Interativo com Streamlit**: Uma aplicação web (`app.py`) que oferece as seguintes visualizações dinâmicas:
    *   **Temperatura do Núcleo vs. Velocidade do Núcleo**
    *   **Temperatura do Núcleo ao Longo do Dia**
    *   **Consumo de Energia da CPU ao Longo do Dia**
    *   **Consumo de Energia da CPU vs. Temperatura do Núcleo**

## Estrutura do Projeto

A organização do projeto segue a seguinte estrutura de arquivos:
```
Registros CPU
├── .venv/
├── dashboard/
│   ├── src/
│   │   ├── charts/
│   │   │   └── line_charts.py
│   │   └── queries/
│   │       └── queries.py 
│   └── app.py
├── data_loaded_processed/
├── data_loaded_raw/
├── data_processed/
├── data_raw/
├── notebooks/
│   └── exploracao.ipynb
├── scripts/
│   ├── load.py
│   └── pipeline.py
├── main.py
├── README.md
├── run_dashboard.bat
└── run_pipeline.bat
```
## Tecnologias Utilizadas

O projeto faz uso das seguintes tecnologias e bibliotecas:

*   **Python**: A linguagem de programação central para todas as etapas do projeto.
*   **Pandas**: Utilizada para manipulação e análise eficiente de DataFrames durante o processamento e leitura de dados.
*   **Streamlit**: Framework para a construção rápida de aplicações web interativas e o dashboard.
*   **Altair**: Biblioteca de visualização usada para criar os gráficos interativos no dashboard.
*   **SQLAlchemy**: Toolkit Python SQL para interação com o banco de dados PostgreSQL.
*   **Psycopg2**: Adaptador PostgreSQL para Python, utilizado pela SQLAlchemy para conexão com o banco de dados.
*   **PostgreSQL**: Sistema de gerenciamento de banco de dados relacional utilizado para armazenar os dados de telemetria da CPU.

## Dados

Os dados de entrada são arquivos CSV contendo telemetria da CPU. As colunas principais incluem:

*   `time`: Data/hora da coleta.
*   `core_temp_X`: Temperatura atual de cada núcleo (0 a 5) em graus Celsius (°C).
*   `low_temp_X` / `high_temp_X`: Temperaturas mínimas e máximas registradas para cada núcleo.
*   `core_load_X`: Carga de trabalho de cada núcleo (em %).
*   `core_speed_X`: Velocidade de clock de cada núcleo (em MHz).
*   `cpu_power`: Consumo total de energia da CPU.

## Processo ETL Detalhado

O processo ETL é dividido em duas etapas principais, executadas pelos scripts `pipeline.py` (Transformação) e `load.py` (Carregamento).

### Transformação (`pipeline.py`)

O script `pipeline.py` é responsável por preparar os dados brutos para o armazenamento e análise.

1.  **Leitura de Arquivos**: Lê arquivos CSV da pasta `data_raw`, ignorando as 7 primeiras linhas e utilizando a codificação `latin1` para garantir a compatibilidade.
2.  **Limpeza de Colunas**:
    *   Remove colunas que começam com o prefixo "Unnamed".
    *   Descarta colunas de resumo genéricas como "Core 0", "Core 1", etc.
    *   Elimina quaisquer colunas que estejam completamente vazias.
3.  **Normalização de Tempo**: A coluna `Time` é convertida para o formato `datetime` (`"%H:%M:%S %m/%d/%y"`), corrigindo possíveis erros.
4.  **Remoção de Valores Nulos**: Linhas com valores completamente vazios ou com qualquer valor nulo são removidas para garantir a qualidade dos dados.
5.  **Reordenação e Renomeação**: As colunas são selecionadas, reordenadas e renomeadas para um padrão `snake_case` para padronização e facilidade de consulta no banco de dados.
6.  **Salvamento e Movimentação**: O DataFrame processado é salvo como um novo arquivo CSV na pasta `data_processed`. O arquivo original de `data_raw` é então movido para `data_loaded_raw`, indicando que foi processado com sucesso.

### Carregamento (`load.py`)

O script `load.py` é responsável por carregar os dados transformados no banco de dados PostgreSQL.

1.  **Configuração de Conexão**: Conecta-se a um banco de dados PostgreSQL no meu caso: esquema `coretemp` e na tabela `raw_data`.
2.  **Processamento por Arquivo**: Itera sobre os arquivos CSV localizados na pasta `data_processed`.
3.  **Carregamento Transacional**: Cada arquivo é lido para um DataFrame Pandas e seus dados são adicionados à tabela `coretemp.raw_data` usando `append`. O carregamento é feito dentro de uma transação, o que significa que se um erro ocorrer durante o processamento de *qualquer* arquivo, toda a transação é revertida (`rollback`), garantindo que nenhum dado parcial seja gravado.
4.  **Movimentação Condicional**: Apenas se o carregamento do arquivo for bem-sucedido e a transação for confirmada (`commit`), o arquivo é movido da pasta `data_processed` para `data_loaded_processed`.

## Dashboard Interativo (`app.py`)

O dashboard Streamlit exibe quatro gráficos de linha, utilizando dados consultados do PostgreSQL. Todos os gráficos utilizam suas devidas funções (definidas em `src/charts/charts.py`) que renderiza gráficos **Altair**.

### Gráficos Exibidos:

1.  **Temperatura do Núcleo vs. Velocidade do Núcleo**:
    *   **Título**: 'Temperatura do Núcleo vs Velocidade do Núcleo'
    *   **Eixo X**: "core temp"
    *   **Eixo Y**: "core speed"
    *   Exibe os valores Mínimo, Médio e Máximo da velocidade do núcleo para cada temperatura.
2.  **Temperatura do Núcleo ao Longo do Dia**:
    *   **Título**: 'Temperatura do Núcleo ao Longo do Dia'
    *   **Eixo X**: "time of day" (hora do dia)
    *   **Eixo Y**: "core temp"
    *   Mostra os valores Mínimo, Médio e Máximo da temperatura do núcleo para cada hora do dia.
3.  **Energia do CPU ao Longo do Dia**:
    *   **Título**: 'Energia do CPU ao Longo do Dia'
    *   **Eixo X**: "time of day" (hora do dia)
    *   **Eixo Y**: "cpu power"
    *   Apresenta os valores Mínimo, Médio e Máximo do consumo de energia da CPU para cada hora do dia.
4.  **Energia do CPU vs. Temperatura do Núcleo**:
    *   **Título**: 'Energia do CPU vs Temperatura do Núcleo'
    *   **Eixo X**: "core temp"
    *   **Eixo Y**: "cpu power"
    *   Ilustra os valores Mínimo, Médio e Máximo do consumo de energia da CPU para cada temperatura do núcleo.
5.  **Média Diária de Minutos por Faixa de Temperatura**:
    *   **Título**: 'Média Diária de Minutos por Faixa de Temperatura'
    *   **Eixo X**: "Faixas de temperatura (<60, >=60 & <70, >=70 & <80, >=80 & <90, >=90)"
    *   **Eixo Y**: "Média diária em minutos"
    *   Mostra quanto tempo, em média por dia, o processador permaneceu em cada faixa de temperatura.
    
## Como Executar o Projeto

Para configurar e executar o projeto, siga os passos abaixo:

1.  **Configuração do Ambiente Python**:
    *   Recomendo criar e ativar um ambiente virtual:
        python -m venv .venv
        # Para Windows:
        .venv\Scripts\activate
        # Para macOS/Linux:
        source .venv/bin/activate

    *   Instale as dependências necessárias:
        `pandas streamlit altair sqlalchemy psycopg2-binary`

2.  **Configuração do PostgreSQL**:
    *   Certifique-se de ter uma instância do PostgreSQL (o projeto espera `localhost:5432`).
    *   Crie seu banco de dados.
    *   Ajuste as credenciais nos arquivos `load.py` e `queries.py` conforme sua configuração.

3.  **Execute o arquivo run_app.bat**: 
    isso inicializará o arquivo main.py, criando os seguintes diretórios:
    *   `data_raw`
    *   `data_loaded_raw`
    *   `data_processed`
    *   `data_loaded_processed`
4.  **Dados Brutos**: Coloque seus arquivos CSV de telemetria da CPU (extraídos do `coretemp`) dentro da pasta `data_raw`.

5.  **Executar o Pipeline ETL**:
    *   Volte ao terminal onde está sendo executado o main.py e siga as instruções para processar os arquivos:
        python pipeline.py
        Este script moverá os arquivos de `data_raw` para `data_loaded_raw` e salvará os arquivos processados em `data_processed`.
    *   Em seguida, continue seguindo as instruções no terminal para inserir os dados no PostgreSQL:
        python load.py
        Este script carregará os arquivos de `data_processed` para a tabela `raw_data` no esquema `coretemp` e moverá os arquivos para `data_loaded_processed`.
    `Você pode modificar os parametros para upload dos arquivos para onde desejar dentro do arquivo load.py.`

6.  **Executar o Dashboard Streamlit**:
    *   Inicie a aplicação Streamlit:
        Execute o arquivo run_dashboard.bat
    *   O dashboard será automaticamente aberto em seu navegador web padrão.
    `Os parâmetros para criação do dashboard estão no arquivo app.py dentro do diretório dashboard.`

## Contribuição

Contribuições são bem-vindas!