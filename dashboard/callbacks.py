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
                    "backgroundColor": QUAL_PALETTE[i % len(QUAL_PALETTE)],
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

        # ── Palette dédiée : couleurs bien contrastées entre centres ──
        FLOW_PALETTE = [
            "#636EFA",  # bleu vif
            "#EF553B",  # rouge-orange
            "#00CC96",  # vert menthe
            "#AB63FA",  # violet
            "#FFA15A",  # orange
            "#19D3F3",  # cyan
            "#FF6692",  # rose
            "#B6E880",  # vert clair
        ]

        fig_flow = go.Figure()
        origins = []
        all_dest_lats, all_dest_lons = [], []  # pour le zoom auto

        if centres_sel:
            centre_color_map = {
                c: FLOW_PALETTE[i % len(FLOW_PALETTE)]
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
    @app.callback(
        Output("wordcloud", "src"),
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
            return no_update

        df = pd.DataFrame(stored_data) if stored_data is not None else df_base
        dff = filter_df(df, centres, equipes, pays, villes, orgs, annees)

        mots_series = dff["Mots-cles"].dropna().astype(str)
        if mots_series.empty:
            return ""

        sample = mots_series.sample(min(len(mots_series), 2000), random_state=42)
        text = " ".join(sample)

        wc = WordCloud(
            width=900,
            height=400,
            background_color="white",
            colormap="tab10",
        ).generate(text)

        buf = io.BytesIO()
        wc.to_image().save(buf, format="PNG")
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()



    # ========================================================
    # ========================================================
    # 3 — RÉSEAU : centres / auteurs Inria / auteurs étrangers
    #     + duplication figure pour modal "plein écran interne"
    # ========================================================
    @app.callback(
        [
            Output("network", "figure"),
            Output("network-fullscreen", "figure"),
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
            Input("network-max-nodes", "value"),  # gardé pour compat, non utilisé
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
    ):
        # On ne dessine le réseau que dans l'onglet dédié
        if tab != "tab-network":
            return no_update, no_update

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

        # ------------- Traces des arêtes (gris clair, pas vert) -------------
        edge_x, edge_y = [], []
        for u, v in G.edges():
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]

        edge_trace = go.Scattergl(
            x=edge_x,
            y=edge_y,
            mode="lines",
            line=dict(width=0.8, color="rgba(160,160,160,0.45)"),
            hoverinfo="none",
            showlegend=False,
        )

        # ------------- Couleurs centres -------------
        centre_names = sorted({a["label"] for a in node_attrs.values() if a["type"] == "centre"})
        centre_color_map = {
            name: QUAL_PALETTE[i % len(QUAL_PALETTE)]
            for i, name in enumerate(centre_names)
        }

        # ------------- Préparer coordonnées + tailles + hover strings -------------
        centre_x, centre_y, centre_size, centre_outline, centre_label, centre_hover = [], [], [], [], [], []
        fr_x, fr_y, fr_size, fr_label, fr_hover = [], [], [], [], []
        fg_x, fg_y, fg_size, fg_label, fg_hover = [], [], [], [], []

        for nid, attrs in node_attrs.items():
            x, y = pos[nid]
            ntype = attrs["type"]

            if ntype == "centre":
                centre_x.append(x)
                centre_y.append(y)
                centre_label.append(attrs["label"])
                centre_outline.append(centre_color_map.get(attrs["label"], "#E91E63"))
                centre_size.append(24 + 5 * math.sqrt(max(attrs["pubs"], 1)))

                centre_hover.append(
                    f"<b>Centre</b> : {attrs['label']}<br>"
                    f"Publications : {attrs['pubs']}<br>"
                    f"Auteurs Inria : {attrs['nb_fr']}<br>"
                    f"Auteurs copubliants : {attrs['nb_foreign']}<br>"
                    f"Pays : {attrs['nb_countries']}<br>"
                    f"Organismes : {attrs['nb_orgs']}"
                )

            elif ntype == "fr":
                fr_x.append(x)
                fr_y.append(y)
                fr_label.append(attrs["label"])
                fr_size.append(10 + 3 * math.sqrt(max(attrs["pubs"], 1)))

                fr_hover.append(
                    f"<b>Auteur Inria</b><br>"
                    f"Nom : {attrs['label']}<br>"
                    f"# pubs : {attrs['pubs']}<br>"
                    f"# pays partenaires : {attrs.get('nb_countries', 0)}"
                )

            elif ntype == "foreign":
                fg_x.append(x)
                fg_y.append(y)
                fg_label.append(attrs["label"])
                fg_size.append(8 + 2.5 * math.sqrt(max(attrs["pubs"], 1)))

                fg_hover.append(
                    f"<b>Auteur étranger</b><br>"
                    f"Nom : {attrs['label']}<br>"
                    f"Pays principal : {attrs.get('country', 'Pays inconnu')}<br>"
                    f"# pubs : {attrs['pubs']}"
                )

        # ------------- Centres : ronds blancs contour coloré + nom centré -------------
        centre_trace = go.Scattergl(
            x=centre_x,
            y=centre_y,
            mode="markers+text",
            name="Centres",
            marker=dict(
                size=centre_size,
                color="white",
                line=dict(width=3, color=centre_outline),
                opacity=0.98,
            ),
            text=centre_label,
            textposition="middle center",
            textfont=dict(size=9, color="#111111"),
            customdata=centre_hover,
            hovertemplate="%{customdata}<extra></extra>",
        )

        # ------------- Auteurs Inria : verts (taille ∝ pubs) -------------
        fr_trace = go.Scattergl(
            x=fr_x,
            y=fr_y,
            mode="markers",
            name="Auteurs Inria",
            marker=dict(
                size=fr_size,
                color="rgba(0,150,136,0.95)",
                line=dict(width=0.8, color="rgba(0,0,0,0.55)"),
                opacity=0.9,
            ),
            customdata=fr_hover,
            hovertemplate="%{customdata}<extra></extra>",
        )

        # ------------- Auteurs étrangers : noirs (taille ∝ pubs) -------------
        fg_trace = go.Scattergl(
            x=fg_x,
            y=fg_y,
            mode="markers",
            name="Auteurs étrangers",
            marker=dict(
                size=fg_size,
                color="rgba(30,30,30,0.95)",
                line=dict(width=0.8, color="rgba(250,250,250,0.7)"),
                opacity=0.9,
            ),
            customdata=fg_hover,
            hovertemplate="%{customdata}<extra></extra>",
        )

        # Labels auteurs (optionnels)
        fr_labels_trace = go.Scattergl(
            x=fr_x, y=fr_y,
            mode="text",
            text=fr_label,
            textfont=dict(size=7, color="rgba(80,80,80,0.85)"),
            hoverinfo="skip",
            showlegend=False,
        )
        fg_labels_trace = go.Scattergl(
            x=fg_x, y=fg_y,
            mode="text",
            text=fg_label,
            textfont=dict(size=7, color="rgba(120,120,120,0.8)"),
            hoverinfo="skip",
            showlegend=False,
        )

        fig_net = go.Figure(
            data=[
                edge_trace,
                centre_trace,
                fr_trace,
                fg_trace,
                fr_labels_trace,
                fg_labels_trace,
            ]
        )

        fig_net.update_layout(
            template=GRAPH_TEMPLATE,
            title="Réseau de copublications",
            showlegend=True,
            legend=dict(
                orientation="v",
                x=0.01,
                y=0.99,
                xanchor="left",
                yanchor="top",
                bgcolor="rgba(255,255,255,0.85)",
                bordercolor="rgba(0,0,0,0.2)",
                borderwidth=1,
                font=dict(size=10),
            ),
            xaxis=dict(showgrid=False, zeroline=False, visible=False),
            yaxis=dict(showgrid=False, zeroline=False, visible=False, scaleanchor="x", scaleratio=1),
            margin=dict(l=10, r=10, t=60, b=10),
            hovermode="closest",
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
        )
        fig_net.layout.hovermode = "closest"

        # Même figure dans la vue "plein écran"
        return fig_net, fig_net


    # ========================================================
    # 3bis — MODAL plein écran (fenêtre flottante)
    # ========================================================
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

            fig_sunburst = px.sunburst(
                sun_df,
                path=["Centre", "Equipe", "Organisme_copubliant"],
                values="Publications",
                color="Centre",
                color_discrete_sequence=QUAL_PALETTE,
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

            fig_sankey = go.Figure(
                data=[
                    go.Sankey(
                        node=dict(
                            pad=15,
                            thickness=15,
                            line=dict(color="black", width=0.3),
                            label=labels,
                            color=[
                                QUAL_PALETTE[i % len(QUAL_PALETTE)]
                                for i in range(len(labels))
                            ],
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
            # On ne garde que les lignes avec centre + domaine
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
                # Centres à tracer : ceux filtrés s'il y en a, sinon les principaux
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

                # Si rien (centres filtrés pas présents), on prend les top
                if not centres_to_plot:
                    centres_to_plot = (
                        dom_df.groupby("Centre")["Publications"]
                        .sum()
                        .sort_values(ascending=False)
                        .head(5)
                        .index.tolist()
                    )

                # Top domaines (axes du radar)
                top_dom = (
                    dom_df.groupby("Domaine(s)")["Publications"]
                    .sum()
                    .sort_values(ascending=False)
                    .head(6)
                    .index.tolist()
                )

                categories = top_dom
                categories_closed = categories + categories[:1]

                fig_radar = go.Figure()

                # Une trace par centre → superposition des polygones
                for i, centre in enumerate(centres_to_plot):
                    sub = dom_df[dom_df["Centre"] == centre]
                    vals = []
                    for dom in categories:
                        vals.append(
                            sub.loc[sub["Domaine(s)"] == dom, "Publications"].sum()
                        )
                    vals_closed = vals + vals[:1]

                    fig_radar.add_trace(
                        go.Scatterpolar(
                            r=vals_closed,
                            theta=categories_closed,
                            fill="toself",
                            name=centre,
                            line=dict(color=QUAL_PALETTE[i % len(QUAL_PALETTE)]),
                            opacity=0.55,
                        )
                    )

                fig_radar.update_layout(
                    template=GRAPH_TEMPLATE,
                    title=(
                        "Profil par domaine – centres : "
                        + ", ".join(centres_to_plot)
                    ),
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            tickfont=dict(size=10),
                        )
                    ),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.2,
                        xanchor="center",
                        x=0.5,
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