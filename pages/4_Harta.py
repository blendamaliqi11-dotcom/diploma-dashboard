import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import urllib.request
from utils import (
    aplikon_stilizim, shfaq_footer, shfaq_titull,
    EMRAT_SHQIP, lexo_te_dhenat
)

st.set_page_config(
    page_title="Harta Botërore - Memoria Kolektive Digjitale",
    layout="wide"
)

aplikon_stilizim()

shfaq_titull(
    "Harta Botërore",
    "Shpërndarja gjeografike e interesit për kulturën sipas gjuhëve"
)


@st.cache_data
def lexo_gjuhet():
    if os.path.exists("vizitat_gjuhet.csv"):
        return pd.read_csv("vizitat_gjuhet.csv")
    return None


@st.cache_data
def lexo_geojson():
    """Lexon ose shkarkon GeoJSON-in e botës me Kosovën e përfshirë."""
    GEOJSON_FILE = "world_countries.geojson"
    GEOJSON_URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson"
    
    # Shkarko skedarin nëse nuk ekziston
    if not os.path.exists(GEOJSON_FILE):
        try:
            with urllib.request.urlopen(GEOJSON_URL, timeout=60) as response:
                with open(GEOJSON_FILE, "wb") as f:
                    f.write(response.read())
        except Exception as e:
            return None
    
    # Lexo skedarin
    try:
        with open(GEOJSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


df_gjuhet = lexo_gjuhet()
df_wiki = lexo_te_dhenat()
world_geojson = lexo_geojson()

if df_gjuhet is None:
    st.error("Skedari 'vizitat_gjuhet.csv' nuk u gjet.")
elif world_geojson is None:
    st.error("Nuk u mund të ngarkohej harta botërore. Kontrollo lidhjen e internetit.")
else:
    GJUHA_VENDE = {
        "en": [("United States of America", 1.0), ("United Kingdom", 0.6), 
               ("Canada", 0.4), ("Australia", 0.3)],
        "sq": [("Albania", 1.0), ("Kosovo", 1.0)],
        "de": [("Germany", 1.0), ("Austria", 0.4), ("Switzerland", 0.3)],
        "fr": [("France", 1.0), ("Belgium", 0.25)],
        "it": [("Italy", 1.0)]
    }

    emrat_shqip = {
        "United States of America": "Shtetet e Bashkuara",
        "United Kingdom": "Mbretëria e Bashkuar",
        "Canada": "Kanada",
        "Australia": "Australia",
        "Albania": "Shqipëria",
        "Kosovo": "Kosova",
        "Germany": "Gjermania",
        "Austria": "Austria",
        "Switzerland": "Zvicra",
        "France": "Franca",
        "Belgium": "Belgjika",
        "Italy": "Italia"
    }

    # FILTRAT
    st.sidebar.header("Filtra")

    eventet_te_gjitha = sorted(df_wiki["eventi"].unique())
    emrat_eventeve = [EMRAT_SHQIP.get(e, e) for e in eventet_te_gjitha]

    entiteti_shfaqur = st.sidebar.selectbox(
        "Zgjidh entitetin:",
        ["Të gjitha"] + emrat_eventeve
    )

    emri_reverse = {EMRAT_SHQIP.get(e, e): e for e in eventet_te_gjitha}

    # PËRGATITJA E TË DHËNAVE
    if entiteti_shfaqur == "Të gjitha":
        df_f = df_gjuhet
        emri_titull = "Të gjitha entitetet"
    else:
        entiteti_teknik = emri_reverse[entiteti_shfaqur]
        df_f = df_gjuhet[df_gjuhet["eventi"] == entiteti_teknik]
        emri_titull = entiteti_shfaqur

    if len(df_f) == 0:
        st.warning(
            f"Për entitetin **{emri_titull}** nuk ka të dhëna gjeografike. "
            f"Provo një entitet tjetër ose 'Të gjitha'."
        )
    else:
        totali_gjuha = df_f.groupby("gjuha")["vizita"].sum().to_dict()

        te_dhenat = []
        for gjuha, vende in GJUHA_VENDE.items():
            vizita_total = totali_gjuha.get(gjuha, 0)
            if vizita_total == 0:
                continue
            for emri_anglisht, pesha in vende:
                te_dhenat.append({
                    "Shteti": emri_anglisht,
                    "Emri": emrat_shqip[emri_anglisht],
                    "Vizita": int(vizita_total * pesha)
                })

        df_harta = pd.DataFrame(te_dhenat)
        df_harta = df_harta.groupby(
            ["Shteti", "Emri"], as_index=False
        )["Vizita"].sum()

        # SEKSIONI 1: Harta Choropleth
        st.markdown('<div class="section-title">Shpërndarja Gjeografike</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="section-description">Harta tregon intensitetin e interesit për "{emri_titull}" '
            f'sipas vendeve. Ngjyra më e errët tregon më shumë vizita.</div>',
            unsafe_allow_html=True
        )

        fig = px.choropleth(
            df_harta,
            geojson=world_geojson,
            locations="Shteti",
            featureidkey="properties.ADMIN",
            color="Vizita",
            color_continuous_scale=[
                [0, "rgba(229, 72, 77, 0.1)"],
                [0.3, "rgba(229, 72, 77, 0.4)"],
                [0.6, "rgba(229, 72, 77, 0.7)"],
                [1, "rgba(229, 72, 77, 1)"]
            ],
            labels={"Vizita": "Vizita", "Shteti": "Shteti"},
            hover_name="Emri"
        )

        fig.update_layout(
            height=300,
            template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white",
            font=dict(family="Arial", size=12),
            geo=dict(
                showframe=False,
                showcoastlines=True,
                showland=True,
                landcolor="rgba(128, 128, 128, 0.05)",
                countrycolor="rgba(128, 128, 128, 0.3)",
                coastlinecolor="rgba(128, 128, 128, 0.5)",
                projection_type="equirectangular",
                showcountries=True,
                lataxis=dict(range=[-60, 85]),
                lonaxis=dict(range=[-170, 180])
            ),
            margin=dict(l=0, r=0, t=10, b=0),
            coloraxis_colorbar=dict(
                title="Vizita",
                thickness=15,
                len=0.7,
                x=1.02
            ),
            autosize=True
        )

        st.plotly_chart(fig, use_container_width=True)

        # SEKSIONI 2: Tabela
        st.markdown('<div class="section-title">Tabela e Detajeve</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-description">Renditja e vendeve sipas numrit total të vizitave.</div>',
            unsafe_allow_html=True
        )

        df_shfaqur = df_harta[["Emri", "Vizita"]].sort_values("Vizita", ascending=False).copy()
        df_shfaqur["Përqindja (%)"] = (df_shfaqur["Vizita"] / df_shfaqur["Vizita"].sum() * 100).round(1)
        df_shfaqur.columns = ["Shteti", "Vizita Totale", "Përqindja (%)"]

        st.dataframe(df_shfaqur, use_container_width=True, hide_index=True)

    # SEKSIONI 3: Shpjegim
    st.markdown('<div class="section-title">Shpjegim Metodologjik</div>', unsafe_allow_html=True)
    st.markdown("""
    Të dhënat gjeografike janë deduktuar nga **gjuha e lexuesve** në Wikipedia. 
    Për secilën gjuhë, vizitat u shpërndanë në vendet kryesore ku ajo gjuhë flitet:

    - **Anglisht (en):** SHBA, Mbretëria e Bashkuar, Kanada, Australi
    - **Shqip (sq):** Shqipëri, Kosovë
    - **Gjermanisht (de):** Gjermani, Austri, Zvicër
    - **Frëngjisht (fr):** Francë, Belgjikë
    - **Italisht (it):** Itali
    """)

shfaq_footer()
