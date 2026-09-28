import streamlit as st
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
# METODOLOGJIA
# =====================================================
st.markdown('<div class="section-title">Metodologjia</div>', unsafe_allow_html=True)

st.markdown("""
Studimi u zhvillua në **pesë faza**:

1. **Mbledhja** e të dhënave përmes API-ve dhe burimeve publike
2. **Organizimi** në një bazë të dhënash të centralizuar
3. **Analiza përshkruese** — mesatarja, mediana, devijimi standard
4. **Analiza inferenciale** — korrelacione dhe teste statistikore
5. **Parashikimi** me modele të mësimit të makinerisë
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

# =====================================================
# KONTRIBUTI
# =====================================================
st.markdown('<div class="section-title">Kontributi i Pritur</div>', unsafe_allow_html=True)

st.markdown("""
- Metodologji e **përsëritshme** për analizën e interesit kulturor
- Një **mjet interaktiv** për studiues dhe institucione kulturore
- Testim i **modeleve parashikuese** për seri kohore kulturore
- Theksim i **kontekstit gjuhësor** në interpretimin e të dhënave globale
""")

shfaq_footer()
