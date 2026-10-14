import os
import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA E FAVICON DA GUIA
# ==========================================
logo_path = "Logo_State_University_of_Ponta_Grossa.png"

page_icon_obj = "🧠"
if os.path.exists(logo_path):
    try:
        page_icon_obj = Image.open(logo_path)
    except Exception:
        page_icon_obj = "🧠"

st.set_page_config(
    page_title="UEPG | Dashboard Neurológico & BioFire® ME",
    page_icon=page_icon_obj,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# 2. ESTILIZAÇÃO CSS CUSTOMIZADA (CORES UEPG)
# ==========================================
st.markdown(
    """
    <style>
        .main {
            background-color: #F8FAFC;
        }

        /* BARRA LATERAL (SIDEBAR) PERSONALIZADA */
        [data-testid="stSidebar"] {
            background-color: #1B2E4B !important;
            color: #FFFFFF !important;
        }
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3, 
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] p {
            color: #FFFFFF !important;
        }
        [data-testid="stSidebar"] div[data-baseweb="select"] {
            background-color: #2B4370 !important;
            border-radius: 8px;
        }
        [data-testid="stSidebar"] div[data-baseweb="select"] span {
            color: #FFFFFF !important;
        }

        /* CABEÇALHO DO DASHBOARD */
        .uepg-header {
            background: linear-gradient(90deg, #1B2E4B 0%, #2B4370 60%, #1CAAD9 100%);
            padding: 22px 28px;
            border-radius: 12px;
            color: white;
            margin-bottom: 25px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.08);
        }
        .uepg-header h1 {
            color: #FFFFFF !important;
            font-size: 26px !important;
            font-weight: 700 !important;
            margin-bottom: 6px !important;
        }
        .uepg-header p {
            color: #E2E8F0 !important;
            font-size: 14px !important;
            margin: 0 !important;
        }

        /* CARDS DE MÉTRICAS (KPIs) PADRONIZADOS E DE ALTO CONTRASTE */
        div[data-testid="stMetric"] {
            background-color: #FFFFFF !important;
            border-left: 5px solid #1CAAD9 !important;
            border-radius: 10px !important;
            padding: 16px 18px !important;
            box-shadow: 0px 3px 8px rgba(0,0,0,0.06) !important;
            min-height: 110px !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
        }
        div[data-testid="stMetric"] label {
            color: #475569 !important;
            font-size: 13px !important;
            font-weight: 700 !important;
            margin-bottom: 4px !important;
        }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: #1B2E4B !important;
            font-size: 26px !important;
            font-weight: 800 !important;
        }
        div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
            color: #0284C7 !important;
            font-size: 12px !important;
            font-weight: 600 !important;
        }

        /* SEÇÃO DE TÍTULOS */
        .section-title {
            color: #1B2E4B;
            font-size: 19px;
            font-weight: 700;
            border-bottom: 3px solid #1CAAD9;
            padding-bottom: 6px;
            margin-top: 25px;
            margin-bottom: 18px;
        }
        
        /* CAIXA DIDÁTICA INFORMATIVA */
        .didactic-box {
            background-color: #EFF6FF;
            border-left: 4px solid #1CAAD9;
            padding: 10px 14px;
            border-radius: 6px;
            margin-bottom: 15px;
            color: #1E293B;
            font-size: 13px;
            line-height: 1.5;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Paleta de Cores
COLOR_PALETTE = {
    "Azul_Escuro": "#1B2E4B",
    "Azul_Medio": "#2B4370",
    "Azul_Claro": "#1CAAD9",
    "Verde_Sucesso": "#10B981",
    "Vermelho_Alerta": "#EF4444",
    "Amarelo_Alerta": "#F59E0B",
    "Roxo_Suave": "#8B5CF6",
    "Cinza_Neutro": "#94A3B8",
}

# ==========================================
# 3. MAPEAMENTOS DIDÁTICOS EM PORTUGUÊS
# ==========================================
MAPA_DESFECHO = {
    "ALTA": "Alta Hospitalar",
    "OB": "Óbito",
    "SEQ": "Sequela Neurológica",
    "TRANSF": "Transferência",
    "CP": "Cuidados Paliativos",
}

MAPA_EF_NEURO = {
    "NOR": "Normal (Sem Déficits)",
    "ALT": "Alterado Generalizado",
    "CONV": "Crise Convulsiva",
    "DEF": "Déficit Motor Focal",
    "COMA": "Coma",
    "SED": "Sedado / RNC em UTI",
    "DEF+CONV": "Déficit Motor + Convulsão",
    "RNC": "Rebaixamento da Consciência",
}

MAPA_SUSPEITA = {
    "MEN": "Meningite",
    "MEN/ENC": "Meningite / Encefalite",
    "SEP": "Sepse",
    "OUT": "Outros Diagnósticos",
    "RASTREIO": "Rastreio Infeccioso",
    "EV": "Enterovirose",
    "MEN/ENC+MCC": "Meningite/Encefalite+MCC",
    "MF": "Meningite Fúngica",
    "VENTRICULITE": "Ventriculite",
}

MAPA_AGENTES = {
    "NEG": "Não Detectado (Negativo)",
    "NME": "Neisseria meningitidis",
    "EV": "Enterovirus",
    "SPN": "Streptococcus pneumoniae",
    "HSV2": "Herpes Simplex Vírus 2",
    "GBS": "Streptococcus agalactiae (GBS)",
    "HHV6": "Herpesvírus Humano 6",
    "VZV": "Vírus Varicela-Zoster",
    "SEP": "Streptococcus agalactiae",
    "SEPI": "Staphylococcus epidermidis",
    "KPC": "Klebsiella pneumoniae (KPC)",
}


# ==========================================
# 4. CARGA E TRATAMENTO DOS DADOS
# ==========================================
@st.cache_data
def carregar_dados():
    file_path = "analise_estatistica_biofire_TCC (1).xlsx"

    if not os.path.exists(file_path):
        st.error(f"❌ Arquivo '{file_path}' não foi encontrado no diretório.")
        st.stop()

    df = pd.read_excel(file_path, sheet_name="banco limpo por virgula")

    df["Idade_Anos"] = pd.to_numeric(
        df["Idade (anos)"]
        .astype(str)
        .str.replace(",", ".")
        .str.extract(r"(\d+\.?\d*)")[0],
        errors="coerce",
    )

    df["Desfecho_Didatico"] = (
        df["Desfecho"].map(MAPA_DESFECHO).fillna("Não Informado")
    )
    df["EF_Inicial_Didatico"] = (
        df["EF Neurológico Inicial"].map(MAPA_EF_NEURO).fillna("Não Informado")
    )
    df["EF_Final_Didatico"] = (
        df["EF Neurológico final"].map(MAPA_EF_NEURO).fillna("Não Informado")
    )
    df["Suspeita_Didatica"] = (
        df["Suspeita diagnóstica"]
        .map(MAPA_SUSPEITA)
        .fillna(df["Suspeita diagnóstica"])
    )
    df["Biofire_Agente_Nome"] = (
        df["Resultado do Painel Biofire® ME"]
        .map(MAPA_AGENTES)
        .fillna(df["Resultado do Painel Biofire® ME"])
    )
    df["Cultura_Agente_Nome"] = (
        df["Resultado da Cultura Convencional"]
        .map(MAPA_AGENTES)
        .fillna(df["Resultado da Cultura Convencional"])
    )

    return df


try:
    df_raw = carregar_dados()
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# ==========================================
# 5. CABEÇALHO E SIDEBAR PERSONALIZADA
# ==========================================
col_header_1, col_header_2 = st.columns([1, 5])
with col_header_1:
    if os.path.exists(logo_path):
        st.image(logo_path, width=140)
    else:
        st.markdown("### 🎓 UEPG")

with col_header_2:
    st.markdown(
        """
        <div class="uepg-header">
            <h1>Universidade Estadual de Ponta Grossa — UEPG</h1>
            <p>Painel de Análise Clínica: Diagnóstico Molecular BioFire® ME, Aspectos Neurológicos e Desfechos</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

# Sidebar Personalizada
st.sidebar.markdown("## 🔍 Filtros de Pesquisa")
st.sidebar.markdown("---")

setores_opcoes = sorted(df_raw["Setor de Internamento"].dropna().unique())
setores_sel = st.sidebar.multiselect(
    "Setor de Internamento:",
    options=setores_opcoes,
    default=setores_opcoes,
)

classif_opcoes = sorted(df_raw["Classificação padronizada"].dropna().unique())
classif_sel = st.sidebar.multiselect(
    "Classificação Diagnóstica Final:",
    options=classif_opcoes,
    default=classif_opcoes,
)

biofire_opcoes = sorted(df_raw["Biofire positivo?"].dropna().unique())
biofire_sel = st.sidebar.multiselect(
    "BioFire® Positivo?",
    options=biofire_opcoes,
    default=biofire_opcoes,
)

# Filtro
df = df_raw[
    (df_raw["Setor de Internamento"].isin(setores_sel))
    & (df_raw["Classificação padronizada"].isin(classif_sel))
    & (df_raw["Biofire positivo?"].isin(biofire_sel))
]

# ==========================================
# 6. CARDS DE INDICADORES (KPIs)
# ==========================================
total_casos = len(df)
obitos = (df["Desfecho"] == "OB").sum()
sequelas = (df["Desfecho"] == "SEQ").sum()
biofire_pos = (df["Biofire positivo?"] == "SIM").sum()
tempo_medio_terapia = df["Tempo até início de terapia direcionada (h)"].mean()

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

kpi1.metric("Total de Episódios", f"{total_casos}")
kpi2.metric(
    "Óbitos",
    f"{obitos}",
    delta=f"{(obitos/total_casos*100):.1f}% do total"
    if total_casos > 0
    else "0%",
)
kpi3.metric(
    "Sequelas Neurológicas",
    f"{sequelas}",
    delta=f"{(sequelas/total_casos*100):.1f}% do total"
    if total_casos > 0
    else "0%",
)
kpi4.metric(
    "BioFire® Positivo",
    f"{biofire_pos}",
    delta=f"{(biofire_pos/total_casos*100):.1f}% positividade"
    if total_casos > 0
    else "0%",
)
kpi5.metric(
    "Média Tempo Terapia",
    f"{tempo_medio_terapia:.1f} h" if pd.notnull(tempo_medio_terapia) else "N/A",
)

st.markdown("---")

# ==========================================
# 7. SEÇÃO 1: ASPECTOS NEUROLÓGICOS
# ==========================================
st.markdown(
    "<div class='section-title'>1. Aspectos Neurológicos: Evolução Clínico-Exame Físico</div>",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class='didactic-box'>
    <b>💡 Entendimento Clínico:</b> Compare o estado neurológico do paciente na <b>admissão/punção lombar (Inicial)</b> com o estado na <b>alta/desfecho (Final)</b>. Observe o perfil de desfecho associado a quadros mais graves como coma e convulsão.
</div>
""",
    unsafe_allow_html=True,
)

col_neuro_1, col_neuro_2 = st.columns(2)

with col_neuro_1:
    fig_ef_init = px.histogram(
        df,
        x="EF_Inicial_Didatico",
        color="Desfecho_Didatico",
        title="Exame Físico Neurológico INICIAL por Desfecho",
        labels={
            "EF_Inicial_Didatico": "Exame Físico Inicial",
            "count": "Nº Pacientes",
            "Desfecho_Didatico": "Desfecho Final",
        },
        color_discrete_map={
            "Alta Hospitalar": COLOR_PALETTE["Verde_Sucesso"],
            "Óbito": COLOR_PALETTE["Vermelho_Alerta"],
            "Sequela Neurológica": COLOR_PALETTE["Amarelo_Alerta"],
            "Transferência": COLOR_PALETTE["Azul_Claro"],
            "Cuidados Paliativos": COLOR_PALETTE["Roxo_Suave"],
        },
        barmode="stack",
    )
    fig_ef_init.update_layout(
        xaxis_tickangle=-25,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(title="Desfecho"),
    )
    st.plotly_chart(fig_ef_init, use_container_width=True)

with col_neuro_2:
    fig_ef_fin = px.histogram(
        df,
        x="EF_Final_Didatico",
        color="Desfecho_Didatico",
        title="Exame Físico Neurológico FINAL por Desfecho",
        labels={
            "EF_Final_Didatico": "Exame Físico Final",
            "count": "Nº Pacientes",
            "Desfecho_Didatico": "Desfecho Final",
        },
        color_discrete_map={
            "Alta Hospitalar": COLOR_PALETTE["Verde_Sucesso"],
            "Óbito": COLOR_PALETTE["Vermelho_Alerta"],
            "Sequela Neurológica": COLOR_PALETTE["Amarelo_Alerta"],
            "Transferência": COLOR_PALETTE["Azul_Claro"],
            "Cuidados Paliativos": COLOR_PALETTE["Roxo_Suave"],
        },
        barmode="stack",
    )
    fig_ef_fin.update_layout(
        xaxis_tickangle=-25,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(title="Desfecho"),
    )
    st.plotly_chart(fig_ef_fin, use_container_width=True)

# ==========================================
# 8. SEÇÃO 2: ETIOLOGIA E DETECÇÃO DIAGNÓSTICA (EXCLUSIVO BIOFIRE®)
# ==========================================
st.markdown(
    "<div class='section-title'>2. Diagnóstico Etiológico e Desempenho do Painel BioFire® ME</div>",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class='didactic-box'>
    <b>💡 Entendimento Diagnóstico:</b> Apresentação da distribuição de patógenos identificados pelo painel molecular <b>BioFire® ME</b> e os indicadores de acurácia em relação ao padrão de referência clínica.
</div>
""",
    unsafe_allow_html=True,
)

# Gráfico de Patógenos BioFire ME
df_bio_pos = (
    df[df["Resultado do Painel Biofire® ME"] != "NEG"]["Biofire_Agente_Nome"]
    .value_counts()
    .reset_index(name="Casos")
)
df_bio_pos.columns = ["Patógeno", "Casos"]

if len(df_bio_pos) > 0:
    fig_bio = px.bar(
        df_bio_pos,
        x="Patógeno",
        y="Casos",
        text="Casos",
        title="Distribuição de Patógenos Identificados pelo Painel BioFire® ME",
        color="Casos",
        color_continuous_scale=["#1CAAD9", "#1B2E4B"],
    )
    fig_bio.update_traces(textposition="outside")
    fig_bio.update_layout(
        xaxis_tickangle=0,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_bio, use_container_width=True)
else:
    st.info("Nenhum agente detectado no BioFire® nos filtros selecionados.")

# Acurácia do Exame
st.markdown("##### 🎯 Indicadores de Acurácia Diagnóstica (vs. Referência Clínica)")
vp = df_raw["VP"].sum()
fp = df_raw["FP"].sum()
vn = df_raw["VN"].sum()
fn = df_raw["FN"].sum()

sens = (vp / (vp + fn)) * 100 if (vp + fn) > 0 else 0
esp = (vn / (vn + fp)) * 100 if (vn + fp) > 0 else 0
vpp = (vp / (vp + fp)) * 100 if (vp + fp) > 0 else 0
vpn = (vn / (vn + fn)) * 100 if (vn + fn) > 0 else 0

a1, a2, a3, a4 = st.columns(4)
a1.metric("Sensibilidade", f"{sens:.1f}%")
a2.metric("Especificidade", f"{esp:.1f}%")
a3.metric("Valor Preditivo Positivo (VPP)", f"{vpp:.1f}%")
a4.metric("Valor Preditivo Negativo (VPN)", f"{vpn:.1f}%")

# ==========================================
# 9. SEÇÃO 3: DESFECHOS E TEMPO DE INTERNAÇÃO
# ==========================================
st.markdown(
    "<div class='section-title'>3. Análise do Desfecho Clínico e Tempo de Internação</div>",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class='didactic-box'>
    <b>💡 Entendimento dos Desfechos:</b> O gráfico à esquerda exibe o desfecho segundo a classificação diagnóstica padronizada. O gráfico à direita indica a <b>média exata de dias de internação</b> para cada grupo de desfecho.
</div>
""",
    unsafe_allow_html=True,
)

col_desf_1, col_desf_2 = st.columns(2)

with col_desf_1:
    fig_desf_class = px.histogram(
        df,
        x="Classificação padronizada",
        color="Desfecho_Didatico",
        title="Desfechos Clínicos por Diagnóstico Padronizado",
        labels={
            "Classificação padronizada": "Diagnóstico Padronizado",
            "count": "Nº Pacientes",
            "Desfecho_Didatico": "Desfecho",
        },
        color_discrete_map={
            "Alta Hospitalar": COLOR_PALETTE["Verde_Sucesso"],
            "Óbito": COLOR_PALETTE["Vermelho_Alerta"],
            "Sequela Neurológica": COLOR_PALETTE["Amarelo_Alerta"],
            "Transferência": COLOR_PALETTE["Azul_Claro"],
            "Cuidados Paliativos": COLOR_PALETTE["Roxo_Suave"],
        },
        barmode="stack",
    )
    fig_desf_class.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(title="Desfecho"),
    )
    st.plotly_chart(fig_desf_class, use_container_width=True)

with col_desf_2:
    df_tempo_desf = (
        df.groupby("Desfecho_Didatico")["Tempo de internação (dias)"]
        .mean()
        .reset_index()
    )
    df_tempo_desf["Média de Dias"] = df_tempo_desf[
        "Tempo de internação (dias)"
    ].round(1)

    fig_bar_tempo = px.bar(
        df_tempo_desf,
        x="Desfecho_Didatico",
        y="Média de Dias",
        text="Média de Dias",
        title="Média de Dias de Internação por Desfecho Clínico",
        labels={
            "Desfecho_Didatico": "Desfecho Clínico",
            "Média de Dias": "Média de Dias Internado",
        },
        color="Desfecho_Didatico",
        color_discrete_map={
            "Alta Hospitalar": COLOR_PALETTE["Verde_Sucesso"],
            "Óbito": COLOR_PALETTE["Vermelho_Alerta"],
            "Sequela Neurológica": COLOR_PALETTE["Amarelo_Alerta"],
            "Transferência": COLOR_PALETTE["Azul_Claro"],
            "Cuidados Paliativos": COLOR_PALETTE["Roxo_Suave"],
        },
    )
    fig_bar_tempo.update_traces(
        texttemplate="%{text} dias", textposition="outside"
    )
    fig_bar_tempo.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )
    st.plotly_chart(fig_bar_tempo, use_container_width=True)

# ==========================================
# 10. VISÃO ANALÍTICA INDIVIDUAL (TABELA DE DADOS)
# ==========================================
st.markdown(
    "<div class='section-title'>4. Tabela Analítica Individual de Pacientes</div>",
    unsafe_allow_html=True,
)

cols_exibir = [
    "Nº Atendimento",
    "Sexo",
    "Idade_Anos",
    "Setor de Internamento",
    "Suspeita_Didatica",
    "EF_Inicial_Didatico",
    "EF_Final_Didatico",
    "Biofire_Agente_Nome",
    "Cultura_Agente_Nome",
    "Classificação padronizada",
    "Desfecho_Didatico",
    "Tempo de internação (dias)",
]

df_tabela = df[cols_exibir].rename(
    columns={
        "Idade_Anos": "Idade (Anos)",
        "Suspeita_Didatica": "Suspeita Inicial",
        "EF_Inicial_Didatico": "EF Inicial",
        "EF_Final_Didatico": "EF Final",
        "Biofire_Agente_Nome": "Resultado BioFire®",
        "Cultura_Agente_Nome": "Resultado Cultura",
        "Desfecho_Didatico": "Desfecho",
        "Tempo de internação (dias)": "Internação (Dias)",
    }
)

st.dataframe(df_tabela, use_container_width=True, hide_index=True)

# Botão para Baixar Tabela Filtrada
csv_data = df_tabela.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Baixar Tabela Filtrada em CSV",
    data=csv_data,
    file_name="relatorio_pacientes_biofire_uepg.csv",
    mime="text/csv",
)