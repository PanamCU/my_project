import dash_bootstrap_components as dbc

from dash import Dash, Input, Output, dcc, html
from pages import all_map, country, indicators


external_stylesheets = [dbc.themes.LUX] 
app = Dash(__name__, external_stylesheets=external_stylesheets,  use_pages=True)
app.config.suppress_callback_exceptions = True

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "22rem",
    "padding": "2rem 1rem",
    "background-color": "#ffc0cb", # Цвет фона боковой панели меняем на тот, который больше всего подходит
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Показатели стран мира", className="display-6"),
        html.Hr(),
        html.P(
            "Учебный проект студентов БСБО-14-21", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Карта мира", href="/", active="exact"),
                dbc.NavLink("Страны", href="/page-1", active="exact"),
                dbc.NavLink("Статистика", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")])

def render_page_content(pathname):
    if pathname == "/":
        return all_map.layout
    elif pathname == "/page-1":
        return country.layout
    elif pathname == "/page-2":
        return indicators.layout
    # Если пользователь попытается перейти на другую страницу, верните сообщение 404. Мы изменим её в следующей практической.
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

if __name__ == '__main__':
        app.run_server(debug=True)
