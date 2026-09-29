"""
utils.py - Funksione të përbashkëta për të gjitha faqet e dashboard-it
======================================================================
"""

import streamlit as st
import pandas as pd
import sqlite3
import os


# ============================================================
# STILIZIM CSS
# ============================================================

def aplikon_stilizim():
    """Aplikon stilizimin CSS të përbashkët për të gjitha faqet."""
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
            border-bottom: 2px solid #E5484D;
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
        .info-box {
            padding: 15px 20px;
            border-radius: 8px;
            margin: 15px 0;
        }

        @media (prefers-color-scheme: light) {
            .subtitle { color: #555555; }
            .section-title { color: #E5484D; }
            .section-description { color: #666666; }
            .footer { color: #666666; border-top: 1px solid #dddddd; }
            .info-box { background-color: #f0f2f6; color: #262730; }
        }
        @media (prefers-color-scheme: dark) {
            .subtitle { color: #cccccc; }
            .section-title { color: #E5484D; }
            .section-description { color: #b0b0b0; }
            .footer { color: #aaaaaa; border-top: 1px solid #333333; }
            .info-box { background-color: #1e1e1e; color: #fafafa; }
        }
        </style>
    """, unsafe_allow_html=True)


# ============================================================
# FJALORI I EMRave NË SHQIP
# ============================================================

EMRAT_SHQIP = {
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


# ============================================================
# KATEGORITË
# ============================================================

HISTORI = ["World_War_II", "The_Holocaust", "Kosovo_War", "Berlin_Wall",
           "September_11_attacks", "2008_Kosovo_declaration_of_independence"]

ART = ["Mona_Lisa", "The_Starry_Night", "Vincent_van_Gogh", "Leonardo_da_Vinci",
       "Guernica_(Picasso)", "The_Persistence_of_Memory"]

LETERSI = ["Jane_Austen", "Pride_and_Prejudice", "Franz_Kafka", "The_Metamorphosis",
           "Mark_Twain", "Arthur_Rimbaud"]


# ============================================================
# LEXIMI I TË DHËNAVE
# ============================================================

@st.cache_data
def lexo_te_dhenat():
    """Lexon të dhënat nga baza e të dhënave SQLite."""
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
    df["Emri"] = df["eventi"].map(EMRAT_SHQIP).fillna(df["eventi"])
    return df


@st.cache_data
def lexo_trends(skedari):
    """Lexon një skedar CSV nga Google Trends."""
    if os.path.exists(skedari):
        df_t = pd.read_csv(skedari)
        df_t["Time"] = pd.to_datetime(df_t["Time"])
        return df_t
    return None


@st.cache_data
def lexo_ml(skedari):
    """Lexon një skedar CSV nga ML."""
    if os.path.exists(skedari):
        return pd.read_csv(skedari)
    return None


# ============================================================
# FILTRIMI
# ============================================================

def filtro_sipas_kategorise(df, kategoria):
    """Filtron DataFrame sipas kategorisë së zgjedhur."""
    if kategoria == "Histori":
        return df[df["eventi"].isin(HISTORI)]
    elif kategoria == "Art":
        return df[df["eventi"].isin(ART)]
    elif kategoria == "Letërsi":
        return df[df["eventi"].isin(LETERSI)]
    return df


# ============================================================
# FOOTER
# ============================================================

def shfaq_footer():
    """Shfaq footer-in standard."""
    st.markdown(
        '<div class="footer">'
        'Burimi i të dhënave: Wikipedia Pageviews API, Google Trends & Machine Learning (ARIMA)'
        '</div>',
        unsafe_allow_html=True
    )


def shfaq_titull(kryesori, nentitulli):
    """Shfaq titullin dhe nëntitullin e një faqeje."""
    st.title(kryesori)
    st.markdown(f'<div class="subtitle">{nentitulli}</div>', unsafe_allow_html=True)
