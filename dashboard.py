import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

# Konfigurimi i faqes
st.set_page_config(
    page_title="Diploma - Memoria Kolektive Digjitale",
    layout="wide"
)

# Stilizim CSS
st.markdown("""
    <style>
    /* Redukto hapësirën në krye të faqes */
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

    /* Light mode */
    @media (prefers-color-scheme: light) {
        .subtitle { color: #555555; }
        .section-title { color: #ff4b4b; }
        .section-description { color: #666666; }
        .footer { color: #666666; border-top: 1px solid #dddddd; }
    }

    /* Dark mode */
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
st.markdown('<div class="subtitle">Analiza e interesit për Historinë, Artin dhe Letërsinë në Wikipedia</div>', unsafe_allow_html=True)

# Lidhemi me bazën e të dhënave
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

# Menu në anën e majtë
st.sidebar.header("Filtra")

# Zgjedhja e kategorisë
kategoria = st.sidebar.selectbox(
    "Zgjidh kategorinë:",
    ["Të gjitha", "Histori", "Art", "Letërsi"]
)

# Ndarja e eventeve sipas kategorive
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

# Zgjedhja e viteve
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
    title="Totali i Vizitave (2015-2025)",
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
    title="Evolucioni i Vizitave (2015-2025)",
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

# =====================================================
# Footer
# =====================================================
st.markdown(
    '<div class="footer">'
    'Burimi i të dhënave: Wikipedia Pageviews API'
    '</div>',
    unsafe_allow_html=True
)