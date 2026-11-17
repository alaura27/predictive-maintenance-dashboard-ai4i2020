# ⚙️ Dashboard Analítico de Manutenção Preditiva (AI4I 2020)

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/Status-Conclu%C3%ADdo-success)

Painel interativo construído em **Python**, **Streamlit** e **Pandas** para monitoramento de telemetria industrial, análise exploratória de falhas e diagnóstico preventivo do sistema de refrigeração utilizando o **AI4I 2020 Predictive Maintenance Dataset**.

---

## 🎯 Objetivo do Projeto

Em ambientes industriais modernos (Indústria 4.0), paradas não planejadas geram altos custos operacionais. Este projeto transforma dados brutos de sensores de máquinas em um **dashboard executivo e operacional** capaz de:

- Monitorar indicadores críticos de falha em tempo real (**KPIs**).
- Identificar a relação física entre **velocidade de rotação (RPM)**, **torque (Nm)** e quebras de equipamento.
- Realizar **Feature Engineering** calculando o **Delta de Temperatura (`Process temperature [K] - Air temperature [K]`)** para rastrear anomalias térmicas.
- Quantificar o peso (correlação) de cada variável operacional na ocorrência de falhas (`Machine failure`).
- Ler os sensores térmicos e de rotação para **sugerir automaticamente inspeções no sistema de refrigeração** e listar as máquinas em zona de risco.

---

## 📊 Funcionalidades do Dashboard

### 1. Apresentação Inicial & Filtros Dinâmicos
- **Barra Lateral Interativa**: Filtro por categoria de qualidade do equipamento (`Type`: `L`, `M`, `H`) e intervalo de desgaste da ferramenta (`Tool wear [min]`).
- **Inspeção da Base**: Visualização rápida das primeiras linhas do conjunto de dados filtrado e tabela de estatísticas descritivas (`count`, `mean`, `std`, `min`, `max`, quartis).

### 2. KPIs em Destaque (`st.metric`)
- **Total de Equipamentos Monitorados**: Contagem dinâmica dos equipamentos ativos no filtro (`10.000` na base completa).
- **Falhas Críticas Detectadas**: Soma total de ocorrências de `Machine failure` (`339` falhas na base completa).
- **Taxa de Falha (%)**: Percentual de quebra em relação ao total monitorado (`3,39%`), com alerta de limite operacional (`3,0%`).

### 3. Gráficos Básicos (Visão Operacional)
- **Velocidade de Rotação `[rpm]` vs Torque `[Nm]`**: Gráfico de dispersão (`st.scatter_chart`) com amostragem otimizada (`1.000` linhas) colorido pelo status de falha (`Machine failure`).
- **Ocorrências por Tipo de Falha Específica**: Gráfico de barras (`st.bar_chart`) comparando os modos de falha:
  - **HDF** (*Heat Dissipation Failure* — Dissipação de Calor): `115` ocorrências
  - **OSF** (*Overstrain Failure* — Sobrecarga): `98` ocorrências
  - **PWF** (*Power Failure* — Queda/Extremo de Potência): `95` ocorrências
  - **TWF** (*Tool Wear Failure* — Desgaste da Ferramenta): `46` ocorrências

### 4. Análise Profunda & Feature Engineering
- **Engenharia de Atributos (`Delta Temperature [K]`)**:
  $$\text{Delta Temperature [K]} = \text{Process temperature [K]} - \text{Air temperature [K]}$$
  Gráfico de dispersão cruzando `Delta Temperature [K]` vs `Tool wear [min]`, colorido pela falha térmica (`HDF`).
- **Correlação com `Machine failure`**: Matriz de correlação das variáveis numéricas exibida em gráfico de barras ordenado para destacar os fatores de maior impacto na quebra.

### 5. 🌡️ Painel Industrial de Sensores & Sistema de Refrigeração
- Leitura contínua dos sensores térmicos (`Air temperature [K]`, `Process temperature [K]` e `Delta Temperature [K]` mínimo).
- Identificação automática de equipamentos operando na **zona crítica de dissipação de calor** (`Delta Temperature < 8.6 K` combinado com `Rotational speed < 1380 rpm`).
- Sistema de recomendação automática (`st.error`, `st.warning`, `st.success`) para **inspeção imediata de bombas de fluido refrigerante, trocadores de calor e dutos de ventilação**, acompanhado da tabela nominal (`UDI` e `Product ID`) das máquinas sinalizadas.

---

## 🗂️ Sobre o Dataset (AI4I 2020)

O conjunto de dados **AI4I 2020 Predictive Maintenance Dataset** contém **10.000 registros** e **14 variáveis** que simulam dados reais de manutenção preditiva na indústria:

| Coluna | Descrição |
| :--- | :--- |
| `UDI` | Identificador único do registro (`1` a `10000`) |
| `Product ID` | Código do produto/equipamento (prefixo `L`, `M` ou `H`) |
| `Type` | Variante de qualidade do produto (`L` = Baixa 50%, `M` = Média 30%, `H` = Alta 20%) |
| `Air temperature [K]` | Temperatura do ar ambiente em Kelvin |
| `Process temperature [K]` | Temperatura do processo em Kelvin |
| `Rotational speed [rpm]` | Velocidade de rotação calculada a partir de uma potência de 2860 W |
| `Torque [Nm]` | Torque aplicado em Newton-metro |
| `Tool wear [min]` | Tempo acumulado de desgaste da ferramenta em minutos |
| `Machine failure` | Indicador binário de falha da máquina (`0` = Normal, `1` = Falha) |
| `TWF`, `HDF`, `PWF`, `OSF`, `RNF` | Modos específicos de falha (Desgaste, Calor, Energia, Sobrecarga, Aleatória) |

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
- **Python 3.10+** instalado

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/SEU-USUARIO/predictive-maintenance-dashboard-ai4i2020.git
   cd predictive-maintenance-dashboard-ai4i2020
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o dashboard no Streamlit:**
   ```bash
   streamlit run app.py
   ```

4. **Acesse no navegador:**
   O painel abrirá automaticamente em `http://localhost:8501`.

---

## 📁 Estrutura do Repositório

```text
predictive_maintenance_app/
├── ai4i2020.csv        # Base de dados AI4I 2020 Predictive Maintenance (10.000 registros)
├── app.py              # Aplicação principal do dashboard em Streamlit
├── requirements.txt    # Dependências Python do projeto
├── .gitignore          # Arquivos e diretórios ignorados pelo Git
└── README.md           # Documentação completa e apresentação do projeto
```

---

## 💡 Principais Insights Técnicos Extraídos

1. **Predominância de Falhas Térmicas (`HDF`)**: A falha por dissipação de calor é a principal causa isolada de parada (`115` casos), ocorrendo especificamente quando o diferencial térmico (`Delta Temperature [K]`) cai abaixo de `8.6 K` e a velocidade de rotação é inferior a `1380 rpm`.
2. **Relação Torque vs Rotação (`PWF` & `OSF`)**: Operações em regimes extremos de torque elevado com baixa rotação aumentam drasticamente a probabilidade de falha por potência (`PWF`) e sobrecarga mecânica (`OSF`).
3. **Janela Preventiva de Ferramental (`TWF`)**: O desgaste de ferramenta concentra quebras na faixa de `200` a `240` minutos de operação contínua, permitindo agendar trocas preventivas antes da falha.
