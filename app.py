from dash import Dash, html, dcc
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
print(df_idf_ligne.groups.keys().__sizeof__())

app.layout = html.Div(children=[
    html.H1("TP Data tools"),
    html.H2("Gauthier de Ponthaud"),
    html.Div(style={'display':'Flex'},children=[
    dcc.Graph(
        id='bar-chart_trafic',
        figure=px.bar(df_ratp_trafic, x=df_ratp_trafic["Station"], y=df_ratp_trafic["Trafic"])
    ),
    dcc.Graph(
        id='pie-chart_ville',
        figure=px.pie(df_ratp_ville, df_ratp_ville["Station"], df_ratp_ville["Trafic"])
    )]),
    dcc.Graph(
        id='bar-chart_exploitant',
        figure=px.bar(df_idf_exploit, x=df_idf_exploit.groups.keys(), y=df_idf_exploit.size())
    ),

    dcc.Graph(
            id='bar-chart_ligne',
            figure=px.bar(df_idf_ligne, x=df_idf_ligne.groups.keys(), y=df_idf_ligne.size())
        ),

])

if __name__ == '__main__':
    app.run_server(debug=True)
