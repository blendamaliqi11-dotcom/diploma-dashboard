import streamlit as st
import os
from utils import (
    aplikon_stilizim, shfaq_footer, shfaq_titull,
    merr_fotot, EMRAT_SHQIP, HISTORI, ART, LETERSI
)

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
# ENTITETET E STUDIUARA (FOTO)
# =====================================================
st.markdown('<div class="section-title">Entitetet e Studiuara</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-description">'
    '</div>',
    unsafe_allow_html=True
)

# Marrim të gjitha fotot njëherësh (me cache)
te_gjitha_eventet = HISTORI + ART + LETERSI

with st.spinner("Duke ngarkuar fotot nga Wikipedia..."):
    FOTOT = merr_fotot(te_gjitha_eventet)


def shfaq_kategorine(emri, eventet):
    """Shfaq një kategori me 6 foto në 2 rreshta x 3 kolona (madhësi uniforme)."""
    st.markdown(f"### {emri}")
    
    # 2 rreshta x 3 kolona = 6 foto
    for rreshti in range(2):
        cols = st.columns(3)
        for i, kolona in enumerate(cols):
            idx = rreshti * 3 + i
            if idx >= len(eventet):
                break
            
            eventi = eventet[idx]
            emri_shqip = EMRAT_SHQIP.get(eventi, eventi)
            
            with kolona:
                if eventi in FOTOT:
                    # Foto me dimensione fikse + object-fit cover
                    st.markdown(
                        f'<div style="width: 100%; height: 160px; overflow: hidden; '
                        f'border-radius: 8px; background: rgba(128,128,128,0.1);">'
                        f'<img src="{FOTOT[eventi]}" '
                        f'style="width: 100%; height: 100%; object-fit: cover; '
                        f'display: block;" />'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                else:
                    # Fallback nëse nuk ka foto
                    st.markdown(
                        '<div style="height: 160px; display: flex; align-items: center; '
                        'justify-content: center; background: rgba(128,128,128,0.1); '
                        'border-radius: 8px; font-size: 14px; opacity: 0.7;">'
                        f'{emri_shqip}</div>',
                        unsafe_allow_html=True
                    )
                
                # Emri poshtë fotos
                st.markdown(
                    f'<div style="text-align: center; margin-top: 8px; '
                    f'font-size: 13px; font-weight: 500;">{emri_shqip}</div>',
                    unsafe_allow_html=True
                )

    st.markdown("<br>", unsafe_allow_html=True)


# Shfaqim 3 kategoritë
shfaq_kategorine("Historia", HISTORI)
shfaq_kategorine("Arti", ART)
shfaq_kategorine("Letërsia", LETERSI)

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



col_l, col_m, col_r = st.columns([1, 2, 1])

with col_m:
    if os.path.exists("arkitektura.light.png"):
        st.image("arkitektura.light.png", use_container_width=True)
    elif os.path.exists("arkitektura.dark.png"):
        st.image("arkitektura.dark.png", use_container_width=True)
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
