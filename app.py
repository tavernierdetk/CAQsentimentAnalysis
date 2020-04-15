import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([

    dcc.DatePickerSingle(
        id='my-date-picker-single',
        min_date_allowed=dt(2020, 1, 1),
        max_date_allowed=dt(2023, 1, 1),
        initial_visible_month=dt(2020, 4, 1),
        date=str(dt(2020, 4, 1, 23, 59, 59))
    ),
    html.Div(id='output-container-date-picker-single'),
    html.Label('AM/PM'),
    dcc.Dropdown(
        options=[
            {'label': 'AM', 'value': 'AM'},
            {'label': 'PM', 'value': 'PM'}
        ],
        value='AM'
    ),
    html.Label('Heure'),
    dcc.Dropdown(
        options=[
            {'label': '00', 'value': '0'},
            {'label': '01', 'value': '1'},
            {'label': '02', 'value': '2'},
            {'label': '03', 'value': '3'},
            {'label': '04', 'value': '4'},
            {'label': '05', 'value': '5'},
            {'label': '06', 'value': '6'},
            {'label': '07', 'value': '7'},
            {'label': '08', 'value': '8'},
            {'label': '09', 'value': '9'},
            {'label': '10', 'value': '10'},
            {'label': '11', 'value': '11'}

        ],
        value='0',
        clearable=False
    ),
    html.Label(':'),
    dcc.Dropdown(
        options=[
            {'label': '00', 'value': '00'},
            {'label': '05', 'value': '05'},
            {'label': '10', 'value': '10'},
            {'label': '15', 'value': '15'},
            {'label': '20', 'value': '20'},
            {'label': '25', 'value': '25'},
            {'label': '30', 'value': '30'},
            {'label': '35', 'value': '35'},
            {'label': '40', 'value': '40'},
            {'label': '45', 'value': '45'},
            {'label': '50', 'value': '50'},
            {'label': '55', 'value': '55'}

        ],
        value='00',
        clearable=False
    ),

    html.Label('Type of post'),
    dcc.RadioItems(
        options=[
            {'label': 'Added Photos', 'value': 'added_photos'},
            {'label': 'Added Video', 'value': 'added_video'},
            {'label': 'Shared Story', 'value': 'shared_story'},
            {'label': 'Mobile Status Update', 'value': 'mobile_status_update'}
        ],
        value='shared_story'
    ),



    html.Label('Text Input'),
    dcc.Input(value='Contenu de la publication', size='2000'),

], style={'columnCount': 2})

if __name__ == '__main__':
    app.run_server(debug=True)