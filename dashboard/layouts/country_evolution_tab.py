from dash import dcc, html
import dash_bootstrap_components as dbc


def country_evolution_tab_layout():
    return dbc.Container(
        [
            # ── Carte d'explication ──
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                "À propos de cet onglet",
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
                                        "Cet onglet présente l'évolution annuelle du nombre de copublications "
                                        "pour les pays partenaires les plus actifs.",
                                        className="mb-2",
                                    ),
                                    html.P(
                                        "Utilisez le curseur ci-dessous pour ajuster le nombre de pays affichés. "
                                        "Les filtres globaux (centre, équipe, pays…) s'appliquent à tous les graphiques.",
                                        className="mb-0",
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

            # ── Contrôle : nombre de pays à afficher ──
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            html.Div(
                                [
                                    html.Label(
                                        "Nombre de pays à afficher (Top N)",
                                        className="fw-semibold small mb-2",
                                    ),
                                    dcc.Slider(
                                        id="country-top-n",
                                        min=5,
                                        max=30,
                                        step=5,
                                        value=10,
                                        marks={i: str(i) for i in range(5, 35, 5)},
                                        tooltip={"placement": "bottom", "always_visible": False},
                                    ),
                                ]
                            )
                        ),
                        className="shadow-sm mb-3",
                        style={"borderRadius": "18px"},
                    ),
                    md=12,
                )
            ),

            # ── Graphique principal : courbes par pays ──
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                "Évolution annuelle des copublications par pays",
                                className="fw-semibold small text-uppercase",
                                style={
                                    "backgroundColor": "transparent",
                                    "borderBottom": "none",
                                    "padding": "0.5rem 0.75rem 0 0.75rem",
                                },
                            ),
                            dbc.CardBody(
                                dcc.Loading(
                                    dcc.Graph(
                                        id="country_line_chart",
                                        config={"displayModeBar": True, "displaylogo": False, "responsive": True},
                                        style={"height": "420px"},
                                    )
                                ),
                                style={"padding": "0.25rem"},
                            ),
                        ],
                        className="shadow-sm mb-3",
                        style={"borderRadius": "18px"},
                    ),
                    md=12,
                )
            ),

            # ── Heatmap + Barres côte à côte ──
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    "Heatmap pays × année",
                                    className="fw-semibold small text-uppercase",
                                    style={
                                        "backgroundColor": "transparent",
                                        "borderBottom": "none",
                                        "padding": "0.5rem 0.75rem 0 0.75rem",
                                    },
                                ),
                                dbc.CardBody(
                                    dcc.Loading(
                                        dcc.Graph(
                                            id="country_heatmap",
                                            config={"displayModeBar": True, "displaylogo": False, "responsive": True},
                                            style={"height": "400px"},
                                        )
                                    ),
                                    style={"padding": "0.25rem"},
                                ),
                            ],
                            className="shadow-sm mb-3",
                            style={"borderRadius": "18px"},
                        ),
                        md=7,
                        sm=12,
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    "Volume total par pays",
                                    className="fw-semibold small text-uppercase",
                                    style={
                                        "backgroundColor": "transparent",
                                        "borderBottom": "none",
                                        "padding": "0.5rem 0.75rem 0 0.75rem",
                                    },
                                ),
                                dbc.CardBody(
                                    dcc.Loading(
                                        dcc.Graph(
                                            id="country_top_bar",
                                            config={"displayModeBar": True, "displaylogo": False, "responsive": True},
                                            style={"height": "400px"},
                                        )
                                    ),
                                    style={"padding": "0.25rem"},
                                ),
                            ],
                            className="shadow-sm mb-3",
                            style={"borderRadius": "18px"},
                        ),
                        md=5,
                        sm=12,
                    ),
                ],
                className="mb-3",
            ),
        ],
        fluid=True,
        className="mt-2",
        style={"padding": "10px"},
    )