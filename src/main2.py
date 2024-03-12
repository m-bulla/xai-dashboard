# import libraries
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
import numpy as np
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
import dash_bootstrap_components as dbc # pip install dash-bootstrap-components
from PIL import Image

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], requests_pathname_prefix='/example_dash-app/')
app.url_base_pathname = '/example_dash-app/'
app.routes_pathname_prefix = app.url_base_pathname

server = app.server

# -- Import or create data here that is used for visualizations

ai_garage_logo = Image.open('assets2/AIGarage_logo.png')
invent_logo = Image.open('assets2/capgemini_invent_logo.png')

# ------------------------------------------------------------------------------
# App layout & style formats
# copy and insert the styles for your corresponding html element

# change your developer name below
developer = "Felix Eger"

# style arguments for sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "25rem",
    "padding": "2rem 1rem",
    "background-color": "#31333F",
}

# style arguments for main content to the right
CONTENT_STYLE = {
    "margin-left": "25rem",
    "margin-right": "0rem",
    "top": 0,
    "left": 0,
    "bottom" : 0, 
    "padding-top": "10rem",
    "padding-left":"3rem",
    "padding-right":"3rem",
    #"padding": "2rem 1rem",
    "padding-bottom":"18rem",
    "background-color": "#272936"
}

# style arguments for header
MAIN_HEADER_STYLE = {
    "textAlign":"left", 
    "color":"#ffffff", 
    "fontSize": '35px',
    'font-family':'Ubuntu',
    'font-weight': 'bold'
}

# style arguments for subheader
SUB_HEADER_STYLE = {
    'textAlign':"left", 
    "color":"#ffffff", 
    'fontSize': '25px',
    'font-family':'Ubuntu',
    'font-weight': 'bold'
}

# style arguments for widget-header
HEADER_WIDGET_STYLE = {
    'textAlign':"left", 
    "color":"#ffffff", 
    'fontSize': '25px',
    'font-family':'Ubuntu',
    'font-weight':'lighter'
}

# style arguments for footer
FOOTER_STYLE = {
    'textAlign':'left',
    "padding-left":"3rem", 
    "color":"#76777f",
    'display': 'inline-block',
    'font-family':'Ubuntu'
}

# style argument for footer name (developer)
FOOTER_STYLE_DEVELOPER = {
    'textAlign':'left',
    "padding-left":"0.25rem",
    "color":"#76777f",
    'font-weight': 'bold',
    'display': 'inline-block',
    'font-family':'Ubuntu'
}


# creation of sidebar, containing the widgets and images 
sidebar = html.Div(
    [   # load the image and add line and break after 
        html.Img(src=invent_logo, style={'height':'auto', 'width':'100%'}),
        html.Hr(style = {"color":"white"}),
        # specify header and subheader
        html.H1("Blueprint Dash, Capgemini AI Garage", style = MAIN_HEADER_STYLE, className="display-2"),
        html.Br(),
        html.H2(
            "This dashboard visualizes a random, uniform distribution", style = SUB_HEADER_STYLE, className="lead"
        ),
        html.Br(),
        # specify widgets with titles 
        html.H4(
            "Mean of the distribution", style = HEADER_WIDGET_STYLE
        ),
        html.Br(),
        # if using a slider style the marks with a function instead of explicit style coding 
        dcc.Slider(-5, 5, 1,
              value=0,
               id='mean',
               marks = {tick:{"label":str(tick), "style":{"color":"white","fontSize":"15px"}} for tick in range(-5,6,1)},
                tooltip={"placement": "top", "always_visible": True}
                ),
        html.Br(),
        html.H4(
            "Standard deviation of the distribution", style = HEADER_WIDGET_STYLE
        ),
        html.Br(),
        dcc.Slider(1, 3, 1,
                value=1,
                id='std',
                # explicit implementation, don't use:
                # marks = {1:{"label":"1", "style":{"color":"white", "fontSize":"15px"}, 2:{"label":"2", "style":{"color":"white", "fontSize":"15px"}, 3:{"label":"3", "style":{"color":"white", "fontSize":"15px"}}
                marks = {tick:{"label":str(tick), "style":{"color":"white","fontSize":"15px"}} for tick in [1, 2, 3]},
                tooltip={"placement": "top", "always_visible": True}
                ),
        html.Br(),
        html.H4(
            "Amount of samples", style = HEADER_WIDGET_STYLE
        ),
        html.Br(),
        dcc.Slider(1, 1000, 1,
                value=500,
                id='samples',
                marks = {tick:{"label":str(tick), "style":{"color":"white","fontSize":"15px"}} for tick in [1,250,500,750,1000]},
                tooltip={"placement": "top", "always_visible": True}
                )
    ],
    style = SIDEBAR_STYLE
)

# creation of content page with empty children filled through callback 
content = html.Div(id = "page-content", children = [], style= CONTENT_STYLE)

# final layout connecting sidebar and content
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
# creation of graph filling the children of content 
@app.callback(
     Output(component_id='page-content', component_property='children'),
     Input(component_id='mean', component_property='value'),
     Input(component_id='std', component_property='value'),
     Input(component_id='samples', component_property='value')
 )
def update_graph(mean, std, samples):
     print(mean, std, samples)

     container = f"The amount of samples chosen by the user are {samples}"

     # create samples, alternatively make copy of dataframe here
     x = np.random.normal(mean, std, size = samples)

     count, index = np.histogram(x, bins = 12)

     return[
        html.Br(),
        html.Div(
            dcc.Graph(id='my_hist', 
            figure = go.Figure().add_traces(go.Scatter(x = index, y = count, line = dict(width = 1, shape="hvh"), mode="lines", marker={"color":"white"}))
            .update_layout(
                title = {"text": "Histogram of random samples"},
                title_font_size=35,
                showlegend = False,
                yaxis_title = "Frequency",
                xaxis_title = "Values",
                plot_bgcolor = "#272936",
                paper_bgcolor = "#272936",
                font={"color":"#ffffff"},
                height = 600,
                title_font_family="Ubuntu"
                ).update_yaxes(
                    showgrid = True,
                    zeroline = False
                ).update_xaxes(
                    showgrid = False,
                    zeroline = False
                ),
            # for more formatting, refer to: https://plotly.com/python/reference/layout/
            style={"width": "100%","height": "100%", "background-color": "#272936"}
            ),
            style = {"width":"100%", "height":"100%"}
        ),
        html.Br(),
        html.Div([html.Footer("Developed by ", style = FOOTER_STYLE), html.Footer(developer, style = FOOTER_STYLE_DEVELOPER)])
        ]


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, host = "0.0.0.0" ,port=8050)
