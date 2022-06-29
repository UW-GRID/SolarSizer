"""

Creates GUI with functionality to input latitude, longitude, and a csv file.
These user inputted values are run through the PySAM model.

Run this app with `python app.py` and visit http://127.0.0.1:8050/ in your web browser.
"""

import base64
import io
import time

import dash
from dash.dependencies import Input, Output, State
from dash import callback_context, dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

import numpy as np
import plotly.express as px

from pysam import pysam_model
#from utils import parse_load_profile as plp
from utils import pull_irradiance
from utils import convert_load_profile

#GLOBAL_LAT = None
#GLOBAL_LON = None
#GLOBAL_CONTENTS = None

app = dash.Dash(__name__)

app.layout = html.Div( children=[

    #  Logo and Header
    dbc.Row([
        dbc.Col(
            [html.Img(
            src='/assets/SolarSizerLogo.png',
            style={
                'width': '25%',
                'height': '13vh',
                'float': 'left',
                'display': 'inline-block',
                },
            ),],
            ),
        dbc.Col([
            dbc.Row(
                [html.Div(
                children='Solar Sizer',
                style={
                    'textAlign': 'left',
                    'fontSize': 55,
                }
            ),],
            ),
            dbc.Row(
                [html.Div(
                children='A web application for planning off-grid solar projects',
                style={
                    'textAlign': 'left',
                    'fontSize': 24,
                }
                ),],
                ),
            ],
            style={
                'height': '25vh',
                'width': '70%',
                'float': 'right',
                }),
        ],
            style={
                'height': '16vh',
            }
        ),

    # Separate bar
    dbc.Row(
        style={
            'height': '5vh',
            'background-color': 'cornflowerblue'
        }
    ),

    # Main block
    dbc.Row([
        html.Div([

        dbc.Row([
            dbc.Col([
                html.Div([
            'What is SolarSizer?'
                ],
                style={
                    'font-size':24,
                    'font-weight': 'bold'
                    }
            ),
                html.Div([
                    'The SolarSizer program assists in the planning of small off-grid solar '
                    'projects by creating a user-friendly dashboard. Based on the input '
                    'location and load profile, the model returns an equipment list of a solar '
                    'array capable of meeting the load profile. SolarSizer applies a model '
                    'designed by GRID yet with additional optimization and simplicity. '
                    'The project also added documentation for testing and expanding the original '
                    'code.'
                ],
                style={
                    'font-size': 20,
                }
                ),
                html.Br(),
                html.Div([
            'Who is GRID?'
        ],
            style={
                'font-size':24,
                'font-weight': 'bold'
            }),
        html.Div([
            html.Div(['The Global Renewables Infrastructure Development (GRID) is a student '
            'organization at University of Washington with the goal of researching and developing '
            'renewable energy technologies. The main focus of GRID is to help undersized, climate '
            'frontline communities by providing the resources to employ renewable energy '
            'techniques with optimal design. Projects are off-grid and small-scale, yet '
            'contribute to equitable green solutions to energy demands. For more information '
            'on GRID and ongoing projects, check out the official site at ',
            html.A("sites.uw.edu/grid/", href='https://sites.uw.edu/grid/', target="_blank"),], ),
        ],
                 style={
                    'font-size': 20,
                }),
                ],
                style={
                    'float': 'left',
                    'height': '35vh',
                    'width': '56%',
                    },
                ),
            dbc.Col([
                html.Img(
                src= '/assets/chelsea-WvusC5M-TM8-unsplash.jpg',
                style={
                    'width': '100%',
                    'height': '40vh',
                    'textAlign': 'center',
                }
                ),
        # ),
                ],
                style={
                    'float': "right",
                    'height': '35vh',
                    'width': '44%'
                }
                ),
        ],
                style={
                    'height': '35vh',
                }
        ),

        # html.Center(

        html.Br(),
        html.Br(),
        html.Br(),
        html.Div([
            'How it works'
        ],
            style={
                'font-size':24,
                'font-weight': 'bold'
                }),
        html.Div([
            'The input box can be found at the bottom of this page. After you submit a location '
            'and load profile, you can run the program. The software pulls in irradiance data '
            'from The National Solar Radiation Database hosted by the National Renewable Energy '
            'Laboratory using the Physical Solar Model (PSM) v3. See the next section for '
            'detailed instructions on how to get started.'
        ],
                 style={
                    'font-size': 20,
                }),
        html.Br(),
        html.Div([
            html.Div([
            'Instructions'
        ],
            style={
                'font-size':20,
                'font-weight': 'bold'
                }),
        html.Div([
            'To run the program, first find the latitude and longitude in degrees of your desired '
            'location within the United States. The location must be within the US! You can use '
            'Google Maps to find the latitude and longitude of any location.'
        ],
                style={'padding-bottom': '10px',
                       'font-size': 20,
                       }),
        html.Div([
            'Next, upload your load profile by clicking the box labelled '
            '“Upload Load Profile”. Your load profile must be in csv format. '
            'We have provided a template of a load profile within the data directory '
            'in the SolarSizer github: ',
            html.A("github.com/UW-Solar-GRID/SolarSizer/blob/main/doc/load_profile_template.csv",
                href='https://github.com/UW-Solar-GRID/SolarSizer/blob/main/doc/'
                'load_profile_template.csv',
                target="_blank"),
            'You can refer to the load profile example within the data directory on how to '
            'fill out the template'
        ],
                style={'padding-bottom': '10px', 'font-size': 20,}),
        html.Div([
            'Once you have input your location and uploaded a load profile, press the RUN button '
            'to start the program. The solar array produced by the model will be displayed on '
            'the right. This contains the uptime percentage for each array specification.'
        ],
                style={'padding-bottom': '10px', 'font-size': 20,}),
            ],
                style={
                    'padding-left': '30px'
                }),
        html.Br(),
            ],

            style={
                'padding-left': '30px',
                'padding-right': '30px',
                'padding-top': '30px',
                'padding-bottom': '30px',
            }),

        # Row for input and output
        dbc.Row([
            # Scrolling output, floating to the right
            dbc.Col(
                children=[
                    html.Center([
                        html.Div(['Your chart will show here'], style={'font-size': 24})
                        ],
                        style={'vertical-align': 'top'}
                    ),
                    dbc.Row([
                        html.Br(),
                        html.Br(),
                        dcc.Loading(
                            id="loading-1",
                            type="default",
                            children=[html.Div(id='model-status')],
                        ),
                        ]),
                    ],
                style={
                    'width': '64%',
                    'height': '68vh',
                    'float': 'right',
                    'background-color': 'silver',
                    'overflow': 'scroll',
                    'borderRadius': '8px',
                    'padding-top': '20px',
                    'padding-left': '5px',
                    'padding-right': '5px',
                    'vertical-align': 'top',
                    },
            ),

            # Input card, floating to the left
            dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        html.Br(),
                        html.Div([
                        html.Div('Enter latitude and longitude:',
                            style={'fontSize': 35,'width': '100%',}),
                        html.Div('Note: chosen point must be in the United States',
                            style={'color': 'black', 'fontSize': 14, 'padding-bottom': '3px',}),

                        html.Label('Latitude (in degrees):'),
                        dcc.Input(id='lat', type='number'),
                        html.Div(id=''),
                        html.Br(),

                        html.Label('Longitude (in degrees):'),
                        dcc.Input(id='lon', type='number'),
                        html.Div(id=''),
                        html.Br(),
                    ],
                    style={'width': '100%', 'display': 'inline-block'}
                    ),
                    ]),

                    html.Br(),
                    html.Br(),

                    dbc.Row([
                        html.Div('Upload a load profile:', style={'fontSize': 35,}),
                        dbc.Row(
                            [
                                html.Center([
                                    dbc.Row([html.Div('Note: load profile must be in csv format, '
                                    'see template in data directory',
                                    style={'color': 'black', 'fontSize': 14}),]),
                                    dcc.Upload(
                                        id='upload-data',
                                        children=[
                                            html.Div(
                                                ['Drag and Drop or Select File',],
                                                style={
                                                    'vertical-align': 'top',
                                                    'textAlign': 'center',
                                                    'font-size': 25,
                                                    },
                                                )
                                            ],
                                        style={
                                            'width': '80%',
                                            'height': '80px',
                                            'lineHeight': '60px',
                                            'borderWidth': '2px',
                                            'borderStyle': 'dashed',
                                            'borderRadius': '5px',
                                            'margin': '10px',
                                            'vertical-align': 'top'
                                        },
                                        # Allow multiple files to be uploaded
                                        multiple=False,
                                    ),
                                ])
                            ]
                        ),

                        ],
                    style={
                        'vertical-align': 'top'
                        },
                    justify='center',
                    ),

                    html.Br(),
                    html.Br(),

                    dbc.Row([
                        html.Button('Run', id='btn-nclicks-1', n_clicks=0,
                                    style={
                                        'font-size': 30,
                                        'width': '80%',
                                        'height': '80px',
                                        'borderWidth': '2px',
                                        'borderRadius': '20px',
                                        'textAlign': 'center',
                                        'color': 'black',
                                    },
                                    ),
                    ],
                        style={
                            'padding-top': '35px',
                        }
                    )
                ],
                style={
                    'padding-top': '20px',
                    'padding-right': '3px',
                    'padding-bottom': '5px',
                    'padding-left': '8px',
                }
                )
            ],
            style={
                'display': 'inline-block',
                'height': '60vh',
                'width': '35%',
                'float': 'left',
                'text-align': 'center',
                'color':'black',
                'background-color': 'cornflowerblue',
                'borderRadius': '10px',
                # 'opacity': '0.4',
                },
            ),
        ],

        style={
            'padding-top' : '45px',
            'padding-left': '3px',
            'padding-right': '5px',
        }
        ),
        ],

        style={
            'width': '100%',
            'height': '70vh',
            'overflow': 'scroll',
            'background-color': 'white',
        }
        ),
    ],
    style={
            'width': '100%',
            'height': '70vh',
            'overflow': 'scroll',
            'borderRadius': '7px',
            'background-color': 'white',
        } ,

    ),

    html.Br(),

    html.Br(),

    html.Div(id="output"),

    html.Div(id='output-data-upload'),
],
style={
    'padding-top': '30px',
    'padding-right': '150px',
    'padding-bottom': '10px',
    'padding-left': '150px',
}
)


@app.callback(Output('output', 'children'),
              Input('lat', 'value'),
              Input('lon', 'value'))

def update_output(lat, lon):
    """
    Updates output with input values run through FakeSAM model.
    """

    time.sleep(3)
    if lat is not None and lon is not None:
        #GLOBAL_LAT = lat
        #GLOBAL_LON = lon
        #print('global_lat', GLOBAL_LAT)
        #print('global_lon', GLOBAL_LON)

        pull_irradiance.create_irradiance_file(lat,lon,2000)
        #may want to turn this off when testing because will max out request
        #    from API rate. Also might want to see about using average irradiance
        #    from NREL instead of from a set year.

    else:
        pass



@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def load_profile_update_output(contents, filename):
    """
    Decode the uploaded load profile
    Returns TypeError if not a csv file
    Saves dataframe to txt file within create_load_txt function
    """
    if contents is not None:
        #GLOBAL_CONTENTS = contents

        # decode output from file upload
        _, content_string = contents.split(',')

        decoded_b64 = base64.b64decode(content_string)

        # check that type csv
        if filename.endswith('.csv'):

            decoded_csv = io.StringIO(decoded_b64.decode('utf-8'))

            # convert to pandas dataframe
            data = pd.read_csv(decoded_csv)

            # convert to txt
            convert_load_profile.create_load_txt(data)

        else:
            raise TypeError('Load profile must be a csv file')

    else:
        pass


# output is n*4cols data frame
@app.callback(
    Output('model-status', 'children'),
    Input('btn-nclicks-1', 'n_clicks')
)

def display_click():
    """
    Function to check if button has been clicked
    After button click, run model and display results
    """

    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    test_df = pd.DataFrame()
    if 'btn-nclicks-1' in changed_id:
        print('button clicked')

        model_output = pysam_model.pysam_model()
        test_df = model_output

        fig = px.bar(
            test_df,
            x=np.arange(0,test_df['Uptime_Percent'].shape[0]),
            y='Uptime_Percent',
            labels={
                     "x": "Array",
                     'Uptime_Percent': 'Uptime Percent'
                 },
            )
        return None

    if not test_df.empty:
        msg = 'Model finished running, result below:'
        #msg2 = 'Chart is loading'
        return [
            html.Div(msg),

            html.Div([
                dash_table.DataTable(
                    data=test_df.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in test_df.columns],
                ),
                html.Hr(),

                dcc.Graph(
                    id='example-graph',
                    figure=fig
                )
            ])
                ]

    return None
    # else:
    #     msg = "placeholder"
    #     # msg = 'Click button to run model once the lat and lon are
    #              inputted and a .csv load profile is uploaded'
    #     return html.Div(msg)

if __name__ == '__main__':
    app.run_server(debug=True)
