from dash import dcc, html
import dash_bootstrap_components as dbc


def main_tab_layout(df):
    """
    Mise en page de l'onglet 'Vue principale'

    - Ligne 1 : explication gauche + barres années + explication droite
    - Ligne 2 : Top 10 pays / Top 10 villes / Top 10 organismes
    - Ligne 3 : explication flux / flow map avec filtre centre local
    """

    # Centres disponibles pour le dropdown du flux
    centres_options = []
    if "Centre" in df.columns:
        centres_uniques = (
            df["Centre"]
            .dropna()
            .astype(str)
            .sort_values()
            .unique()
        )
        centres_options = [{"label": c, "value": c} for c in centres_uniques]

    # ---- Fabrique de cartes graphiques classiques ----
    def card_graph(graph_id: str, title: str) -> dbc.Card:
        return dbc.Card(
            [
                dbc.CardHeader(
                    title,
                    className="fw-semibold small text-uppercase",
                    style={
                        "backgroundColor": "transparent",
                        "borderBottom": "none",
                        "padding": "0.5rem 0.75rem 0 0.75rem",
                    },
                ),
                dbc.CardBody(
                    dcc.Graph(
                        id=graph_id,
                        style={"height": "340px"},
                        config={"displayModeBar": True, "scrollZoom": True, "displaylogo": False, "modeBarButtonsToAdd": ["zoomInMapbox", "zoomOutMapbox", "resetViewMapbox"]},
                    ),
                    className="main-graph-card",
                    style={"padding": "0.25rem"},
                ),
            ],
            className="shadow-sm mb-3",
            style={"borderRadius": "18px", "height": "100%"},
        )

    # ---- Carte texte simple (explications) ----
    def card_text(title: str, children) -> dbc.Card:
        return dbc.Card(
            [
                dbc.CardHeader(
                    title,
                    className="fw-semibold small text-uppercase",
                    style={
                        "backgroundColor": "transparent",
                        "borderBottom": "none",
                        "padding": "0.5rem 0.75rem 0 0.75rem",
                    },
                ),
                dbc.CardBody(
                    children,
                    className="small",
                    style={"padding": "0.75rem"},
                ),
            ],
            className="shadow-sm mb-3",
            style={"borderRadius": "18px", "height": "100%"},
        )

    # ---- Carte spéciale pour le flux ----
    flow_card = dbc.Card(
        [
            dbc.CardHeader(
                html.Div(
                    [
                        html.Span(
                            "Flux de copublications par centre",
                            className="fw-semibold small text-uppercase",
                        ),
                        # Légende inline épaisseur
                        html.Div(
                            [
                                html.Span(
                                    "Épaisseur des arcs",
                                    className="me-2 text-muted",
                                    style={"fontSize": "0.72rem"},
                                ),
                                html.Span("▬ Fort", style={"fontSize": "0.72rem", "color": "#636EFA", "fontWeight": "bold", "marginRight": "6px"}),
                                html.Span("─ Moyen", style={"fontSize": "0.72rem", "color": "#636EFA", "marginRight": "6px"}),
                                html.Span("· Faible", style={"fontSize": "0.72rem", "color": "#636EFA", "opacity": "0.5"}),
                            ],
                            className="d-inline-flex align-items-center ms-3",
                        ),
                        # Bouton plein écran
                        html.Button(
                            "⛶ Agrandir",
                            id="btn-flowmap-fullscreen-open",
                            n_clicks=0,
                            style={
                                "marginLeft": "auto",
                                "padding": "4px 12px",
                                "border": "1px solid rgba(39,52,139,0.25)",
                                "borderRadius": "8px",
                                "background": "rgba(39,52,139,0.06)",
                                "cursor": "pointer",
                                "fontSize": "0.78rem",
                                "fontWeight": "600",
                                "color": "#27348b",
                            },
                        ),
                    ],
                    className="d-flex align-items-center flex-wrap gap-2 w-100",
                ),
                style={
                    "backgroundColor": "transparent",
                    "borderBottom": "none",
                    "padding": "0.5rem 0.75rem 0.25rem 0.75rem",
                },
            ),
            dbc.CardBody(
                dcc.Graph(
                    id="flow_map",
                    style={"height": "500px"},
                    config={
                        "displayModeBar": True,
                        "scrollZoom": True,
                        "displaylogo": False,
                        "modeBarButtonsToAdd": [
                            "zoomInMapbox",
                            "zoomOutMapbox",
                            "resetViewMapbox",
                        ],
                        "toImageButtonOptions": {
                            "height": 900,
                            "width": 1600,
                            "scale": 2,
                        },
                    },
                ),
                className="main-graph-card",
                style={"padding": "0"},
            ),
        ],
        className="shadow-sm mb-3",
        style={"borderRadius": "18px", "height": "100%"},
    )

    # ---- Modal plein écran pour le flow map ----
    flow_fullscreen_modal = html.Div(
        id="flowmap-fullscreen-modal",
        style={"display": "none"},
        children=[
            # Overlay sombre
            html.Div(
                style={
                    "position": "fixed",
                    "inset": "0",
                    "background": "rgba(0,0,0,0.55)",
                    "zIndex": "9998",
                },
                id="flowmap-modal-backdrop",
            ),
            # Fenêtre modale
            html.Div(
                style={
                    "position": "fixed",
                    "inset": "0",
                    "zIndex": "9999",
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "padding": "20px",
                    "pointerEvents": "none",
                },
                children=[
                    html.Div(
                        style={
                            "width": "min(1500px, 96vw)",
                            "height": "min(920px, 94vh)",
                            "background": "white",
                            "borderRadius": "20px",
                            "boxShadow": "0 24px 80px rgba(0,0,0,0.35)",
                            "display": "flex",
                            "flexDirection": "column",
                            "overflow": "hidden",
                            "pointerEvents": "all",
                        },
                        children=[
                            # En-tête modal
                            html.Div(
                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                    "justifyContent": "space-between",
                                    "padding": "12px 18px",
                                    "borderBottom": "1px solid rgba(0,0,0,0.08)",
                                    "background": "linear-gradient(90deg, #27348b08 0%, #00a5cc08 100%)",
                                },
                                children=[
                                    html.Div(
                                        [
                                            html.Span(
                                                "⛶ ",
                                                style={"color": "#27348b", "fontSize": "1.1rem"},
                                            ),
                                            html.Span(
                                                "Flux de copublications — Vue agrandie",
                                                style={"fontWeight": "700", "color": "#27348b", "fontSize": "1rem"},
                                            ),
                                        ]
                                    ),
                                    html.Button(
                                        "✕ Fermer",
                                        id="btn-flowmap-fullscreen-close",
                                        n_clicks=0,
                                        style={
                                            "padding": "6px 16px",
                                            "border": "1px solid rgba(0,0,0,0.18)",
                                            "borderRadius": "10px",
                                            "background": "white",
                                            "cursor": "pointer",
                                            "fontWeight": "600",
                                            "fontSize": "0.85rem",
                                            "color": "#374151",
                                        },
                                    ),
                                ],
                            ),
                            # Graphique plein écran
                            html.Div(
                                style={"flex": "1", "padding": "0"},
                                children=[
                                    dcc.Graph(
                                        id="flow_map_fullscreen",
                                        config={
                                            "displayModeBar": True,
                                            "scrollZoom": True,
                                            "displaylogo": False,
                                            "modeBarButtonsToAdd": [
                                                "zoomInMapbox",
                                                "zoomOutMapbox",
                                                "resetViewMapbox",
                                            ],
                                            "toImageButtonOptions": {
                                                "height": 1200,
                                                "width": 2200,
                                                "scale": 2,
                                            },
                                        },
                                        style={"height": "100%", "width": "100%"},
                                    )
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

    return dbc.Container(
        [
            flow_fullscreen_modal,
            # ---------- Ligne 1 : explications + barres années ----------
            dbc.Row(
                [
                    # Explication gauche
                    dbc.Col(
                        card_text(
                            "À propos du graphique",
                            [
                                html.P(
                                    "Ce graphique montre l'évolution du nombre de "
                                    "copublications par année dans le périmètre "
                                    "défini par les filtres.",
                                    className="mb-2",
                                ),
                                html.P(
                                    "Utilisez ce visuel pour repérer les années "
                                    "fortes, les tendances de croissance ou de "
                                    "stagnation.",
                                    className="mb-0",
                                ),
                            ],
                        ),
                        md=4,
                        sm=12,
                    ),
                    # Graphique central
                    dbc.Col(
                        card_graph(
                            "bar_annee",
                            "Nombre de publications par année",
                        ),
                        md=8,
                        sm=12,
                    ),
                ],
                className="mb-3",
            ),

            # ---------- Ligne 2 : 3 Top 10 sur la même ligne ----------
            dbc.Row(
                [
                    dbc.Col(
                        card_graph(
                            "top_pays",
                            "Top 10 des pays",
                        ),
                        md=4,
                        sm=12,
                    ),
                    dbc.Col(
                        card_graph(
                            "top_villes",
                            "Top 10 des villes",
                        ),
                        md=4,
                        sm=12,
                    ),
                    dbc.Col(
                        card_graph(
                            "top_orgs",
                            "Top 10 des organismes copubliants",
                        ),
                        md=4,
                        sm=12,
                    ),
                ],
                className="mb-3",
            ),

            # ---------- Ligne 3 : flow map pleine largeur ----------
            dbc.Row(
                [
                    dbc.Col(
                        flow_card,
                        md=12,
                        sm=12,
                    ),
                ],
                className="mb-2",
            ),

            # ---------- Ligne 4 : légende + explication ----------
            dbc.Row(
                [
                    # Bloc légende visuelle
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Div(
                                        "Comment lire cette carte",
                                        className="fw-semibold small text-uppercase mb-2",
                                        style={"color": "#27348b"},
                                    ),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Span("●", style={"color": "#636EFA", "fontSize": "1.2rem", "marginRight": "6px"}),
                                                    html.Span("Centre Inria — point d'origine des arcs", className="small"),
                                                ],
                                                className="mb-1 d-flex align-items-center",
                                            ),
                                            html.Div(
                                                [
                                                    html.Span("▶", style={"color": "#636EFA", "fontSize": "0.9rem", "marginRight": "6px"}),
                                                    html.Span("Pointe de flèche — sens de la collaboration", className="small"),
                                                ],
                                                className="mb-1 d-flex align-items-center",
                                            ),
                                            html.Div(
                                                [
                                                    html.Span("▬", style={"color": "#636EFA", "fontSize": "1rem", "fontWeight": "900", "marginRight": "6px"}),
                                                    html.Span("Arc épais = nombreuses copublications", className="small"),
                                                ],
                                                className="mb-1 d-flex align-items-center",
                                            ),
                                            html.Div(
                                                [
                                                    html.Span("─", style={"color": "#636EFA", "opacity": "0.4", "fontSize": "1rem", "marginRight": "6px"}),
                                                    html.Span("Arc fin = peu de copublications", className="small"),
                                                ],
                                                className="mb-0 d-flex align-items-center",
                                            ),
                                        ]
                                    ),
                                ],
                                style={"padding": "0.75rem"},
                            ),
                            className="shadow-sm h-100",
                            style={"borderRadius": "14px"},
                        ),
                        md=4, sm=12,
                    ),
                    # Bloc conseils d'utilisation
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Div(
                                        "Conseils d'utilisation",
                                        className="fw-semibold small text-uppercase mb-2",
                                        style={"color": "#27348b"},
                                    ),
                                    html.P(
                                        "Utilisez les filtres Centre en haut de page pour isoler un ou plusieurs centres "
                                        "et réduire le nombre d'arcs affichés.",
                                        className="small mb-1",
                                    ),
                                    html.P(
                                        "La molette permet de zoomer sur une région. Survolez un arc pour voir le détail "
                                        "de la collaboration (ville, pays, nombre de publications).",
                                        className="small mb-1",
                                    ),
                                    html.P(
                                        "Les arcs sont classés en 3 niveaux d'épaisseur : fort (top 25 %), "
                                        "moyen (25-50 %), faible (bas 50 %).",
                                        className="small mb-0",
                                    ),
                                ],
                                style={"padding": "0.75rem"},
                            ),
                            className="shadow-sm h-100",
                            style={"borderRadius": "14px"},
                        ),
                        md=8, sm=12,
                    ),
                ],
                className="mb-3",
            ),
        ],
        fluid=True,
        className="mt-2",
    )