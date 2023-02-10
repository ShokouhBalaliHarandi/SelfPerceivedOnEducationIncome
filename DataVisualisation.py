import plotly.express as pe
import pandas as pd
import matplotlib.pylab as plt
import plotly.graph_objects as go
from ipywidgets import Dropdown, VBox

#this function visual data on map
#values: the data related to 
def figOnMap(df, colName):
    fig = pe.choropleth(
    df,
    locations="country",
    color=colName,
    locationmode="country names",
    color_continuous_scale=pe.colors.sequential.Plasma,#"YlGn",
    range_color=(df[colName].min(),df[colName].max()),
    title="Values in {} by Country".format(colName)
)
    return fig

#this function plots given list
#xLst: list of x-bar
#xLabel : label of x-bar
#yLst: list of y bar
#yLabel: label of y bar
#colorBase: to make difference for value of lists
def plotOnScat(xLst, xLabel, yLst, yLabel):
    plt.scatter(xLst, yLst)#""", c=colorBase, cmap="viridis""")
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    #plt.colorbar()
    return plt

#this function make interactive map by the years in the dataframes dynamically
#df: dataframe
#baseyear: base year for first load
def interactiveMap(df : pd.DataFrame, baseYear):
    # Create a Plotly Express choropleth map for datasource
    fig = figOnMap(df, baseYear)

    # Get the column headers from the DataFrame: "country", "isced11", "levels" are constant and unique together
    options = [col for col in df.columns if col != "country" and col != "isced11" and col != "levels"]

    #make dropdown by years
    dropdown = go.layout.Updatemenu(
        buttons=list([
            dict(
                args=[{"marker.color": df[col]}],
                label=col,
                method="update"
            ) for col in df.columns if col != "country" and col != "isced11" and col != "levels"
        ]),
        direction="down",
        showactive=True
    )
    #make dropdown interactive by changing value
    fig.update_layout(updatemenus=[dropdown])

    return fig
    
    