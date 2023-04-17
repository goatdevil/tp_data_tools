from dash import Dash, html,dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)
df_ratp=pd.read_csv("trafic-annuel-entrant-par-station-du-reseau-ferre-2021.csv",sep=";")
df_idf=pd.read_csv("emplacement-des-gares-idf.csv",sep=";")
df_ratp_sorted=df_ratp.sort_values(by="Trafic",ascending=False)
df_ratp_trafic=df_ratp_sorted[0:10]
df_ratp_ville=df_ratp_sorted.groupby(["Ville"]).sum()[0:5]
print(df_ratp_ville)


app.layout = html.Div(children=[
    html.H1("TP Data tools"),
    html.H2("Gauthier de Ponthaud"),
    dcc.Graph(
            id='bar-chart_trafic',
            figure=px.bar(df_ratp_trafic, x=df_ratp_trafic["Station"], y=df_ratp_trafic["Trafic"])
        ),
    dcc.Graph(
            id='pie-chart_ville',
            figure=px.pie(df_ratp_ville,df_ratp_ville["Station"],df_ratp_ville["Trafic"])
        ),


],style={'width': '49%', 'display': 'inline-grid', 'vertical-align': 'middle'})


if __name__ == '__main__':
    app.run_server(debug=True)
