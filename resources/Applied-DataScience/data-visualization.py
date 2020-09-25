import pymysql
import pandas as pd
import plotly.plotly as py
from plotly.graph_objs import *
py.sign_in('eduonix','5OAS2hbNIB8GQl6FUe4L')

conn = pymysql.connect("localhost", "root","", "world")
cursor = conn.cursor()
cursor.execute('select Name, Continent, Population, LifeExpectancy, GNP from Country')
rows = cursor.fetchall()
str(rows)[0:300]
df = pd.DataFrame([[ij for ij in i] for i in rows])
df.rename(columns={0:'Name', 1: 'Continent', 2:'Population',3:'LifeExpectancy', 4:'GNP'},inplace=True)

print(df.head())

country_names = df['Name']
for i in range(len(country_names)):
    try:
        country_names[i] = str(country_names[i]).decode('utf-8')
    except:
        country_names[i] = 'Country name decode error'


trace1 = Scatter(
    x=df['GNP'],
    y=df['LifeExpectancy'],
    text=country_names,
    mode='markers'
)
layout = Layout(
    title='Life expectancy vs GNP from MySQL world database',
    xaxis=XAxis( type='log', title='GNP' ),
    yaxis=YAxis( title='Life expectancy' ),
)
data = Data([trace1])
fig = Figure(data=data, layout=layout)
py.iplot(fig, filename='world GNP vs life expectancy')

sizemode='area'
sizeref = df['Population'].max()/1e2**2

colors = {
    'Asia':"rgb(255,65,54)", 
    'Europe':"rgb(133,20,75)",
    'Africa':"rgb(0,116,217)",
    'North America':"rgb(255,133,27)",
    'South America':"rgb(23,190,207)",
    'Antarctica':"rgb(61,153,112)",
    'Oceania':"rgb(255,220,0)",
}

# Define a hover-text generating function (returns a list of strings)
def make_text(X):
    return 'Country: %s\
    <br>Life Expectancy: %s years\
    <br>Population: %s million'\
    % (X['Name'], X['LifeExpectancy'], X['Population']/1e6)  

# Define a trace-generating function (returns a Scatter object)
def make_trace(X, continent, sizes, color):  
    return Scatter(
        x=X['GNP'],  # GDP on the x-xaxis
        y=X['LifeExpectancy'],    # life Exp on th y-axis
        name=continent,    # label continent names on hover
        mode='markers',    # (!) point markers only on this plot
        text=X.apply(make_text, axis=1).tolist(),
        marker= Marker(
            color=color,           # marker color
            size=sizes,            # (!) marker sizes (sizes is a list)
            sizeref=sizeref,       # link sizeref
            sizemode=sizemode,     # link sizemode
            opacity=0.6,           # (!) partly transparent markers
            line= Line(width=3,color="white")  # marker borders
        )
    )

# Initialize data object 
data = Data()

# Group data frame by continent sub-dataframe (named X), 
#   make one trace object per continent and append to data object
for continent, X in df.groupby('Continent'):
    
    sizes = X['Population']                 # get population array 
    color = colors[continent]               # get bubble color
    
    data.append(
        make_trace(X, continent, sizes, color)  # append trace to data object
    ) 

    # Set plot and axis titles
title = "Life expectancy vs GNP from MySQL world database (bubble chart)"
x_title = "Gross National Product"
y_title = "Life Expectancy [in years]"

# Define a dictionary of axis style options
axis_style = dict(  
    type='log',
    zeroline=False,       # remove thick zero line
    gridcolor='#FFFFFF',  # white grid lines
    ticks='outside',      # draw ticks outside axes 
    ticklen=8,            # tick length
    tickwidth=1.5         #   and width
)

# Make layout object
layout = Layout(
    title=title,             # set plot title
    plot_bgcolor='#EFECEA',  # set plot color to grey
    hovermode="closest",
    xaxis=XAxis(
        axis_style,      # add axis style dictionary
        title=x_title,   # x-axis title
        range=[2.0,7.2], # log of min and max x limits
    ),
    yaxis=YAxis(
        axis_style,      # add axis style dictionary
        title=y_title,   # y-axis title
    )
)

# Make Figure object
fig = Figure(data=data, layout=layout)

# (@) Send to Plotly and show in notebook
py.iplot(fig, filename='s3_life-gdp')