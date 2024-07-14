# Importer les bibliothèques nécessaires
from dash import html, dcc

# créer le 'layout' de la page 2 -
def create_page2_layout(df):
    return html.Div([
        html.H1('Comparatif de textile', style={'textAlign': 'center', 'color': 'mediumturquoise'}),

        html.Div(dcc.Dropdown(id = 'page-2-dropdown',
                              options= [{'label': 'Diagramme à barres empilées : pays impliqués dans chaque étape de la fabrication', 'value': 'pays_fab'},
                                        {'label': 'Diagramme à barres : matériaux utilisés dans les produits', 'value': 'bar_mat'},
                                        {'label': 'Diagramme à barres : nombre de produits pour chaque type d\'entreprise', 'value': 'bar_bu'},
                                        {'label': 'Diagramme à barres : nombre de produits qui ont une traçabilité', 'value': 'bar_trace'},
                                        {'label': 'Diagramme à barres : nombre de produits pour chaque type de processus de fabrication', 'value': 'bar_process'},
                                        {'label': 'Diagramme à barres : nombre de produits pour chaque durée de marketing', 'value': 'bar_market'},
                                        {'label': 'Diagramme à barres : nombre de produits pour chaque nombre de références', 'value': 'bar_ref'}],
                              value= 'pays_fab')),

        html.Div(id='page-2-table'),

        html.Br(),
    
        html.Button(dcc.Link('Retour à la page d\'accueil', href='/'))

    ], style = {'background' : 'beige'})
