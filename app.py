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
color1='#e377c2'
color2='#2ca02c'
color3='#8c564b'
sourceurl = 'https://git.generalassemb.ly/intuit-ds-15/05-cleaning-combining-data/blob/master/data/chicago.csv'
githublink = 'https://github.com/Malathy-Muthu/304-titanic-dropdown'


###### Import a dataframe #######
df = pd.read_csv('assets/chicago.csv')
df['Baths'] = df['Bath'].map({2:'Two', 3: 'Three', 4:'Four'})
variables_list=['Price', 'CrimeIndex', 'SchoolIndex','HouseSizeSqft','LotSizeSqft']

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Layout of the app ########
app.layout = html.Div([
    html.H1('Chicago Housing Market Analysis',style={'color': 'blue', 'fontSize': 40, 'textAlign': 'center','text-decoration': 'underline'}),
    html.H3('Choose a continuous variable from the drop down below for summary statistics:',style={'color': '#800000', 'fontSize': 25, 'textAlign': 'center'}),
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


######### Interactive callbacks go here 1 st Bar chart #########
@app.callback(Output('display-value', 'figure'),
              [Input('dropdown', 'value')])
def display_value(continuous_var):
    grouped_mean=df.groupby(['Baths', 'HouseType'])[continuous_var].mean()
    results=pd.DataFrame(grouped_mean)
    # Create a grouped bar chart
    mydata1 = go.Bar(
        x=results.loc['Two'].index,
        y=results.loc['Two'][continuous_var],
        name='Two Baths',
        marker=dict(color=color1)
    )
    mydata2 = go.Bar(
        x=results.loc['Three'].index,
        y=results.loc['Three'][continuous_var],
        name='Three Baths',
        marker=dict(color=color2)
    )
    mydata3 = go.Bar(
        x=results.loc['Four'].index,
        y=results.loc['Four'][continuous_var],
        name='Four Baths',
        marker=dict(color=color3)
    )

    mylayout = go.Layout(
        title='Grouped bar chart',
        xaxis = dict(title = 'HouseType'), # x-axis label
        yaxis = dict(title = str(continuous_var)), # y-axis label

    )
    
    fig = go.Figure(data=[mydata1, mydata2, mydata3], layout=mylayout)
   
    return fig

######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
