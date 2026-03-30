from dash import html, dcc
import dash_bootstrap_components as dbc

def wordcloud_tab_layout():
    return dbc.Container(
        [
            # ── Carte d'explication ──
            dbc.Row(
                [
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
                                            "Nuage de mots constitué à partir des résumés (colonne Resume) des copublications déclarés dans HAL.",
                                            className="mb-2",
                                        ),
                                        html.P(
                                            "Les mots vides (articles, prépositions…) sont automatiquement exclus. Seuls les mots significatifs d'au moins 3 caractères sont conservés.",
                                            className="mb-0",
                                            style={"fontWeight": "600"},
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
                ]
            ),

            # ── Wordcloud + Tableau côte à côte ──
            dbc.Row(
                [
                    # Wordcloud (gauche)
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                html.Img(
                                    id="wordcloud",
                                    style={
                                        "width": "100%",
                                        "borderRadius": "10px",
                                    },
                                ),
                                style={"padding": "0.75rem"},
                            ),
                            className="shadow-sm h-100",
                            style={"borderRadius": "18px"},
                        ),
                        md=7,
                        sm=12,
                        className="mb-3",
                    ),

                    # Tableau Top 20 (droite)
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    "Top 20 des mots-clés",
                                    className="fw-semibold small text-uppercase",
                                    style={
                                        "backgroundColor": "transparent",
                                        "borderBottom": "none",
                                        "padding": "0.5rem 0.75rem 0 0.75rem",
                                    },
                                ),
                                dbc.CardBody(
                                    dcc.Loading(
                                        html.Div(
                                            id="wordcloud-top-table",
                                            style={"overflowY": "auto", "maxHeight": "420px"},
                                        ),
                                        type="default",
                                    ),
                                    style={"padding": "0.5rem 0.75rem"},
                                ),
                            ],
                            className="shadow-sm h-100",
                            style={"borderRadius": "18px"},
                        ),
                        md=5,
                        sm=12,
                        className="mb-3",
                    ),
                ],
                className="align-items-stretch",
            ),
        ],
        fluid=True,
        className="mt-2",
    )