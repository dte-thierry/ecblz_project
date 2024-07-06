# Importer le module datetime
from datetime import datetime

# Importer les bibliothèques nécessaires
import dash
import dash_bootstrap_components as dbc 
from dash import html
from dash import dcc
from dash import dash_table
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px

# Charger les données
df = pd.read_csv('data/ecbl-textiles.csv')

# Choisir des feuilles de style CSS
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', \
#                         'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialiser l'application Dash
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

# Définition des layouts de l'application
# Page 0 - Accueil ---------------------------------------------------------------------
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id = 'page-content')
])

index_page = html.Div([
    html.H1(
        'Dashboard EcoBalyze', 
        style={'color' : 'blue', 'textAlign': 'center'}),

    #html.Br(),

    html.Div(
        html.A(
            id="my-link",
            children="Cliquer ici pour visiter le site EcoBalyze",
            href="https://ecobalyse.beta.gouv.fr/#/",
            target="_blank",
            style={'color': 'blue'}
        ),
        style={'textAlign': 'center'}
    ),

    html.Br(),

    html.Button(
        dcc.Link('Comparatif de Coût Environnemental - pef -', 
                 href='/page-1')),
    html.Br(),

    html.Button(
        dcc.Link('Comparatif de Textile', 
                 href='/page-2'))

], style={'alignItems': 'center'})

# Page 1 - xxxxxxx ---------------------------------------------------------------------


# Page 2 - xxxxxxx ---------------------------------------------------------------------


# Mise à jour de l'index ---------------------------------------------------------------
@app.callback(dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/page-1':
        return layout_1
    elif pathname == '/page-2':
        return layout_2
    else:
        return index_page

# Point d'entrée de l'application ------------------------------------------------------
def afficher_date():
    # Obtenir la date actuelle
    current_date = datetime.now()
    # Afficher la date actuelle dans le format souhaité
    print(f"Today's date is {current_date.strftime('%a. %d %b. %Y')}")

if __name__ == '__main__':
    # afficher_date()
    app.run_server(debug=True)

