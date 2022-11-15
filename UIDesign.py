import dash
from dash import Dash, dcc, html, ctx
import plotly
from dash.dependencies import Input, Output
#import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.graph_objs as go
#import pandas as pd
import math

from vicolib import setSlowFilterPeakingTime, startRun, stopRun, \
    getRunStatus, getRunStatistics

#from vicolib import scanTcpDevices, scanUsbDevices, getNumberOfDevices, \
#    getDeviceInfoByIndex, getIPAddress, setSlowFilterPeakingTime, \
#        setStopCondition, setMCANumberOfBins, setMCABytesPerBin, \
#            startRun, stopRun, getRunStatus, getRunStatistics, getMCADataUInt32

#from vicolibtypes import MCUStatusType, DPPStatusType, VICOStatusType, \
#    InterfaceType, StopConditionType

import DetectorData

# Simple error handling function
def CHECK_ERROR(status):
    if status != 0x00:
        print("Error encountered! Status =", status)
        TimeoutError("Error encountered! Status =", status)


# Build Components
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])


mytitle = dcc.Markdown(children='# Minesense - Sensor Analysis')
empty = html.P(id="output")

livetext = dcc.Markdown(children='')
temptext = dcc.Markdown(children='')

inputruntime = dbc.FormFloating(
    [
        dbc.Input(placeholder="10"),
        dbc.Label("Default 10s"),
    ]
)
runtimeval = dcc.Markdown(children='')

inputpeaking = dbc.FormFloating(
    [
        dbc.Input(placeholder="1000"),
        dbc.Label("Default 1000ns"),
    ]
)
peakingval = dcc.Markdown(children='')

runalert = dbc.Alert("Run in progress!", color="danger", is_open=False)

livegraph = dcc.Graph(figure={}, animate = True)

onoff = daq.BooleanSwitch(on=False, label="Begin Run", color="#F58025")

resetdetector = dbc.Button("Reset Detector", id = "reset", color="danger", n_clicks=0, size="sm")
clearoutput = dbc.Button("Clear Output", id = "Clear Output", color="danger", n_clicks=0, size="sm")

checkbox = dcc.Checklist(
    ['Output Counts', 'Input Counts'],
    ['Output Counts', 'Input Counts']
)
metricinterval = dcc.Interval(interval=1*100, # in milliseconds 
                          n_intervals=0)

graphinterval = dcc.Interval(interval=1*1000, # in milliseconds 
                          n_intervals=0)

X = []
Y = []
Y2 = []

# Reset Stats
outcount = 0
incount = 0
realtime = 0
livetime = 0

# Customize Layout
app.layout = dbc.Container(
    [
         dbc.Row([dbc.Col(mytitle), dbc.Col(runalert, width = 2)]),
         dbc.Row(dbc.Col(temptext)),
         dbc.Row(
             [
                 dbc.Col(dbc.Label("Runtime:"), width = {"size": 2, "order": 0}),
                 dbc.Col(runtimeval, width = {"size": 2, "order": 1}),
                 dbc.Col(dbc.Label("Peaking Time:"), width = {"size": 2, "order": 2}),
                 dbc.Col(peakingval, width = {"size":2, "order": 3})
                 ]
             ),
         dbc.Row(
             [
                 dbc.Col(inputruntime, width = {"size": 2, "order": 0}),
                 dbc.Col(inputpeaking, width = {"size": 2, "order": 1}),
                 dbc.Col(checkbox, width = {"size": 2, "order": 2}),
                 dbc.Col(onoff, width = {"size": 1, "order": 3}),
                 dbc.Col(resetdetector, width = {"size": 1, "order": 4}),
                 dbc.Col(clearoutput, width = {"size": 1, "order": 5}),
                 ]
             ),
         dbc.Row(
             [  
                 dbc.Col(livegraph, width = 10),
                 dbc.Col(livetext)
                 ]
             ),
         metricinterval,
         graphinterval
         ]
    )

# Turning Program On and Off Callback
@app.callback(
    Output(runalert, "is_open"), 
    Input(onoff, 'on')
)

def update_output(on):
    global outcount
    global incount
    global realtime
    global livetime
    global X
    global Y
    global Y2
    if on == False:
        stopRun(DetectorData.serialNumber) 
        return False
    elif on == True:
        
        # Start Sensor
        response = startRun(DetectorData.serialNumber)
        response = getRunStatus(DetectorData.serialNumber)
        runStatus = response.get("isRunActive")
        
        # Acquire Data
        while runStatus:
            response = getRunStatistics(DetectorData.serialNumber)
            outcount = response.get("outputCountRate")
            incount = response.get("inputCountRate")
            realtime = response.get("realtime")
            livetime = response.get("livetime")
            
            # Sort Data
            if 0 < realtime < DetectorData.measurementTime:
                X.append(realtime)
                Y.append(outcount)
                Y2.append(incount)
            
        
        return True
    
# Adjust Runtime

# Adjust Peaking Time
# =============================================================================
# @app.callback(
#     Output(peakingval, 'children'),
#    Input(inputpeaking, 'value')
# )
# 
# def adjust_peaking(peak):
#     peakingTime = peak
#     #setSlowFilterPeakingTime(DetectorData.serialNumber, peakingTime)
#     # CHECK_ERROR(response.get("dppStatusType"))
#     return peakingTime
# =============================================================================
    
          
# Live Text Callback
@app.callback(
    Output(livetext, 'children'),
    Input(metricinterval, 'n_intervals')
)

def update_metrics(n):
    return "Output count: {0} cps\n"\
       "Input rate: {1}  cps  \n"\
       "Run realtime: {2} s    \n"\
       "Run livetime: {3} s\n".format(outcount, incount, realtime, livetime)
       
# Runtime Adjustment
# =============================================================================
# @app.callback(
#     Output(livegraph, 'figure'),
#     Input(inputruntime, 'children')
# )
# =============================================================================


# Live Graph Callback
@app.callback(
    Output(livegraph, 'figure'),
    [Input(graphinterval, 'n_intervals'),
     Input(checkbox, 'value'),
     Input(component_id='reset', component_property='n_clicks')]
)
def update_graph_live(n, options_chosen, n_clicks):
    
    if ctx.triggered_id == "reset":
        return {}

    else:
        # Create plots
        data = [plotly.graph_objs.Scatter(
                x=X,
                y=Y,
                name='Output Counts',
                mode='lines+markers',
                showlegend=True
        ),
        plotly.graph_objs.Scatter(
                x=X,
                y=Y2,
                name='Input Counts',
                mode='lines+markers',
                showlegend=True
        )]
        
        min_y_list = []
        max_y_list = []
        
        
        if len(Y) > 0:
            # Input for Checkbox
            filtered_data = []
            for i in range(len(data)):
                if data[i]['name'] in (options_chosen):
                    filtered_data.append(data[i])
                
            # Setting minimums and maximums on filtered
            for i in range(len(filtered_data)):
                min_y_list.append(min(filtered_data[i]['y']))
                max_y_list.append(max(filtered_data[i]['y']))
            min_y = min(min_y_list)
            max_y = max(max_y_list)
            
            # Return Figure
            return {'data': filtered_data,
                    'layout': go.Layout(xaxis=dict(
                            range=[0,DetectorData.measurementTime]),yaxis = 
                            dict(range = [min_y,max_y]),
                            ),
                    }
        else:
            return {'data': data,
                    }
    #return dash.no_update
        

    
@app.callback(
    Output(runtimeval,'children'),
    Input('reset','n_clicks')
    )
def text(nclick):
    return 'Button has been clicked {} times'.format(nclick)
    # Resetting Graph
# =============================================================================
#     elif ctx.triggered_id == "Clear Output":
#         return {}
#     
#     return dash.no_update
# =============================================================================

# Restart Detector Button Callback
# =============================================================================
# @app.callback(
#    Input(component_id='Reset Detector', component_property='n_clicks')
# )
# def reset_click(n):
#     if ctx.triggered_id == "Reset Detector":
#         exec("DetectorData.py")
# =============================================================================

# Clear Output Button Callback
# =============================================================================
# @app.callback(
#     Output(empty, 'children'),
#     Input(component_id='Clear Output', component_property='n_clicks')
# )
# def reset_click(n):
#     if ctx.triggered_id == "Clear Output":
#          sys.modules[__name__].__dict__.clear()
#     return dash.no_update
# =============================================================================

# Run App
if __name__ == '__main__':
    app.run_server(debug=False, port=8064)