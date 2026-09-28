import streamlit as st
from utils import aplikon_stilizim, lexo_te_dhenat, shfaq_footer

# Konfigurimi i faqes
st.set_page_config(
    page_title="Memoria Kolektive Digjitale",
    layout="wide",
    initial_sidebar_state="expanded"
)

aplikon_stilizim()

# =====================================================
# STILIZIM I VEÇANTË PËR FAQEN KRYESORE
# =====================================================
st.markdown("""
    <style>
    /* Hero Section */
    .hero {
        padding: 50px 40px;
        border-radius: 12px;
        margin-bottom: 40px;
        text-align: center;
        border: 1px solid rgba(128, 128, 128, 0.3);
    }
    .hero-title {
        font-size: 42px;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
        line-height: 1.15;
    }
    .hero-subtitle {
        font-size: 17px;
        margin-top: 18px;
        font-weight: 400;
        max-width: 780px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.7;
        opacity: 0.8;
    }

    /* Stats Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 18px;
        margin: 40px 0;
    }
    .stat-card {
        padding: 26px 22px;
        border-radius: 10px;
        transition: all 0.25s ease;
        border-left: 3px solid #A0A0A0;
    }
    .stat-card:hover {
        transform: translateY(-3px);
    }
    .stat-value {
        font-size: 34px;
        font-weight: 700;
        margin: 0;
        line-height: 1;
    }
    .stat-label {
        font-size: 12px;
        margin-top: 10px;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 500;
        opacity: 0.7;
    }

    /* Info Box */
    .info-box {
        padding: 28px 32px;
        border-radius: 10px;
        margin: 25px 0;
        border-left: 3px solid #A0A0A0;
    }
    .info-box h3 {
        margin-top: 0;
        font-size: 17px;
        font-weight: 600;
    }
    .info-box p {
        line-height: 1.75;
        font-size: 15px;
        margin-bottom: 0;
    }

    /* Feature List */
    .feature-list {
        list-style: none;
        padding: 0;
        margin: 12px 0 0 0;
    }
    .feature-list li {
        padding: 10px 0;
        font-size: 15px;
        line-height: 1.6;
    }

    /* Responsive */
    @media (max-width: 900px) {
        .stats-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        .hero-title {
            font-size: 30px;
        }
        .hero {
            padding: 35px 20px;
        }
    }

    /* ============================================
       LIGHT MODE
       ============================================ */
    @media (prefers-color-scheme: light) {
        .hero {
            background-color: #252525 !important;
        }
        .hero-title {
            color: #f5f5f5 !important;
        }
        .hero-subtitle {
            color: #c0c0c0 !important;
        }
        .stat-card {
            background-color: #252525 !important;
            border-top: 1px solid #333333 !important;
            border-right: 1px solid #333333 !important;
            border-bottom: 1px solid #333333 !important;
        }
        .stat-value {
            color: #f5f5f5 !important;
        }
        .stat-label {
            color: #a0a0a0 !important;
        }
        .info-box {
            background-color: #252525 !important;
            border-top: 1px solid #333333 !important;
            border-right: 1px solid #333333 !important;
            border-bottom: 1px solid #333333 !important;
        }
        .info-box h3 {
            color: #f5f5f5 !important;
        }
        .info-box p {
            color: #c0c0c0 !important;
        }
        .info-box b {
            color: #f5f5f5 !important;
        }
        .feature-list li {
            color: #c0c0c0 !important;
        }
    }

    /* ============================================
       DARK MODE
       ============================================ */
    @media (prefers-color-scheme: dark) {
        .hero {
            background-color: #252525 !important;
        }
        .hero-title {
            color: #f5f5f5 !important;
        }
        .hero-subtitle {
            color: #b0b0b0 !important;
        }
        .stat-card {
            background-color: #252525 !important;
            border-top: 1px solid #333333 !important;
            border-right: 1px solid #333333 !important;
            border-bottom: 1px solid #333333 !important;
        }
        .stat-value {
            color: #f5f5f5 !important;
        }
        .stat-label {
            color: #a0a0a0 !important;
        }
        .info-box {
            background-color: #252525 !important;
            border-top: 1px solid #333333 !important;
            border-right: 1px solid #333333 !important;
            border-bottom: 1px solid #333333 !important;
        }
        .info-box h3 {
            color: #f5f5f5 !important;
        }
        .info-box p {
            color: #b0b0b0 !important;
        }
        .info-box b {
            color: #f5f5f5 !important;
        }
        .feature-list li {
            color: #b0b0b0 !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================
# HERO SECTION
# =====================================================
st.markdown("""
    <div class="hero">
        <h1 class="hero-title">Memoria Kolektive Digjitale</h1>
        <p class="hero-subtitle">
            Një analizë e thellë e interesit publik për historinë, artin dhe letërsinë 
            përmes të dhënave nga Wikipedia, Google Trends dhe modeleve parashikuese.
        </p>
    </div>
""", unsafe_allow_html=True)

# =====================================================
# STATS CARDS
# =====================================================
df = lexo_te_dhenat()
total_vizita = df["total_vizita"].sum()

st.markdown(f"""
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-value">18</div>
            <div class="stat-label">Entitete Kulturore</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">11</div>
            <div class="stat-label">Vite Studimi</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{total_vizita/1_000_000:.0f}M</div>
            <div class="stat-label">Vizita Totale</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">5</div>
            <div class="stat-label">Faza Kërkimore</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# =====================================================
# INFORMACIONI KRYESOR
# =====================================================
st.markdown('<div class="section-title">Çfarë Eksploron Ky Studim</div>', unsafe_allow_html=True)

st.markdown("""
    <div class="info-box">
        <h3>Një pamje e re mbi sjelljen kulturore</h3>
        <p>
            Ky dashboard kombinon dy burime të pavarura të dhënash për të kuptuar se si 
            njerëzit ndërveprojnë me trashëgiminë kulturore në epokën digjitale. Përmes 
            analizës së miliona vizitave dhe kërkimeve, zbulohen modele që reflektojnë 
            memorien kolektive të shoqërisë.
        </p>
    </div>
""", unsafe_allow_html=True)

# =====================================================
# KATEGORITË
# =====================================================
st.markdown('<div class="section-title">Tre Fushat e Studimit</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="info-box">
            <h3>Historia</h3>
            <p>
                Nga Lufta e Dytë Botërore te Pavarësia e Kosovës. Analiza e eventeve 
                që kanë formësuar identitetin kolektiv.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="info-box">
            <h3>Arti</h3>
            <p>
                Nga Mona Lisa te Ylli i Natës. Studimi i interesit për veprat 
                dhe artistët që kanë përcaktuar estetikën botërore.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="info-box">
            <h3>Letërsia</h3>
            <p>
                Nga Franz Kafka te Jane Austen. Eksplorimi i interesit për autorët 
                dhe veprat që kanë formësuar mendimin njerëzor.
            </p>
        </div>
    """, unsafe_allow_html=True)

# =====================================================
# ÇFARË DO TË GJEJË PËRDORUESI
# =====================================================
st.markdown('<div class="section-title">Çfarë Do të Gjeni Te Ky Dashboard</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="info-box">
            <h3>Analiza e të Dhënave</h3>
            <ul class="feature-list">
                <li><b>Wikipedia Analytics</b> — Evolucioni i vizitave ndër vite</li>
                <li><b>Google Trends</b> — Krahasimi i kërkimeve online</li>
                <li><b>Statistika Përshkruese</b> — Treguesit kryesorë për secilin entitet</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="info-box">
            <h3>Modele Parashikuese</h3>
            <ul class="feature-list">
                <li><b>Machine Learning</b> — Parashikimi i vizitave për 2026</li>
                <li><b>ARIMA vs Linear Regression</b> — Krahasimi i saktësisë</li>
                <li><b>Gjetjet Kryesore</b> — Konkluzione dhe interpretime</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# =====================================================
# NAVIGIMI
# =====================================================
st.markdown('<div class="section-title">Filloni Eksplorimin</div>', unsafe_allow_html=True)

st.markdown("""
    <div class="info-box">
        <h3>Navigimi</h3>
        <p>
            Përdorni menunë në anën e majtë për të eksploruar secilën pjesë të studimit. 
            Çdo faqe ofron filtra interaktivë që ju mundësojnë të personalizoni analizën 
            sipas kategorisë dhe periudhës kohore.
        </p>
    </div>
""", unsafe_allow_html=True)

# Footer
shfaq_footer()
