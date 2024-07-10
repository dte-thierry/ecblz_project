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
import plotly.graph_objects as go

# Importer le layout de la page d'accueil - page 0 -
from page0 import create_page0_layout

# Charger les données
df = pd.read_csv('data/ecbl-textiles.csv')
df['pef_group'] = ['acceptable' if pef < 1500 else 'excessif' for pef in df['pef']]

# Arrondir la colonne 'mass' à 3 chiffres après la virgule
df['mass'] = df['mass'].round(3)
# Supprimer la colonne '_id'
df = df.drop(columns=['_id'])
# Renommer la colonne 'Unnamed: 1' en 'tag'
df = df.rename(columns={'Unnamed: 1': 'tag'})
# Définir les catégories de produits
categories = df['product'].unique()

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
layout_1 = html.Div([
    html.H1('Comparatif de coût environnemental - PEF -', style={'textAlign': 'center', 'color': 'mediumturquoise'}),

    html.Div(dcc.Dropdown(id = 'page-1-dropdown',
                        options= [{'label': 'Tableau : -pef- de moins de 1500 pts pour 0.150 kg', 'value': 'acceptable'},
                                  {'label': 'Tableau : -pef- de plus de 1500 pts pour 0.150 kg', 'value': 'excessif'},
                                  {'label': 'Etiquettes : Top 5 des meilleurs scores -pef-', 'value': 'top5_pef'},  
                                  {'label': 'Histogramme -pef- : distribution des scores de performance environnementale', 'value': 'hist_pef'}, 
                                  {'label': 'Diagramme à barres -pef_group- : nbre de produits dans chaque groupe', 'value': 'bar_pef'}, 
                                  {'label': 'Diagramme de dispersion de -price- vs -pef- : ', 'value': 'disp_pef'}],                               
                        value= 'acceptable')),
        
    html.Div(dcc.Slider(id='page-1-slider',
                      min=0,
                      max=len(categories) - 1,
                      step=None,
                      marks={i: categories[i] for i in range(len(categories))},
                      value=0)),  
    
    html.Div(id='page-1-table'),

    html.Br(),
    
    html.Button(dcc.Link('Retour à la page d\'accueil', href='/'))

], style = {'background' : 'beige'})

@app.callback(Output (component_id='page-1-table', component_property='children'),
    [Input (component_id='page-1-dropdown', component_property='value'),
     Input (component_id='page-1-slider', component_property='value')])

def update_page1_content(value, slider_value):
    # obtenir la catégorie du slider
    category = categories[slider_value]
    # Filtrer le dataframe en fonction de la catégorie
    filtered_df = df[df["product"] == category]  

    if value in ['acceptable', 'excessif']:
        filtered_df = filtered_df[filtered_df["pef_group"] == value]
        return dash_table.DataTable(data=filtered_df.to_dict('records'), columns=[{'name': i, 'id': i} for i in filtered_df.columns])
    
    elif value == 'top5_pef':        
        top5_pef = filtered_df.nsmallest(5, 'pef')  # Sélectionner les 5 meilleurs (les plus petits) scores - pef -
        top5_price = top5_pef.sort_values('price') # Ordonner du moins cher au plus cher
        cards = []
        for _, product in top5_price.iterrows():
            card_content = [
                html.H5(f"{product['tag']}", className="card-title"),
                html.P(f"Coût environnemental: {product['pef']}", className="card-text"),
            ]
            card = html.Div(
                dbc.Card(card_content, color="primary", inverse=True),
                className="col-md-8",
                style={"maxWidth": "260px"},
            )
            cards.append(card)
        return cards
    
    elif value == 'hist_pef':
        # calculer la moyenne pef
        mean_pef = df['pef'].mean()
        # créer l'histogramme
        fig = go.Figure(data=[go.Histogram(x=df['pef'])])
        # ajouter une ligne horizontale pour représenter la moyenne
        fig.add_shape(
            type="line",
            x0=0,
            x1=1,
            xref='paper',
            y0=mean_pef,
            y1=mean_pef,
            line=dict(
                color="Red",
                width=3,
            )
        )
        # mettre à jour le layout
        fig.update_layout(
            title_text='Histogramme PEF : Distribution des scores de performance environnementale',
            xaxis_title="Nombre de produits",
            yaxis_title="PEF Score",
            annotations=[
                dict(
                    x=1,
                    y=mean_pef,
                    xref='paper',
                    yref='y',
                    text=f"Moyenne PEF : {mean_pef:.2f}",
                    showarrow=False,
                    font=dict(
                        size=12,
                        color="Black"
                    ),
                    bgcolor="White",
                    bordercolor="Black",
                    borderwidth=2,
                    borderpad=4,
                    opacity=0.8
                )
            ]
        )  
        return dcc.Graph(figure=fig) 
    

# Page 2 - Comparatif de textile -------------------------------------------------------
layout_2 = html.Div([
    html.H1('Comparatif de textile', style={'textAlign': 'center', 'color': 'mediumturquoise'}),

    html.Div(dcc.Dropdown(id = 'product-dropdown',
                          options= [{'label': 'Table : ' + product + " : ayant le coût environnemental (pef) le plus faible", 'value': product} for product in df['product'].unique()] +
                                   [{'label': 'Diagramme à barres empilées : pays impliqués dans chaque étape de la fabrication', 'value': 'pays_fab'}],
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

