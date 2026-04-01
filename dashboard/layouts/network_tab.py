from dash import dcc, html
import dash_bootstrap_components as dbc


def network_tab_layout():
    return dbc.Container(
        [
            dcc.Store(id="network-graph-data"),

            # ---------- Carte "À propos" ----------
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                "À propos du graphique",
                                className="fw-semibold small text-uppercase",
                                style={
                                    "backgroundColor": "transparent",
                                    "borderBottom": "none",
                                    "padding": "0.5rem 0.75rem 0 0.75rem",
                                },
                            ),
                            dbc.CardBody(
                                [
                                    html.P(
                                        "Filtrez par pays pour observer les liens entre auteurs Inria et auteurs étrangers. "
                                        "Ajoutez un filtre équipe pour affiner sur une équipe spécifique.",
                                        className="mb-2",
                                    ),
                                    html.P(
                                        [
                                            html.Strong("Interactions : "),
                                            "survolez un nœud pour voir son nom · "
                                            "cliquez pour afficher sa fiche et mettre en avant ses connexions · "
                                            "double-clic pour réinitialiser.",
                                        ],
                                        className="mb-0",
                                        style={"fontWeight": "500"},
                                    ),
                                ],
                                className="small",
                                style={"padding": "0.75rem"},
                            ),
                        ],
                        className="shadow-sm mb-3",
                        style={"borderRadius": "18px"},
                    ),
                    md=12,
                )
            ),

            # Sliders cachés pour compat callbacks (valeurs fixes)
            html.Div(dcc.Slider(id="network-max-pubs", min=200, max=10000, step=200, value=2000),
                     style={"display": "none"}),
            html.Div(dcc.Slider(id="network-max-nodes", min=100, max=5000, step=100, value=1500),
                     style={"display": "none"}),

            # ---------- Barre de contrôles ----------
            html.Div(
                [
                    html.Button(
                        "⛶ Plein écran",
                        id="btn-network-fullscreen-open",
                        n_clicks=0,
                        style={
                            "padding": "8px 14px",
                            "border": "1px solid rgba(0,0,0,0.2)",
                            "borderRadius": "10px",
                            "background": "white",
                            "cursor": "pointer",
                            "fontWeight": "600",
                            "height": "40px",
                        },
                    ),
                    # Toggle anonymisation auteurs étrangers
                    html.Button(
                        "👁 Anonymiser noms étrangers",
                        id="network-anonymize",
                        n_clicks=0,
                        style={
                            "padding": "8px 14px",
                            "border": "1px solid rgba(0,0,0,0.2)",
                            "borderRadius": "10px",
                            "background": "white",
                            "cursor": "pointer",
                            "fontWeight": "600",
                            "height": "40px",
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "gap": "10px",
                    "marginBottom": "10px",
                    "flexWrap": "wrap",
                },
            ),

            # ---------- Graphe + fiche côte à côte ----------
            dbc.Row(
                [
                    # Graphe principal (9/12)
                    dbc.Col(
                        dcc.Loading(
                            type="default",
                            children=dcc.Graph(
                                id="network",
                                config={
                                    "displayModeBar": True,
                                    "scrollZoom": True,
                                    "doubleClick": "reset",
                                    "responsive": True,
                                    "displaylogo": False,
                                    "toImageButtonOptions": {
                                        "height": 1200,
                                        "width": 1600,
                                        "scale": 2,
                                    },
                                },
                                style={"height": "80vh", "minHeight": "650px"},
                            ),
                        ),
                        md=12, sm=12,
                    ),
                ],
                className="g-2",
            ),

            # ---------- Modal plein écran ----------
            html.Div(
                id="network-fullscreen-modal",
                style={
                    "display": "none",
                    "position": "fixed",
                    "inset": "0",
                    "background": "rgba(0,0,0,0.35)",
                    "zIndex": "9999",
                    "padding": "24px",
                },
                children=[
                    html.Div(
                        style={
                            "width": "min(1400px, 96vw)",
                            "height": "min(900px, 92vh)",
                            "background": "white",
                            "borderRadius": "18px",
                            "boxShadow": "0 20px 60px rgba(0,0,0,0.25)",
                            "margin": "0 auto",
                            "display": "flex",
                            "flexDirection": "column",
                            "overflow": "hidden",
                        },
                        children=[
                            html.Div(
                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                    "justifyContent": "space-between",
                                    "padding": "12px 14px",
                                    "borderBottom": "1px solid rgba(0,0,0,0.08)",
                                },
                                children=[
                                    html.Div(
                                        "Réseau de copublications — Plein écran",
                                        style={"fontWeight": "700"},
                                    ),
                                    html.Button(
                                        "Fermer",
                                        id="btn-network-fullscreen-close",
                                        n_clicks=0,
                                        style={
                                            "padding": "8px 12px",
                                            "border": "1px solid rgba(0,0,0,0.2)",
                                            "borderRadius": "10px",
                                            "background": "white",
                                            "cursor": "pointer",
                                            "fontWeight": "600",
                                        },
                                    ),
                                ],
                            ),
                            html.Div(
                                style={"flex": "1", "padding": "10px"},
                                children=[
                                    dcc.Graph(
                                        id="network-fullscreen",
                                        config={
                                            "displayModeBar": True,
                                            "scrollZoom": True,
                                            "doubleClick": "reset",
                                            "responsive": True,
                                            "displaylogo": False,
                                            "toImageButtonOptions": {
                                                "height": 1600,
                                                "width": 2200,
                                                "scale": 2,
                                            },
                                        },
                                        style={"height": "100%", "width": "100%"},
                                    )
                                ],
                            ),
                        ],
                    )
                ],
            ),
        ],
        fluid=True,
        className="mt-2",
        style={"padding": "10px"},
    )