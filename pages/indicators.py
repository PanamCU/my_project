from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from data import df  

layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div([
            html.H1("Статистика", style={'textAlign': 'center'}),
            html.P("Анализ основных показателей по странам мира.", style={'textAlign': 'center'}),
            html.Hr(style={'color': 'black'}),
        ])),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Label("Выберите континент:"),
            dcc.Dropdown(
                id='continent-dropdown',
                options=[{'label': cont, 'value': cont} for cont in df['continent'].unique()],
                value=[df['continent'].unique()[0]],
                multi=True
            ),
        ], width=3),
        dbc.Col([
            dbc.Label("Выберите интервал лет:"),
            dcc.RangeSlider(
                id='year-slider',
                min=df['Year'].min(),
                max=df['Year'].max(),
                value=[df['Year'].min(), df['Year'].max()],
                marks={str(year): str(year) for year in range(df['Year'].min(), df['Year'].max()+1)},
            ),
        ], width=9),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Label("Выберите показатель:"),
            dbc.RadioItems(
                options=[
                    {'label': 'Продолжительность жизни', 'value': 'Life expectancy'},
                    {'label': 'Население', 'value': 'Population'},
                    {'label': 'ВВП', 'value': 'GDP'},
                    {'label': 'Школьное образование', 'value': 'Schooling'},
                ],
                value='Life expectancy',
                id='indicator-radio',
            ),
        ], width=3),
        dbc.Col([
            dcc.Graph(id='indicator-graph', config={'displayModeBar': False}),
        ], width=9),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='top-3-countries-bar', config={'displayModeBar': False}, style={'width': '100%', 'height': '35vh'}),
        ], width=6),
        dbc.Col([
            dcc.Graph(id='histogram', config={'displayModeBar': False}),
        ], width=6),
    ]),
])

@callback(
    Output('indicator-graph', 'figure'),
    [
        Input('continent-dropdown', 'value'),
        Input('year-slider', 'value'),
        Input('indicator-radio', 'value'),
    ]
)
def update_graph(selected_continents, selected_years, selected_indicator):
    if isinstance(selected_continents, str):
        selected_continents = [selected_continents]
    
    filtered_df = df[(df['continent'].isin(selected_continents)) &
                     (df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])]
    
    line_fig = px.line(filtered_df, x='Year', y=selected_indicator, color='Country',
                       labels={'Year': 'Год', selected_indicator: selected_indicator},
                       title=f'Динамика по странам')
    
    line_fig.update_layout(margin={"r": 20, "t": 50, "l": 20, "b": 20})
    
    return line_fig

@callback(
    Output('top-3-countries-bar', 'figure'),
    [
        Input('continent-dropdown', 'value'),
        Input('year-slider', 'value'),
        Input('indicator-radio', 'value'),
    ]
)
def update_top_3_countries(selected_continents, selected_years, selected_indicator):
    if isinstance(selected_continents, str):
        selected_continents = [selected_continents]
    
    filtered_df = df[(df['continent'].isin(selected_continents)) &
                     (df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])]
    
    top_3_countries = filtered_df.groupby('Country')[selected_indicator].sum().nlargest(3).reset_index()
    
    bar_fig = px.bar(top_3_countries, x='Country', y=selected_indicator, color='Country',
                     title=f'Топ 3 страны по выбанному показателю',
                     labels={'Country': 'Страна', selected_indicator: selected_indicator})
    
    return bar_fig

@callback(
    Output('histogram', 'figure'),
    [
        Input('continent-dropdown', 'value'),
        Input('year-slider', 'value'),
        Input('indicator-radio', 'value'),
    ]
)
def update_histogram(selected_continents, selected_years, selected_indicator):
    if isinstance(selected_continents, str):
        selected_continents = [selected_continents]
    
    filtered_df = df[(df['continent'].isin(selected_continents)) &
                     (df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])]
    
    histogram_fig = px.histogram(filtered_df, x=selected_indicator, title=f'Гистограмма по выбранному показателю')
    
    return histogram_fig
