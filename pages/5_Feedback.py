import streamlit as st
import requests
from datetime import datetime
from utils import aplikon_stilizim, shfaq_footer, shfaq_titull

st.set_page_config(
    page_title="Feedback - Memoria Kolektive Digjitale",
    layout="wide"
)

aplikon_stilizim()

shfaq_titull(
    "Feedback",
    "Vlerësoni dashboard-in dhe ndihmoni në përmirësimin e projektit"
)

# URL-ja e Google Apps Script
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyEFaz7iz797Wik_ScwyJH_9MFYyDyPl_ZZ9ozAh-NSgAJQy960TdgqH2rRbklCGlDh5A/exec"

# =====================================================
# HYRJE
# =====================================================
st.markdown("""
Dashboard-i që sapo eksploruat është pjesë e një punimi diplome. 
Vlerësimi juaj është shumë i vlefshëm për të kuptuar pikat e forta dhe 
ato që mund të përmirësohen. Formulari zgjat vetëm 2 minuta.
""")

# =====================================================
# FORMULARI
# =====================================================
st.markdown('<div class="section-title">Vlerësoni Dashboard-in</div>', unsafe_allow_html=True)

with st.form("feedback_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        navigimi = st.slider("Sa i lehtë ishte navigimi?", 1, 5, 3)
        qartesia = st.slider("Sa e qartë ishte përmbajtja?", 1, 5, 3)
        dizajni = st.slider("Sa profesional ishte dizajni?", 1, 5, 3)
    
    with col2:
        grafiket = st.slider("Sa të dobishme ishin grafikët?", 1, 5, 3)
        rekomandimi = st.radio(
            "A do ta rekomandonit?",
            ["Po", "Ndoshta", "Jo"]
        )
        faqja_preferuar = st.selectbox(
            "Cila faqe ju pëlqeu më shumë?",
            ["Dashboard", "Wikipedia", "Google Trends", "Machine Learning", "Rreth Projektit"]
        )
    
    sugjerime = st.text_area(
        "Sugjerime për përmirësim (opsionale):",
        placeholder="Shkruani këtu çdo koment ose sugjerim..."
    )
    
    dergo = st.form_submit_button("Dërgo Vlerësimin", use_container_width=True)

# =====================================================
# DËRGIMI I TË DHËNAVE
# =====================================================
if dergo:
    te_dhenat = {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "navigimi": navigimi,
        "qartesia": qartesia,
        "dizajni": dizajni,
        "faqja_preferuar": faqja_preferuar,
        "grafiket": grafiket,
        "rekomandimi": rekomandimi,
        "sugjerime": sugjerime
    }
    
    try:
        response = requests.post(
            GOOGLE_SCRIPT_URL,
            json=te_dhenat,
            timeout=10
        )
        
        if response.status_code == 200:
            st.success("Faleminderit për vlerësimin! Përgjigja u ruajt me sukses.")
            st.markdown("""
                <div style="padding: 15px 20px; border-radius: 8px; 
                            border-left: 3px solid #E5484D; margin-top: 15px;
                            background-color: rgba(128, 128, 128, 0.1);">
                    <b>Vlerësimi juaj është regjistruar.</b><br>
                    Faleminderit që kontribuat në përmirësimin e këtij projekti.
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Ndodhi një problem. Ju lutem provoni përsëri.")
    except Exception as e:
        st.error(f"Gabim gjatë dërgimit: {e}")
        st.info("Përgjigja juaj mund të mos jetë ruajtur. Provoni përsëri.")

# =====================================================
# Footer
# =====================================================
shfaq_footer()
