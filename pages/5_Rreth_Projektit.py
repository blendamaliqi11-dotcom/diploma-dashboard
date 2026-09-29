import streamlit as st
import os
from utils import aplikon_stilizim, shfaq_footer, shfaq_titull

st.set_page_config(
    page_title="Rreth Projektit - Memoria Kolektive Digjitale",
    layout="wide"
)

aplikon_stilizim()

shfaq_titull(
    "Rreth Projektit",
    "Konteksti, metodologjia dhe burimet e studimit"
)

# =====================================================
# QËLLIMI I STUDIMIT
# =====================================================
st.markdown('<div class="section-title">Qëllimi i Studimit</div>', unsafe_allow_html=True)

st.markdown("""
Ky studim analizon **interesin publik për trashëgiminë kulturore** përmes të dhënave 
digjitale nga platformat online. Pyetja qendrore është:

> *A ndryshon interesi për historinë, artin dhe letërsinë ndër vite, dhe a mund të 
> parashikohet ai për të ardhmen?*

Studimi integron tre burime të pavarura të dhënash për të krijuar një pamje të plotë 
të sjelljes kulturore në epokën digjitale.
""")

# =====================================================
# BURIMET E TË DHËNAVE
# =====================================================
st.markdown('<div class="section-title">Burimet e të Dhënave</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Wikipedia")
    st.markdown("""
    - Vizita në artikuj enciklopedikë
    - 18 entitete, 5 gjuhë
    - Periudha: 2015-2025
    """)

with col2:
    st.markdown("### Google Trends")
    st.markdown("""
    - Vëllimi i kërkimeve online
    - 18 terma kulturorë
    - Vlera relative (0-100)
    """)

with col3:
    st.markdown("### Goodreads")
    st.markdown("""
    - Vlerësime librash
    - 7 vepra klasike
    - Numri i lexuesve
    """)

# =====================================================
# ARKITEKTURA E SISTEMIT
# =====================================================
st.markdown('<div class="section-title">Arkitektura e Sistemit</div>', unsafe_allow_html=True)

st.markdown("""
Sistemi është ndërtuar në **tre shtresa kryesore**:

1. **Mbledhja e të Dhënave** — Përmes API-ve të Wikipedia-s dhe Google Trends
2. **Përpunimi dhe Ruajtja** — Në një bazë të dhënash SQLite
3. **Analiza dhe Prezantimi** — Analiza SQL, Machine Learning, dhe Dashboard interaktiv
""")

# =====================================================
# ZBULIMI I TEMËS DHE SHFAQJA E DIAGRAMIT
# =====================================================
tema = st.get_option("theme.base") or "light"

# Zgjedhim imazhin sipas temës (skedarët në GitHub kanë pikë, jo nënvizë)
if tema == "dark":
    imazhi = "arkitektura.dark.png"
    imazhi_fallback = "arkitektura_dark.png"
else:
    imazhi = "arkitektura.light.png"
    imazhi_fallback = "arkitektura_light.png"

# Shfaqim diagramin e arkitekturës (i zvogëluar dhe i centruar)
col_l, col_m, col_r = st.columns([1, 2, 1])

with col_m:
    if os.path.exists(imazhi):
        st.image(imazhi, use_container_width=True)
    elif os.path.exists(imazhi_fallback):
        st.image(imazhi_fallback, use_container_width=True)
    elif os.path.exists("arkitektura.dark.png"):
        st.image("arkitektura.dark.png", use_container_width=True)
    elif os.path.exists("arkitektura.light.png"):
        st.image("arkitektura.light.png", use_container_width=True)
    elif os.path.exists("arkitektura_dark.png"):
        st.image("arkitektura_dark.png", use_container_width=True)
    elif os.path.exists("arkitektura_light.png"):
        st.image("arkitektura_light.png", use_container_width=True)
    else:
        st.warning("Diagrami i arkitekturës nuk u gjet në dosjen kryesore.")

# =====================================================
# METODOLOGJIA (E SHKURTUAR)
# =====================================================
st.markdown('<div class="section-title">Metodologjia</div>', unsafe_allow_html=True)

st.markdown("""
Studimi u zhvillua në **pesë faza**: mbledhja e të dhënave, organizimi në bazë të dhënash, 
analiza përshkruese, analiza inferenciale dhe parashikimi me modele të mësimit të makinerisë.
""")

# =====================================================
# KUFIZIMET E STUDIMIT
# =====================================================
st.markdown('<div class="section-title">Kufizimet e Studimit</div>', unsafe_allow_html=True)

st.markdown("""
- **Wikipedia** mat vetëm lexuesit e enciklopedisë, jo interesin e gjerë kulturor
- **Google Trends** jep vlera relative, jo volume absolute
- **Korrelacione, jo kauzalitet** — nuk mund të provohen marrëdhënie shkakësore
- **Mbulimi gjeografik** i kufizuar për vende me popullsi të vogël
- **Goodreads** tregon vlerësimet, jo aktin e leximit
""")

shfaq_footer()
