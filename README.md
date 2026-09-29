# Memoria Kolektive Digjitale

**Analiza e interesit publik për historinë, artin dhe letërsinë përmes të dhënave digjitale (2015-2025)**

[![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.64-red?logo=streamlit&logoColor=white)](https://streamlit.io/)

🔗 **Demo Live:** [diploma-memoria-kolektive.streamlit.app](https://diploma-memoria-kolektive.streamlit.app)

---

## Përshkrimi i Projektit

Ky projekt është zhvilluar si pjesë e një **punimi diplome në Shkenca Kompjuterike**. Ai analizon interesin publik për trashëgiminë kulturore përmes dy burimeve të pavarura të dhënash dhe aplikon teknika të avancuara të **Machine Learning** për parashikimin e trendeve të ardhshme.

### Pyetja Qendrore Kërkimore

> *A ndryshon interesi publik për trashëgiminë kulturore ndër vite, dhe a mund të parashikohet ky interes për periudhat e ardhshme?*

---

## Veçoritë Kryesore

- **Analiza e Wikipedia-s** — Evolucioni i vizitave për 18 entitete kulturore (2015-2025)
- **Google Trends** — Krahasimi i kërkimeve online për 18 terma kulturorë
- **Machine Learning** — Parashikimi i vizitave për 2026 me ARIMA dhe Linear Regression
- **Harta Botërore** — Shpërndarja gjeografike e interesit sipas gjuhëve
- **Analiza Statistikore** — Korrelacione, teste t, dhe statistika përshkruese
- **Analiza e Rrjetit** — Lidhjet mes temave kulturore në Wikipedia
- **Dashboard Interaktiv** — Ndërfaqe multi-page me filtra dinamikë
- **Sistem Feedback** — Mbledhje automatike e vlerësimeve në Google Sheets

---

## Arkitektura e Sistemit

<p align="center">
  <img src="https://raw.githubusercontent.com/blendamaliqi11-dotcom/diploma-dashboard/main/arkitektura.dark.png" alt="Arkitektura e Sistemit" width="400">
</p>


## Teknologjitë e Përdorura

| Kategoria | Teknologjitë |
|-----------|--------------|
| **Gjuha** | Python 3.13 |
| **Data Science** | Pandas, NumPy, SciPy, Scikit-learn, statsmodels |
| **Vizualizimi** | Plotly, Streamlit |
| **Baza e Dhënave** | SQLite |
| **Machine Learning** | ARIMA, Linear Regression |
| **Deployment** | Streamlit Cloud, GitHub |

---

## Të Dhënat

### Burimet

1. **Wikipedia Pageviews API** — Vizita ditore në artikuj enciklopedikë (2015-2025)
2. **Google Trends** — Vëllimi i kërkimeve online (2015-2025)
3. **Goodreads** — Vlerësime dhe lexueshmëri librash

### Entitetet e Studiuara (18 total)

**Historia (6):** Lufta e Dytë Botërore, Holokausti, Lufta e Kosovës, Muri i Berlinit, Sulmet e 11 Shtatorit, Pavarësia e Kosovës (2008)

**Arti (6):** Mona Lisa, Ylli i Natës, Vincent van Gogh, Leonardo da Vinci, Guernica, Këmbëngulja e Kujtesës

**Letërsia (6):** Jane Austen, Krenari dhe Paragjykim, Franz Kafka, Metamorfoza, Mark Twain, Arthur Rimbaud

---


## Instalimi

    git clone https://github.com/blendamaliqi11-dotcom/diploma-dashboard.git
    cd diploma-dashboard
    pip install -r requirements.txt
    streamlit run dashboard.py

---

## Rezultatet Kryesore

- **15 nga 18 entitete** kanë trend rritës statistikisht sinjifikant (r > 0.5, p < 0.05)
- **ARIMA është superior** për 6 entitete, Linear Regression për 3, pa dallim për 9
- **Lufta e Dytë Botërore** ka 168 milionë vizita totale në Wikipedia
- **Leonardo da Vinci** parashikohet të rritet +21% në 2026
- **Anglishtja dominon** Wikipedia-n, por shqipja është dominante për "Luftën e Kosovës"

---

## Kufizimet e Studimit

- Të dhënat e Wikipedia-s reflektojnë vetëm vizitat në artikuj enciklopedikë
- Google Trends jep vlera relative (0-100), jo volume absolute
- **Korrelacione, jo kauzalitet** — nuk mund të provohen marrëdhënie shkakësore
- Mbulimi gjeografik i kufizuar për vende me popullsi të vogël
- Të dhënat gjeografike janë deduktuar nga gjuha e lexuesve
---

## Testimi

Projekti përfshin **15 unit tests** me pytest për të verifikuar funksionet kryesore:

    pytest test_utils.py -v

Të gjitha testet kaluan me sukses.

---

## Autori

**Blenda Maliqi**
Punim diplome — Bachelor në Shkenca Kompjuterike
2025-2026

Gmail: [blendamaliqi11@gmail.com](mailto:blendamaliqi11@gmail.com)

---

## Licensa

Ky projekt është krijuar për qëllime akademike. Të gjitha të dhënat janë marrë nga burime publike.

---


⭐ Nëse ju pëlqeu ky projekt, mos harroni t'i jepni një yll në GitHub!
