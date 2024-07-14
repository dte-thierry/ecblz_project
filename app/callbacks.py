from dash import html, dcc
import dash_bootstrap_components as dbc
from dash import dash_table

import plotly.graph_objects as go
import plotly.express as px

import pandas as pd
import numpy as np

# Charger les données
def load_and_process_data(file_path):      
    # Charger les données
    df = pd.read_csv(file_path)    
    df['pef_group'] = ['acceptable' if pef < 1516 else 'excessif' for pef in df['pef']]
    # Arrondir la colonne 'mass' à 3 chiffres après la virgule
    df['mass'] = df['mass'].round(3)
    # Supprimer la colonne '_id'
    df = df.drop(columns=['_id'])
    # Renommer la colonne 'Unnamed: 1' en 'tag'
    df = df.rename(columns={'Unnamed: 1': 'tag'})
    # Définir les catégories de produits
    categories = df['product'].unique()
    return df, categories


# Page 1 - Comparatif de coût environnemental - PEF ------------------------------------

def update_page1_content(value, slider_value, categories, df):
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
        fig = go.Figure(data=[go.Histogram(y=df['pef'])])
        # ajouter une ligne verticale pour représenter la moyenne
        fig.add_shape(
            type="line",
            x0=mean_pef,
            x1=mean_pef,
            yref='paper',
            y0=0,
            y1=1,
            line=dict(
                color="Red",
                width=3,
            )
        )
        # mettre à jour le layout
        fig.update_layout(
            title_text='Histogramme PEF : Distribution des scores de performance environnementale',
            yaxis_title="Nombre de produits",
            xaxis_title="PEF Score",
            annotations=[
                dict(
                    y=1,
                    x=mean_pef,
                    yref='paper',
                    xref='x',
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

    elif value == 'bar_pef':
        # regrouper le dataframe par 'pef_group', et compter le nombre de textiles dans chaque groupe
        group_counts = df['pef_group'].value_counts()
        # Créer le graphique
        fig = go.Figure(data=go.Bar(x=group_counts.index, y=group_counts.values))
        # Update the layout
        fig.update_layout(
            title_text='Diagramme à barres PEF Group : Nombre de produits dans chaque groupe',
            xaxis_title="Groupe PEF",
            yaxis_title="Nombre de produits"
        )
        return dcc.Graph(figure=fig)
    
    elif value == 'disp_pef':
        # Créer le diagramme de dispersion
        fig = go.Figure()

        # Ajouter les points de données, colorés par catégorie
        for category in filtered_df['product'].unique():
            df_category = filtered_df[filtered_df['product'] == category]
            fig.add_trace(go.Scatter(x=df_category['price'], y=df_category['pef'], mode='markers', name=category))

        # Calculer la ligne de tendance
        m, b = np.polyfit(filtered_df['price'], filtered_df['pef'], 1)
        fig.add_trace(go.Scatter(x=filtered_df['price'], y=m*filtered_df['price'] + b, mode='lines', name='Tendances globales', line=dict(color='red')))

        # Mettre à jour le layout
        fig.update_layout(
            title_text='Diagramme de dispersion : Prix (en €uros) / Score PEF',
            xaxis_title="Prix (en €uros)",
            yaxis_title="Score PEF"
        )
        return dcc.Graph(figure=fig)

def toggle_slider(value):
    if value == 'hist_pef':
        # Cacher le slider et changer sa clé
        return {'display': 'none'}, value
    else:
        # Afficher le slider et changer sa clé
        return {'display': 'block'}, value


# Page 2 - Comparatif de textile -------------------------------------------------------

def update_page2_content(value, categories, df):
    if value == 'pays_fab':

        # calculer le total de chaque étape 
        total_fabric = df['countryFabric'].count()
        total_spinning = df['countrySpinning'].count()
        total_dyeing = df['countryDyeing'].count()
        total_making = df['countryMaking'].count()

        # Calculer les pourcentages de chaque pays pour chaque étape de fabrication
        fabric_percentages = ((df['countryFabric'].value_counts() / total_fabric) * 100).round(2)
        spinning_percentages = ((df['countrySpinning'].value_counts() / total_spinning) * 100).round(2)
        dyeing_percentages = ((df['countryDyeing'].value_counts() / total_dyeing) * 100).round(2)
        making_percentages = ((df['countryMaking'].value_counts() / total_making) * 100).round(2)

        # trier les pourcentages en ordre croissant
        fabric_percentages.sort_values(inplace=True)
        spinning_percentages.sort_values(inplace=True)
        dyeing_percentages.sort_values(inplace=True)
        making_percentages.sort_values(inplace=True)

        # Créer les traces pour le diagramme à barres
        trace1 = go.Bar(
            x=fabric_percentages.index,
            y=fabric_percentages.values,
            name='Tissu'
        )
        trace2 = go.Bar(
            x=spinning_percentages.index,
            y=spinning_percentages.values,
            name='Filature'
        )
        trace3 = go.Bar(
            x=dyeing_percentages.index,
            y=dyeing_percentages.values,
            name='Teinture'
        )
        trace4 = go.Bar(
            x=making_percentages.index,
            y=making_percentages.values,
            name='Fabrication'
        )
        # Créer la figure pour le diagramme à barres
        figure = {
            'data': [trace1, trace2, trace3, trace4],
            'layout': go.Layout(
                title='Répartition des pays pour chaque étape de fabrication (en %)',
                barmode='stack'
            )
        }
        # Définir les codes pays
        country_codes = {
        "TR": "Turquie",
        "MM": "Myanmar",
        "IN": "Inde",
        "CN": "Chine",
        "ROC": "Région Océanie",
        "VN": "Vietnam",
        "BD": "Bangladesh",
        "RNA": "Région Amérique du Nord",
        "RAF": "Région Afrique",
        "---": "Inconnu",
        "REE": "Région Europe de l'Est",
        "TN": "Tunisie",
        "RLA": "Région Amérique Latine",
        "MA": "Maroc",
        "REO": "Région Europe de l'Ouest",
        "KH": "Cambodge",
        "FR": "France",
        "PK": "Pakistan",
        "RAS": "Région Asie",
        "RME": "Région Moyen-Orient"
        }
        # définir 5 listes pour 5 colonnes
        country_codes1 = list(country_codes.items())[:4]
        country_codes2 = list(country_codes.items())[4:8]
        country_codes3 = list(country_codes.items())[8:12]
        country_codes4 = list(country_codes.items())[12:16]
        country_codes5 = list(country_codes.items())[16:]
        # Créer 5 colonnes de codes pays
        column1 = html.Ul([html.Li(f"{code} : {country}") for code, country in country_codes1])
        column2 = html.Ul([html.Li(f"{code} : {country}") for code, country in country_codes2])
        column3 = html.Ul([html.Li(f"{code} : {country}") for code, country in country_codes3])
        column4 = html.Ul([html.Li(f"{code} : {country}") for code, country in country_codes4])
        column5 = html.Ul([html.Li(f"{code} : {country}") for code, country in country_codes5])
        # créer un 'div' HTML avec 5 colonnes
        div = html.Div([
            html.Div(column1, style={'width': '20%', 'display': 'inline-block'}),
            html.Div(column2, style={'width': '20%', 'display': 'inline-block'}),
            html.Div(column3, style={'width': '20%', 'display': 'inline-block'}),
            html.Div(column4, style={'width': '20%', 'display': 'inline-block'}),
            html.Div(column5, style={'width': '20%', 'display': 'inline-block'})
        ])
        # retourne le graphe et le 'div' HTML
        return html.Div([dcc.Graph(figure=figure), div], style = {'background' : 'white'})
    
    elif value == 'bar_mat':
        return None
    
    elif value == 'bar_bu':
        return None
    
    elif value == 'bar_trace':
        return None
    
    elif value == 'bar_process':
        return None
    
    elif value == 'bar_market':
        return None
    
    elif value == 'bar_ref':
        return None
    

def display_page(pathname, index_page, layout_1, layout_2):
    if pathname == '/page-1':
        return layout_1
    elif pathname == '/page-2':
        return layout_2
    else:
        return index_page
