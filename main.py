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

# Importer le layout de la page d'accueil - page 0 -
from page0 import create_page0_layout

# Charger les données
df = pd.read_csv('data/ecbl-textiles.csv')
df['pef_group'] = ['acceptable' if pef < 1500 else 'excessif' for pef in df['pef']]

# Arrondir la colonne 'mass' à 2 chiffres après la virgule
df['mass'] = df['mass'].round(2)
# Supprimer la colonne '_id'
df = df.drop(columns=['_id'])
# Renommer la colonne 'Unnamed: 1' en 'tag'
df = df.rename(columns={'Unnamed: 1': 'tag'})

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

index_page = create_page0_layout()

# Page 1 - Comparatif de coût environnemental - PEF ------------------------------------
layout_1 = html.Div([
    html.H1('Comparatif de coût environnemental - PEF -', style={'textAlign': 'center', 'color': 'mediumturquoise'}),

    html.Div(dcc.Dropdown(id = 'page-1-dropdown',
                        options= [{'label': 'acceptable - pef de moins de 1500 pts pour 0.150 kg', 'value': 'acceptable'},
                                  {'label': 'excessif - pef de plus de 1500 pts pour 0.150 kg', 'value': 'excessif'}],
                                  # Ajout de nouvelles options                                  
                        value= 'acceptable')),
        
    html.Div(id='page-1-table'),

    html.Br(),
    
    html.Button(dcc.Link('Retour à la page d\'accueil', href='/'))

], style = {'background' : 'beige'})

@app.callback(Output (component_id='page-1-table', component_property='children'),
    [Input (component_id='page-1-dropdown', component_property='value')])
def update_page1_content(value):
    if value in ['acceptable', 'excessif']:
        filtered_df = df[df["pef_group"] == value]
        return dash_table.DataTable(data=filtered_df.to_dict('records'), columns=[{'name': i, 'id': i} for i in filtered_df.columns])
    

# Page 2 - Comparatif de textile -------------------------------------------------------
layout_2 = html.Div([
    html.H1('Comparatif de textile', style={'textAlign': 'center', 'color': 'mediumturquoise'}),

    html.Div(dcc.Dropdown(id = 'product-dropdown',
                          options= [{'label': product + " : ayant le coût environnemental (pef) le plus faible", 'value': product} for product in df['product'].unique()],
                          value= df['product'].unique()[0])),

    html.Div(id='page-2-table'),
    
    html.Br(),
    
    html.Button(dcc.Link('Retour à la page d\'accueil', href='/'))

], style = {'background' : 'beige'})

@app.callback(Output (component_id='page-2-table', component_property='children'),
    [Input (component_id='product-dropdown', component_property='value')])
def update_page2_content(product):
    # Sélectionner uniquement les colonnes 'pef', 'mass', 'product', 'price', 'description'
    df1 = df[['pef', 'mass', 'product', 'price', 'description']]
    # Filtrer le dataframe pour le produit sélectionné
    filtered_df = df1[df1["product"] == product]
    
    # Trier le dataframe par 'pef' en ordre croissant et sélectionner le top 5
    top_5_df = filtered_df.sort_values(by='pef', ascending=True).head(5)
    
    # Retourner le top 5 dataframe sous forme de DataTable
    return dash_table.DataTable(data=top_5_df.to_dict('records'), columns=[{'name': i, 'id': i} for i in top_5_df.columns])

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

