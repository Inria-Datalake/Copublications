import base64
import io
import numpy as np
import pandas as pd
import dash
from dash import Output, Input, State, no_update, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import networkx as nx
from dash.exceptions import PreventUpdate
import json
import math

from data import filter_df
from style import (
    GRAPH_TEMPLATE,
    PRIMARY,
    PRIMARY_LIGHT,
    ACCENT,
    DARK,
    CYAN_SCALE,
    QUAL_PALETTE,
    CENTRE_COLOR_MAP,
    get_centre_color,
)

# ============================================================
#  Coordonnées des centres Inria — noms exacts issus des données + variantes
# ============================================================
CENTER_COORDS = {

    # ════════════════════════════════════════════════════════
    # Inria Univ. Côte d'Azur  (Sophia Antipolis, Valbonne)
    # Bâtiment Euler, 2004 route des Lucioles, 06902 Valbonne
    # ════════════════════════════════════════════════════════
    "Inria Univ. Cote Azur":                   (43.6160, 7.0678),
    "Inria Univ. Côte d'Azur":                 (43.6160, 7.0678),
    "Inria Univ. Côte Azur":                   (43.6160, 7.0678),
    "Inria Univ Cote Azur":                    (43.6160, 7.0678),
    "Sophia":                                  (43.6160, 7.0678),
    "Sophia Antipolis":                        (43.6160, 7.0678),
    "Inria Sophia":                            (43.6160, 7.0678),
    "Inria Sophia Antipolis":                  (43.6160, 7.0678),
    "Inria Sophia Antipolis - Méditerranée":   (43.6160, 7.0678),
    "Inria Sophia Antipolis Méditerranée":     (43.6160, 7.0678),

    # ════════════════════════════════════════════════════════
    # Inria Saclay  (Palaiseau — bâtiment Alan Turing, École Polytechnique)
    # 1 rue Honoré d'Estienne d'Orves, 91120 Palaiseau
    # ════════════════════════════════════════════════════════
    "Inria Saclay":                            (48.7136, 2.2122),
    "Inria Saclay - Île-de-France":            (48.7136, 2.2122),
    "Inria Saclay Ile-de-France":              (48.7136, 2.2122),
    "Inria Saclay IPP":                        (48.7136, 2.2122),
    "Inria Saclay UPS":                        (48.7136, 2.2122),
    "Saclay":                                  (48.7136, 2.2122),

    # ════════════════════════════════════════════════════════
    # Inria Univ. Rennes  (campus Beaulieu, Rennes)
    # Campus de Beaulieu, 263 avenue du Général Leclerc, 35042 Rennes
    # ════════════════════════════════════════════════════════
    "Inria Univ. Rennes":                      (48.1147, -1.6387),
    "Inria Univ Rennes":                       (48.1147, -1.6387),
    "Rennes":                                  (48.1147, -1.6387),
    "Inria Rennes":                            (48.1147, -1.6387),
    "Inria Rennes - Bretagne Atlantique":      (48.1147, -1.6387),
    "Inria Rennes Bretagne Atlantique":        (48.1147, -1.6387),

    # ════════════════════════════════════════════════════════
    # Inria Paris  (2 rue Simone Iff, 75012 Paris)
    # ════════════════════════════════════════════════════════
    "Inria Paris":                             (48.8474, 2.3842),
    "Inria de Paris":                          (48.8474, 2.3842),
    "Paris":                                   (48.8474, 2.3842),
    "CRI Paris":                               (48.8474, 2.3842),

    # ════════════════════════════════════════════════════════
    # Inria Paris Sorbonne  (Campus Pierre et Marie Curie, Paris 5e)
    # 4 place Jussieu, 75005 Paris
    # ════════════════════════════════════════════════════════
    "Inria Paris Sorbonne":                    (48.8468, 2.3544),
    "Inria Paris - Sorbonne":                  (48.8468, 2.3544),
    "Inria Sorbonne":                          (48.8468, 2.3544),

    # ════════════════════════════════════════════════════════
    # Inria Univ. Grenoble  (Montbonnot-Saint-Martin)
    # 655 avenue de l'Europe, 38334 Montbonnot-Saint-Martin
    # ════════════════════════════════════════════════════════
    "Inria Univ. Grenoble":                    (45.2095, 5.8346),
    "Inria Univ Grenoble":                     (45.2095, 5.8346),
    "Grenoble":                                (45.2095, 5.8346),
    "Inria Grenoble":                          (45.2095, 5.8346),
    "Inria Grenoble - Rhône-Alpes":            (45.2095, 5.8346),
    "Inria Grenoble Rhône-Alpes":              (45.2095, 5.8346),

    # ════════════════════════════════════════════════════════
    # Inria Univ. Lorraine  (Villers-lès-Nancy)
    # 615 rue du Jardin Botanique, 54600 Villers-lès-Nancy
    # ════════════════════════════════════════════════════════
    "Inria Univ. Lorraine":                    (48.6656, 6.1550),
    "Inria Univ Lorraine":                     (48.6656, 6.1550),
    "Nancy":                                   (48.6656, 6.1550),
    "Inria Nancy":                             (48.6656, 6.1550),
    "Inria Nancy - Grand Est":                 (48.6656, 6.1550),
    "Inria Nancy Grand Est":                   (48.6656, 6.1550),
    "Grand Est":                               (48.6656, 6.1550),

    # ════════════════════════════════════════════════════════
    # Inria Lille  (Villeneuve d'Ascq — Cité Scientifique)
    # Parc scientifique de la Haute Borne, 40 av. Halley, 59650 Villeneuve d'Ascq
    # ════════════════════════════════════════════════════════
    "Inria Lille":                             (50.6078, 3.1311),
    "Inria Lille - Nord Europe":               (50.6078, 3.1311),
    "Inria Lille Nord Europe":                 (50.6078, 3.1311),
    "Lille":                                   (50.6078, 3.1311),

    # ════════════════════════════════════════════════════════
    # Inria Univ. Bordeaux  (Talence — campus INRIA)
    # 200 avenue de la Vieille Tour, 33405 Talence
    # ════════════════════════════════════════════════════════
    "Inria Univ. Bordeaux":                    (44.8084, -0.5954),
    "Inria Univ Bordeaux":                     (44.8084, -0.5954),
    "Bordeaux":                                (44.8084, -0.5954),
    "Inria Bordeaux":                          (44.8084, -0.5954),
    "Inria Bordeaux - Sud-Ouest":              (44.8084, -0.5954),
    "Inria Bordeaux Sud-Ouest":                (44.8084, -0.5954),

    # ════════════════════════════════════════════════════════
    # Inria Lyon  (site INSA Lyon, Villeurbanne)
    # 56 boulevard Niels Bohr, 69100 Villeurbanne
    # ════════════════════════════════════════════════════════
    "Inria Lyon":                              (45.7826, 4.8791),
    "Lyon":                                    (45.7826, 4.8791),

    # ════════════════════════════════════════════════════════
    # Inria Siège  (Paris 13e — Domaine de Voluceau, Le Chesnay)
    # Domaine de Voluceau, Rocquencourt, 78153 Le Chesnay-Rocquencourt
    # ════════════════════════════════════════════════════════
    "Inria siege":                             (48.8243, 2.0996),
    "Inria siège":                             (48.8243, 2.0996),
    "Inria Siege":                             (48.8243, 2.0996),
    "Inria Siège":                             (48.8243, 2.0996),
    "Inria siege social":                      (48.8243, 2.0996),

    # ════════════════════════════════════════════════════════
    # Montpellier  (site LIRMM)
    # 860 rue de Saint-Priest, 34090 Montpellier
    # ════════════════════════════════════════════════════════
    "Montpellier":                             (43.6324, 3.8618),
    "Inria Montpellier":                       (43.6324, 3.8618),
}

# ============================================================
#  Fonctions utilitaires pour les arcs courbés + glow
# ============================================================
def curved_arc(lat1, lon1, lat2, lon2, curvature=0.20, steps=22):
    lat_c = (lat1 + lat2) / 2 + (lat2 - lat1) * curvature
    lon_c = (lon1 + lon2) / 2 - (lon2 - lon1) * curvature

    t = np.linspace(0, 1, steps)
    lat_curve = (1 - t) ** 2 * lat1 + 2 * (1 - t) * t * lat_c + t**2 * lat2
    lon_curve = (1 - t) ** 2 * lon1 + 2 * (1 - t) * t * lon_c + t**2 * lon2

    return lat_curve, lon_curve


def add_glow_arc(fig, lat_curve, lon_curve, rgb="39,52,139"):
    glow_layers = [
        (10, f"rgba({rgb}, 0.04)"),
        (8, f"rgba({rgb}, 0.07)"),
        (6, f"rgba({rgb}, 0.10)"),
    ]

    for width, color in glow_layers:
        fig.add_trace(
            go.Scattermapbox(
                lat=lat_curve,
                lon=lon_curve,
                mode="lines",
                line=dict(width=width, color=color),
                hoverinfo="skip",
                showlegend=False,
            )
        )


# ============================================================
#  REGISTER CALLBACKS
# ============================================================
def register_callbacks(app, df_base):

    # ========================================================
    # 0a — Titre dynamique du rapport
    # ========================================================
    @app.callback(
        Output("report-title", "children"),
        [
            Input("centre", "value"),
            Input("equipe", "value"),
            Input("pays", "value"),
            Input("ville", "value"),
            Input("org", "value"),
            Input("annee", "value"),
        ],
    )
    def update_report_title(centres, equipes, pays, villes, orgs, annees):
        # Centres
        if centres:
            if len(centres) == 1:
                txt_centre = f"centre Inria {centres[0]}"
            else:
                txt_centre = "centres Inria " + ", ".join(centres)
        else:
            txt_centre = "tous les centres Inria"

        # Équipes
        if equipes:
            if len(equipes) == 1:
                txt_eq = f"équipe {equipes[0]}"
            else:
                txt_eq = "équipes " + ", ".join(equipes)
        else:
            txt_eq = "toutes les équipes"

        # Villes
        if villes:
            if len(villes) == 1:
                txt_ville = f"ville {villes[0]}"
            else:
                txt_ville = "villes " + ", ".join(villes)
        else:
            txt_ville = "toutes les villes"

        # Pays
        if pays:
            if len(pays) == 1:
                txt_pays = f"pays {pays[0]}"
            else:
                txt_pays = "pays " + ", ".join(pays)
        else:
            txt_pays = "tous les pays"

        # Années
        if annees:
            try:
                an_min = min(annees)
                an_max = max(annees)
                if an_min == an_max:
                    txt_periode = f"année {an_min}"
                else:
                    txt_periode = f"période {an_min}–{an_max}"
            except Exception:
                txt_periode = "période sélectionnée"
        else:
            txt_periode = "toutes les années"

        return (
            f"Copublications internationales – {txt_centre}, "
            f"{txt_eq}, {txt_ville}, {txt_pays} ({txt_periode})"
        )

    # ========================================================
    # 0 — SIDEBAR
    # ========================================================
    @app.callback(
        Output("sidebar", "is_open"),
        Input("sidebar-toggle", "n_clicks"),
        State("sidebar", "is_open"),
        prevent_initial_call=True,
    )
    def toggle_sidebar(n_clicks, is_open):
        return not is_open if n_clicks else is_open

    # ========================================================
    # 0bis — Upload CSV → store-data
    # ========================================================
    @app.callback(
        Output("store-data", "data"),
        Input("upload-data", "contents"),
        prevent_initial_call=True,
    )
    def update_uploaded_data(contents):
        if contents is None:
            return no_update

        content_type, content_string = contents.split(",", 1)
        decoded = base64.b64decode(content_string)

        try:
            df_new = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        except Exception:
            return no_update

        return df_new.to_dict("records")

    # ========================================================
    # 0ter — FILTRES EN CASCADE (mode doux : ne pas nettoyer les values)
    # ========================================================
    def _as_list(x):
        if x is None:
            return []
        return x if isinstance(x, list) else [x]

    def _build_options(series):
        if series is None:
            return []
        vals = sorted([v for v in series.dropna().unique() if str(v).strip() != ""])
        return [{"label": str(v), "value": v} for v in vals]

    def _filter_except(df, centres, equipes, pays, villes, orgs, annees, except_key):
        dff = df.copy()

        if except_key != "centre" and centres and "Centre" in dff.columns:
            dff = dff[dff["Centre"].isin(_as_list(centres))]
        if except_key != "equipe" and equipes and "Equipe" in dff.columns:
            dff = dff[dff["Equipe"].isin(_as_list(equipes))]
        if except_key != "pays" and pays and "Pays" in dff.columns:
            dff = dff[dff["Pays"].isin(_as_list(pays))]
        if except_key != "ville" and villes and "Ville" in dff.columns:
            dff = dff[dff["Ville"].isin(_as_list(villes))]
        if except_key != "org" and orgs and "Organisme_copubliant" in dff.columns:
            dff = dff[dff["Organisme_copubliant"].isin(_as_list(orgs))]
        if except_key != "annee" and annees and "Année" in dff.columns:
            dff = dff[dff["Année"].isin(_as_list(annees))]

        return dff

    @app.callback(
        Output("centre", "options"),
        Output("equipe", "options"),
        Output("pays", "options"),
        Output("ville", "options"),
        Output("org", "options"),
        Output("annee", "options"),
        Input("centre", "value"),
        Input("equipe", "value"),
        Input("pays", "value"),
        Input("ville", "value"),
        Input("org", "value"),
        Input("annee", "value"),
        Input("store-data", "data"),
    )
    def update_filter_dropdowns_soft(centres, equipes, pays, villes, orgs, annees, stored_data):
        df = pd.DataFrame(stored_data) if stored_data is not None else df_base

        dff_centre = _filter_except(df, centres, equipes, pays, villes, orgs, annees, except_key="centre")
        dff_equipe = _filter_except(df, centres, equipes, pays, villes, orgs, annees, except_key="equipe")
        dff_pays   = _filter_except(df, centres, equipes, pays, villes, orgs, annees, except_key="pays")
        dff_ville  = _filter_except(df, centres, equipes, pays, villes, orgs, annees, except_key="ville")
        dff_org    = _filter_except(df, centres, equipes, pays, villes, orgs, annees, except_key="org")
        dff_annee  = _filter_except(df, centres, equipes, pays, villes, orgs, annees, except_key="annee")

        centre_opts = _build_options(dff_centre["Centre"]) if "Centre" in dff_centre.columns else []
        equipe_opts = _build_options(dff_equipe["Equipe"]) if "Equipe" in dff_equipe.columns else []
        pays_opts   = _build_options(dff_pays["Pays"]) if "Pays" in dff_pays.columns else []
        ville_opts  = _build_options(dff_ville["Ville"]) if "Ville" in dff_ville.columns else []
        org_opts    = _build_options(dff_org["Organisme_copubliant"]) if "Organisme_copubliant" in dff_org.columns else []
        annee_opts  = _build_options(dff_annee["Année"]) if "Année" in dff_annee.columns else []

        return centre_opts, equipe_opts, pays_opts, ville_opts, org_opts, annee_opts

    # ========================================================
    # 1 — KPI + GRAPH PRINCIPAUX + CARTE + FLOW MAP
    # ========================================================
    @app.callback(
        [
            Output("kpi-zone", "children"),
            Output("bar_annee", "figure"),
            Output("top_pays", "figure"),
            Output("top_villes", "figure"),
            Output("top_orgs", "figure"),
            Output("map", "figure"),
            Output("flow_map", "figure"),
        ],
        [
            Input("centre", "value"),
            Input("equipe", "value"),
            Input("pays", "value"),
            Input("ville", "value"),
            Input("org", "value"),
            Input("annee", "value"),
            Input("store-data", "data"),
        ],
    )
    def update_main(centres, equipes, pays, villes, orgs, annees, stored_data):

        # Choix du dataframe : CSV uploadé ou df initial
        if stored_data is not None:
            df = pd.DataFrame(stored_data)
        else:
            df = df_base

        dff = filter_df(df, centres, equipes, pays, villes, orgs, annees)

        # ======================== KPI ========================
        def kpi_card(label, value, color):
            return dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div(label, className="small text-muted"),
                            html.H3(
                                value,
                                className="fw-bold mb-0",
                                style={"color": color},
                            ),
                        ]
                    ),
                    className="shadow-sm",
                    style={"borderRadius": "14px", "border": f"1px solid {color}20"},
                ),
                md=4,
                sm=6,
                xs=12,
            )

        kpi_global = dbc.Row(
            [
                kpi_card("Publications", dff["HalID"].nunique(), PRIMARY),
                kpi_card("Villes", dff["Ville"].nunique(), PRIMARY_LIGHT),
                kpi_card("Pays", dff["Pays"].nunique(), ACCENT),
                kpi_card("Équipes", dff["Equipe"].nunique(), PRIMARY_LIGHT),
                kpi_card("Auteurs Inria", dff["Auteurs_FR"].nunique(), PRIMARY),
                kpi_card("Copubliants", dff["Auteurs_copubliants"].nunique(), PRIMARY_LIGHT),
            ],
            className="g-2",
        )

        centre_counts = (
            dff.groupby("Centre")["HalID"]
            .nunique()
            .sort_values(ascending=False)
        )

        centre_badges = [
            dbc.Badge(
                f"{c}: {n}",
                pill=True,
                className="me-1 mb-1",
                style={
                    "backgroundColor": get_centre_color(c, i),
                    "color": "white",
                    "fontSize": "0.8rem",
                },
            )
            for i, (c, n) in enumerate(centre_counts.items())
        ]

        kpi_centres_block = html.Div(
            [
                html.Div(
                    "Publications par centre",
                    className="fw-bold small text-muted mb-1",
                ),
                html.Div(centre_badges, className="d-flex flex-wrap"),
            ]
        )

        kpis = html.Div([kpi_global, html.Hr(), kpi_centres_block])

        # ==================== BARRES PAR ANNÉE ====================
        pubs_by_year = (
            dff.groupby("Année")["HalID"]
            .nunique()
            .reset_index(name="Publications")
        )

        fig_year = px.bar(
            pubs_by_year,
            x="Année",
            y="Publications",
            color="Année",
            color_discrete_sequence=QUAL_PALETTE,
        )
        fig_year.update_layout(
            template=GRAPH_TEMPLATE,
            showlegend=False,
            margin=dict(l=10, r=10, t=60, b=40),
        )

        # ========== Utilitaire barres arrondies (Top X) ==========
        def top_bar_rounded(df_group, label, legend_below: bool = False):
            """Top 10 en donut (mêmes couleurs)"""
            if df_group.empty:
                return go.Figure().update_layout(
                    template=GRAPH_TEMPLATE,
                    title=None,
                    showlegend=True,
                    margin=dict(l=10, r=10, t=10, b=10),
                )

            df_top = (
                df_group.sort_values("Publications", ascending=True)
                .tail(10)
                .reset_index(drop=True)
            )

            colors = [QUAL_PALETTE[i % len(QUAL_PALETTE)] for i in range(len(df_top))]

            fig = go.Figure(
                go.Pie(
                    labels=df_top[label],
                    values=df_top["Publications"],
                    hole=0.55,
                    sort=False,
                    direction="clockwise",
                    marker=dict(colors=colors),
                    textinfo="percent",
                    hovertemplate=f"{label} : %{{label}}<br>Publications : %{{value}}<extra></extra>",
                    showlegend=True,
                )
            )

            fig.update_layout(
                template=GRAPH_TEMPLATE,
                title=None,
                showlegend=True,
                margin=dict(l=10, r=10, t=10, b=10),
            )

            if legend_below:
                fig.update_layout(
                    legend=dict(
                        orientation="h",
                        x=0.5,
                        xanchor="center",
                        y=-0.15,
                        yanchor="top",
                        font=dict(size=9),
                    ),
                    margin=dict(l=10, r=10, t=10, b=90),
                )
            else:
                fig.update_layout(
                    legend=dict(
                        orientation="v",
                        y=0.5,
                        yanchor="middle",
                        x=1.02,
                        xanchor="left",
                    )
                )

            return fig

        fig_pays = top_bar_rounded(
            dff.groupby("Pays")["HalID"].nunique().reset_index(name="Publications"),
            "Pays",
        )

        fig_villes = top_bar_rounded(
            dff.groupby("Ville")["HalID"].nunique().reset_index(name="Publications"),
            "Ville",
        )

        fig_orgs = top_bar_rounded(
            dff.groupby("Organisme_copubliant")["HalID"]
            .nunique()
            .reset_index(name="Publications"),
            "Organisme_copubliant",
            legend_below=True,
        )

        # ====================== CARTE MONDIALE ======================
        map_df = (
            dff.dropna(subset=["Latitude", "Longitude"])
            .groupby(["Ville", "Pays", "Latitude", "Longitude"])["HalID"]
            .nunique()
            .reset_index(name="Publications")
        )
        MAX_MAP_POINTS = 600
        map_df = map_df.sort_values("Publications", ascending=False).head(MAX_MAP_POINTS)

        if map_df.empty:
            fig_map = go.Figure().update_layout(
                template=GRAPH_TEMPLATE,
                title="Carte mondiale des copublications (aucune donnée)",
                height=400,
                margin=dict(l=0, r=0, t=50, b=0),
            )
        else:
            fig_map = px.scatter_mapbox(
                map_df,
                lat="Latitude",
                lon="Longitude",
                size="Publications",
                size_max=50,
                color="Pays",
                hover_name="Ville",
                hover_data={"Pays": True, "Publications": True},
                zoom=1,
                title="Carte mondiale des copublications",
            )

            fig_map.update_layout(
                mapbox=dict(
                    style="open-street-map",
                    center=dict(lat=25, lon=5),
                    zoom=1,
                ),
                height=400,
                margin=dict(l=0, r=0, t=50, b=0),
                autosize=False,
                uirevision="LOCK",
                legend=dict(
                    orientation="v",
                    x=1.02,
                    xanchor="left",
                    y=1,
                    yanchor="top",
                    font=dict(size=10),
                    bgcolor="rgba(255,255,255,0.85)",
                    bordercolor="rgba(0,0,0,0.1)",
                    borderwidth=0.5,
                ),
            )

        # ======================== FLOW MAP =========================
        def hex_to_rgb(hex_color: str):
            h = hex_color.lstrip("#")
            if len(h) == 3:
                h = "".join([c * 2 for c in h])
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

        def _lookup_centre_coords(centre_name: str, flow_df_fallback):
            """Recherche coordonnées : exact → sous-chaîne → fallback moyenne."""
            if centre_name in CENTER_COORDS:
                return CENTER_COORDS[centre_name]
            c_low = centre_name.lower()
            for key, coords in CENTER_COORDS.items():
                if key.lower() in c_low or c_low in key.lower():
                    return coords
            # Fallback : barycentre des destinations (dernier recours)
            return (
                float(flow_df_fallback["Latitude"].mean()),
                float(flow_df_fallback["Longitude"].mean()),
            )

        # ── Sélection des centres à afficher ──
        if centres and len(centres) > 0:
            centres_sel = [str(c) for c in centres if c is not None and str(c).strip() != ""]
        else:
            centres_sel = sorted(dff["Centre"].dropna().astype(str).unique().tolist())

        MAX_CENTRES_FLOW   = 8   # jusqu'à 8 centres simultanés
        MAX_DEST_PER_CENTRE = 40  # top 40 destinations par centre (lisibilité)
        centres_sel = centres_sel[:MAX_CENTRES_FLOW]

        fig_flow = go.Figure()
        origins = []
        all_dest_lats, all_dest_lons = [], []

        # ── Palette fixe par centre ──
        if centres_sel:
            centre_color_map = {
                c: get_centre_color(c, i)
                for i, c in enumerate(centres_sel)
            }

            for centre_sel in centres_sel:
                flow_raw = (
                    dff[dff["Centre"].astype(str) == centre_sel]
                    .dropna(subset=["Latitude", "Longitude"])
                )
                if flow_raw.empty:
                    continue

                flow_df = (
                    flow_raw.groupby(["Ville", "Pays", "Latitude", "Longitude"])
                    .agg(
                        Publications=("HalID", "nunique"),
                        UE_flag=(
                            "UE/Non_UE",
                            lambda x: "UE"
                            if (x == "UE").sum() >= (x != "UE").sum()
                            else "Non_UE",
                        ),
                    )
                    .reset_index()
                    .sort_values("Publications", ascending=False)
                    .head(MAX_DEST_PER_CENTRE)
                )
                if flow_df.empty:
                    continue

                origin_lat, origin_lon = _lookup_centre_coords(centre_sel, flow_df)
                origins.append((origin_lat, origin_lon))

                centre_hex = centre_color_map[centre_sel]
                r, g, b = hex_to_rgb(centre_hex)
                centre_rgb = f"{r},{g},{b}"

                max_pub = float(flow_df["Publications"].max()) if not flow_df.empty else 1
                total_pubs = int(flow_df["Publications"].sum())

                # ── Seuils visuels pour classer les liens ──
                p75 = float(flow_df["Publications"].quantile(0.75))
                p50 = float(flow_df["Publications"].quantile(0.50))

                for _, row in flow_df.iterrows():
                    pub = float(row["Publications"])
                    is_ue = row["UE_flag"] == "UE"

                    # Épaisseur : 3 niveaux selon le rang — renforcés pour fond clair
                    if pub >= p75:
                        line_width = 5.5
                        alpha_line = 0.95
                    elif pub >= p50:
                        line_width = 3.0
                        alpha_line = 0.75
                    else:
                        line_width = 1.5
                        alpha_line = 0.50

                    dest_lat = float(row["Latitude"])
                    dest_lon = float(row["Longitude"])
                    all_dest_lats.append(dest_lat)
                    all_dest_lons.append(dest_lon)

                    lat_curve, lon_curve = curved_arc(
                        origin_lat, origin_lon, dest_lat, dest_lon
                    )

                    tooltip = (
                        f"<b>{centre_sel}</b> → <b>{row['Ville']}</b><br>"
                        f"Pays : {row['Pays']}<br>"
                        f"Publications : <b>{int(pub)}</b><br>"
                        f"Zone : {'🇪🇺 UE' if is_ue else '🌍 Hors UE'}"
                    )

                    # — Arc glow (halo large, très transparent) —
                    fig_flow.add_trace(
                        go.Scattermapbox(
                            lat=list(lat_curve) + [None],
                            lon=list(lon_curve) + [None],
                            mode="lines",
                            line=dict(
                                width=line_width + 6,
                                color=f"rgba({centre_rgb},0.07)",
                            ),
                            hoverinfo="skip",
                            showlegend=False,
                        )
                    )

                    # — Arc principal —
                    fig_flow.add_trace(
                        go.Scattermapbox(
                            lat=list(lat_curve) + [None],
                            lon=list(lon_curve) + [None],
                            mode="lines",
                            line=dict(
                                width=line_width,
                                color=f"rgba({centre_rgb},{alpha_line})",
                            ),
                            hoverinfo="text",
                            text=[tooltip] * (len(lat_curve) + 1),
                            showlegend=False,
                        )
                    )

                    # — Pointe de flèche : marker à 90 % de l'arc —
                    tip_idx = int(len(lat_curve) * 0.90)
                    tip_size = 6 + 4 * (pub / max_pub)  # taille ∝ pubs
                    fig_flow.add_trace(
                        go.Scattermapbox(
                            lat=[float(lat_curve[tip_idx])],
                            lon=[float(lon_curve[tip_idx])],
                            mode="markers",
                            marker=dict(
                                size=tip_size,
                                color=centre_hex,
                                opacity=alpha_line + 0.05,
                            ),
                            hoverinfo="text",
                            text=[tooltip],
                            showlegend=False,
                        )
                    )

                # ── Halo externe du centre (anneau pulsé) ──
                fig_flow.add_trace(
                    go.Scattermapbox(
                        lat=[origin_lat],
                        lon=[origin_lon],
                        mode="markers",
                        marker=dict(
                            size=52,
                            color=f"rgba({centre_rgb},0.10)",
                        ),
                        hoverinfo="skip",
                        showlegend=False,
                    )
                )
                # ── Anneau intermédiaire ──
                fig_flow.add_trace(
                    go.Scattermapbox(
                        lat=[origin_lat],
                        lon=[origin_lon],
                        mode="markers",
                        marker=dict(
                            size=34,
                            color=f"rgba({centre_rgb},0.20)",
                        ),
                        hoverinfo="skip",
                        showlegend=False,
                    )
                )
                # ── Disque central plein ──
                fig_flow.add_trace(
                    go.Scattermapbox(
                        lat=[origin_lat],
                        lon=[origin_lon],
                        mode="markers+text",
                        marker=dict(
                            size=20,
                            color=centre_hex,
                            opacity=1.0,
                        ),
                        text=[centre_sel],
                        textposition="bottom right",
                        textfont=dict(size=11, color="#111111"),
                        name=centre_sel,
                        showlegend=True,
                        hovertemplate=(
                            f"<b>Centre Inria {centre_sel}</b><br>"
                            f"Destinations : {len(flow_df)}<br>"
                            f"Publications totales : {total_pubs}<br>"
                            "<extra></extra>"
                        ),
                    )
                )

            # ── Zoom automatique sur la boîte englobante ──
            if origins and all_dest_lats:
                all_lats = [o[0] for o in origins] + all_dest_lats
                all_lons = [o[1] for o in origins] + all_dest_lons
                lat_c = (min(all_lats) + max(all_lats)) / 2
                lon_c = (min(all_lons) + max(all_lons)) / 2
                # Zoom adaptatif selon l'étendue géographique
                lat_span = max(all_lats) - min(all_lats)
                lon_span = max(all_lons) - min(all_lons)
                span = max(lat_span, lon_span)
                if span > 120:
                    auto_zoom = 1
                elif span > 60:
                    auto_zoom = 2
                elif span > 30:
                    auto_zoom = 3
                else:
                    auto_zoom = 4
            else:
                lat_c, lon_c, auto_zoom = 25, 5, 1

            fig_flow.update_layout(
                paper_bgcolor="white",
                plot_bgcolor="white",
                font=dict(color="#1e293b"),
                mapbox=dict(
                    style="open-street-map",
                    center=dict(lat=lat_c, lon=lon_c),
                    zoom=auto_zoom,
                ),
                margin=dict(l=0, r=0, t=0, b=0),
                legend=dict(
                    orientation="v",
                    x=0.01,
                    xanchor="left",
                    y=0.99,
                    yanchor="top",
                    bgcolor="rgba(255,255,255,0.88)",
                    bordercolor="rgba(0,0,0,0.12)",
                    borderwidth=1,
                    font=dict(size=11, color="#1e293b"),
                    title=dict(
                        text="Centres Inria",
                        font=dict(size=12, color="#27348b"),
                    ),
                ),
                hoverlabel=dict(
                    bgcolor="#1e293b",
                    font_size=12,
                    font_color="#f1f5f9",
                    bordercolor="rgba(0,0,0,0.2)",
                ),
                uirevision="flow_map_stable",
            )

        return (
            kpis,
            fig_year,
            fig_pays,
            fig_villes,
            fig_orgs,
            fig_map,
            fig_flow,
        )

    # ========================================================
    # 1bis — FLOW MAP plein écran : ouverture / fermeture
    # ========================================================
    @app.callback(
        Output("flowmap-fullscreen-modal", "style"),
        [
            Input("btn-flowmap-fullscreen-open", "n_clicks"),
            Input("btn-flowmap-fullscreen-close", "n_clicks"),
        ],
        State("flowmap-fullscreen-modal", "style"),
        prevent_initial_call=True,
    )
    def toggle_flowmap_fullscreen(open_clicks, close_clicks, current_style):
        ctx = dash.callback_context
        if not ctx.triggered:
            return current_style
        trigger = ctx.triggered[0]["prop_id"].split(".")[0]
        if trigger == "btn-flowmap-fullscreen-open":
            return {"display": "block"}
        return {"display": "none"}

    # ========================================================
    # 1ter — FLOW MAP plein écran : copie de la figure
    # ========================================================
    @app.callback(
        Output("flow_map_fullscreen", "figure"),
        Input("flow_map", "figure"),
        prevent_initial_call=True,
    )
    def sync_flowmap_fullscreen(fig):
        if fig is None:
            return no_update
        return fig



    # ========================================================
    # 2 — WORDCLOUD + TOP 20 MOTS-CLÉS (callback unique)
    # ========================================================
    @app.callback(
        [
            Output("wordcloud", "src"),
            Output("wordcloud-top-table", "children"),
        ],
        [
            Input("centre", "value"),
            Input("equipe", "value"),
            Input("pays", "value"),
            Input("ville", "value"),
            Input("org", "value"),
            Input("annee", "value"),
            Input("tabs", "value"),
            Input("store-data", "data"),
        ],
    )
    def update_wordcloud(centres, equipes, pays, villes, orgs, annees, tab, stored_data):
        if tab != "tab-wordcloud":
            return no_update, no_update

        df = pd.DataFrame(stored_data) if stored_data is not None else df_base
        dff = filter_df(df, centres, equipes, pays, villes, orgs, annees)

        VALEURS_EXCLUES = {"nan", "none", "n/a", "na", "", "null"}

        # ── Mots vides français + anglais à exclure du nuage ──
        STOPWORDS_FR = {
            "le", "la", "les", "de", "du", "des", "un", "une", "et", "en",
            "à", "au", "aux", "que", "qui", "quoi", "dont", "où", "par",
            "pour", "sur", "sous", "dans", "avec", "sans", "est", "sont",
            "été", "être", "avoir", "nous", "vous", "ils", "elles", "on",
            "ce", "se", "sa", "son", "ses", "mon", "ma", "mes", "ton", "ta",
            "tes", "lui", "leur", "leurs", "tout", "tous", "toute", "toutes",
            "plus", "très", "bien", "ainsi", "donc", "comme", "mais", "ou",
            "ni", "car", "si", "puis", "cet", "cette", "ces", "l", "d", "j",
            "s", "m", "n", "y", "qu", "c", "a", "il", "je", "tu", "nous",
            "dont", "lors", "selon", "entre", "après", "avant", "aussi",
            "même", "autres", "autre", "peut", "fait", "font", "faire",
            "the", "of", "and", "in", "to", "a", "is", "for", "this",
            "that", "are", "with", "as", "an", "on", "by", "from", "be",
            "or", "not", "at", "it", "its", "we", "our", "they", "which",
            "have", "has", "been", "can", "more", "also", "than", "these",
            "two", "new", "one", "into", "both", "their", "such", "show",
            "used", "using", "based", "paper", "propose", "presents",
            "presented", "proposed", "approach", "different", "within",
            "between", "while", "however", "here", "first", "second",
            "three", "four", "five", "via", "i.e", "e.g", "al", "et",
        }

        mots_series = (
            dff["Resume"]
            .dropna()
            .astype(str)
            .str.strip()
        )
        mots_series = mots_series[~mots_series.str.lower().isin(VALEURS_EXCLUES)]

        empty_table = html.P("Aucun résumé disponible.", className="text-muted small p-2")

        if mots_series.empty:
            return "", empty_table

        # Échantillon pour les performances
        sample = mots_series.sample(min(len(mots_series), 3000), random_state=42)

        # ── Tokenisation : on découpe par mots, on filtre les stopwords ──
        import re
        mots_liste = []
        for resume in sample:
            for mot in re.split(r"[\s\W]+", resume):
                mot = mot.strip().lower()
                if (
                    len(mot) >= 3
                    and mot not in STOPWORDS_FR
                    and mot.lower() not in VALEURS_EXCLUES
                    and not mot.isdigit()
                ):
                    mots_liste.append(mot)

        if not mots_liste:
            return "", empty_table

        # ── WORDCLOUD ──
        text = " ".join(mots_liste)
        wc = WordCloud(width=900, height=400, background_color="white", colormap="tab10").generate(text)
        buf = io.BytesIO()
        wc.to_image().save(buf, format="PNG")
        img_src = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

        # ── TABLEAU TOP 20 ──
        counts = pd.Series([m.lower() for m in mots_liste]).value_counts()
        total = counts.sum()
        top20 = counts.head(20).reset_index()
        top20.columns = ["Mot-clé", "Occurrences"]
        top20["Pourcentage"] = (top20["Occurrences"] / total * 100).round(2)
        max_pct = top20["Pourcentage"].max()

        bar_colors = [
            PRIMARY, PRIMARY_LIGHT, ACCENT, DARK,
            "#00CC96", "#AB63FA", "#FFA15A", "#19D3F3",
            "#FF6692", "#B6E880", "#636EFA", "#EF553B",
            "#00a5cc", "#27348b", "#a60f79", "#1067a3",
            "#FF97FF", "#FECB52", "#4dc0db", "#c9191e",
        ]

        rows = []
        for i, row in top20.iterrows():
            pct = row["Pourcentage"]
            color = bar_colors[i % len(bar_colors)]
            bar_width = f"{pct / max_pct * 100:.1f}%" if max_pct > 0 else "0%"
            rows.append(
                html.Tr([
                    html.Td(f"{i + 1}", style={"width": "24px", "color": "#9ca3af", "fontSize": "0.73rem",
                        "fontWeight": "700", "textAlign": "right", "paddingRight": "8px", "verticalAlign": "middle"}),
                    html.Td(row["Mot-clé"], style={"fontSize": "0.82rem", "fontWeight": "500",
                        "maxWidth": "140px", "overflow": "hidden", "textOverflow": "ellipsis",
                        "whiteSpace": "nowrap", "verticalAlign": "middle", "paddingRight": "10px"}),
                    html.Td(
                        html.Div([
                            html.Div(
                                html.Div(style={"width": bar_width, "height": "100%",
                                    "backgroundColor": color, "borderRadius": "3px"}),
                                style={"width": "90px", "height": "8px", "backgroundColor": "rgba(0,0,0,0.07)",
                                    "borderRadius": "3px", "overflow": "hidden", "flexShrink": "0"}),
                            html.Span(f"{pct:.2f}%", style={"fontSize": "0.73rem", "color": "#374151",
                                "marginLeft": "7px", "fontWeight": "600", "minWidth": "42px"}),
                        ], style={"display": "flex", "alignItems": "center"}),
                        style={"verticalAlign": "middle"}),
                    html.Td(f"{int(row['Occurrences'])}", style={"fontSize": "0.73rem", "color": "#9ca3af",
                        "textAlign": "right", "verticalAlign": "middle", "paddingLeft": "8px"}),
                ], style={"borderBottom": "1px solid rgba(0,0,0,0.05)"})
            )

        table = html.Table([
            html.Thead(html.Tr([
                html.Th("#",         style={"width": "24px", "fontSize": "0.70rem", "color": "#9ca3af", "textAlign": "right", "paddingRight": "8px", "paddingBottom": "6px"}),
                html.Th("Mot-clé",   style={"fontSize": "0.70rem", "color": "#9ca3af", "paddingBottom": "6px"}),
                html.Th("Fréquence", style={"fontSize": "0.70rem", "color": "#9ca3af", "paddingBottom": "6px"}),
                html.Th("N",         style={"fontSize": "0.70rem", "color": "#9ca3af", "textAlign": "right", "paddingLeft": "8px", "paddingBottom": "6px"}),
            ], style={"borderBottom": "2px solid rgba(0,0,0,0.10)"})),
            html.Tbody(rows),
        ], style={"width": "100%", "borderCollapse": "collapse"})

        return img_src, table


    #     + duplication figure pour modal "plein écran interne"
    # ========================================================
    @app.callback(
        [
            Output("network", "figure"),
            Output("network-fullscreen", "figure"),
            Output("network-graph-data", "data"),
        ],
        [
            Input("centre", "value"),
            Input("equipe", "value"),
            Input("pays", "value"),
            Input("ville", "value"),
            Input("org", "value"),
            Input("annee", "value"),
            Input("tabs", "value"),
            Input("store-data", "data"),
            Input("network-max-pubs", "value"),
            Input("network-max-nodes", "value"),
            Input("toggle-dark", "n_clicks"),
        ],
    )
    def update_network(
        centres,
        equipes,
        pays,
        villes,
        orgs,
        annees,
        tab,
        stored_data,
        max_pubs,
        max_nodes,
        dark_clicks,
    ):
        # On ne dessine le réseau que dans l'onglet dédié
        if tab != "tab-network":
            return no_update, no_update, no_update

        # dataframe source (upload ou df de base)
        df = pd.DataFrame(stored_data) if stored_data is not None else df_base

        # Filtres globaux
        dff = filter_df(df, centres, equipes, pays, villes, orgs, annees)

        if dff.empty or "HalID" not in dff.columns:
            fig_empty = go.Figure()
            fig_empty.update_layout(
                template=GRAPH_TEMPLATE,
                title="Réseau de copublications (aucune donnée pour les filtres actuels)",
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",
                hovermode="closest",
                margin=dict(l=10, r=10, t=60, b=10),
            )
            return fig_empty, fig_empty

        # ---------------- Limitation nb de publications ----------------
        halids = dff["HalID"].dropna().unique().tolist()
        if max_pubs is None:
            max_pubs = 1500
        if len(halids) > max_pubs:
            halids_keep = pd.Series(halids).sample(max_pubs, random_state=42).tolist()
            dff_small = dff[dff["HalID"].isin(halids_keep)].copy()
        else:
            dff_small = dff.copy()

        # ------------ préparation des statistiques centres / auteurs ------------
        centres_stats = {}   # id_centre -> stats
        fr_stats = {}        # id_auteur_fr -> stats
        foreign_stats = {}   # id_auteur_etr -> stats
        edge_weights = {}    # (src, tgt) -> nb de copubs

        for _, row in dff_small.iterrows():
            centre_name = str(row.get("Centre", "") or "Centre Inria")
            centre_id = f"centre::{centre_name}"

            halid = row.get("HalID")
            country = str(row.get("Pays", "") or "Pays inconnu")
            org = str(row.get("Organisme_copubliant", "") or "").strip()

            # -- initialisation stats centre --
            c_stats = centres_stats.setdefault(
                centre_id,
                {
                    "type": "centre",
                    "label": centre_name,
                    "pubs": set(),
                    "fr_authors": set(),
                    "foreign_authors": set(),
                    "countries": set(),
                    "orgs": set(),
                },
            )
            if pd.notna(halid):
                c_stats["pubs"].add(halid)
            if country:
                c_stats["countries"].add(country)
            if org:
                c_stats["orgs"].add(org)

            fr_list = [a.strip() for a in str(row.get("Auteurs_FR", "")).split(";") if a.strip()]
            co_list = [a.strip() for a in str(row.get("Auteurs_copubliants", "")).split(";") if a.strip()]

            # -- auteurs Inria --
            for a in fr_list:
                fr_id = f"fr::{a}"
                st_fr = fr_stats.setdefault(
                    fr_id,
                    {"type": "fr", "label": a, "pubs": set(), "countries": set()},
                )
                if pd.notna(halid):
                    st_fr["pubs"].add(halid)
                if country:
                    st_fr["countries"].add(country)

                c_stats["fr_authors"].add(fr_id)

                key_cf = (centre_id, fr_id)
                edge_weights[key_cf] = edge_weights.get(key_cf, 0) + 1

            # -- auteurs étrangers --
            for b in co_list:
                foreign_id = f"foreign::{b}"
                st_fg = foreign_stats.setdefault(
                    foreign_id,
                    {"type": "foreign", "label": b, "pubs": set(), "country": country},
                )
                if pd.notna(halid):
                    st_fg["pubs"].add(halid)
                if country:
                    st_fg["country"] = country

                c_stats["foreign_authors"].add(foreign_id)

                # liens auteur Inria ↔ auteur étranger
                for a in fr_list:
                    fr_id = f"fr::{a}"
                    key_ff = (fr_id, foreign_id)
                    edge_weights[key_ff] = edge_weights.get(key_ff, 0) + 1

        # ------------- conversion des sets en nombres -------------
        for _, st in centres_stats.items():
            st["pubs"] = len(st["pubs"])
            st["nb_fr"] = len(st["fr_authors"])
            st["nb_foreign"] = len(st["foreign_authors"])
            st["nb_countries"] = len(st["countries"])
            st["nb_orgs"] = len(st["orgs"])

        for st in fr_stats.values():
            st["pubs"] = len(st["pubs"])
            st["nb_countries"] = len(st["countries"])

        for st in foreign_stats.values():
            st["pubs"] = len(st["pubs"])

        # ---------------- Tous les nœuds : centres + auteurs ----------------
        node_attrs = {}
        node_attrs.update(centres_stats)
        node_attrs.update(fr_stats)
        node_attrs.update(foreign_stats)

        filtered_edges = {
            (u, v): w
            for (u, v), w in edge_weights.items()
            if u in node_attrs and v in node_attrs
        }

        # ------------- construction du graphe NetworkX -------------
        G = nx.Graph()
        for nid, attr in node_attrs.items():
            G.add_node(nid, **attr)
        for (u, v), w in filtered_edges.items():
            G.add_edge(u, v, weight=w)

        if G.number_of_nodes() == 0:
            fig_empty = go.Figure().update_layout(
                template=GRAPH_TEMPLATE,
                title="Réseau de copublications (trop filtré / aucune donnée)",
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",
                hovermode="closest",
            )
            return fig_empty, fig_empty

        # --------- layout ressort 2D avec anti-chevauchement ----------
        k = 0.45 + 0.02 * math.log(G.number_of_nodes() + 1)
        pos = nx.spring_layout(G, k=k, iterations=80, seed=42)

        coords = np.array(list(pos.values()))
        max_abs = np.abs(coords).max()
        if max_abs > 0:
            coords = coords / max_abs

        rng = np.random.RandomState(42)
        coords = coords + 0.01 * rng.normal(size=coords.shape)

        n_nodes = len(coords)
        if n_nodes <= 1500:
            d_min = 0.03
            for _ in range(5):
                for i in range(n_nodes):
                    for j in range(i + 1, n_nodes):
                        diff = coords[i] - coords[j]
                        dist = np.linalg.norm(diff)
                        if 0 < dist < d_min:
                            push = (d_min - dist) / dist * 0.5 * diff
                            coords[i] += push
                            coords[j] -= push

        max_abs = np.abs(coords).max()
        if max_abs > 0:
            coords = coords / max_abs

        for nid, c in zip(pos.keys(), coords):
            pos[nid] = c

        # ── Fond selon le mode sombre (impair = sombre, pair/None = clair) ──
        is_dark = bool(dark_clicks) and (dark_clicks % 2 == 1)
        if is_dark:
            BG_NET          = "#0f1117"
            EDGE_NEUTRAL    = "rgba(180,180,200,0.15)"
            EDGE_ALPHA      = 0.25
            FG_COLOR        = "rgba(148,163,184,0.50)"
            LABEL_FR_COLOR  = "rgba(203,213,225,0.60)"
            LABEL_FG_COLOR  = "rgba(148,163,184,0.40)"
            TITLE_COLOR     = "#94a3b8"
            LEGEND_BG       = "rgba(10,12,20,0.88)"
            LEGEND_FG       = "#cbd5e1"
            LEGEND_BORDER   = "rgba(255,255,255,0.10)"
            ANNOT_BG        = "rgba(10,12,20,0.80)"
            ANNOT_FG        = "#94a3b8"
            TEXT_NODE_COLOR = "rgba(255,255,255,0.95)"
            HALO_ALPHA_OUT  = 0.05
            HALO_ALPHA_MID  = 0.18
            DISC_ALPHA      = 0.85
        else:
            BG_NET          = "#f8fafc"
            EDGE_NEUTRAL    = "rgba(100,100,130,0.12)"
            EDGE_ALPHA      = 0.35
            FG_COLOR        = "rgba(100,116,139,0.55)"
            LABEL_FR_COLOR  = "rgba(30,41,59,0.65)"
            LABEL_FG_COLOR  = "rgba(71,85,105,0.50)"
            TITLE_COLOR     = "#475569"
            LEGEND_BG       = "rgba(248,250,252,0.92)"
            LEGEND_FG       = "#334155"
            LEGEND_BORDER   = "rgba(0,0,0,0.10)"
            ANNOT_BG        = "rgba(248,250,252,0.88)"
            ANNOT_FG        = "#64748b"
            TEXT_NODE_COLOR = "rgba(255,255,255,0.95)"
            HALO_ALPHA_OUT  = 0.08
            HALO_ALPHA_MID  = 0.20
            DISC_ALPHA      = 0.90

        # ------------- Couleurs fixes par centre (défini EN PREMIER) -------------
        centre_names = sorted({a["label"] for a in node_attrs.values() if a["type"] == "centre"})
        centre_color_map = {
            name: get_centre_color(name, i)
            for i, name in enumerate(centre_names)
        }

        # Helper : hex → composantes RGB
        def _hex_rgb(hex_color):
            h = hex_color.lstrip("#")
            return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

        # ------------- Arêtes colorées par centre d'origine -------------
        edge_traces = []
        centre_edge_map = {}
        other_edges = []

        for u, v in G.edges():
            u_type = node_attrs.get(u, {}).get("type", "")
            v_type = node_attrs.get(v, {}).get("type", "")
            centre_id = None
            if u_type == "centre":
                centre_id = u
            elif v_type == "centre":
                centre_id = v
            elif u_type == "fr":
                for cid in centres_stats:
                    if u in centres_stats[cid].get("fr_authors", set()):
                        centre_id = cid
                        break
            if centre_id:
                centre_edge_map.setdefault(centre_id, []).append((u, v))
            else:
                other_edges.append((u, v))

        # Arêtes neutres
        if other_edges:
            ex, ey = [], []
            for u, v in other_edges:
                x0, y0 = pos[u]; x1, y1 = pos[v]
                ex += [x0, x1, None]; ey += [y0, y1, None]
            edge_traces.append(go.Scattergl(
                x=ex, y=ey, mode="lines",
                line=dict(width=0.5, color=EDGE_NEUTRAL),
                hoverinfo="none", showlegend=False,
            ))

        # Arêtes colorées par centre
        for cid, edges in centre_edge_map.items():
            centre_lbl = centres_stats[cid]["label"]
            c_hex = centre_color_map.get(centre_lbl, "#888888")
            r_, g_, b_ = _hex_rgb(c_hex)
            edge_color = f"rgba({r_},{g_},{b_},{EDGE_ALPHA})"
            ex, ey = [], []
            for u, v in edges:
                x0, y0 = pos[u]; x1, y1 = pos[v]
                ex += [x0, x1, None]; ey += [y0, y1, None]
            edge_traces.append(go.Scattergl(
                x=ex, y=ey, mode="lines",
                line=dict(width=0.6, color=edge_color),
                hoverinfo="none", showlegend=False,
            ))

        # ── Données enrichies pour chaque nœud (customdata JSON pour la fiche) ──
        import json as _json

        centre_x, centre_y, centre_size = [], [], []
        centre_outline, centre_label = [], []
        centre_hover, centre_custom = [], []

        fr_x, fr_y, fr_size, fr_color_list = [], [], [], []
        fr_labels_list, fr_hover_data, fr_custom = [], [], []

        fg_x, fg_y, fg_size = [], [], []
        fg_labels_list, fg_hover_data, fg_custom = [], [], []

        # Map auteur FR → centre
        fr_to_centre = {}
        for cid, cstats in centres_stats.items():
            for frid in cstats.get("fr_authors", set()):
                fr_to_centre[frid] = cstats["label"]

        for nid, attrs in node_attrs.items():
            x, y = pos[nid]
            ntype = attrs["type"]

            if ntype == "centre":
                c_hex = centre_color_map.get(attrs["label"], "#888888")
                r_, g_, b_ = _hex_rgb(c_hex)
                sz = 38 + 7 * math.sqrt(max(attrs["pubs"], 1))

                centre_x.append(x); centre_y.append(y)
                centre_label.append(attrs["label"])
                centre_outline.append(c_hex)
                centre_size.append(sz)

                # Hover texte riche
                hover_txt = (
                    f"<b style='font-size:13px'>🏛 {attrs['label']}</b><br>"
                    f"📄 <b>{attrs['pubs']}</b> publications<br>"
                    f"👤 <b>{attrs['nb_fr']}</b> auteurs Inria<br>"
                    f"🌍 <b>{attrs['nb_foreign']}</b> auteurs étrangers<br>"
                    f"🗺 <b>{attrs['nb_countries']}</b> pays · "
                    f"🏢 <b>{attrs['nb_orgs']}</b> organismes"
                )
                json_data = _json.dumps({
                    "type": "centre", "id": nid,
                    "label": attrs["label"],
                    "pubs": attrs["pubs"],
                    "nb_fr": attrs["nb_fr"],
                    "nb_foreign": attrs["nb_foreign"],
                    "nb_countries": attrs["nb_countries"],
                    "nb_orgs": attrs["nb_orgs"],
                    "color": c_hex,
                })
                centre_custom.append([hover_txt, json_data])

            elif ntype == "fr":
                centre_lbl = fr_to_centre.get(nid, "")
                c_hex = centre_color_map.get(centre_lbl, "#00bcd4")
                r_, g_, b_ = _hex_rgb(c_hex)

                fr_x.append(x); fr_y.append(y)
                fr_size.append(9 + 3.5 * math.sqrt(max(attrs["pubs"], 1)))
                fr_color_list.append(f"rgba({r_},{g_},{b_},0.90)")
                fr_labels_list.append(attrs["label"])

                hover_txt = (
                    f"<b>👤 {attrs['label']}</b><br>"
                    f"<i>{centre_lbl}</i><br>"
                    f"📄 <b>{attrs['pubs']}</b> pubs · "
                    f"🌍 <b>{attrs.get('nb_countries', 0)}</b> pays"
                )
                json_data = _json.dumps({
                    "type": "fr", "id": nid,
                    "label": attrs["label"],
                    "centre": centre_lbl,
                    "pubs": attrs["pubs"],
                    "nb_countries": attrs.get("nb_countries", 0),
                    "color": c_hex,
                })
                fr_hover_data.append(hover_txt)
                fr_custom.append([hover_txt, json_data])

            elif ntype == "foreign":
                fg_x.append(x); fg_y.append(y)
                fg_size.append(6 + 2.5 * math.sqrt(max(attrs["pubs"], 1)))
                fg_labels_list.append(attrs["label"])

                hover_txt = (
                    f"<b>🌐 {attrs['label']}</b><br>"
                    f"🗺 {attrs.get('country', '?')} · "
                    f"📄 <b>{attrs['pubs']}</b> pubs"
                )
                json_data = _json.dumps({
                    "type": "foreign", "id": nid,
                    "label": attrs["label"],
                    "country": attrs.get("country", "Inconnu"),
                    "pubs": attrs["pubs"],
                    "color": "#64748b",
                })
                fg_hover_data.append(hover_txt)
                fg_custom.append([hover_txt, json_data])

        # ═══════ RENDU GALAXIE ═══════════════════════════════════

        fg_trace = go.Scattergl(
            x=fg_x, y=fg_y, mode="markers",
            name="Auteurs étrangers",
            marker=dict(size=fg_size, color=FG_COLOR,
                        line=dict(width=0, color="rgba(0,0,0,0)")),
            customdata=fg_custom,
            hovertemplate="%{customdata[0]}<extra></extra>",
        )

        fr_trace = go.Scattergl(
            x=fr_x, y=fr_y, mode="markers",
            name="Auteurs Inria",
            marker=dict(size=fr_size, color=fr_color_list,
                        line=dict(width=0.4, color="rgba(255,255,255,0.25)"),
                        opacity=0.92),
            customdata=fr_custom,
            hovertemplate="%{customdata[0]}<extra></extra>",
        )

        # Halos centres
        halo_outer = go.Scattergl(
            x=centre_x, y=centre_y, mode="markers",
            marker=dict(
                size=[s * 3.2 for s in centre_size],
                color=[f"rgba({_hex_rgb(c)[0]},{_hex_rgb(c)[1]},{_hex_rgb(c)[2]},{HALO_ALPHA_OUT})"
                       for c in centre_outline],
                line=dict(width=0, color="rgba(0,0,0,0)"),
            ),
            hoverinfo="skip", showlegend=False,
        )
        halo_mid = go.Scattergl(
            x=centre_x, y=centre_y, mode="markers",
            marker=dict(
                size=[s * 1.9 for s in centre_size],
                color=[f"rgba({_hex_rgb(c)[0]},{_hex_rgb(c)[1]},{_hex_rgb(c)[2]},{HALO_ALPHA_MID})"
                       for c in centre_outline],
                line=dict(width=0, color="rgba(0,0,0,0)"),
            ),
            hoverinfo="skip", showlegend=False,
        )

        # Disque principal centre
        centre_trace = go.Scattergl(
            x=centre_x, y=centre_y, mode="markers+text",
            name="Centres Inria",
            marker=dict(
                size=centre_size,
                color=[f"rgba({_hex_rgb(c)[0]},{_hex_rgb(c)[1]},{_hex_rgb(c)[2]},{DISC_ALPHA})"
                       for c in centre_outline],
                line=dict(width=3.5, color=centre_outline),
            ),
            # Label affiché AU-DESSUS du nœud (pas dedans)
            text=[f"<b>{lbl}</b>" for lbl in centre_label],
            textposition="top center",
            textfont=dict(
                size=12,
                color=TEXT_NODE_COLOR,
                family="Open Sans, Arial, sans-serif",
            ),
            customdata=centre_custom,
            hovertemplate="%{customdata[0]}<extra></extra>",
        )

        # Fond coloré derrière le texte (halo du label)
        centre_label_bg = go.Scattergl(
            x=centre_x,
            y=[yi + 0.06 for yi in centre_y],   # légèrement au-dessus
            mode="markers",
            marker=dict(
                size=[max(len(lbl) * 7.5, 60) for lbl in centre_label],
                color=[f"rgba({_hex_rgb(c)[0]},{_hex_rgb(c)[1]},{_hex_rgb(c)[2]},0.70)"
                       for c in centre_outline],
                symbol="square",
                line=dict(width=0, color="rgba(0,0,0,0)"),
                opacity=1,
            ),
            hoverinfo="skip", showlegend=False,
        )

        # Labels auteurs (petits, au zoom)
        fr_labels_trace = go.Scattergl(
            x=fr_x, y=fr_y, mode="text", text=fr_labels_list,
            textfont=dict(size=6, color=LABEL_FR_COLOR),
            hoverinfo="skip", showlegend=False,
        )
        fg_labels_trace = go.Scattergl(
            x=fg_x, y=fg_y, mode="text", text=fg_labels_list,
            textfont=dict(size=6, color=LABEL_FG_COLOR),
            hoverinfo="skip", showlegend=False,
        )

        # Traces fantômes légende centres
        legend_traces = []
        for cname, chex in centre_color_map.items():
            r_, g_, b_ = _hex_rgb(chex)
            legend_traces.append(go.Scattergl(
                x=[None], y=[None], mode="markers", name=cname,
                marker=dict(size=11, color=f"rgba({r_},{g_},{b_},0.90)",
                            line=dict(width=1.5, color=chex)),
                showlegend=True,
            ))

        all_traces = (
            edge_traces
            + [halo_outer, halo_mid, fg_trace, fr_trace,
               centre_label_bg, centre_trace,
               fr_labels_trace, fg_labels_trace]
            + legend_traces
        )

        fig_net = go.Figure(data=all_traces)

        fig_net.update_layout(
            title=dict(
                text=(f"Réseau de copublications — "
                      f"<b>{G.number_of_nodes():,}</b> nœuds · "
                      f"<b>{G.number_of_edges():,}</b> liens"),
                font=dict(size=13, color=TITLE_COLOR,
                          family="Open Sans, Arial, sans-serif"),
                x=0.5, xanchor="center", pad=dict(t=4),
            ),
            showlegend=True,
            legend=dict(
                title=dict(text="<b>Centres Inria</b>",
                           font=dict(size=11, color=LEGEND_FG)),
                orientation="v",
                x=0.01, xanchor="left", y=0.99, yanchor="top",
                bgcolor=LEGEND_BG,
                bordercolor=LEGEND_BORDER, borderwidth=1,
                font=dict(size=10, color=LEGEND_FG),
                itemsizing="constant", tracegroupgap=1,
            ),
            xaxis=dict(showgrid=False, zeroline=False, visible=False),
            yaxis=dict(showgrid=False, zeroline=False, visible=False,
                       scaleanchor="x", scaleratio=1),
            margin=dict(l=0, r=0, t=45, b=55),
            hovermode="closest",
            paper_bgcolor=BG_NET,
            plot_bgcolor=BG_NET,
            hoverlabel=dict(
                bgcolor="#1e293b", font_size=12,
                font_color="#f1f5f9",
                bordercolor="rgba(255,255,255,0.18)", namelength=0,
            ),
            clickmode="event",
            annotations=[dict(
                x=0.5, y=-0.005, xref="paper", yref="paper",
                xanchor="center", yanchor="top",
                text=(
                    f"<b style='color:{LEGEND_FG}'>Types :</b>"
                    " &nbsp;<span style='color:#60a5fa'>⬤</span> Auteurs Inria (couleur = centre)"
                    " &nbsp;<span style='color:#64748b'>⬤</span> Auteurs étrangers"
                    " &nbsp;<span style='color:#94a3b8'>◯</span> Centre Inria"
                    " &nbsp;— Cliquez sur un nœud pour sa fiche"
                ),
                showarrow=False,
                font=dict(size=10, color=ANNOT_FG),
                bgcolor=ANNOT_BG,
                bordercolor=LEGEND_BORDER,
                borderwidth=1, borderpad=8,
            )],
        )
        fig_net.layout.hovermode = "closest"

        # ── Store de données pour l'interactivité clientside ──
        import json as _json
        node_lookup = {}
        for nid, attrs in node_attrs.items():
            ntype = attrs["type"]
            if ntype == "centre":
                node_lookup[attrs["label"]] = {
                    "type": "centre",
                    "label": attrs["label"],
                    "pubs": attrs["pubs"],
                    "nb_fr": attrs["nb_fr"],
                    "nb_foreign": attrs["nb_foreign"],
                    "nb_countries": attrs["nb_countries"],
                    "nb_orgs": attrs["nb_orgs"],
                    "color": centre_color_map.get(attrs["label"], "#888888"),
                }
            elif ntype == "fr":
                centre_lbl = fr_to_centre.get(nid, "")
                node_lookup[attrs["label"]] = {
                    "type": "fr",
                    "label": attrs["label"],
                    "centre": centre_lbl,
                    "pubs": attrs["pubs"],
                    "nb_countries": attrs.get("nb_countries", 0),
                    "color": centre_color_map.get(centre_lbl, "#00bcd4"),
                }
            elif ntype == "foreign":
                node_lookup[attrs["label"]] = {
                    "type": "foreign",
                    "label": attrs["label"],
                    "country": attrs.get("country", "Inconnu"),
                    "pubs": attrs["pubs"],
                    "color": "#64748b",
                }

        # Même figure dans la vue "plein écran"
        return fig_net, fig_net, node_lookup

    # ========================================================
    # 3bis — FICHE NŒUD (clic sur un nœud) — callback Python
    # ========================================================
    @app.callback(
        Output("network-node-panel", "children"),
        Input("network", "clickData"),
        State("network-graph-data", "data"),
        prevent_initial_call=True,
    )
    def update_node_panel(click_data, node_lookup):
        from network_tab import _empty_panel

        if not click_data or not node_lookup:
            return _empty_panel()

        try:
            pt = click_data["points"][0]
        except (KeyError, IndexError):
            return _empty_panel()

        # Récupérer le nom du nœud depuis le texte ou le customdata
        # On essaie d'abord "text" (labels des centres), puis "hovertext"
        name = pt.get("text") or pt.get("hovertext") or ""

        # Si customdata disponible, lire la 2e colonne (JSON)
        raw = pt.get("customdata")
        data = None

        if isinstance(raw, (list, tuple)) and len(raw) >= 2:
            try:
                import json as _json
                data = _json.loads(str(raw[1]))
            except Exception:
                pass
        if data is None and isinstance(raw, str):
            try:
                import json as _json
                data = _json.loads(raw)
            except Exception:
                pass

        # Fallback : chercher dans le store par nom
        if data is None and name and node_lookup:
            data = node_lookup.get(name)

        if data is None:
            return _empty_panel()

        ntype = data.get("type", "")
        color = data.get("color", "#27348b")

        header_style = {
            "background": f"linear-gradient(135deg, {color}22 0%, {color}08 100%)",
            "borderBottom": f"3px solid {color}",
            "padding": "12px 14px",
            "borderRadius": "14px 14px 0 0",
        }

        def _badge(label, bg=None):
            return html.Span(label, style={
                "backgroundColor": bg or color,
                "color": "white",
                "padding": "3px 10px",
                "borderRadius": "20px",
                "fontSize": "0.72rem",
                "fontWeight": "700",
                "display": "inline-block",
                "marginBottom": "6px",
            })

        def _row(icon, label, value):
            return html.Div([
                html.Span(icon + " "),
                html.Span(label + " : ", className="text-muted small"),
                html.Strong(str(value)),
            ], className="mb-2 small")

        if ntype == "centre":
            body = [
                html.Div([
                    _badge("🏛 Centre Inria"),
                    html.H5(data["label"], className="fw-bold mb-0 mt-1",
                            style={"color": color, "fontSize": "1rem", "wordBreak": "break-word"}),
                ], style=header_style),
                dbc.CardBody([
                    _row("📄", "Publications", f"{data['pubs']:,}"),
                    _row("👤", "Auteurs Inria", f"{data['nb_fr']:,}"),
                    _row("🌍", "Auteurs étrangers", f"{data['nb_foreign']:,}"),
                    _row("🗺", "Pays partenaires", f"{data['nb_countries']:,}"),
                    _row("🏢", "Organismes", f"{data['nb_orgs']:,}"),
                ], style={"padding": "12px 14px"}),
            ]

        elif ntype == "fr":
            body = [
                html.Div([
                    _badge("👤 Auteur Inria"),
                    html.H5(data["label"], className="fw-bold mb-0 mt-1",
                            style={"color": color, "fontSize": "1rem", "wordBreak": "break-word"}),
                ], style=header_style),
                dbc.CardBody([
                    _row("🏛", "Centre", data.get("centre", "—")),
                    _row("📄", "Publications", f"{data['pubs']:,}"),
                    _row("🌍", "Pays partenaires", f"{data.get('nb_countries', 0):,}"),
                ], style={"padding": "12px 14px"}),
            ]

        elif ntype == "foreign":
            body = [
                html.Div([
                    _badge("🌐 Auteur étranger", "#64748b"),
                    html.H5(data["label"], className="fw-bold mb-0 mt-1",
                            style={"color": "#334155", "fontSize": "1rem", "wordBreak": "break-word"}),
                ], style={**header_style,
                           "background": "linear-gradient(135deg, #64748b22 0%, #64748b08 100%)",
                           "borderBottom": "3px solid #64748b"}),
                dbc.CardBody([
                    _row("🗺", "Pays", data.get("country", "—")),
                    _row("📄", "Publications", f"{data['pubs']:,}"),
                ], style={"padding": "12px 14px"}),
            ]

        else:
            return _empty_panel()

        return dbc.Card(body, className="shadow-sm", style={
            "borderRadius": "16px",
            "border": f"1px solid {color}40",
            "overflow": "hidden",
        })


    @app.callback(
        Output("network-fullscreen-modal", "style"),
        [
            Input("btn-network-fullscreen-open", "n_clicks"),
            Input("btn-network-fullscreen-close", "n_clicks"),
        ],
        State("network-fullscreen-modal", "style"),
        prevent_initial_call=True,
    )
    def toggle_network_fullscreen(open_clicks, close_clicks, current_style):
        import dash  # (évite d'ajouter un import global si tu préfères)

        ctx = dash.callback_context
        if not ctx.triggered:
            return current_style

        trigger = ctx.triggered[0]["prop_id"].split(".")[0]

        style_open = {
            "display": "block",
            "position": "fixed",
            "inset": "0",
            "background": "rgba(0,0,0,0.35)",
            "zIndex": "9999",
            "padding": "24px",
        }
        style_closed = {**style_open, "display": "none"}

        if trigger == "btn-network-fullscreen-open":
            return style_open
        if trigger == "btn-network-fullscreen-close":
            return style_closed

        return current_style


    # ========================================================
    # 4 — Onglet "Évolution des copublications"
    # ========================================================
    @app.callback(
        [
            Output("sunburst_collab", "figure"),
            Output("team_timeline", "figure"),
            Output("sankey_collab", "figure"),
            Output("radar_centre", "figure"),
            Output("story_evol", "children"),
        ],
        [
            Input("centre", "value"),
            Input("equipe", "value"),
            Input("pays", "value"),
            Input("ville", "value"),
            Input("org", "value"),
            Input("annee", "value"),
            Input("tabs", "value"),
            Input("store-data", "data"),
        ],
    )
    def update_evolution(
        centres, equipes, pays, villes, orgs, annees, tab, stored_data
    ):
        # On ne calcule l'onglet que lorsqu'il est actif
        if tab != "tab-evolution":
            return no_update, no_update, no_update, no_update, no_update

        # Choix du dataframe (CSV chargé ou df initial)
        df = pd.DataFrame(stored_data) if stored_data is not None else df_base
        dff = filter_df(df, centres, equipes, pays, villes, orgs, annees)

        # ---------- 0) Cas sans données ----------
        if dff.empty:
            empty_fig = go.Figure().update_layout(
                template=GRAPH_TEMPLATE,
                title="Aucune donnée pour les filtres actuels",
            )
            story_div = html.Div(
                [
                    html.H5(
                        "Résumé des copublications",
                        className="mb-2",
                        style={"color": PRIMARY},
                    ),
                    html.P(
                        "Aucune copublication n’est disponible pour les filtres sélectionnés.",
                        className="mb-1",
                    ),
                ],
                style={
                    "backgroundColor": "#f8fbff",
                    "borderRadius": "12px",
                    "border": f"1px solid {PRIMARY_LIGHT}30",
                },
            )
            return empty_fig, empty_fig, empty_fig, empty_fig, story_div

        # =========================================================================
        # 1) SUNBURST Centre → Équipe → Organisme
        # =========================================================================
        if all(col in dff.columns for col in ["Centre", "Equipe", "Organisme_copubliant"]):
            sun_df = (
                dff.groupby(["Centre", "Equipe", "Organisme_copubliant"])["HalID"]
                .nunique()
                .reset_index(name="Publications")
            )

            # Mapping couleur fixe pour les centres présents
            centres_present = sun_df["Centre"].unique().tolist()
            colour_map_sun = {c: get_centre_color(c, i) for i, c in enumerate(centres_present)}

            fig_sunburst = px.sunburst(
                sun_df,
                path=["Centre", "Equipe", "Organisme_copubliant"],
                values="Publications",
                color="Centre",
                color_discrete_map=colour_map_sun,
                title="Centre → Équipe → Organisme",
            )
            fig_sunburst.update_layout(template=GRAPH_TEMPLATE)
        else:
            fig_sunburst = go.Figure().update_layout(
                template=GRAPH_TEMPLATE,
                title="Hiérarchie collaborations (colonnes manquantes)",
            )

        # =========================================================================
        # 2) TEAM TIMELINE : évolution des copublications par équipe
        # =========================================================================
        if all(col in dff.columns for col in ["Année", "Equipe"]):
            team_df = (
                dff.groupby(["Année", "Equipe"])["HalID"]
                .nunique()
                .reset_index(name="Publications")
            )

            fig_team = px.line(
                team_df,
                x="Année",
                y="Publications",
                color="Equipe",
                markers=True,
                color_discrete_sequence=QUAL_PALETTE,
                title="Évolution des copublications par équipe",
            )
            fig_team.update_layout(
                template=GRAPH_TEMPLATE,
                hovermode="x unified",
            )
        else:
            fig_team = go.Figure().update_layout(
                template=GRAPH_TEMPLATE,
                title="Évolution par équipe (colonnes manquantes)",
            )

        # =========================================================================
        # 3) SANKEY Centre → Pays → Organisme
        # =========================================================================
        if all(col in dff.columns for col in ["Centre", "Pays", "Organisme_copubliant"]):
            sankey_df = (
                dff.groupby(["Centre", "Pays", "Organisme_copubliant"])["HalID"]
                .nunique()
                .reset_index(name="Publications")
                .sort_values("Publications", ascending=False)
                .head(80)
            )

            labels = []
            node_index = {}

            def get_index(label):
                if label not in node_index:
                    node_index[label] = len(node_index)
                    labels.append(label)
                return node_index[label]

            sources, targets, values = [], [], []

            for _, row in sankey_df.iterrows():
                c = get_index(f"Centre : {row['Centre']}")
                p = get_index(f"Pays : {row['Pays']}")
                o = get_index(f"Org : {row['Organisme_copubliant']}")
                v = row["Publications"]

                sources.append(c)
                targets.append(p)
                values.append(v)

                sources.append(p)
                targets.append(o)
                values.append(v)

            # Couleurs des nœuds : fixe pour les centres, neutre pour pays/org
            def _sankey_node_color(label: str) -> str:
                if label.startswith("Centre : "):
                    centre_name = label[len("Centre : "):]
                    return get_centre_color(centre_name, 0)
                elif label.startswith("Pays : "):
                    return "rgba(100,130,200,0.70)"
                else:
                    return "rgba(160,160,160,0.55)"

            fig_sankey = go.Figure(
                data=[
                    go.Sankey(
                        node=dict(
                            pad=15,
                            thickness=15,
                            line=dict(color="black", width=0.3),
                            label=labels,
                            color=[_sankey_node_color(lbl) for lbl in labels],
                        ),
                        link=dict(
                            source=sources,
                            target=targets,
                            value=values,
                            color="rgba(39,52,139,0.2)",
                        ),
                    )
                ]
            )
            fig_sankey.update_layout(
                template=GRAPH_TEMPLATE,
                title="Flux Centre → Pays → Organisme",
            )
        else:
            fig_sankey = go.Figure().update_layout(
                template=GRAPH_TEMPLATE,
                title="Flux Centre → Pays → Organisme (colonnes manquantes)",
            )

        # =========================================================================
        # 4) RADAR MULTI-CENTRES PAR DOMAINES
        # =========================================================================
        if "Centre" in dff.columns and "Domaine(s)" in dff.columns:
            dom_df = (
                dff.dropna(subset=["Centre", "Domaine(s)"])
                .groupby(["Centre", "Domaine(s)"])["HalID"]
                .nunique()
                .reset_index(name="Publications")
            )

            if dom_df.empty:
                fig_radar = go.Figure().update_layout(
                    template=GRAPH_TEMPLATE,
                    title="Profil par domaine (aucune donnée domaine)",
                )
            else:
                # ── Centres à tracer ──
                if centres:
                    centres_to_plot = [
                        c for c in centres if c in dom_df["Centre"].unique()
                    ]
                else:
                    centres_to_plot = (
                        dom_df.groupby("Centre")["Publications"]
                        .sum()
                        .sort_values(ascending=False)
                        .head(5)
                        .index.tolist()
                    )
                if not centres_to_plot:
                    centres_to_plot = (
                        dom_df.groupby("Centre")["Publications"]
                        .sum()
                        .sort_values(ascending=False)
                        .head(5)
                        .index.tolist()
                    )

                # ── Top domaines — on prend jusqu'à 8 pour plus de détail ──
                top_dom = (
                    dom_df.groupby("Domaine(s)")["Publications"]
                    .sum()
                    .sort_values(ascending=False)
                    .head(8)
                    .index.tolist()
                )

                # ── Labels : on garde les noms complets, le wrapping se fait au layout ──
                categories_raw    = top_dom
                categories_closed = categories_raw + categories_raw[:1]

                # ── Normalisation en % pour comparer centres de tailles différentes ──
                centre_totals = (
                    dom_df[dom_df["Centre"].isin(centres_to_plot)]
                    .groupby("Centre")["Publications"]
                    .sum()
                    .to_dict()
                )

                fig_radar = go.Figure()

                for i, centre in enumerate(centres_to_plot):
                    sub   = dom_df[dom_df["Centre"] == centre]
                    total = centre_totals.get(centre, 1) or 1
                    vals  = [
                        round(
                            sub.loc[sub["Domaine(s)"] == dom, "Publications"].sum()
                            / total * 100,
                            1,
                        )
                        for dom in categories_raw
                    ]
                    vals_closed = vals + vals[:1]

                    color = get_centre_color(centre, i)

                    # Conversion hex → rgba pour le remplissage
                    def _hex_to_rgba(hex_color, alpha=0.15):
                        h = hex_color.lstrip("#")
                        if len(h) == 3:
                            h = "".join([c * 2 for c in h])
                        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
                        return f"rgba({r},{g},{b},{alpha})"

                    fig_radar.add_trace(
                        go.Scatterpolar(
                            r=vals_closed,
                            theta=categories_closed,
                            fill="toself",
                            name=centre,
                            line=dict(
                                color=color,
                                width=2.5,
                            ),
                            fillcolor=_hex_to_rgba(color, 0.15),
                            opacity=1,
                            hovertemplate=(
                                "<b>" + centre + "</b><br>"
                                "%{theta} : <b>%{r:.1f} %</b><extra></extra>"
                            ),
                        )
                    )

                # ── Titre court (noms des centres sur une seule ligne si possible) ──
                if len(centres_to_plot) <= 3:
                    titre_centres = " · ".join(centres_to_plot)
                else:
                    titre_centres = f"{len(centres_to_plot)} centres"

                # ── Labels avec retour à la ligne pour les noms longs ──
                def _wrap_label(s, maxlen=18):
                    """Coupe le label en plusieurs lignes de maxlen caractères max."""
                    s = str(s).strip()
                    if len(s) <= maxlen:
                        return s
                    # Découpe sur les espaces
                    words = s.split()
                    lines, current = [], ""
                    for w in words:
                        if len(current) + len(w) + 1 <= maxlen:
                            current = (current + " " + w).strip()
                        else:
                            if current:
                                lines.append(current)
                            current = w
                    if current:
                        lines.append(current)
                    return "<br>".join(lines)

                categories_wrapped = [_wrap_label(d) for d in categories_raw]
                categories_closed_wrapped = categories_wrapped + categories_wrapped[:1]

                # Mise à jour des traces avec les labels wrappés
                for trace in fig_radar.data:
                    trace.theta = categories_closed_wrapped

                fig_radar.update_layout(
                    template=GRAPH_TEMPLATE,
                    title=dict(
                        text=f"Profil par domaine — {titre_centres}",
                        font=dict(size=13),
                        x=0.5,
                        xanchor="center",
                        pad=dict(b=6),
                    ),
                    polar=dict(
                        # Zone polaire réduite pour laisser la place aux labels
                        domain=dict(x=[0.12, 0.88], y=[0.10, 0.92]),
                        bgcolor="rgba(240,244,255,0.45)",
                        radialaxis=dict(
                            visible=True,
                            ticksuffix="%",
                            tickfont=dict(size=9, color="#6b7280"),
                            gridcolor="rgba(0,0,0,0.10)",
                            linecolor="rgba(0,0,0,0.12)",
                            range=[0, None],
                            showline=True,
                            tickangle=0,
                        ),
                        angularaxis=dict(
                            tickfont=dict(
                                size=10,
                                color=PRIMARY,
                                family="Open Sans, Arial, sans-serif",
                            ),
                            linecolor="rgba(0,0,0,0.15)",
                            gridcolor="rgba(0,0,0,0.08)",
                            rotation=90,
                            direction="clockwise",
                        ),
                    ),
                    legend=dict(
                        orientation="h",
                        x=0.5,
                        xanchor="center",
                        y=-0.05,
                        yanchor="top",
                        font=dict(size=11),
                        bgcolor="rgba(255,255,255,0.85)",
                        bordercolor="rgba(0,0,0,0.08)",
                        borderwidth=1,
                    ),
                    margin=dict(l=110, r=110, t=60, b=80),
                    hoverlabel=dict(
                        bgcolor="white",
                        font_size=12,
                        font_color=PRIMARY,
                    ),
                )

        else:
            fig_radar = go.Figure().update_layout(
                template=GRAPH_TEMPLATE,
                title="Profil par domaine (colonnes Centre / Domaine(s) manquantes)",
            )

        # =========================================================================
        # 5) STORY MODE (résumé textuel)
        # =========================================================================
        total_pubs = dff["HalID"].nunique() if "HalID" in dff.columns else len(dff)
        nb_pays = dff["Pays"].nunique() if "Pays" in dff.columns else 0
        nb_orgs = (
            dff["Organisme_copubliant"].nunique()
            if "Organisme_copubliant" in dff.columns
            else 0
        )
        years = (
            dff["Année"].dropna().astype(int)
            if "Année" in dff.columns
            else pd.Series([], dtype=int)
        )
        if len(years) > 0:
            an_min, an_max = int(years.min()), int(years.max())
            periode = f"{an_min}–{an_max}"
        else:
            periode = "période inconnue"

        # Centres principaux pour le texte
        centres_present = (
            dff["Centre"].dropna().unique().tolist()
            if "Centre" in dff.columns
            else []
        )
        if centres and centres_present:
            centres_story = [c for c in centres if c in centres_present]
        else:
            centres_story = centres_present

        if len(centres_story) == 0:
            centres_txt = "les centres Inria impliqués"
        elif len(centres_story) == 1:
            centres_txt = f"le centre {centres_story[0]}"
        else:
            centres_txt = "les centres " + ", ".join(centres_story)

        story_children = [
            html.H5(
                "Résumé des copublications",
                className="mb-2",
                style={"color": PRIMARY},
            ),
            html.P(
                f"Sur la période {periode}, les filtres actuels représentent "
                f"{total_pubs} copublications impliquant {nb_pays} pays "
                f"et {nb_orgs} organismes partenaires.",
                className="mb-1",
            ),
            html.P(
                f"Les profils par domaine et les flux décrits ci-dessus mettent en évidence le rôle de {centres_txt}.",
                className="mb-0",
            ),
        ]

        story_div = html.Div(
            story_children,
            style={
                "backgroundColor": "#f8fbff",
                "borderRadius": "12px",
                "border": f"1px solid {PRIMARY_LIGHT}30",
            },
        )

        return fig_sunburst, fig_team, fig_sankey, fig_radar, story_div

    # ========================================================
    # 5 — Onglet "Évolution par pays"
    # ========================================================
    @app.callback(
        [
            Output("country_line_chart", "figure"),
            Output("country_heatmap", "figure"),
            Output("country_top_bar", "figure"),
        ],
        [
            Input("centre", "value"),
            Input("equipe", "value"),
            Input("pays", "value"),
            Input("ville", "value"),
            Input("org", "value"),
            Input("annee", "value"),
            Input("tabs", "value"),
            Input("store-data", "data"),
            Input("country-top-n", "value"),
        ],
    )
    def update_country_evolution(
        centres, equipes, pays, villes, orgs, annees, tab, stored_data, top_n
    ):
        if tab != "tab-country-evolution":
            return no_update, no_update, no_update

        df = pd.DataFrame(stored_data) if stored_data is not None else df_base
        dff = filter_df(df, centres, equipes, pays, villes, orgs, annees)

        if top_n is None:
            top_n = 10

        empty_fig = go.Figure().update_layout(
            template=GRAPH_TEMPLATE,
            title="Aucune donnée pour les filtres actuels",
        )

        if dff.empty or "Pays" not in dff.columns or "Année" not in dff.columns:
            return empty_fig, empty_fig, empty_fig

        # ── Top N pays (par volume total) ──
        top_pays_list = (
            dff.groupby("Pays")["HalID"]
            .nunique()
            .sort_values(ascending=False)
            .head(top_n)
            .index.tolist()
        )
        dff_top = dff[dff["Pays"].isin(top_pays_list)]

        # ── 1) Graphique ligne : évolution par an et par pays ──
        line_df = (
            dff_top.groupby(["Année", "Pays"])["HalID"]
            .nunique()
            .reset_index(name="Publications")
            .sort_values("Année")
        )

        if line_df.empty:
            fig_line = empty_fig
        else:
            fig_line = px.line(
                line_df,
                x="Année",
                y="Publications",
                color="Pays",
                markers=True,
                color_discrete_sequence=QUAL_PALETTE,
                title=f"Évolution annuelle des copublications – Top {top_n} pays",
            )
            fig_line.update_traces(line=dict(width=2.5), marker=dict(size=7))
            fig_line.update_layout(
                template=GRAPH_TEMPLATE,
                hovermode="x unified",
                legend=dict(
                    orientation="v",
                    x=1.02,
                    xanchor="left",
                    y=1,
                    yanchor="top",
                    font=dict(size=10),
                    bgcolor="rgba(255,255,255,0.85)",
                ),
                margin=dict(l=10, r=10, t=50, b=40),
            )

        # ── 2) Heatmap pays × année ──
        pivot_df = (
            dff_top.groupby(["Pays", "Année"])["HalID"]
            .nunique()
            .unstack(fill_value=0)
        )

        if pivot_df.empty:
            fig_heatmap = empty_fig
        else:
            # Trier les pays par total décroissant
            pivot_df = pivot_df.loc[
                pivot_df.sum(axis=1).sort_values(ascending=False).index
            ]
            years_cols = sorted(pivot_df.columns.tolist())
            pivot_df = pivot_df[years_cols]

            fig_heatmap = go.Figure(
                go.Heatmap(
                    z=pivot_df.values,
                    x=[str(int(y)) for y in years_cols],
                    y=pivot_df.index.tolist(),
                    colorscale=[
                        [0, "#ccedf6"],
                        [0.4, "#00a5cc"],
                        [0.7, "#1067a3"],
                        [1, "#27348b"],
                    ],
                    hovertemplate=(
                        "Pays : %{y}<br>Année : %{x}<br>Publications : %{z}<extra></extra>"
                    ),
                    showscale=True,
                )
            )
            fig_heatmap.update_layout(
                template=GRAPH_TEMPLATE,
                title=f"Heatmap des copublications – Top {top_n} pays × année",
                xaxis=dict(title="Année", tickangle=-35),
                yaxis=dict(title=""),
                margin=dict(l=10, r=10, t=50, b=40),
            )

        # ── 3) Barres horizontales : volume total par pays ──
        bar_df = (
            dff_top.groupby("Pays")["HalID"]
            .nunique()
            .reset_index(name="Publications")
            .sort_values("Publications", ascending=True)
        )

        if bar_df.empty:
            fig_bar = empty_fig
        else:
            colors_bar = [QUAL_PALETTE[i % len(QUAL_PALETTE)] for i in range(len(bar_df))]
            fig_bar = go.Figure(
                go.Bar(
                    x=bar_df["Publications"],
                    y=bar_df["Pays"],
                    orientation="h",
                    marker=dict(color=colors_bar, line=dict(width=0)),
                    hovertemplate="Pays : %{y}<br>Publications : %{x}<extra></extra>",
                    text=bar_df["Publications"],
                    textposition="outside",
                )
            )
            fig_bar.update_layout(
                template=GRAPH_TEMPLATE,
                title=f"Volume total – Top {top_n} pays",
                xaxis=dict(title="Publications"),
                yaxis=dict(title=""),
                margin=dict(l=10, r=10, t=50, b=40),
                showlegend=False,
            )

        return fig_line, fig_heatmap, fig_bar

    # ========================================================
    # 6 — ONGLET PARTS RELATIVES (% du total)
    # ========================================================
    @app.callback(
        [
            Output("share-pays",    "figure"),
            Output("share-centre",  "figure"),
            Output("share-org",     "figure"),
            Output("share-equipe",  "figure"),
            Output("share-evol",    "figure"),
            Output("share-kpi-zone","children"),
        ],
        [
            Input("centre",      "value"),
            Input("equipe",      "value"),
            Input("pays",        "value"),
            Input("ville",       "value"),
            Input("org",         "value"),
            Input("annee",       "value"),
            Input("tabs",        "value"),
            Input("store-data",  "data"),
        ],
    )
    def update_share(centres, equipes, pays, villes, orgs, annees, tab, stored_data):
        if tab != "tab-share":
            return (no_update,) * 6

        df  = pd.DataFrame(stored_data) if stored_data is not None else df_base
        dff = filter_df(df, centres, equipes, pays, villes, orgs, annees)

        # ── Total global (sans aucun filtre, juste les années si précisées) ──
        df_global = filter_df(df, None, None, None, None, None, annees)
        total_global = df_global["HalID"].nunique() if not df_global.empty else 1
        total_sel    = dff["HalID"].nunique()

        empty_fig = go.Figure().update_layout(
            template=GRAPH_TEMPLATE,
            title="Aucune sélection ou donnée insuffisante",
        )

        # ────────────────────────────────────────────────────────
        # Fonction utilitaire : donut part sélection vs reste
        # ────────────────────────────────────────────────────────
        def _donut_share(df_sel, col, filtre_vals, label_col=None):
            """
            Pour chaque valeur dans filtre_vals, calcule le % par rapport
            au total global. Retourne un donut ou un bar horizontal.
            """
            if df_sel.empty or col not in df_sel.columns:
                return empty_fig

            lbl = label_col or col

            if filtre_vals:
                # Sélection explicite : on montre chaque valeur + "Reste"
                rows = []
                for val in filtre_vals:
                    sub = df_sel[df_sel[col].astype(str) == str(val)]
                    n   = sub["HalID"].nunique()
                    rows.append({"label": str(val), "n": n, "pct": n / total_global * 100})
                n_sel  = sum(r["n"] for r in rows)
                n_rest = max(total_global - n_sel, 0)
                rows.append({"label": "Reste (non sélectionné)", "n": n_rest,
                             "pct": n_rest / total_global * 100})

                labels = [r["label"] for r in rows]
                values = [r["pct"]   for r in rows]
                # Couleur fixe si col == Centre, sinon QUAL_PALETTE
                if col == "Centre":
                    colors = (
                        [get_centre_color(r["label"], i) for i, r in enumerate(rows[:-1])]
                        + ["rgba(200,200,200,0.35)"]
                    )
                else:
                    colors = (
                        [QUAL_PALETTE[i % len(QUAL_PALETTE)] for i in range(len(rows) - 1)]
                        + ["rgba(200,200,200,0.35)"]
                    )
                pull   = [0.06] * (len(rows) - 1) + [0]

                fig = go.Figure(go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.52,
                    marker=dict(colors=colors),
                    pull=pull,
                    textinfo="percent",
                    hovertemplate="%{label}<br>Part : <b>%{value:.2f}%</b><extra></extra>",
                    sort=False,
                ))
            else:
                # Pas de sélection explicite → top 8 valeurs du df filtré
                grp = (
                    df_sel.groupby(col)["HalID"]
                    .nunique()
                    .sort_values(ascending=False)
                    .head(8)
                    .reset_index(name="n")
                )
                grp["pct"] = grp["n"] / total_global * 100
                n_shown  = grp["n"].sum()
                n_autres = max(total_global - n_shown, 0)
                grp = pd.concat([
                    grp,
                    pd.DataFrame([{col: "Autres / non sélectionnés", "n": n_autres,
                                   "pct": n_autres / total_global * 100}])
                ], ignore_index=True)

                if col == "Centre":
                    colors = (
                        [get_centre_color(str(grp.iloc[i][col]), i) for i in range(len(grp) - 1)]
                        + ["rgba(200,200,200,0.35)"]
                    )
                else:
                    colors = (
                        [QUAL_PALETTE[i % len(QUAL_PALETTE)] for i in range(len(grp) - 1)]
                        + ["rgba(200,200,200,0.35)"]
                    )
                fig = go.Figure(go.Pie(
                    labels=grp[col].astype(str),
                    values=grp["pct"],
                    hole=0.52,
                    marker=dict(colors=colors),
                    textinfo="percent",
                    hovertemplate="%{label}<br>Part : <b>%{value:.2f}%</b><extra></extra>",
                    sort=False,
                ))

            fig.update_layout(
                template=GRAPH_TEMPLATE,
                title=None,
                showlegend=True,
                legend=dict(
                    orientation="v",
                    x=1.02, xanchor="left",
                    y=0.5,  yanchor="middle",
                    font=dict(size=10),
                    bgcolor="rgba(255,255,255,0.85)",
                ),
                margin=dict(l=10, r=10, t=10, b=10),
                annotations=[dict(
                    text=f"<b>{total_sel / total_global * 100:.1f}%</b><br>sélection",
                    x=0.5, y=0.5, font_size=13,
                    showarrow=False,
                )],
            )
            return fig

        fig_pays   = _donut_share(dff, "Pays",                 pays)
        fig_centre = _donut_share(dff, "Centre",               centres)
        fig_org    = _donut_share(dff, "Organisme_copubliant", orgs)
        fig_equipe = _donut_share(dff, "Equipe",               equipes)

        # ────────────────────────────────────────────────────────
        # Évolution annuelle de la part (%)
        # ────────────────────────────────────────────────────────
        if "Année" not in dff.columns or dff.empty:
            fig_evol = empty_fig
        else:
            # Total global par année
            ann_global = (
                df_global.groupby("Année")["HalID"]
                .nunique()
                .reset_index(name="Total_global")
            )

            # Dimensions à tracer : celles pour lesquelles un filtre est actif
            traces_def = []
            if pays:
                traces_def.append(("Pays",                 pays,    "Pays"))
            if centres:
                traces_def.append(("Centre",               centres, "Centre"))
            if orgs:
                traces_def.append(("Organisme_copubliant", orgs,    "Organisme"))
            if equipes:
                traces_def.append(("Equipe",               equipes, "Équipe"))
            if villes:
                traces_def.append(("Ville",                villes,  "Ville"))
            # Si aucun filtre dimensionnel : on trace la sélection globale vs total
            if not traces_def:
                traces_def = [("__global__", None, "Sélection")]

            fig_evol = go.Figure()
            color_idx = 0

            for col, vals, dim_label in traces_def:
                if col == "__global__":
                    ann_sel = (
                        dff.groupby("Année")["HalID"]
                        .nunique()
                        .reset_index(name="n_sel")
                    )
                    merged = ann_sel.merge(ann_global, on="Année", how="left")
                    merged["pct"] = (
                        merged["n_sel"] / merged["Total_global"].replace(0, np.nan) * 100
                    ).round(2)

                    fig_evol.add_trace(go.Scatter(
                        x=merged["Année"],
                        y=merged["pct"],
                        mode="lines+markers",
                        name="Sélection globale",
                        line=dict(width=2.5, color=QUAL_PALETTE[color_idx % len(QUAL_PALETTE)]),
                        marker=dict(size=7),
                        hovertemplate="Année : %{x}<br>Part : <b>%{y:.2f}%</b><extra></extra>",
                    ))
                    color_idx += 1
                else:
                    for val in (vals or []):
                        ann_sel = (
                            dff[dff[col].astype(str) == str(val)]
                            .groupby("Année")["HalID"]
                            .nunique()
                            .reset_index(name="n_sel")
                        )
                        if ann_sel.empty:
                            continue
                        merged = ann_sel.merge(ann_global, on="Année", how="left")
                        merged["pct"] = (
                            merged["n_sel"] / merged["Total_global"].replace(0, np.nan) * 100
                        ).round(2)

                        # Couleur fixe si dimension = Centre, sinon QUAL_PALETTE
                        trace_color = (
                            get_centre_color(str(val), color_idx)
                            if col == "Centre"
                            else QUAL_PALETTE[color_idx % len(QUAL_PALETTE)]
                        )

                        fig_evol.add_trace(go.Scatter(
                            x=merged["Année"],
                            y=merged["pct"],
                            mode="lines+markers",
                            name=f"{dim_label} : {val}",
                            line=dict(width=2.5, color=trace_color),
                            marker=dict(size=7),
                            hovertemplate=f"{dim_label} : {val}<br>Année : %{{x}}<br>Part : <b>%{{y:.2f}}%</b><extra></extra>",
                        ))
                        color_idx += 1

            fig_evol.update_layout(
                template=GRAPH_TEMPLATE,
                hovermode="x unified",
                yaxis=dict(title="Part (% du total annuel)", ticksuffix="%", rangemode="tozero"),
                xaxis=dict(title="Année", dtick=1),
                legend=dict(
                    orientation="h",
                    x=0.5, xanchor="center",
                    y=-0.22, yanchor="top",
                    font=dict(size=10),
                ),
                margin=dict(l=10, r=10, t=20, b=60),
            )

        # ────────────────────────────────────────────────────────
        # KPI résumé
        # ────────────────────────────────────────────────────────
        pct_global = total_sel / total_global * 100 if total_global else 0

        def _kpi(label, val, color):
            return dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.Div(label, className="small text-muted mb-1"),
                        html.H4(val, className="fw-bold mb-0", style={"color": color}),
                    ]),
                    className="shadow-sm text-center",
                    style={"borderRadius": "14px", "border": f"1px solid {color}22"},
                ),
                md=3, sm=6, xs=12,
            )

        kpi_zone = dbc.Row([
            _kpi("Publications sélectionnées",  f"{total_sel:,}",          PRIMARY),
            _kpi("Total global (période)",       f"{total_global:,}",       PRIMARY_LIGHT),
            _kpi("Part de la sélection",         f"{pct_global:.2f} %",     ACCENT),
            _kpi("Publications hors sélection",  f"{total_global - total_sel:,}", DARK),
        ], className="g-2 mt-1 mb-3")

        return fig_pays, fig_centre, fig_org, fig_equipe, fig_evol, kpi_zone