import dash_bootstrap_components as dbc

# === PALETTE DATALAKE / INRIA ===
# Cyan
CYAN_1 = "#00a5cc"
CYAN_2 = "#4dc0db"
CYAN_3 = "#80d2e7"
CYAN_4 = "#ccedf6"

# Bleu
BLUE_1 = "#1067a3"
BLUE_2 = "#5896bf"
BLUE_3 = "#87b2d2"
BLUE_4 = "#cfe1ed"

# Indigo
INDIGO_1 = "#27348b"
INDIGO_2 = "#6870ae"
INDIGO_3 = "#939ac6"
INDIGO_4 = "#d4d7e8"

# Violet
PURPLE_1 = "#5d4b9a"
PURPLE_2 = "#8e81b9"
PURPLE_3 = "#afa4cc"
PURPLE_4 = "#dfdbec"

# Magenta
MAGENTA_1 = "#a60f79"
MAGENTA_2 = "#c157a1"
MAGENTA_3 = "#d288bd"
MAGENTA_4 = "#eccfe5"

# Rouge
RED_1 = "#c9191e"
RED_2 = "#d95e61"
RED_3 = "#e58c8e"
RED_4 = "#f5d1d1"

# === COULEURS PRINCIPALES ===
PRIMARY = INDIGO_1
PRIMARY_LIGHT = CYAN_2
ACCENT = MAGENTA_1
DARK = BLUE_1
WHITE = "#ffffff"
BG = CYAN_4

# === ÉCHELLES CONTINUES POUR BARS ===
CYAN_SCALE = [CYAN_4, CYAN_1]
BLUE_SCALE = [BLUE_4, BLUE_1]
PURPLE_SCALE = [PURPLE_4, PURPLE_1]
MAGENTA_SCALE = [MAGENTA_4, MAGENTA_1]
RED_SCALE = [RED_4, RED_1]

# === SEQUENCES QUALITATIVES ===
CYAN_SEQ = [CYAN_1, CYAN_2, CYAN_3, CYAN_4]
BLUE_SEQ = [BLUE_1, BLUE_2, BLUE_3, BLUE_4]
PURPLE_SEQ = [PURPLE_1, PURPLE_2, PURPLE_3, PURPLE_4]
MAGENTA_SEQ = [MAGENTA_1, MAGENTA_2, MAGENTA_3, MAGENTA_4]
RED_SEQ = [RED_1, RED_2, RED_3, RED_4]

# Theme Bootstrap
THEME = dbc.themes.BOOTSTRAP

# Palette qualitative façon carte mondiale
QUAL_PALETTE = [
    "#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A",
    "#19D3F3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"
]

# ============================================================
# PALETTE FIXE PAR CENTRE INRIA
# Une couleur unique et stable par centre, utilisée dans tous
# les graphiques (flow map, radar, KPI badges, réseau…)
# ============================================================
CENTRE_COLOR_MAP = {
    # Noms canoniques (tels qu'ils apparaissent dans les données)
    "Inria Univ. Bordeaux":      "#EF553B",   # rouge-orange
    "Inria Univ. Grenoble":      "#00CC96",   # vert menthe
    "Inria Lille":               "#636EFA",   # bleu vif
    "Inria Lyon":                "#FFA15A",   # orange
    "Inria Univ. Lorraine":      "#AB63FA",   # violet
    "Inria Paris":               "#19D3F3",   # cyan
    "Inria Paris Sorbonne":      "#FF6692",   # rose
    "Inria Univ. Rennes":        "#B6E880",   # vert clair
    "Inria Saclay":              "#FF97FF",   # mauve
    "Inria Univ. Cote Azur":     "#FECB52",   # jaune doré
    "Inria siege":               "#636EFA",   # bleu (siège = même famille Paris)
    "Inria Montpellier":         "#00a5cc",   # cyan Inria

    # Variantes orthographiques — même couleur que le nom canonique
    "Inria Univ. Côte d'Azur":   "#FECB52",
    "Inria Univ. Côte Azur":     "#FECB52",
    "Inria Univ Cote Azur":      "#FECB52",
    "Sophia":                    "#FECB52",
    "Sophia Antipolis":          "#FECB52",
    "Inria Sophia":              "#FECB52",
    "Inria Sophia Antipolis":    "#FECB52",
    "Inria Sophia Antipolis - Méditerranée": "#FECB52",
    "Inria Sophia Antipolis Méditerranée":   "#FECB52",

    "Inria Saclay - Île-de-France":  "#FF97FF",
    "Inria Saclay Ile-de-France":    "#FF97FF",
    "Inria Saclay IPP":              "#FF97FF",
    "Inria Saclay UPS":              "#FF97FF",
    "Saclay":                        "#FF97FF",

    "Inria Univ. Rennes":                     "#B6E880",
    "Inria Univ Rennes":                      "#B6E880",
    "Rennes":                                 "#B6E880",
    "Inria Rennes":                           "#B6E880",
    "Inria Rennes - Bretagne Atlantique":     "#B6E880",
    "Inria Rennes Bretagne Atlantique":       "#B6E880",

    "Inria de Paris":                         "#19D3F3",
    "Paris":                                  "#19D3F3",
    "CRI Paris":                              "#19D3F3",
    "Inria Paris - Sorbonne":                 "#FF6692",
    "Inria Sorbonne":                         "#FF6692",

    "Inria Univ. Grenoble":                   "#00CC96",
    "Inria Univ Grenoble":                    "#00CC96",
    "Grenoble":                               "#00CC96",
    "Inria Grenoble":                         "#00CC96",
    "Inria Grenoble - Rhône-Alpes":           "#00CC96",
    "Inria Grenoble Rhône-Alpes":             "#00CC96",

    "Inria Univ. Lorraine":                   "#AB63FA",
    "Inria Univ Lorraine":                    "#AB63FA",
    "Nancy":                                  "#AB63FA",
    "Inria Nancy":                            "#AB63FA",
    "Inria Nancy - Grand Est":                "#AB63FA",
    "Inria Nancy Grand Est":                  "#AB63FA",
    "Grand Est":                              "#AB63FA",

    "Inria Lille - Nord Europe":              "#636EFA",
    "Inria Lille Nord Europe":                "#636EFA",
    "Lille":                                  "#636EFA",

    "Inria Univ Bordeaux":                    "#EF553B",
    "Bordeaux":                               "#EF553B",
    "Inria Bordeaux":                         "#EF553B",
    "Inria Bordeaux - Sud-Ouest":             "#EF553B",
    "Inria Bordeaux Sud-Ouest":               "#EF553B",

    "Lyon":                                   "#FFA15A",

    "Inria siège":                            "#636EFA",
    "Inria Siege":                            "#636EFA",
    "Inria Siège":                            "#636EFA",
}


def get_centre_color(centre_name: str, fallback_index: int = 0) -> str:
    """
    Retourne la couleur fixe d'un centre.
    - Recherche exacte d'abord
    - Puis recherche souple (sous-chaîne insensible à la casse)
    - Sinon fallback sur QUAL_PALETTE[fallback_index]
    """
    if centre_name in CENTRE_COLOR_MAP:
        return CENTRE_COLOR_MAP[centre_name]
    c_low = centre_name.lower()
    for key, color in CENTRE_COLOR_MAP.items():
        if key.lower() in c_low or c_low in key.lower():
            return color
    return QUAL_PALETTE[fallback_index % len(QUAL_PALETTE)]

# === TEMPLATE PLOTLY ===
GRAPH_TEMPLATE = dict(
    layout=dict(
        paper_bgcolor=WHITE,
        plot_bgcolor=WHITE,
        font=dict(
            family="Open Sans, Arial, sans-serif",
            color=PRIMARY,   # ❗ une seule couleur, pas une liste
            size=13,
        ),
        title=dict(
            x=0.5,
            xanchor="center",
            font=dict(
                size=20,
                color=PRIMARY,
                family="Open Sans, Arial, sans-serif",
            ),
        ),
        margin=dict(l=10, r=10, t=45, b=40),
        hoverlabel=dict(
            bgcolor=WHITE,
            font_size=12,
            font_family="Open Sans, Arial, sans-serif",
        ),
    )
)