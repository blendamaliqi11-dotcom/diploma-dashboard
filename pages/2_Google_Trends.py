import streamlit as st
import plotly.graph_objects as go
from utils import (
    aplikon_stilizim, lexo_trends, shfaq_footer, shfaq_titull
)

st.set_page_config(
    page_title="Google Trends - Memoria Kolektive Digjitale",
    layout="wide"
)

aplikon_stilizim()

shfaq_titull(
    "Analitika e Google Trends",
    "Krahasimi i kërkimeve në Google për tema kulturore (2015-2025)"
)

# =====================================================
# FILTRAT
# =====================================================
st.sidebar.header("Filtra")

kategoria = st.sidebar.selectbox(
    "Zgjidh kategorinë:",
    ["Të gjitha", "Histori", "Art", "Letërsi"]
)

# Leximi i të dhënave
trends_art = lexo_trends("trends_art.csv")
trends_histori = lexo_trends("trends_histori.csv")
trends_letersi = lexo_trends("trends_letersi.csv")

# Marrim vetëm vitet nga 2015 e tutje
te_gjitha_vitet = set()
for df_t in [trends_art, trends_histori, trends_letersi]:
    if df_t is not None:
        vitet_filtruara = df_t[df_t["Time"].dt.year >= 2015]["Time"].dt.year.unique()
        te_gjitha_vitet.update(vitet_filtruara)

vitet = sorted(te_gjitha_vitet)

if len(vitet) > 0:
    viti_min = st.sidebar.slider(
        "Viti i fillimit:",
        min_value=2015,
        max_value=int(vitet[-1]),
        value=2015
    )
    viti_max = st.sidebar.slider(
        "Viti i fundit:",
        min_value=2015,
        max_value=int(vitet[-1]),
        value=int(vitet[-1])
    )
else:
    viti_min, viti_max = 2015, 2025


def filtro_vitet(df):
    """Filtron DataFrame sipas viteve të zgjedhura (nga 2015 e tutje)."""
    if df is None:
        return None
    df_f = df[(df["Time"].dt.year >= max(2015, viti_min)) & (df["Time"].dt.year <= viti_max)]
    return df_f


def krijo_grafik(df, titulli):
    """Krijon një grafik me linja për të gjithë termat."""
    if df is None or len(df) == 0:
        return None
    
    terma = [c for c in df.columns if c not in ["Time"]]
    fig = go.Figure()
    for term in terma:
        fig.add_trace(go.Scatter(
            x=df["Time"], y=df[term],
            mode="lines", name=term
        ))
    fig.update_layout(
        height=500,
        title=titulli,
        xaxis_title="Data",
        yaxis_title="Interesi (0-100)",
        template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white",
        font=dict(family="Arial", size=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig


# =====================================================
# SEKSIONI 1: Arti
# =====================================================
if trends_art is not None and kategoria in ["Të gjitha", "Art"]:
    st.markdown('<div class="section-title">1. Interesi për Artin</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-description">Krahasimi i interesit për pikturat dhe artistët në Google Trends. Vlerat shkojnë nga 0 (interes minimal) në 100 (interes maksimal).</div>', unsafe_allow_html=True)
    
    trends_art_f = filtro_vitet(trends_art)
    fig = krijo_grafik(trends_art_f, "Google Trends: Arti")
    if fig:
        st.plotly_chart(fig, use_container_width=True)

# =====================================================
# SEKSIONI 2: Historia
# =====================================================
if trends_histori is not None and kategoria in ["Të gjitha", "Histori"]:
    st.markdown('<div class="section-title">2. Interesi për Historinë</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-description">Krahasimi i interesit për eventet historike në Google Trends. Vëre kulmet në vitet e përvjetorëve.</div>', unsafe_allow_html=True)
    
    trends_histori_f = filtro_vitet(trends_histori)
    fig = krijo_grafik(trends_histori_f, "Google Trends: Historia")
    if fig:
        st.plotly_chart(fig, use_container_width=True)

# =====================================================
# SEKSIONI 3: Letërsia
# =====================================================
if trends_letersi is not None and kategoria in ["Të gjitha", "Letërsi"]:
    st.markdown('<div class="section-title">3. Interesi për Letërsinë</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-description">Krahasimi i interesit për autorët dhe veprat letrare në Google Trends.</div>', unsafe_allow_html=True)
    
    trends_letersi_f = filtro_vitet(trends_letersi)
    fig = krijo_grafik(trends_letersi_f, "Google Trends: Letërsia")
    if fig:
        st.plotly_chart(fig, use_container_width=True)

shfaq_footer()
