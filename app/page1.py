# Importer les bibliothèques nécessaires
from dash import html, dcc

# créer le 'layout' de la page 1 -
def create_page1_layout(df, categories):
    return html.Div([
    html.H1('Comparatif de coût environnemental - PEF -', style={'textAlign': 'center', 'color': 'mediumturquoise'}),

    html.Div(dcc.Dropdown(id = 'page-1-dropdown',
                        options= [{'label': 'Tableau : -pef- de moins de 1516 pts pour 0.150 kg', 'value': 'acceptable'},
                                  {'label': 'Tableau : -pef- de plus de 1516 pts pour 0.150 kg', 'value': 'excessif'},
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


