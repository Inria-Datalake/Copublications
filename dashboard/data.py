import os
from pathlib import Path
import pandas as pd

# 📌 Chemins corrigés
BASE_DIR = Path(r"C:\Users\abapst\nb_python\Copublications\dashboard")

XLSX_PATH = BASE_DIR / "dashboard.xlsx"
CSV_PATH  = BASE_DIR / "dashboard.csv"


def create_csv_from_xlsx(xlsx_path=XLSX_PATH, csv_path=CSV_PATH, sheet_name=0, force=False):
    """
    Crée dashboard.csv depuis dashboard.xlsx.
    - force=False : crée seulement si absent
    - force=True  : recrée même s'il existe
    """
    print("XLSX attendu :", xlsx_path)
    print("CSV attendu  :", csv_path)

    if not xlsx_path.exists():
        raise FileNotFoundError(f"Fichier Excel introuvable : {xlsx_path}")

    csv_path.parent.mkdir(parents=True, exist_ok=True)

    if csv_path.exists() and not force:
        print("[INFO] CSV déjà présent, pas de recréation.")
        return

    print("[INFO] Lecture du XLSX...")
    df_excel = pd.read_excel(xlsx_path, sheet_name=sheet_name, dtype=str)

    print("[INFO] Écriture du CSV...")
    df_excel.to_csv(csv_path, index=False, encoding="utf-8-sig", sep=",")

    print(f"[OK] CSV créé : {csv_path} ({csv_path.stat().st_size} octets)")


def load_data():
    """Lecture robuste du CSV + nettoyage colonnes et valeurs + harmonisation noms."""
    
    # 🔹 Création / vérification du CSV
    create_csv_from_xlsx(force=False)

    df = None
    last_err = None

    encodings = ["utf-8-sig", "utf-8", "latin1"]
    seps = [",", ";"]

    for enc in encodings:
        for sep in seps:
            try:
                df_try = pd.read_csv(
                    CSV_PATH,
                    encoding=enc,
                    sep=sep,
                    engine="python",
                    on_bad_lines="skip",
                    dtype=str,
                )

                if df_try is not None and df_try.shape[1] >= 2:
                    df = df_try
                    break
            except Exception as e:
                last_err = e
                df = None
        if df is not None:
            break

    if df is None:
        raise RuntimeError(f"Impossible de lire le CSV. Dernière erreur: {last_err}")

    # Nettoyage colonnes
    df.columns = (
        df.columns.astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
    )

    rename_map = {
        "Auteurs FR": "Auteurs_FR",
        "Auteurs copubliants": "Auteurs_copubliants",
        "Organisme copubliant": "Organisme_copubliant",
        "UE/Non UE": "UE/Non_UE",
        "ID Aurehal": "ID_Aurehal",
        "Ann�e": "Année",
        "Domaines consolid�s": "Domaines consolidés",
    }
    df = df.rename(columns=rename_map)

    # Nettoyage valeurs texte
    for c in df.columns:
        if df[c].dtype == "object":
            df[c] = df[c].astype(str).str.strip()

    # Latitude / Longitude
    for col in ["Latitude", "Longitude"]:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", ".", regex=False)
                .replace({"": None, "nan": None, "None": None})
            )

    # Conversions numériques
    for col in ["Année", "Latitude", "Longitude"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Harmonisation centres
    if "Centre" in df.columns:
        df["Centre"] = df["Centre"].astype(str).str.strip()
        df["Centre"] = df["Centre"].replace({
            # Saclay
            "Inria Saclay IPP":          "Inria Saclay",
            "Inria Saclay UPS":          "Inria Saclay",
            "Inria Saclay - Île-de-France": "Inria Saclay",
            "Inria Saclay Ile-de-France":"Inria Saclay",
            # Paris — fusion Paris + Paris Sorbonne
            "Inria Paris Sorbonne":      "Inria Paris",
            "Inria Paris - Sorbonne":    "Inria Paris",
            "Inria Sorbonne":            "Inria Paris",
            "Inria de Paris":            "Inria Paris",
            "CRI Paris":                 "Inria Paris",
            # Bordeaux
            "Inria Bordeaux - Sud-Ouest":"Inria Univ. Bordeaux",
            "Inria Bordeaux Sud-Ouest":  "Inria Univ. Bordeaux",
            "Inria Bordeaux":            "Inria Univ. Bordeaux",
            "Bordeaux":                  "Inria Univ. Bordeaux",
            # Grenoble
            "Inria Grenoble - Rhône-Alpes": "Inria Univ. Grenoble",
            "Inria Grenoble Rhône-Alpes":"Inria Univ. Grenoble",
            "Inria Grenoble":            "Inria Univ. Grenoble",
            "Grenoble":                  "Inria Univ. Grenoble",
            # Rennes
            "Inria Rennes - Bretagne Atlantique": "Inria Univ. Rennes",
            "Inria Rennes Bretagne Atlantique":   "Inria Univ. Rennes",
            "Inria Rennes":              "Inria Univ. Rennes",
            "Rennes":                    "Inria Univ. Rennes",
            # Lorraine / Nancy
            "Inria Nancy - Grand Est":   "Inria Univ. Lorraine",
            "Inria Nancy Grand Est":     "Inria Univ. Lorraine",
            "Inria Nancy":               "Inria Univ. Lorraine",
            "Nancy":                     "Inria Univ. Lorraine",
            "Grand Est":                 "Inria Univ. Lorraine",
            # Lille
            "Inria Lille - Nord Europe": "Inria Lille",
            "Inria Lille Nord Europe":   "Inria Lille",
            "Lille":                     "Inria Lille",
            # Côte d'Azur
            "Inria Univ. Côte d'Azur":  "Inria Univ. Cote Azur",
            "Inria Univ. Côte Azur":    "Inria Univ. Cote Azur",
            "Inria Univ Cote Azur":     "Inria Univ. Cote Azur",
            "Inria Sophia Antipolis":    "Inria Univ. Cote Azur",
            "Inria Sophia Antipolis - Méditerranée": "Inria Univ. Cote Azur",
            "Sophia Antipolis":          "Inria Univ. Cote Azur",
            "Sophia":                    "Inria Univ. Cote Azur",
            # Lyon
            "Lyon":                      "Inria Lyon",
            # Siège
            "Inria siège":               "Inria Siege",
            "Inria Siège":               "Inria Siege",
            "Inria siege":               "Inria Siege",
        })

    # Filtrage années
    if "Année" in df.columns:
        df = df[df["Année"].between(2017, 2026, inclusive="both")]

    return df


def filter_df(df, centres, equipes, pays, villes, organismes, annees):
    dff = df.copy()

    if centres and "Centre" in dff.columns:
        dff = dff[dff["Centre"].isin(centres)]
    if equipes and "Equipe" in dff.columns:
        dff = dff[dff["Equipe"].isin(equipes)]
    if pays and "Pays" in dff.columns:
        dff = dff[dff["Pays"].isin(pays)]
    if villes and "Ville" in dff.columns:
        dff = dff[dff["Ville"].isin(villes)]
    if organismes and "Organisme_copubliant" in dff.columns:
        dff = dff[dff["Organisme_copubliant"].isin(organismes)]
    if annees and "Année" in dff.columns:
        dff = dff[dff["Année"].isin(annees)]

    return dff


# 🔹 Test direct
if __name__ == "__main__":
    create_csv_from_xlsx(force=True)
    df_test = load_data()
    print("Lignes :", len(df_test))