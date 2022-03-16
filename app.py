######### Import your libraries #######
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly as py
import plotly.graph_objs as go


###### Define your variables #####
tabtitle = 'Chicago Housing!'
color1='#92A5E8'
color2='#8E44AD'
color3='#FFC300'
sourceurl = 'https://www.kaggle.com/c/titanic'
githublink = 'https://github.com/plotly-dash-apps/304-titanic-dropdown'


###### Import a dataframe #######
df = pd.read_csv('assets/chicago.csv')
df['Baths'] = df['Bath'].map({2:'Two', 3: 'Three', 4:'Four'})
variables_list=['Price', 'CrimeIndex', 'SchoolIndex','HouseSizeSqft','HouseSizeSqft']

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Layout of the app ########
app.layout = html.Div([
    html.H3('Choose a continuous variable for summary statistics:'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in variables_list],
        value=variables_list[0]
    ),
    html.Br(),
    dcc.Graph(id='display-value'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


######### Interactive callbacks go here #########
@app.callback(Output('display-value', 'figure'),
              [Input('dropdown', 'value')])
def display_value(continuous_var):
    grouped_mean=df.groupby(['HouseType', 'Neighborhood'])[continuous_var].mean()
    results=pd.DataFrame(grouped_mean)
    # Create a grouped bar chart
    mydata1 = go.Bar(
        x=results.loc['Two'].index,
        y=results.loc['Two'][continuous_var],
        name='First Class',
        marker=dict(color=color1)
    )
    mydata2 = go.Bar(
        x=results.loc['Three'].index,
        y=results.loc['Three'][continuous_var],
        name='Second Class',
        marker=dict(color=color2)
    )
    mydata3 = go.Bar(
        x=results.loc['Four'].index,
        y=results.loc['Four'][continuous_var],
        name='Third Class',
        marker=dict(color=color3)
    )

    mylayout = go.Layout(
        title='Grouped bar chart',
        xaxis = dict(title = 'Neighborhood'), # x-axis label
        yaxis = dict(title = str(continuous_var)), # y-axis label

    )
    fig = go.Figure(data=[mydata1, mydata2, mydata3], layout=mylayout)
    return fig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
