from dash import Dash, html, dcc, dependencies
import plotly.express as px
import pandas as pd

app = Dash(__name__)
df_ratp = pd.read_csv("trafic-annuel-entrant-par-station-du-reseau-ferre-2021.csv", sep=";")
df_idf = pd.read_csv("emplacement-des-gares-idf.csv", sep=";")
# step 1
df_ratp_sorted = df_ratp.sort_values(by="Trafic", ascending=False)
df_ratp_trafic = df_ratp_sorted[0:10]
df_ratp_ville = df_ratp_sorted.groupby(["Ville"]).sum()[0:5]



# step 2
df_idf_exploit = df_idf.groupby(["exploitant"])
df_idf_ligne = df_idf.groupby(["ligne"])
print(df_idf.groupby(["ligne"]).groups.keys())



app.layout = html.Div(children=[
    html.H1("TP Data tools"),
    html.H2("Gauthier de Ponthaud"),
    dcc.Dropdown(
            id='category-filter_reseau',
            options=[{'label': category, 'value': category} for category in df_ratp_trafic.groupby(['Réseau']).groups.keys()],
            value=None,
            placeholder='Choisissez un resau'
        ),
    html.Div(style={'display':'Flex'},children=[

    dcc.Graph(
        id='bar_chart_trafic',
        figure=px.bar(df_ratp_trafic, x=df_ratp_trafic["Station"], y=df_ratp_trafic["Trafic"])
    ),
    dcc.Graph(
        id='pie_chart_ville',
        figure=px.pie(df_ratp_ville,df_ratp_ville["Station"], df_ratp_ville["Trafic"])
    )


    ]),
    dcc.Dropdown(
            id='category-filter_exploitant',
            options=[{'label': category, 'value': category} for category in df_idf.groupby(['exploitant']).groups.keys()],
            value=None,
            placeholder='Choisissez un exploitant'
        ),
    dcc.Graph(
        id='bar_chart_exploitant',
        figure=px.bar(df_idf_exploit, x=df_idf_exploit.groups.keys(), y=df_idf_exploit.size())
    ),

    dcc.Graph(
            id='graph_ligne',
            figure=px.bar(df_idf_ligne, x=df_idf_ligne.groups.keys(), y=df_idf_ligne.size())
        ),

])
@app.callback(
    dependencies.Output('bar_chart_trafic', 'figure'),
    dependencies.Input('category-filter_reseau', 'value')
)

def update_bar_chart_trafic(category):
    if category is None:
        # Keep all categories if no value has been selected
        filtered_df = df_ratp_trafic
    else:
        # Filter the df based on selection


        filtered_df = df_ratp_trafic[df_ratp_trafic['Réseau'] == category]

    return px.bar(filtered_df, x='Station', y='Trafic')
@app.callback(
    dependencies.Output('graph_ligne', 'figure'),
    dependencies.Input('category-filter_exploitant', 'value')
)
def update_bar_chart_ligne(category):
    if category is None:
        # Keep all categories if no value has been selected
        filtered_df = df_idf_ligne
    else:
        # Filter the df based on selection
        filtered_df = df_idf[df_idf['exploitant'] == category]
        print(filtered_df.head())
        filtered_df=filtered_df.groupby(["ligne"])

    return px.bar(filtered_df, x=filtered_df.groups.keys(), y=filtered_df.size())



if __name__ == '__main__':
    app.run_server(debug=True)