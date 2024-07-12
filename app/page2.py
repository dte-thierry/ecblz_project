# Importer les bibliothèques nécessaires
from dash import html, dcc

# créer le 'layout' de la page 2 -
def create_page2_layout(df):
    return html.Div([
        html.H1('Comparatif de textile', style={'textAlign': 'center', 'color': 'mediumturquoise'}),

        html.Div(dcc.Dropdown(id = 'product-dropdown',
                              options= [{'label': 'Table : ' + product + " : ayant le coût environnemental (pef) le plus faible", 'value': product} for product in df['product'].unique()] +
                                       [{'label': 'Diagramme à barres empilées : pays impliqués dans chaque étape de la fabrication', 'value': 'pays_fab'}],
                              value= df['product'].unique()[0])),

        html.Div(id='page-2-table'),
    
        html.Br(),
    
        html.Button(dcc.Link('Retour à la page d\'accueil', href='/'))

    ], style = {'background' : 'beige'})
