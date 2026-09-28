import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import (
    aplikon_stilizim, lexo_ml, EMRAT_SHQIP, HISTORI, ART, LETERSI,
    shfaq_footer, shfaq_titull
)

st.set_page_config(
    page_title="Machine Learning - Memoria Kolektive Digjitale",
    layout="wide"
)

aplikon_stilizim()

shfaq_titull(
    "Parashikimi me Machine Learning",
    "Modelet ARIMA dhe Linear Regression për parashikimin e vizitave në 2026"
)

# =====================================================
# FILTRAT
# =====================================================
st.sidebar.header("Filtra")

kategoria = st.sidebar.selectbox(
    "Zgjidh kategorinë:",
    ["Të gjitha", "Histori", "Art", "Letërsi"]
)

# Leximi
ml_krahasimi = lexo_ml("ml_krahasimi.csv")
ml_parashikimet = lexo_ml("ml_parashikimet_2026.csv")
ml_vizuale = lexo_ml("ml_parashikimet_vizuale.csv")

# Filtrat e viteve për grafikun vizual
if ml_vizuale is not None:
    ml_vizuale["data"] = pd.to_datetime(ml_vizuale["data"])
    vitet = sorted(ml_vizuale["data"].dt.year.unique())
    
    viti_min = st.sidebar.slider(
        "Viti i fillimit:",
        min_value=int(vitet[0]),
        max_value=int(vitet[-1]),
        value=int(vitet[0])
    )
    viti_max = st.sidebar.slider(
        "Viti i fundit:",
        min_value=int(vitet[0]),
        max_value=int(vitet[-1]),
        value=int(vitet[-1])
    )
else:
    viti_min, viti_max = 2015, 2026


def filtro_kategori(df, kategoria, kolona="eventi"):
    if df is None:
        return None
    if kategoria == "Histori":
        return df[df[kolona].isin(HISTORI)]
    elif kategoria == "Art":
        return df[df[kolona].isin(ART)]
    elif kategoria == "Letërsi":
        return df[df[kolona].isin(LETERSI)]
    return df


def filtro_vitet(df, viti_min, viti_max, kolona="data"):
    if df is None:
        return None
    df["data"] = pd.to_datetime(df["data"])
    return df[(df[kolona].dt.year >= viti_min) & (df[kolona].dt.year <= viti_max)]


# =====================================================
# SEKSIONI 1: Parashikimi 2026
# =====================================================
if ml_vizuale is not None:
    st.markdown('<div class="section-title">1. Parashikimi i Vizitave për 2026</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-description">Vija e vazhdueshme tregon të dhënat historike, vija e ndërprerë tregon parashikimin për 2026.</div>', unsafe_allow_html=True)

    ml_filtruar = filtro_kategori(ml_vizuale, kategoria)
    ml_filtruar = filtro_vitet(ml_filtruar, viti_min, viti_max)

    if ml_parashikimet is not None:
        entitetet_top = filtro_kategori(ml_parashikimet, kategoria).head(5)["eventi"].tolist()
    else:
        entitetet_top = ml_filtruar["eventi"].unique()[:5]

    ml_top = ml_filtruar[ml_filtruar["eventi"].isin(entitetet_top)]

    if len(ml_top) > 0:
        fig_ml = go.Figure()

        for eventi in entitetet_top:
            df_eventi = ml_top[ml_top["eventi"] == eventi].sort_values("data")
            emri = EMRAT_SHQIP.get(eventi, eventi)

            df_hist = df_eventi[df_eventi["tipi"] == "Historik"]
            if len(df_hist) > 0:
                fig_ml.add_trace(go.Scatter(
                    x=df_hist["data"], y=df_hist["vizita"],
                    mode="lines", name=f"{emri} (Historik)",
                    line=dict(width=2)
                ))

            df_par = df_eventi[df_eventi["tipi"] == "Parashikim 2026"]
            if len(df_par) > 0:
                fig_ml.add_trace(go.Scatter(
                    x=df_par["data"], y=df_par["vizita"],
                    mode="lines", name=f"{emri} (2026)",
                    line=dict(width=2, dash="dash")
                ))

        fig_ml.update_layout(
            height=600,
            title="Parashikimi i Vizitave për 2026 (ARIMA)",
            xaxis_title="Data",
            yaxis_title="Vizita Mujore",
            template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white",
            font=dict(family="Arial", size=12),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
        )
        st.plotly_chart(fig_ml, use_container_width=True)
    else:
        st.info("Nuk ka të dhëna për periudhën e zgjedhur.")

    # Tabela e parashikimeve
    st.markdown('<div class="section-title">2. Tabela e Parashikimeve</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-description">Krahasimi i totalit të vizitave në 2025 me parashikimin për 2026.</div>', unsafe_allow_html=True)

    if ml_parashikimet is not None:
        ml_p = filtro_kategori(ml_parashikimet, kategoria).copy()
        ml_p["Entiteti"] = ml_p["eventi"].map(EMRAT_SHQIP).fillna(ml_p["eventi"])
        ml_p = ml_p[["Entiteti", "Total_2025", "Parashikimi_2026", "Ndryshimi_%"]]
        ml_p.columns = ["Entiteti", "Totali 2025", "Parashikimi 2026", "Ndryshimi (%)"]
        st.dataframe(ml_p, use_container_width=True, hide_index=True)


# =====================================================
# SEKSIONI 3: Krahasimi i modeleve
# =====================================================
if ml_krahasimi is not None:
    st.markdown('<div class="section-title">3. Krahasimi i Modeleve: ARIMA vs Linear Regression</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-description">Krahasimi i saktësisë së dy modeleve duke përdorur MAE (Mean Absolute Error). Modeli me MAE më të ulët është më i saktë.</div>', unsafe_allow_html=True)

    ml_k = filtro_kategori(ml_krahasimi, kategoria).copy()
    ml_k["Entiteti"] = ml_k["eventi"].map(EMRAT_SHQIP).fillna(ml_k["eventi"])
    ml_k = ml_k[["Entiteti", "MAE_ARIMA", "MAE_LR", "Fituesi"]]
    ml_k.columns = ["Entiteti", "MAE ARIMA", "MAE Linear Regression", "Fituesi"]
    st.dataframe(ml_k, use_container_width=True, hide_index=True)

    # Përmbledhje
    fituesit = filtro_kategori(ml_krahasimi, kategoria)["Fituesi"].value_counts()
    st.markdown('<div class="section-description" style="margin-top: 20px;"><b>Përmbledhje:</b></div>', unsafe_allow_html=True)

    cols = st.columns(len(fituesit))
    for i, (fituesi, nr) in enumerate(fituesit.items()):
        with cols[i]:
            st.metric(fituesi, f"{nr} entitete")

shfaq_footer()
