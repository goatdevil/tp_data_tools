from dash import Dash, html, dcc, dependencies
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd



app = Dash(__name__)
df_ratp = pd.read_csv("trafic-annuel-entrant-par-station-du-reseau-ferre-2021.csv", sep=";")
df_idf = pd.read_csv("emplacement-des-gares-idf_changer.csv", sep=";")
# step 1
df_ratp_sorted = df_ratp.sort_values(by="Trafic", ascending=False)
df_ratp_trafic = df_ratp_sorted[0:10]
df_ratp_ville = df_ratp.groupby(["Ville"]).sum().sort_values(by="Trafic", ascending=False)[0:5]
print(df_ratp_ville.index)



# step 2
df_idf_exploit = df_idf.groupby(["exploitant"])
df_idf_ligne = df_idf.groupby(["ligne"])


#step 4
df_idf[['lat', 'lng']] = df_idf['geo_point'].str.split(',', expand=True)
df_idf['lat'] = df_idf['lat'].str.strip().astype(float)
df_idf['lng'] = df_idf['lng'].str.strip().astype(float)
df_map=pd.DataFrame({'Nom':df_idf['nom_iv'],'Lat':df_idf['lat'],'Lon':df_idf['lng'],'Ligne':df_idf["ligne"]})
couleur=[]
dico_couleur = {"METRO 1":"#FFCE00",
                "METRO 2":"#0064B0",
                "METRO 3":"#9F9825",
                "METRO 3bis":"#98D4E2",
                "METRO 4":"#C04191",
                "METRO 5":"#F28E42",
                "METRO 6":"#83C491",
                "METRO 7":"#F3A4BA",
                "METRO 7bis":"#83C491",
                "METRO 8":"#CEADD2",
                "METRO 9":"#D5C900",
                "METRO 10":"#E3B32A",
                "METRO 11":"#8D5E2A",
                "METRO 12":"#00814F",
                "METRO 13":"#98D4E2",
                "METRO 14":"#662483",
                "RER A":"#F7403A",
                "RER B":"#4B92DB",
                "RER C":"#F3D311",
                "RER D":"#3F9C35",
                "RER E":"#DE81D3",
                "TRAM 1":"#0064B0",
                "TRAM 2":"#C04191",
                "TRAM 3a":"#F28E42",
                "TRAM 3b":"#00814F",
                "TRAM 4":"#E3B32A",
                "TRAM 5":"#662483",
                "TRAM 6":"#E3051C",
                "TRAM 7":"#8D5E2A",
                "TRAM 8":"#9F9825",
                "TRAM 9":"#5291CE",
                "TRAM 11":"#FB4F14",
                "TRAM 13":"#6e4c1e",
                "TRAIN H":"#844C54",
                "TRAIN J":"#B6BF00",
                "TRAIN K":"#AE9A00",
                "TRAIN L":"#7577C0",
                "TRAIN N":"#00B092",
                "TRAIN P":"#EAAB00",
                "TRAIN R":"#E59FDB",
                "TRAIN U":"#C90062",
                "ORLYVAL":"rgb(94,197,237)",
                "CDGVAL":"rgb(22,15,85)",
                "FUNICULAIRE MONTMARTRE":"rgb(0,10,130)",
                "GL":"rgb(173,20,121)"
                }
couleur=[]
for point in df_map.values:
    couleur.append(dico_couleur[point[3]])
df_map["couleur"]=couleur

#print(ligne)


grouped_df_map=df_map.groupby(['Ligne'])
ligne=grouped_df_map.groups.keys()


#print(grouped_df_map.get_group('TRAM 6')['couleur'])


marker=go.scattermapbox.Marker(
    size=10,
    color='rgb(242,177,172)'
)
fig=go.Figure()
indice=0

for x in ligne:
    new_df_map=grouped_df_map.get_group(x)
    fig.add_trace(go.Scattermapbox(
            mode="markers",
            name=x,
            lat=new_df_map['Lat'],
            lon=new_df_map['Lon'],
            hovertext=new_df_map['Nom'],
            marker={
                'color': new_df_map["couleur"],
                'size':10
            },
        ))
    indice+=1

fig.update_layout(margin ={'l':0,'t':0,'b':0,'r':0},
                  mapbox = {
                      'center': {'lon':2.3473213170674256 , 'lat': 48.85493637743783},
                      'style': "stamen-terrain",
                      'zoom': 9},
                  width=1600,
                  height=900,)



app.layout = html.Div(children=[
    html.Div(className="header",children=[
        html.H1("TP Data Tools"),
        html.H2("Gauthier de Ponthaud"),
    ]),

    html.Div(className="separeteur"),
    html.P("Choissiez un réseau pour filtrer les résultats exposer dans le graphique en barre"),
    dcc.Dropdown(
            id='category-filter_reseau',
            options=[{'label': category, 'value': category} for category in df_ratp_trafic.groupby(['Réseau']).groups.keys()],
            value=None,
            placeholder='Choisissez un resau'
        ),
    html.Div(className="ratp_Charts",style={'display':'Flex'},children=[
    dcc.Graph(
        className='bar_chart_trafic',
        id='bar_chart_trafic',
        figure=px.bar(df_ratp_trafic, x=df_ratp_trafic["Station"], y=df_ratp_trafic["Trafic"],title="Traffic par Station")
    ),
    dcc.Graph(
        className='pie_chart_ville',
        id='pie_chart_ville',
        figure=px.pie(df_ratp_ville,df_ratp_ville.index, df_ratp_ville["Trafic"],title="Traffic par station (5 plus grosses stations uniquement)").update_layout(showlegend=False,)

    )


    ]),
    html.Div(className="separeteur"),
    html.P("Choissiez un exploitant pour filtrer les résultats exposer dans le graphique de nombre de station par ligneà"),
    dcc.Dropdown(
            id='category-filter_exploitant',
            options=[{'label': category, 'value': category} for category in df_idf.groupby(['exploitant']).groups.keys()],
            value=None,
            placeholder='Choisissez un exploitant'
        ),
    html.Div(className="idf_Charts",children=[
    html.H3("Nombre de stations par exploitant"),
    dcc.Graph(
        className='bar_chart_exploitant',
        id='bar_chart_exploitant',
        figure=px.bar(df_idf_exploit, x=df_idf_exploit.groups.keys(), y=df_idf_exploit.size())
    ),
    html.H3("Nombre de stations par ligne"),
    dcc.Graph(
            className='graph_ligne',
            id='graph_ligne',
            figure=px.bar(df_idf_ligne, x=df_idf_ligne.groups.keys(), y=df_idf_ligne.size())
        ),
    ]),
    html.Div(className="separeteur"),
    html.H3("Carte des transports d'île de France"),
    html.Div(className="map",children=[
    html.P("vous pouvez cliquer sur les noms des lignes dans la légende pour effacer ou faire apparaitre les points."),
    dcc.Graph(
        id="map",
        figure=fig
    ),
    ]),




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