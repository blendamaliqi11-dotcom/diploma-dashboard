import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import os

# Konfigurimi i faqes
st.set_page_config(
    page_title="Diploma - Memoria Kolektive Digjitale",
    layout="wide"
)

# Stilizim CSS
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    [data-testid="stAppViewBlockContainer"] {
        padding-top: 1rem !important;
    }
    [data-testid="stHeader"] {
        height: 0 !important;
        background: transparent !important;
    }

    .subtitle {
        font-size: 18px;
        font-weight: 400;
        margin-top: 5px;
        margin-bottom: 30px;
    }
    .section-title {
        font-size: 20px;
        font-weight: 600;
        margin-top: 35px;
        margin-bottom: 15px;
        padding-bottom: 8px;
        border-bottom: 2px solid #ff4b4b;
    }
    .section-description {
        font-size: 14px;
        margin-bottom: 20px;
    }
    .footer {
        text-align: center;
        padding: 15px 0 5px 0;
        font-size: 12px;
        margin-top: 0;
    }

    @media (prefers-color-scheme: light) {
        .subtitle { color: #555555; }
        .section-title { color: #ff4b4b; }
        .section-description { color: #666666; }
        .footer { color: #666666; border-top: 1px solid #dddddd; }
    }
    @media (prefers-color-scheme: dark) {
        .subtitle { color: #cccccc; }
        .section-title { color: #ff4b4b; }
        .section-description { color: #b0b0b0; }
        .footer { color: #aaaaaa; border-top: 1px solid #333333; }
    }
    </style>
""", unsafe_allow_html=True)

# Titulli kryesor
st.title("Memoria Kolektive Digjitale")
st.markdown('<div class="subtitle">Analiza e interesit për Historinë, Artin dhe Letërsinë në Wikipedia dhe Google</div>', unsafe_allow_html=True)

# =====================================================
# TË DHËNAT NGA WIKIPEDIA
# =====================================================
@st.cache_data
def lexo_te_dhenat():
    conn = sqlite3.connect("diploma.db")
    query = """
    SELECT eventi, viti, SUM(vizita) AS total_vizita
    FROM vizitat
    GROUP BY eventi, viti
    ORDER BY eventi, viti;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    df["viti"] = df["viti"].astype(int)
    return df

df = lexo_te_dhenat()

# Fjalor për emrat në shqip
emrat_shqip = {
    "World_War_II": "Lufta e Dytë Botërore",
    "The_Holocaust": "Holokausti",
    "Kosovo_War": "Lufta e Kosovës",
    "Berlin_Wall": "Muri i Berlinit",
    "September_11_attacks": "Sulmet e 11 Shtatorit",
    "2008_Kosovo_declaration_of_independence": "Pavarësia e Kosovës (2008)",
    "Mona_Lisa": "Mona Lisa",
    "The_Starry_Night": "Ylli i Natës",
    "Vincent_van_Gogh": "Vincent van Gogh",
    "Leonardo_da_Vinci": "Leonardo da Vinci",
    "Guernica_(Picasso)": "Guernica (Picasso)",
    "The_Persistence_of_Memory": "Këmbëngulja e Kujtesës",
    "Jane_Austen": "Jane Austen",
    "Pride_and_Prejudice": "Krenari dhe Paragjykim",
    "Franz_Kafka": "Franz Kafka",
    "The_Metamorphosis": "Metamorfoza",
    "Mark_Twain": "Mark Twain",
    "Arthur_Rimbaud": "Arthur Rimbaud"
}

df["Emri"] = df["eventi"].map(emrat_shqip).fillna(df["eventi"])

# =====================================================
# TË DHËNAT NGA GOOGLE TRENDS
# =====================================================
@st.cache_data
def lexo_trends(skedari):
    if os.path.exists(skedari):
        df_t = pd.read_csv(skedari)
        df_t["Time"] = pd.to_datetime(df_t["Time"])
        return df_t
    return None

trends_art = lexo_trends("trends_art.csv")
trends_histori = lexo_trends("trends_histori.csv")
trends_letersi = lexo_trends("trends_letersi.csv")

# =====================================================
# TË DHËNAT NGA ML
# =====================================================
@st.cache_data
def lexo_ml(skedari):
    if os.path.exists(skedari):
        return pd.read_csv(skedari)
    return None

ml_krahasimi = lexo_ml("ml_krahasimi.csv")
ml_parashikimet = lexo_ml("ml_parashikimet_2026.csv")
ml_vizuale = lexo_ml("ml_parashikimet_vizuale.csv")

# =====================================================
# MENU NË ANËN E MAJTË
# =====================================================
st.sidebar.header("Filtra")

kategoria = st.sidebar.selectbox(
    "Zgjidh kategorinë:",
    ["Të gjitha", "Histori", "Art", "Letërsi"]
)

histori = ["World_War_II", "The_Holocaust", "Kosovo_War", "Berlin_Wall",
           "September_11_attacks", "2008_Kosovo_declaration_of_independence"]
art = ["Mona_Lisa", "The_Starry_Night", "Vincent_van_Gogh", "Leonardo_da_Vinci",
       "Guernica_(Picasso)", "The_Persistence_of_Memory"]
letersi = ["Jane_Austen", "Pride_and_Prejudice", "Franz_Kafka", "The_Metamorphosis",
           "Mark_Twain", "Arthur_Rimbaud"]

if kategoria == "Histori":
    df_filtruar = df[df["eventi"].isin(histori)]
elif kategoria == "Art":
    df_filtruar = df[df["eventi"].isin(art)]
elif kategoria == "Letërsi":
    df_filtruar = df[df["eventi"].isin(letersi)]
else:
    df_filtruar = df

vitet = sorted(df["viti"].unique())
viti_min = st.sidebar.slider("Viti i fillimit:", min_value=int(vitet[0]), max_value=int(vitet[-1]), value=int(vitet[0]))
viti_max = st.sidebar.slider("Viti i fundit:", min_value=int(vitet[0]), max_value=int(vitet[-1]), value=int(vitet[-1]))

df_filtruar = df_filtruar[(df_filtruar["viti"] >= viti_min) & (df_filtruar["viti"] <= viti_max)]

# =====================================================
# SEKSIONI 1: Totali i vizitave (Wikipedia)
# =====================================================
st.markdown('<div class="section-title">1. Totali i Vizitave në Wikipedia sipas Entitetit</div>', unsafe_allow_html=True)
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
# SEKSIONI 2: Evolucioni ndër vite (Wikipedia)
# =====================================================
st.markdown('<div class="section-title">2. Evolucioni i Vizitave në Wikipedia ndër Vite</div>', unsafe_allow_html=True)
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
# SEKSIONI 3: Statistika përshkruese (Wikipedia)
# =====================================================
st.markdown('<div class="section-title">3. Statistika Përshkruese të Vizitave në Wikipedia</div>', unsafe_allow_html=True)
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

# =====================================================
# SEKSIONI 4: Google Trends - Arti
# =====================================================
if trends_art is not None and kategoria in ["Të gjitha", "Art"]:
    st.markdown('<div class="section-title">4. Google Trends: Interesi për Artin</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-description">Krahasimi i interesit për pikturat dhe artistët në Google Trends. Vlerat shkojnë nga 0 (interes minimal) në 100 (interes maksimal).</div>', unsafe_allow_html=True)

    terma_art = [c for c in trends_art.columns if c not in ["Time"]]
    fig_art = go.Figure()
    for term in terma_art:
        fig_art.add_trace(go.Scatter(
            x=trends_art["Time"], y=trends_art[term],
            mode="lines", name=term
        ))
    fig_art.update_layout(
        height=500,
        title="Google Trends: Interesi për Artin (2015-2025)",
        xaxis_title="Data",
        yaxis_title="Interesi (0-100)",
        template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white",
        font=dict(family="Arial", size=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_art, use_container_width=True)

# =====================================================
# SEKSIONI 5: Google Trends - Historia
# =====================================================
if trends_histori is not None and kategoria in ["Të gjitha", "Histori"]:
    st.markdown('<div class="section-title">5. Google Trends: Interesi për Historinë</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-description">Krahasimi i interesit për eventet historike në Google Trends. Vë re kulmet në vitet e përvjetorëve.</div>', unsafe_allow_html=True)

    terma_histori = [c for c in trends_histori.columns if c not in ["Time"]]
    fig_histori = go.Figure()
    for term in terma_histori:
        fig_histori.add_trace(go.Scatter(
            x=trends_histori["Time"], y=trends_histori[term],
            mode="lines", name=term
        ))
    fig_histori.update_layout(
        height=500,
        title="Google Trends: Interesi për Historinë (2015-2025)",
        xaxis_title="Data",
        yaxis_title="Interesi (0-100)",
        template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white",
        font=dict(family="Arial", size=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_histori, use_container_width=True)

# =====================================================
# SEKSIONI 6: Google Trends - Letërsia
# =====================================================
if trends_letersi is not None and kategoria in ["Të gjitha", "Letërsi"]:
    st.markdown('<div class="section-title">6. Google Trends: Interesi për Letërsinë</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-description">Krahasimi i interesit për autorët dhe veprat letrare në Google Trends.</div>', unsafe_allow_html=True)

    terma_letersi = [c for c in trends_letersi.columns if c not in ["Time"]]
    fig_letersi = go.Figure()
    for term in terma_letersi:
        fig_letersi.add_trace(go.Scatter(
            x=trends_letersi["Time"], y=trends_letersi[term],
            mode="lines", name=term
        ))
    fig_letersi.update_layout(
        height=500,
        title="Google Trends: Interesi për Letërsinë (2015-2025)",
        xaxis_title="Data",
        yaxis_title="Interesi (0-100)",
        template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white",
        font=dict(family="Arial", size=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_letersi, use_container_width=True)

# =====================================================
# SEKSIONI 7: Parashikimi me Machine Learning
# =====================================================
if ml_vizuale is not None:
    st.markdown('<div class="section-title">7. Parashikimi me Machine Learning (ARIMA)</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-description">Parashikimi i vizitave për vitin 2026 duke përdorur modelin ARIMA (AutoRegressive Integrated Moving Average). Vija e vazhdueshme tregon të dhënat historike, vija e ndërprerë tregon parashikimin.</div>', unsafe_allow_html=True)

    # Filtro sipas kategorisë
    if kategoria == "Histori":
        ml_filtruar = ml_vizuale[ml_vizuale["eventi"].isin(histori)]
    elif kategoria == "Art":
        ml_filtruar = ml_vizuale[ml_vizuale["eventi"].isin(art)]
    elif kategoria == "Letërsi":
        ml_filtruar = ml_vizuale[ml_vizuale["eventi"].isin(letersi)]
    else:
        ml_filtruar = ml_vizuale

    # Marrim vetëm 5 entitetet kryesore për të mos e mbushur grafikun
    entitetet_top = ml_parashikimet.head(5)["eventi"].tolist() if ml_parashikimet is not None else ml_filtruar["eventi"].unique()[:5]
    ml_top = ml_filtruar[ml_filtruar["eventi"].isin(entitetet_top)]

    # Krijojmë grafikun me dy vija për secilin entitet
    fig_ml = go.Figure()

    for eventi in entitetet_top:
        df_eventi = ml_top[ml_top["eventi"] == eventi].sort_values("data")
        df_eventi["data"] = pd.to_datetime(df_eventi["data"])

        # Historiku
        df_hist = df_eventi[df_eventi["tipi"] == "Historik"]
        emri_shqip = emrat_shqip.get(eventi, eventi)

        fig_ml.add_trace(go.Scatter(
            x=df_hist["data"], y=df_hist["vizita"],
            mode="lines", name=f"{emri_shqip} (Historik)",
            line=dict(width=2)
        ))

        # Parashikimi
        df_par = df_eventi[df_eventi["tipi"] == "Parashikim 2026"]
        if len(df_par) > 0:
            fig_ml.add_trace(go.Scatter(
                x=df_par["data"], y=df_par["vizita"],
                mode="lines", name=f"{emri_shqip} (2026)",
                line=dict(width=2, dash="dash")
            ))

    fig_ml.update_layout(
        height=600,
        title="Parashikimi i Vizitave për 2026 (ARIMA) - Top 5 Entitetet",
        xaxis_title="Data",
        yaxis_title="Vizita Mujore",
        template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white",
        font=dict(family="Arial", size=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
    )
    st.plotly_chart(fig_ml, use_container_width=True)

    # Tabela e parashikimeve
    st.markdown('<div class="section-description" style="margin-top: 30px;"><b>Tabela e parashikimeve për 2026:</b> Krahasimi i totalit të vizitave në 2025 me parashikimin për 2026.</div>', unsafe_allow_html=True)

    if ml_parashikimet is not None:
        # Filtro sipas kategorisë
        if kategoria == "Histori":
            ml_p_filtruar = ml_parashikimet[ml_parashikimet["eventi"].isin(histori)]
        elif kategoria == "Art":
            ml_p_filtruar = ml_parashikimet[ml_parashikimet["eventi"].isin(art)]
        elif kategoria == "Letërsi":
            ml_p_filtruar = ml_parashikimet[ml_parashikimet["eventi"].isin(letersi)]
        else:
            ml_p_filtruar = ml_parashikimet

        ml_p_shfaqur = ml_p_filtruar.copy()
        ml_p_shfaqur["Entiteti"] = ml_p_shfaqur["eventi"].map(emrat_shqip).fillna(ml_p_shfaqur["eventi"])
        ml_p_shfaqur = ml_p_shfaqur[["Entiteti", "Total_2025", "Parashikimi_2026", "Ndryshimi_%"]]
        ml_p_shfaqur.columns = ["Entiteti", "Totali 2025", "Parashikimi 2026", "Ndryshimi (%)"]

        st.dataframe(ml_p_shfaqur, use_container_width=True, hide_index=True)

# =====================================================
# SEKSIONI 8: Krahasimi i Modeleve
# =====================================================
if ml_krahasimi is not None:
    st.markdown('<div class="section-title">8. Krahasimi i Modeleve: ARIMA vs Linear Regression</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-description">Krahasimi i saktësisë së dy modeleve të parashikimit duke përdorur MAE (Mean Absolute Error). Modeli me MAE më të ulët është më i saktë.</div>', unsafe_allow_html=True)

    # Filtro sipas kategorisë
    if kategoria == "Histori":
        ml_k_filtruar = ml_krahasimi[ml_krahasimi["eventi"].isin(histori)]
    elif kategoria == "Art":
        ml_k_filtruar = ml_krahasimi[ml_krahasimi["eventi"].isin(art)]
    elif kategoria == "Letërsi":
        ml_k_filtruar = ml_krahasimi[ml_krahasimi["eventi"].isin(letersi)]
    else:
        ml_k_filtruar = ml_krahasimi

    ml_k_shfaqur = ml_k_filtruar.copy()
    ml_k_shfaqur["Entiteti"] = ml_k_shfaqur["eventi"].map(emrat_shqip).fillna(ml_k_shfaqur["eventi"])
    ml_k_shfaqur = ml_k_shfaqur[["Entiteti", "MAE_ARIMA", "MAE_LR", "Fituesi"]]
    ml_k_shfaqur.columns = ["Entiteti", "MAE ARIMA", "MAE Linear Regression", "Fituesi"]

    st.dataframe(ml_k_shfaqur, use_container_width=True, hide_index=True)

    # Përmbledhje
    fituesit = ml_k_filtruar["Fituesi"].value_counts()
    st.markdown('<div class="section-description" style="margin-top: 20px;"><b>Përmbledhje:</b> Rezultatet e krahasimit për kategorinë e zgjedhur.</div>', unsafe_allow_html=True)

    cols = st.columns(len(fituesit))
    for i, (fituesi, nr) in enumerate(fituesit.items()):
        with cols[i]:
            st.metric(fituesi, f"{nr} entitete")

# =====================================================
# Footer
# =====================================================
st.markdown(
    '<div class="footer">'
    'Burimi i të dhënave: Wikipedia Pageviews API, Google Trends & Machine Learning (ARIMA)'
    '</div>',
    unsafe_allow_html=True
)
