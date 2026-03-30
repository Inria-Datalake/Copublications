from dash import dcc, html
import dash_bootstrap_components as dbc


def share_tab_layout():
    return dbc.Container(
        [
            # ── Explication ──
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
                                        "Cet onglet calcule la part relative de chaque élément sélectionné "
                                        "par rapport au total global des copublications (sans filtre).",
                                        className="mb-1",
                                    ),
                                    html.P(
                                        [
                                            html.Strong("Exemple : "),
                                            "si vous sélectionnez les pays « Allemagne » et « Italie », "
                                            "chaque graphique montre leur part (%) dans le total toutes années confondues, "
                                            "puis leur évolution annuelle en % du total de chaque année.",
                                        ],
                                        className="mb-1",
                                    ),
                                    html.P(
                                        "Les graphiques s'adaptent automatiquement à chaque filtre actif "
                                        "(centre, équipe, pays, ville, organisme, année).",
                                        className="mb-0 text-muted",
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

            # ── Ligne 1 : part par pays + part par centre ──
            dbc.Row(
                [
                    dbc.Col(_card_graph("share-pays",    "Part des pays sélectionnés (% du total)"),   md=6, sm=12),
                    dbc.Col(_card_graph("share-centre",  "Part des centres sélectionnés (% du total)"), md=6, sm=12),
                ],
                className="mb-3",
            ),

            # ── Ligne 2 : part par organisme + part par équipe ──
            dbc.Row(
                [
                    dbc.Col(_card_graph("share-org",    "Part des organismes sélectionnés (% du total)"), md=6, sm=12),
                    dbc.Col(_card_graph("share-equipe", "Part des équipes sélectionnées (% du total)"),   md=6, sm=12),
                ],
                className="mb-3",
            ),

            # ── Ligne 3 : évolution annuelle de la part (%) ──
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                "Évolution annuelle de la part (% du total de chaque année)",
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
                                        id="share-evol",
                                        config={"displayModeBar": True, "displaylogo": False, "responsive": True},
                                        style={"height": "380px"},
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

            # ── Ligne 4 : résumé KPI ──
            dbc.Row(
                dbc.Col(
                    html.Div(id="share-kpi-zone"),
                    md=12,
                )
            ),
        ],
        fluid=True,
        className="mt-2",
        style={"padding": "10px"},
    )


def _card_graph(graph_id, title):
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
                dcc.Loading(
                    dcc.Graph(
                        id=graph_id,
                        config={"displayModeBar": True, "displaylogo": False, "responsive": True},
                        style={"height": "340px"},
                    )
                ),
                style={"padding": "0.25rem"},
            ),
        ],
        className="shadow-sm mb-3",
        style={"borderRadius": "18px", "height": "100%"},
    )