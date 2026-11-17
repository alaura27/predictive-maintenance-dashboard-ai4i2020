import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Manutenção Preditiva & Operações (AI4I 2020)",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Carregamento de dados com cache
@st.cache_data
def load_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    # Feature Engineering: Delta de Temperatura
    df["Delta Temperature [K]"] = df["Process temperature [K]"] - df["Air temperature [K]"]
    return df

df_raw = load_data("ai4i2020.csv")

# Barra lateral de filtros interativos
st.sidebar.header("🔍 Filtros de Monitoramento")
selected_types = st.sidebar.multiselect(
    "Tipo de Produto / Equipamento (Type):",
    options=sorted(df_raw["Type"].unique()),
    default=sorted(df_raw["Type"].unique()),
    help="L = Baixa qualidade (50%), M = Média (30%), H = Alta (20%)",
)

min_wear, max_wear = int(df_raw["Tool wear [min]"].min()), int(df_raw["Tool wear [min]"].max())
wear_range = st.sidebar.slider(
    "Faixa de Desgaste da Ferramenta [min]:",
    min_value=min_wear,
    max_value=max_wear,
    value=(min_wear, max_wear),
)

# Aplicação dos filtros
df = df_raw[
    (df_raw["Type"].isin(selected_types))
    & (df_raw["Tool wear [min]"].between(wear_range[0], wear_range[1]))
].copy()

# Cabeçalho e Apresentação Inicial dos Dados
st.title("⚙️ Dashboard Analítico de Manutenção Preditiva (AI4I 2020)")
st.markdown(
    """
    Bem-vindo ao painel de controle e análise de comportamento operacional e falhas de equipamentos (**AI4I 2020 Predictive Maintenance Dataset**).
    Este dashboard monitora telemetria industrial em tempo real — incluindo temperatura do ar e do processo, velocidade de rotação, torque e desgaste da ferramenta — para identificar padrões críticos de quebra e apoiar decisões preventivas.
    """
)

with st.expander("📋 Visualizar Apresentação Inicial dos Dados (Amostra e Estatísticas)", expanded=False):
    tab_amostra, tab_estatisticas = st.tabs(["Amostra do Dataset", "Resumo Estatístico"])
    with tab_amostra:
        st.write(f"Exibindo as primeiras 10 linhas de **{len(df):,}** registros filtrados:")
        st.dataframe(df.head(10), use_container_width=True)
    with tab_estatisticas:
        st.dataframe(df.describe().T, use_container_width=True)

st.divider()

# 1. KPIs em Destaque
st.subheader("📊 Indicadores-Chave de Desempenho (KPIs)")

total_equipamentos = len(df)
falhas_criticas = int(df["Machine failure"].sum()) if total_equipamentos > 0 else 0
taxa_falha = (falhas_criticas / total_equipamentos * 100) if total_equipamentos > 0 else 0.0

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric(
        label="Total de Equipamentos Monitorados",
        value=f"{total_equipamentos:,}".replace(",", "."),
        delta=f"{len(df) - len(df_raw)} vs total" if len(df) != len(df_raw) else "100% da base",
    )
with kpi2:
    st.metric(
        label="Falhas Críticas Detectadas",
        value=f"{falhas_criticas:,}".replace(",", "."),
        delta="Unidades com falha",
        delta_color="inverse",
    )
with kpi3:
    st.metric(
        label="Taxa de Falha",
        value=f"{taxa_falha:.2f}%",
        delta="Acima do limite (3.0%)" if taxa_falha > 3.0 else "Dentro do esperado (<3.0%)",
        delta_color="inverse" if taxa_falha > 3.0 else "normal",
    )

st.divider()

# 2. Gráficos Básicos (2 colunas)
st.subheader("📈 Análise Operacional e Distribuição de Falhas")
col_basico1, col_basico2 = st.columns(2)

with col_basico1:
    st.markdown("#### Velocidade de Rotação [rpm] vs Torque [Nm]")
    st.caption("Amostra de até 1.000 linhas otimizada para renderização (colorido por `Machine failure`).")
    if len(df) > 0:
        sample_size = min(1000, len(df))
        df_sample = df.sample(n=sample_size, random_state=42).copy()
        df_sample["Status de Falha"] = df_sample["Machine failure"].map({0: "0 - Normal", 1: "1 - Falha"})
        st.scatter_chart(
            data=df_sample,
            x="Rotational speed [rpm]",
            y="Torque [Nm]",
            color="Machine failure",
            use_container_width=True,
        )
    else:
        st.info("Nenhum dado disponível para os filtros selecionados.")

with col_basico2:
    st.markdown("#### Ocorrências por Tipo de Falha Específica")
    st.caption("Soma das falhas: TWF (Desgaste), HDF (Calor), PWF (Energia) e OSF (Sobrecarga).")
    falhas_especificas = pd.DataFrame(
        {
            "Tipo de Falha": [
                "TWF (Desgaste Ferramenta)",
                "HDF (Dissipação Calor)",
                "PWF (Queda Energia)",
                "OSF (Sobrecarga)",
            ],
            "Total de Ocorrências": [
                int(df["TWF"].sum()),
                int(df["HDF"].sum()),
                int(df["PWF"].sum()),
                int(df["OSF"].sum()),
            ],
        }
    ).set_index("Tipo de Falha")
    st.bar_chart(falhas_especificas, use_container_width=True)

st.divider()

# 3. Análise Profunda / Feature Engineering (2 colunas)
st.subheader("🔬 Análise Profunda & Feature Engineering")
col_prof1, col_prof2 = st.columns(2)

with col_prof1:
    st.markdown("#### Delta de Temperatura [K] vs Desgaste da Ferramenta [min]")
    st.caption("`Delta Temperature [K] = Process temperature [K] - Air temperature [K]` colorido por falha `HDF`.")
    if len(df) > 0:
        sample_size_hdf = min(1000, len(df))
        df_sample_hdf = df.sample(n=sample_size_hdf, random_state=42)
        st.scatter_chart(
            data=df_sample_hdf,
            x="Delta Temperature [K]",
            y="Tool wear [min]",
            color="HDF",
            use_container_width=True,
        )
    else:
        st.info("Nenhum dado disponível para os filtros selecionados.")

with col_prof2:
    st.markdown("#### Correlação das Variáveis com `Machine failure`")
    st.caption("Peso de cada variável numérica na quebra da máquina (excluindo a própria coluna `Machine failure`).")
    cols_numericas = [
        "Air temperature [K]",
        "Process temperature [K]",
        "Delta Temperature [K]",
        "Rotational speed [rpm]",
        "Torque [Nm]",
        "Tool wear [min]",
        "TWF",
        "HDF",
        "PWF",
        "OSF",
        "RNF",
        "Machine failure",
    ]
    if len(df) > 1 and df["Machine failure"].nunique() > 1:
        corr_series = (
            df[cols_numericas]
            .corr()["Machine failure"]
            .drop("Machine failure")
            .sort_values(ascending=False)
        )
        corr_df = corr_series.to_frame(name="Correlação com Machine failure")
        st.bar_chart(corr_df, use_container_width=True)
    else:
        st.info("Dados insuficientes ou sem variação de falha para calcular a correlação.")

st.divider()

# 4. Painel Industrial de Leitura de Sensores & Sistema de Refrigeração
st.subheader("🌡️ Painel Industrial de Sensores & Sistema de Refrigeração")
st.caption(
    "Monitoramento contínuo dos sensores térmicos e de rotação para detecção precoce de falhas de dissipação de calor (HDF)."
)

if total_equipamentos > 0:
    temp_ar_media = df["Air temperature [K]"].mean()
    temp_proc_media = df["Process temperature [K]"].mean()
    delta_medio = df["Delta Temperature [K]"].mean()
    delta_min = df["Delta Temperature [K]"].min()
    soma_hdf = int(df["HDF"].sum())
    soma_twf = int(df["TWF"].sum())

    # Critério físico do dataset AI4I 2020 para risco de falha de dissipação de calor (HDF):
    # Diferença entre temperatura do processo e do ar < 8.6 K e rotação < 1380 rpm
    df_risco_refrigeracao = df[
        (df["Delta Temperature [K]"] < 8.6) & (df["Rotational speed [rpm]"] < 1380)
    ]
    qtd_risco_refrigeracao = len(df_risco_refrigeracao)

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.metric("Sensor Temp. do Ar (Média)", f"{temp_ar_media:.1f} K")
    with s2:
        st.metric("Sensor Temp. Processo (Média)", f"{temp_proc_media:.1f} K")
    with s3:
        st.metric(
            "Delta Térmico Mínimo Lido",
            f"{delta_min:.1f} K",
            delta="Abaixo de 8.6 K (Crítico)" if delta_min < 8.6 else "Nominal (>= 8.6 K)",
            delta_color="inverse" if delta_min < 8.6 else "normal",
        )
    with s4:
        st.metric(
            "Máquinas em Risco Térmico",
            f"{qtd_risco_refrigeracao}",
            delta=f"{soma_hdf} falhas HDF confirmadas",
            delta_color="inverse" if qtd_risco_refrigeracao > 0 or soma_hdf > 0 else "normal",
        )

    # Condicionais de recomendação de inspeção no sistema de refrigeração
    if soma_hdf > 0 and (soma_hdf >= soma_twf or qtd_risco_refrigeracao > 0):
        st.error(
            f"🚨 **INSPEÇÃO IMEDIATA NO SISTEMA DE REFRIGERAÇÃO REQUERIDA:** "
            f"Os sensores registraram **{soma_hdf} falhas por dissipação de calor (HDF)** "
            f"(predominante frente a {soma_twf} falhas TWF) e **{qtd_risco_refrigeracao} equipamentos** operando na zona crítica "
            f"(`Delta Temperature < 8.6 K` com `Rotational speed < 1380 rpm`).\n\n"
            "**Plano de Ação Recomendado:**\n"
            "- Inspecionar imediatamente bombas de fluido refrigerante, trocadores de calor e obstruções nos dutos de ventilação.\n"
            "- Verificar a vazão de ar ao redor dos motores que operam abaixo de 1.380 rpm sob alto torque."
        )
    elif qtd_risco_refrigeracao > 0 or delta_min < 8.6:
        st.warning(
            f"⚠️ **ALERTA PREVENTIVO DE REFRIGERAÇÃO:** "
            f"Os sensores detectaram Delta Térmico mínimo de **{delta_min:.2f} K** (< 8.6 K) com **{qtd_risco_refrigeracao} máquinas** "
            "próximas ao limite térmico de dissipação. Sugere-se inspeção preventiva no sistema de refrigeração e limpeza de filtros."
        )
    else:
        st.success(
            f"✅ **SISTEMA DE REFRIGERAÇÃO OPERANDO NORMALMENTE:** "
            f"Leituras dos sensores térmicos estáveis (Delta médio de **{delta_medio:.2f} K**, mínimo de **{delta_min:.2f} K**) "
            "e nenhuma falha por dissipação de calor (HDF) registrada no filtro atual."
        )

    with st.expander("🔧 Ver Equipamentos que Exigem Inspeção no Sistema de Refrigeração", expanded=False):
        df_inspecao = df[(df["HDF"] == 1) | ((df["Delta Temperature [K]"] < 8.6) & (df["Rotational speed [rpm]"] < 1380))]
        st.write(f"Total de equipamentos sinalizados pelos sensores térmicos: **{len(df_inspecao)}**")
        st.dataframe(
            df_inspecao[
                [
                    "UDI",
                    "Product ID",
                    "Type",
                    "Air temperature [K]",
                    "Process temperature [K]",
                    "Delta Temperature [K]",
                    "Rotational speed [rpm]",
                    "Torque [Nm]",
                    "HDF",
                ]
            ],
            use_container_width=True,
        )
else:
    st.warning("⚠️ Nenhum sensor ativo para os filtros selecionados na barra lateral.")


