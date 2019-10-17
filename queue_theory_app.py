import plotly_express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_table as dt
from dash_table.Format import Format, Scheme, Sign, Symbol
import dash_daq as daq

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# sliders

arrivals_per_hour_slider = list(range(100, 1100, 100))
service_mins_per_server_slider = list(range(1, 16, 1))
max_wait_time_slider = list(range(0, 125, 5))



dd = {'Average service time (mins)': 0,
'Customers served per hour': 0,
'Time spent in the queue (mins)': 0,
#'Customers in the system': np.round(N, 2),
'Server use (recommended < 0.8)': 0,
'Number of servers obtained': 0}

df = pd.DataFrame(dd, index=[''])

app.layout = html.Div([
    html.Img(
                src="https://images.pexels.com/photos/761295/pexels-photo-761295.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500",
                style={
                    'height': '20%',
                    'width': '20%',
                    'float': 'center',
                    'position': 'left',
                    'padding-top': 0,
                    'padding-right': 0
                },
            ),
    html.H3("Simulation  (Queue Theory)"),
            
    # html.Br(),
    html.Div([
        # html.Br(),
        html.Label('Select number of arrivals per hour'),
        daq.Slider( # Slider to select the number of arrivals
                id="arrivalSlider",
                # count=100,
                min=np.min(arrivals_per_hour_slider),
                max=np.max(arrivals_per_hour_slider),
                step=100,
                # value=[np.min(arrivals_per_hour_slider), np.max(arrivals_per_hour_slider)],
                marks={i: str(i) for i in arrivals_per_hour_slider},
                size=700,
            included=False),
    ]),
    html.Br(),
    html.Div([
        html.Br(),
        html.Label('Select average time of service (mins)'),
        daq.Slider( # Slider to select service_mins_per_server
                id="serviceSlider", 
                # count=100,
                min=np.min(service_mins_per_server_slider),
                max=np.max(service_mins_per_server_slider),
                step=5,
                marks={i: str(i) for i in service_mins_per_server_slider},
                size=700,
            included=False),
    html.Br(),
    html.Div([
        html.Br(),
        html.Label('Select maximum desirable time of waiting (mins)'),
        daq.Slider( # Slider to select waiting time
                id="waitingSlider",
                # count=100,
                min=np.min(max_wait_time_slider),
                max=np.max(max_wait_time_slider),
                step=10,
                # value=[np.min(arrivals_per_hour_slider), np.max(arrivals_per_hour_slider)],
                marks={i: str(i) for i in max_wait_time_slider},
                size=700,
            included=False),
    ]),

]),
    html.Br(),
    html.H4("Results"),
    dt.DataTable(
        id='sim_table',
        columns=[{'name': i, 'id': i} for i in df.columns],
        style_table={
        'height': 'auto',
        'minWidth': '0px', 'width': '10px', 'maxWidth': '30px',
        # 'width': '10px',
        'whiteSpace': 'normal'
        },
        # fixed_columns={ 'headers': True},
        data=df.to_dict('records'),
        # data = []
 )
   
])


@app.callback(
    Output('sim_table', 'data'),
    [Input('arrivalSlider', "value"),
    Input('serviceSlider', "value"),
    Input('waitingSlider', "value")])
def update_datatable(arrival, service, waiting):

    total_nr_servers = np.arange(500)
    total_nr_servers = np.append(total_nr_servers, 0) # to initiate table with entry zero

    def weird_division(n, d):
        # function to avoid warnings for division by zero
        return n / d if d else 0
    
    for s in total_nr_servers:

        if arrival is None:
            arrivals = 0
        else:
            arrivals = weird_division(arrival, s) # (λ)
        
        if service is None:
            Service_rate = 0
        else:    
            Service_rate = weird_division(60, service) # x customers per hour (μ)
    
        # How much time do they spend in the restaurant?:
        # T = 1/(Service_rate - arrivals) # 1/μ−λ == t hours
        T = weird_division(1, (Service_rate - arrivals)) # 1/μ−λ == t hours

        # How much time waiting in line?:
        # W = T - 1/Service_rate # t hours
        W = T - weird_division(1, Service_rate) # t hours

        # How many customers in the system?:
        # N = input_values * T

        # What is the server utilization?:
        
        if Service_rate == 0:
            sut = 0
            service = 0 # to initialize as zero in the table, instead of negative numbers
        else:
            sut = arrivals/Service_rate
        
        if waiting == 0:
            W = 0

        if waiting is None:
            pass
        else:
            if np.round(W * 60, 0) > 0 and np.round(W * 60, 0) < waiting:
                break
        
    dd = {'Average service time (mins)': service,
    'Customers served per hour': np.round(Service_rate, 0),
    'Time spent in the queue (mins)': np.round(W * 60, 2),
    #'Customers in the system': np.round(N, 2),
    'Server use (recommended < 0.8)': np.round(sut, 2),
    'Number of servers obtained': np.round(s, 0)}

    df = pd.DataFrame(dd, index=[''])

    return df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)