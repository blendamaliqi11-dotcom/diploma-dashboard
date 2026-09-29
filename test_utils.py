"""
test_utils.py - Unit tests për funksionet e utils.py
=====================================================
Teston nëse funksionet kryesore punojnë saktë.
Ekzekutimi: pytest test_utils.py -v
"""

import pytest
import pandas as pd
import os
from utils import (
    lexo_te_dhenat, lexo_trends, lexo_ml, filtro_sipas_kategorise,
    HISTORI, ART, LETERSI
)


# ============================================================
# TESTET PËR lexo_te_dhenat()
# ============================================================

def test_lexo_te_dhenat_kthen_dataframe():
    """Kontrollon nëse lexo_te_dhenat() kthen një DataFrame."""
    df = lexo_te_dhenat()
    assert isinstance(df, pd.DataFrame)


def test_lexo_te_dhenat_ka_18_entitete():
    """Kontrollon nëse ka saktësisht 18 entitete."""
    df = lexo_te_dhenat()
    numri = df["eventi"].nunique()
    assert numri == 18, f"Pritej 18, u gjet {numri}"


def test_lexo_te_dhenat_ka_vite_2015_2025():
    """Kontrollon nëse periudha është 2015-2025."""
    df = lexo_te_dhenat()
    vitet = sorted(df["viti"].unique())
    assert vitet[0] == 2015
    assert vitet[-1] == 2025


def test_lexo_te_dhenat_ka_kolonat_e_duhura():
    """Kontrollon nëse kolonat kryesore ekzistojnë."""
    df = lexo_te_dhenat()
    for kolona in ["eventi", "viti", "total_vizita", "Emri"]:
        assert kolona in df.columns, f"Mungon kolona: {kolona}"


# ============================================================
# TESTET PËR filtro_sipas_kategorise()
# ============================================================

def test_filtro_histori():
    """Kontrollon filtrimin e historisë."""
    df = lexo_te_dhenat()
    rezultati = filtro_sipas_kategorise(df, "Histori")
    
    entitetet = rezultati["eventi"].unique()
    assert len(entitetet) == 6, f"Pritej 6 entitete historike"
    for e in entitetet:
        assert e in HISTORI, f"{e} nuk i përket Historisë"


def test_filtro_art():
    """Kontrollon filtrimin e artit."""
    df = lexo_te_dhenat()
    rezultati = filtro_sipas_kategorise(df, "Art")
    
    entitetet = rezultati["eventi"].unique()
    assert len(entitetet) == 6
    for e in entitetet:
        assert e in ART


def test_filtro_letersi():
    """Kontrollon filtrimin e letërsisë."""
    df = lexo_te_dhenat()
    rezultati = filtro_sipas_kategorise(df, "Letërsi")
    
    entitetet = rezultati["eventi"].unique()
    assert len(entitetet) == 6
    for e in entitetet:
        assert e in LETERSI


def test_filtro_te_gjitha():
    """Kontrollon që 'Të gjitha' kthen të gjithë DataFrame-in."""
    df = lexo_te_dhenat()
    rezultati = filtro_sipas_kategorise(df, "Të gjitha")
    assert len(rezultati) == len(df)


# ============================================================
# TESTET PËR lexo_trends()
# ============================================================

def test_lexo_trends_art_ekziston():
    """Kontrollon nëse skedari i Google Trends për Artin lexohet."""
    df = lexo_trends("trends_art.csv")
    if os.path.exists("trends_art.csv"):
        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert "Time" in df.columns


def test_lexo_trends_histori_ekziston():
    """Kontrollon nëse skedari i Google Trends për Historinë lexohet."""
    df = lexo_trends("trends_histori.csv")
    if os.path.exists("trends_histori.csv"):
        assert df is not None
        assert "Time" in df.columns


def test_lexo_trends_skedar_mungon():
    """Kontrollon sjelljen kur skedari nuk ekziston."""
    df = lexo_trends("skedar_qe_nuk_ekziston.csv")
    assert df is None


# ============================================================
# TESTET PËR lexo_ml()
# ============================================================

def test_lexo_ml_parashikimet():
    """Kontrollon nëse parashikimet ML lexohen."""
    df = lexo_ml("ml_parashikimet_2026.csv")
    if os.path.exists("ml_parashikimet_2026.csv"):
        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert "eventi" in df.columns


def test_lexo_ml_skedar_mungon():
    """Kontrollon sjelljen kur skedari ML nuk ekziston."""
    df = lexo_ml("skedar_ml_qe_nuk_ekziston.csv")
    assert df is None


# ============================================================
# TESTET E INTEGRIMIT
# ============================================================

def test_integrimi_histori_ka_vizita():
    """Kontrollon që historitë kanë vizita pozitive."""
    df = lexo_te_dhenat()
    df_histori = filtro_sipas_kategorise(df, "Histori")
    assert df_histori["total_vizita"].min() > 0


def test_integrimi_emrat_shqip():
    """Kontrollon që të gjithë entitetet kanë emër në shqip."""
    df = lexo_te_dhenat()
    pa_emra = df[df["Emri"] == df["eventi"]]
    # Nuk duhet të ketë më shumë se disa pa emër (nëse ka)
    assert len(pa_emra) < 3, "Shumë entitete pa emër në shqip"