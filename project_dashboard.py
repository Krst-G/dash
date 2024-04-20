import dash
from dash import Dash, html, dcc, callback
from dash.dependencies import Input, Output, State
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
## Table weather monthly bppra
weather_bppra= pd.read_csv('./data/df_bppra_monthly.csv')


### For Dropdown
df_cities =weather_bppra[weather_bppra['city'].isin(['Berlin', 'Paris', 'Prague','Rome', 'Warsaw'])]


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
             #color=
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


###### Berlin Paris Prague BARPLOTS
fig_weather_bppra = px.bar(weather_bppra, 
             x='month_year', 
             y='avg_temp_c',  
             color='city',
             barmode='group',
             height=400, title = "Distribution of avg Temperatures per Month")
fig_weather_bppra = fig_weather_bppra.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
        )
graph_bppra = dcc.Graph(figure=fig_weather_bppra)
##################

app =dash.Dash(external_stylesheets=[dbc.themes.DARKLY]) 

# Do not forget to add server=app.server!!!
server = app.server

graph = dcc.Graph()
cities =df_cities['city'].unique().tolist() 
dropdown = dcc.Dropdown(['Berlin', 'Paris', 'Prague', 'Rome', 'Warsaw'], value=['Berlin', 'Paris', 'Prague','Rome', 'Warsaw'], 
                        clearable=False, multi=True, style ={'paddingLeft': '30px', 
                                                             "backgroundColor": "#222222", "color": "#222222"})

app.layout = html.Div([
    html.H1('In need of a perfect weekend getaway?', style={'textAlign': 'center', 'color': 'coral'}),
    html.H2('Let us check some  weather details for these five cities ', style={'paddingLeft': '30px'}),
    # html.H3('A map of the cities'),
    html.Div([
        html.Div('Berlin - Paris - Prague - Rome - Warsaw',
                 style={'backgroundColor': 'coral', 'color': 'black', 'width': "Germany"}),
        dcc.Graph(figure=fig_scatter),
        d_table,
        dcc.Graph(figure=fig_daily),dropdown,
        graph_bppra,
        dcc.Graph(figure=fig_weather)
    ])
])

@app.callback(
    Output(graph_bppra, "figure"), 
    Input(dropdown, "value"))     ### check if error now gone bc no more ' '
def update_bar_chart(selected_cities): 
    mask = df_cities["city"].isin(selected_cities)
    filtered_df = df_cities[mask]
    fig = px.bar(filtered_df, 
                 x='month_year', 
                 y='avg_temp_c',  
                 color='city',
                 color_discrete_map={'Berlin': '#0b2df4', 'Paris': '#F7545D', 'Prague': '#7FD497'
                                     , 'Rome':'#AF76F8', 'Warsaw':'#F79C54'},
                 barmode='group',
                 height=300, title="Avg Temperature Values")
    fig = fig.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )

    return fig

# whatever you are returning here is connected to the component property of
                       #the output which is figure

if __name__ == '__main__':
     app.run_server() 