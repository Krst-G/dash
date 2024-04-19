import dash
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table
from dash import dcc

df_geo = pd.read_csv('./data/df_geo.csv')
df_2 = pd.read_csv('./data/df_5_daily.csv')
## For distribution of weather days Barplot
weather_days = pd.read_csv('./data/weather_days.csv')
## Table weather days
weather_table= pd.read_csv('./data/weather_table.csv')

d_table = dash_table.DataTable(weather_table.to_dict('records'),
                                  [{"name": i, "id": i} for i in weather_table.columns],
                               style_data={'color': 'white','backgroundColor': 'black'},
                               style_header={
                                  'backgroundColor': 'rgb(210, 210, 210)',
                                  'color': 'black','fontWeight': 'bold'},
                              style_table={
                                         'minHeight': '100px', 'height': '200px', 'maxHeight': '200px',
                                         'minWidth': '1200px', 'width': '1200px', 'maxWidth': '1400px', 
                                         'marginLeft': 'auto', 'marginRight': 'auto',
                                     'marginTop': 0, 'marginBottom': 0} 
                                     )

fig_scatter = px.scatter_mapbox(
                        data_frame=df_geo,
                        lat='lat', 
                        lon='lon', 
                        hover_name='city',
                        color='city',
                        height=600,
                        # start location and zoom level
                        zoom=4, 
                        center={'lat': 48.25, 'lon': 11.4}, 
                        mapbox_style='open-street-map'
                       )
fig_scatter = fig_scatter.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
        )

fig_weather = px.bar(weather_days, 
             x='month_year', 
             y='sunny_days',  
             color='city',
             barmode='group',
             height=400, title = "Distribution of Sunny Days")
fig_weather = fig_weather.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
        )


fig_daily = px.scatter(data_frame=df_2, 
              x='date', 
              y='avg_temp_c', 
              height=500, 
              title="Daily Mean Temperatures of Last year",
              #markers=True,
              color='city'
             )
fig_daily = fig_daily.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white")


app =dash.Dash(external_stylesheets=[dbc.themes.DARKLY]) 

# Do not forget to add server=app.server!!!
server = app.server


app.layout = html.Div([
    html.H1('Weather comparison of five cities', style={'textAlign': 'center', 'color': 'coral'}),
    html.H2('Berlin - Paris - Prague - Rome - Warsaw', style={'paddingLeft': '30px'}),
    # html.H3('A map of the cities'),
    html.Div([
        html.Div('Map',
                 style={'backgroundColor': 'coral', 'color': 'black', 'width': "Germany"}),
        dcc.Graph(figure=fig_scatter),
        d_table,
        dcc.Graph(figure=fig_daily),
        dcc.Graph(figure=fig_weather)
    ])
])

if __name__ == '__main__':
     app.run_server() 