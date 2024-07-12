from dash import html, dcc
import dash_bootstrap_components as dbc
from dash import dash_table

import plotly.graph_objects as go
import pandas as pd

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

def toggle_slider(value):
    if value == 'hist_pef':
        # Cacher le slider et changer sa clé
        return {'display': 'none'}, value
    else:
        # Afficher le slider et changer sa clé
        return {'display': 'block'}, value


# Page 2 - Comparatif de textile -------------------------------------------------------

def update_page2_content(product, df):
    # Sélectionner uniquement les colonnes 'pef', 'mass', 'product', 'price', 'description'
    df1 = df[['pef', 'mass', 'product', 'price', 'description']]
    # Filtrer le dataframe pour le produit sélectionné
    filtered_df = df1[df1["product"] == product]
    
    # Trier le dataframe par 'pef' en ordre croissant et sélectionner le top 5
    top_5_df = filtered_df.sort_values(by='pef', ascending=True).head(5)
    
    # Retourner le top 5 dataframe sous forme de DataTable
    return dash_table.DataTable(data=top_5_df.to_dict('records'), columns=[{'name': i, 'id': i} for i in top_5_df.columns])


def display_page(pathname, index_page, layout_1, layout_2):
    if pathname == '/page-1':
        return layout_1
    elif pathname == '/page-2':
        return layout_2
    else:
        return index_page
