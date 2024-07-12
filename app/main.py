# Importer le module datetime
from datetime import datetime

# Importer les bibliothèques nécessaires
import dash
import dash_bootstrap_components as dbc 
from dash import html
from dash import dcc
from dash import dash_table
from dash.dependencies import Input, Output

import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import os

# Importer le layout de la page d'accueil - page 0 -
from page0 import create_page0_layout

# Importer le layout de la page 1
from page1 import create_page1_layout 

# Importer le layout de la page 2
from page2 import create_page2_layout

# Importer les fonctions de callbacks
from callbacks import load_and_process_data
from callbacks import update_page1_content, toggle_slider, update_page2_content, display_page

# Charger les données et les catégories de produits 
file_path = os.path.join(os.getcwd(), 'data', 'ecbl-textiles.csv')
df, categories = load_and_process_data(file_path)

# Choisir des feuilles de style CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', \
                        'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialiser l'application Dash
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

# Définition des layouts de l'application
# Page 0 - Accueil ---------------------------------------------------------------------
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id = 'page-content')
])

index_page = create_page0_layout()

# Page 1 - Comparatif de coût environnemental - PEF ------------------------------------
layout_1 = create_page1_layout(df, categories)

@app.callback(Output (component_id='page-1-table', component_property='children'),
    [Input (component_id='page-1-dropdown', component_property='value'),
     Input (component_id='page-1-slider', component_property='value')])
def page1_callback(value, slider_value):
    return update_page1_content(value, slider_value, categories, df) 

# Ajouter un nouveau rappel pour contrôler la visibilité du slider
@app.callback(
    Output('page-1-slider', 'style'),
    Output('page-1-slider', 'key'),
    [Input('page-1-dropdown', 'value')]
)
def slider_callback(value):
    return toggle_slider(value)


# Page 2 - Comparatif de textile -------------------------------------------------------
layout_2 = create_page2_layout(df)

@app.callback(Output (component_id='page-2-table', component_property='children'),
    [Input (component_id='product-dropdown', component_property='value')])
def page2_callback(product):
    return update_page2_content(product, df)


# Mise à jour de l'index ---------------------------------------------------------------
@app.callback(dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')])
def page_callback(pathname):
    return display_page(pathname, index_page, layout_1, layout_2)


# Point d'entrée de l'application ------------------------------------------------------
def afficher_date():
    # Obtenir la date actuelle
    current_date = datetime.now()
    # Afficher la date actuelle dans le format souhaité
    print(f"Today's date is {current_date.strftime('%a. %d %b. %Y')}")

if __name__ == '__main__':
    # afficher_date()
    app.run_server(debug=True)

