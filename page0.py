from dash import html, dcc

# Définir une function pour créer le 'layout' de la page d'accueil - page 0 -
def create_page0_layout():
    return html.Div([
    html.H1(
        'Dashboard EcoBalyze', 
        style={'color' : 'mediumturquoise', 'textAlign': 'center'}),

    html.Div(
        html.A(
            id="link1",
            children="Cliquer ici pour visiter le site EcoBalyze",
            href="https://ecobalyse.beta.gouv.fr/#/",
            target="_blank",
            style={'color': 'blue'}
        ),
        style={'textAlign': 'center'}
    ),

    # Ajouter une balise div et un paragraphe d'information
    html.Div([
        dcc.Markdown('''
            ## A propos ...                        
        ''')
    ], style={'color': 'mediumturquoise'}),

    html.Div([
        html.P([
            html.H3('Textiles & Environnement'),
            "L'industrie textile est l'une des plus polluantes au monde ", html.Sup('1 , 2 , 3 , 4 , 5'), ".", html.Br(),
            "En lien avec les préoccupations actuelles, et sur la base d'",
            html.A(id="link2", children="Écobalyze", href="https://ecobalyse.beta.gouv.fr/", target="_blank", style={'color': 'blue'}),
            ", cet outil propose un comparatif de coûts environnementaux, en vue de favoriser un modèle de production plus durable, ", 
            "et fournir des recommandations, ou des conseils, sur la manière de réduire l'impact écologique de textiles courants.", html.Br(), html.Br(),
            html.Code("En savoir plus : "), html.Br(),
            html.Sup('1'), html.A(id="sup1", children="la-goose.com", href="https://la-goose.com/les-impacts-environnementaux-du-textile-comment-les-reduire/", target="_blank", style={'color': 'blue'}), ", ",
            html.Sup('2'), html.A(id="sup2", children="oxfamfrance.org", href="https://www.oxfamfrance.org/agir-oxfam/impact-de-la-mode-consequences-sociales-environnementales/", target="_blank", style={'color': 'blue'}), ", ",
            html.Sup('3'), html.A(id="sup3", children="ecologie.gouv.fr", href="https://www.ecologie.gouv.fr/mieux-informer-consommateur-vers-affichage-environnemental-des-vetements-indiquer-leur-impact", target="_blank", style={'color': 'blue'}), ", ",
            html.Sup('4'), html.A(id="sup4", children="climateseed.com", href="https://climateseed.com/fr/blog/secteur-du-textile-impact-environnemental-et-r%C3%A9glementation", target="_blank", style={'color': 'blue'}), ", ",
            html.Sup('5'), html.A(id="sup5", children="wwf.ch", href="https://www.wwf.ch/fr/nos-objectifs/rapport-du-wwf-sur-lindustrie-de-lhabillement-et-des-textiles", target="_blank", style={'color': 'blue'}), ", "
        ])
    ]),

    html.Br(),

    html.Button(
        dcc.Link('Comparatif de Coût Environnemental - pef -', 
                 href='/page-1')),
    html.Br(),

    html.Button(
        dcc.Link('Comparatif de Textile', 
                 href='/page-2'))

    ], style={'background' : 'beige', 'alignItems': 'center'})
