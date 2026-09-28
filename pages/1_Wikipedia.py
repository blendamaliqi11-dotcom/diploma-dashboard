import streamlit as st
import plotly.express as px
from utils import (
    aplikon_stilizim, lexo_te_dhenat, filtro_sipas_kategorise,
    shfaq_footer, shfaq_titull
)

st.set_page_config(
    page_title="Wikipedia - Memoria Kolektive Digjitale",
    layout="wide"
)

aplikon_stilizim()

shfaq_titull(
    "Wikipedia Analytics",
    "Analiza e vizitave në artikujt e Wikipedia-s për 18 entitete kulturore (2015-2025)"
)

# Menyja e filtrimit
st.sidebar.header("Filtra")

kategoria = st.sidebar.selectbox(
    "Zgjidh kategorinë:",
    ["Të gjitha", "Histori", "Art", "Letërsi"]
)

df = lexo_te_dhenat()
df_filtruar = filtro_sipas_kategorise(df, kategoria)

vitet = sorted(df["viti"].unique())
viti_min = st.sidebar.slider("Viti i fillimit:", min_value=int(vitet[0]), max_value=int(vitet[-1]), value=int(vitet[0]))
viti_max = st.sidebar.slider("Viti i fundit:", min_value=int(vitet[0]), max_value=int(vitet[-1]), value=int(vitet[-1]))

df_filtruar = df_filtruar[(df_filtruar["viti"] >= viti_min) & (df_filtruar["viti"] <= viti_max)]

# =====================================================
# SEKSIONI 1: Totali i vizitave
# =====================================================
st.markdown('<div class="section-title">1. Totali i Vizitave sipas Entitetit</div>', unsafe_allow_html=True)
st.markdown('<div class="section-description">Shuma totale e vizitave në Wikipedia për secilin entitet gjatë periudhës së zgjedhur.</div>', unsafe_allow_html=True)

totali = df_filtruar.groupby("Emri")["total_vizita"].sum().reset_index()
totali = totali.sort_values("total_vizita", ascending=True)

fig1 = px.bar(
    totali,
    x="total_vizita",
    y="Emri",
    orientation="h",
    title="Totali i Vizitave në Wikipedia (2015-2025)",
    labels={"total_vizita": "Numri i Vizitave", "Emri": "Entiteti"},
    color="total_vizita",
    color_continuous_scale="Blues"
)
fig1.update_layout(
    height=600,
    showlegend=False,
    coloraxis_showscale=False,
    template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white",
    font=dict(family="Arial", size=12),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig1, use_container_width=True)

# =====================================================
# SEKSIONI 2: Evolucioni ndër vite
# =====================================================
st.markdown('<div class="section-title">2. Evolucioni i Vizitave ndër Vite</div>', unsafe_allow_html=True)
st.markdown('<div class="section-description">Trendi i vizitave nga viti 2015 deri në 2025 për secilin entitet të zgjedhur.</div>', unsafe_allow_html=True)

fig2 = px.line(
    df_filtruar,
    x="viti",
    y="total_vizita",
    color="Emri",
    title="Evolucioni i Vizitave në Wikipedia (2015-2025)",
    labels={"total_vizita": "Numri i Vizitave", "viti": "Viti", "Emri": "Entiteti"},
    markers=True
)
fig2.update_layout(
    height=600,
    template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white",
    font=dict(family="Arial", size=12),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)
fig2.update_xaxes(dtick=1)
st.plotly_chart(fig2, use_container_width=True)

# =====================================================
# SEKSIONI 3: Statistika përshkruese
# =====================================================
st.markdown('<div class="section-title">3. Statistika Përshkruese</div>', unsafe_allow_html=True)
st.markdown('<div class="section-description">Përmbledhje statistikore për secilin entitet: mesatarja, mediana, minimumi, maksimumi dhe totali i vizitave.</div>', unsafe_allow_html=True)

stats = df_filtruar.groupby("Emri")["total_vizita"].agg([
    ("Mesatare", "mean"),
    ("Mediane", "median"),
    ("Minimum", "min"),
    ("Maksimum", "max"),
    ("Total", "sum")
]).round(0).astype(int).reset_index()

stats = stats.sort_values("Total", ascending=False)
stats.columns = ["Entiteti", "Mesatare", "Mediane", "Minimum", "Maksimum", "Total"]

st.dataframe(stats, use_container_width=True, hide_index=True)

shfaq_footer()
