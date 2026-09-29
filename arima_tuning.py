"""
arima_tuning.py - Përmirësime të avancuara të Machine Learning
================================================================
1. Hyperparameter tuning për ARIMA (grid search)
2. Cross-validation për seritë kohore (TimeSeriesSplit)
3. Testi Diebold-Mariano për krahasimin statistikor të modeleve
"""

import sqlite3
import pandas as pd
import numpy as np
import warnings
import itertools
from statsmodels.tsa.arima.model import ARIMA
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error
from scipy import stats

warnings.filterwarnings("ignore")


# ============================================================
# LEXIMI I TË DHËNAVE
# ============================================================

def lexo_te_dhenat_mujore():
    """Lexon të dhënat ditore dhe kthen seri mujore."""
    conn = sqlite3.connect("diploma.db")
    query = "SELECT eventi, data, vizita FROM vizitat ORDER BY eventi, data;"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    df["muaji"] = df["data"].astype(str).str[:6]
    df_mujore = df.groupby(["eventi", "muaji"])["vizita"].sum().reset_index()
    df_mujore["data_dt"] = pd.to_datetime(df_mujore["muaji"], format="%Y%m")
    df_mujore = df_mujore.sort_values(["eventi", "data_dt"]).reset_index(drop=True)
    
    return df_mujore


# ============================================================
# 1. HYPERPARAMETER TUNING PËR ARIMA
# ============================================================

def gjej_arima_optimal(seria, p_range=range(0, 3), d_range=range(0, 2), q_range=range(0, 3)):
    """Grid search për të gjetur ARIMA(p,d,q) optimal sipas AIC."""
    rezultati_me_i_mire = None
    aic_me_i_ulete = float("inf")
    
    for p, d, q in itertools.product(p_range, d_range, q_range):
        try:
            model = ARIMA(seria, order=(p, d, q))
            model_fit = model.fit()
            
            if model_fit.aic < aic_me_i_ulete:
                aic_me_i_ulete = model_fit.aic
                rezultati_me_i_mire = {
                    "order": (p, d, q),
                    "aic": aic_me_i_ulete,
                    "bic": model_fit.bic
                }
        except Exception:
            continue
    
    return rezultati_me_i_mire


# ============================================================
# 2. CROSS-VALIDATION PËR SERITË KOHORE
# ============================================================

def cross_validate_arima(seria, order, n_splits=5):
    """Cross-validation për seritë kohore duke përdorur TimeSeriesSplit."""
    tscv = TimeSeriesSplit(n_splits=n_splits)
    gabimet_mae = []
    
    for train_idx, test_idx in tscv.split(seria):
        try:
            train = seria.iloc[train_idx]
            test = seria.iloc[test_idx]
            
            model = ARIMA(train, order=order)
            model_fit = model.fit()
            parashikimi = model_fit.forecast(steps=len(test))
            
            mae = mean_absolute_error(test, parashikimi)
            gabimet_mae.append(mae)
        except Exception:
            continue
    
    if len(gabimet_mae) == 0:
        return None
    
    return {
        "MAE_mesatare": round(np.mean(gabimet_mae), 2),
        "MAE_devijimi": round(np.std(gabimet_mae), 2),
        "numri_folds": len(gabimet_mae)
    }


# ============================================================
# 3. TESTI DIEBOLD-MARIANO
# ============================================================

def diebold_mariano_test(gabimet_model1, gabimet_model2, h=1):
    """
    Testi Diebold-Mariano për të krahasuar saktësinë e dy modeleve.
    
    Hipoteza zero (H0): Të dy modelet kanë saktësi të njëjtë
    Hipoteza alternative (H1): Modelet kanë saktësi të ndryshme
    
    Nëse p < 0.05, dallimi është statistikisht i rëndësishëm.
    """
    gabimet_model1 = np.array(gabimet_model1)
    gabimet_model2 = np.array(gabimet_model2)
    
    # Humbja katrore (squared loss)
    d = gabimet_model1 ** 2 - gabimet_model2 ** 2
    
    # Statistika DM
    mesatarja_d = np.mean(d)
    varianca_d = np.var(d, ddof=1)
    n = len(d)
    
    if varianca_d == 0:
        return {"DM_stat": 0, "p_value": 1.0, "fituesi": "Barazim"}
    
    dm_stat = mesatarja_d / np.sqrt(varianca_d / n)
    
    # P-value (two-tailed)
    p_value = 2 * (1 - stats.norm.cdf(abs(dm_stat)))
    
    if p_value < 0.05:
        if dm_stat < 0:
            fituesi = "Modeli 1 (ARIMA)"
        else:
            fituesi = "Modeli 2 (Linear Regression)"
    else:
        fituesi = "Pa dallim sinjifikant"
    
    return {
        "DM_stat": round(dm_stat, 3),
        "p_value": round(p_value, 4),
        "fituesi": fituesi
    }


# ============================================================
# EKZEKUTIMI KRYESOR
# ============================================================

print("=" * 70)
print("PËRMIRËSIME TË AVANCUARA TË MACHINE LEARNING")
print("=" * 70)

df = lexo_te_dhenat_mujore()
print(f"\n Të dhënat: {len(df)} rreshta, {df['eventi'].nunique()} entitete")

# ============================================================
# FAZA 1: GRID SEARCH PËR ARIMA
# ============================================================
print("\n\n" + "=" * 70)
print("FAZA 1: HYPERPARAMETER TUNING (Grid Search për ARIMA)")
print("=" * 70)

rezultatet_tuning = []

for eventi in df["eventi"].unique():
    seria = df[df["eventi"] == eventi].set_index("data_dt")["vizita"].sort_index()
    seria = seria.asfreq("MS").ffill()
    
    print(f"\n  {eventi}...")
    rezultati = gjej_arima_optimal(seria)
    
    if rezultati:
        rezultatet_tuning.append({
            "eventi": eventi,
            "order": str(rezultati["order"]),
            "AIC": round(rezultati["aic"], 2),
            "BIC": round(rezultati["bic"], 2)
        })
        print(f"     Optimal: ARIMA{rezultati['order']} (AIC: {rezultati['aic']:.2f})")

df_tuning = pd.DataFrame(rezultatet_tuning)
df_tuning.to_csv("ml_tuning_optimal.csv", index=False)
print(f"\n✅ U ruajt: ml_tuning_optimal.csv")

# ============================================================
# FAZA 2: CROSS-VALIDATION
# ============================================================
print("\n\n" + "=" * 70)
print("FAZA 2: CROSS-VALIDATION (TimeSeriesSplit)")
print("=" * 70)

rezultatet_cv = []

for _, row in df_tuning.iterrows():
    eventi = row["eventi"]
    order = eval(row["order"])
    
    seria = df[df["eventi"] == eventi].set_index("data_dt")["vizita"].sort_index()
    seria = seria.asfreq("MS").ffill()
    
    rezultati = cross_validate_arima(seria, order)
    
    if rezultati:
        rezultatet_cv.append({
            "eventi": eventi,
            "order": str(order),
            "MAE_cv_mesatare": rezultati["MAE_mesatare"],
            "MAE_cv_devijimi": rezultati["MAE_devijimi"],
            "numri_folds": rezultati["numri_folds"]
        })
        print(f"  {eventi}: MAE = {rezultati['MAE_mesatare']:.0f} ± {rezultati['MAE_devijimi']:.0f}")

df_cv = pd.DataFrame(rezultatet_cv)
df_cv.to_csv("ml_cross_validation.csv", index=False)
print(f"\n✅ U ruajt: ml_cross_validation.csv")

# ============================================================
# FAZA 3: TESTI DIEBOLD-MARIANO
# ============================================================
print("\n\n" + "=" * 70)
print("FAZA 3: TESTI DIEBOLD-MARIANO")
print("=" * 70)
print("(Krahason saktësinë e ARIMA dhe Linear Regression)")
print()

rezultatet_dm = []

for eventi in df["eventi"].unique():
    seria = df[df["eventi"] == eventi].set_index("data_dt")["vizita"].sort_index()
    seria = seria.asfreq("MS").ffill()
    
    # Marrim order optimal për këtë event
    order_row = df_tuning[df_tuning["eventi"] == eventi]
    if len(order_row) == 0:
        continue
    order = eval(order_row.iloc[0]["order"])
    
    # Ndarja train/test
    ndarja = int(len(seria) * 0.8)
    train = seria[:ndarja]
    test = seria[ndarja:]
    
    try:
        # ARIMA
        model_arima = ARIMA(train, order=order)
        model_arima_fit = model_arima.fit()
        parashikimi_arima = model_arima_fit.forecast(steps=len(test))
        gabimet_arima = test.values - parashikimi_arima.values
        
        # Linear Regression
        X_train = np.arange(len(train)).reshape(-1, 1)
        X_test = np.arange(len(train), len(seria)).reshape(-1, 1)
        model_lr = LinearRegression()
        model_lr.fit(X_train, train.values)
        parashikimi_lr = model_lr.predict(X_test)
        gabimet_lr = test.values - parashikimi_lr
        
        # Testi DM
        rezultati_dm = diebold_mariano_test(gabimet_arima, gabimet_lr)
        
        rezultatet_dm.append({
            "eventi": eventi,
            "ARIMA_order": str(order),
            "DM_stat": rezultati_dm["DM_stat"],
            "p_value": rezultati_dm["p_value"],
            "Fituesi_DM": rezultati_dm["fituesi"]
        })
        
        print(f"  {eventi}:")
        print(f"     DM = {rezultati_dm['DM_stat']}, p = {rezultati_dm['p_value']} → {rezultati_dm['fituesi']}")
    
    except Exception as e:
        print(f"  {eventi}: Gabim - {e}")

df_dm = pd.DataFrame(rezultatet_dm)
df_dm.to_csv("ml_diebold_mariano.csv", index=False)
print(f"\n✅ U ruajt: ml_diebold_mariano.csv")

# ============================================================
# PËRMBLEDHJE
# ============================================================
print("\n\n" + "=" * 70)
print("PËRMBLEDHJE E PËRMIRËSIMEVE")
print("=" * 70)

print(f"\n Hyperparameter Tuning:")
print(f"   U testuan {len(df_tuning)} entitete")
print(f"   Modelet optimale u gjetën për secilin")

print(f"\n Cross-Validation:")
if len(df_cv) > 0:
    print(f"   MAE mesatare globale: {df_cv['MAE_cv_mesatare'].mean():.0f}")
    print(f"   Numri i folds: {df_cv['numri_folds'].iloc[0]}")

print(f"\n Diebold-Mariano Test:")
if len(df_dm) > 0:
    fituesit = df_dm["Fituesi_DM"].value_counts()
    for fituesi, nr in fituesit.items():
        print(f"   {fituesi}: {nr} entitete")

print("\n" + "=" * 70)
print("🎉 PËRMIRËSIMET PËRFUNDUAN ME SUKSES!")
print("=" * 70)