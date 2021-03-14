from plotly.subplots import make_subplots
import plotly.graph_objects as go

import pandas as pd

def df_to_html(df_path):
    df = pd.read_csv(df_path)
    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=False,
        vertical_spacing=0.13,
        subplot_titles=['Soil Sensors', 'Air Humidity', 'Air Temp', 'Light Sensor'],
        specs=[[{"type": "scatter"}],
               [{"type": "scatter"}],
              [{"type": "scatter"}],
              [{"type": "scatter"}]]
    )
    for i in range(5):
        fig.add_trace(
            go.Scatter(
                x=df["timestamp"],
                y=df[f'soil_sensor_{i}'],
                mode="lines",
                name=f'soil_sensor_{i}',
            ),
            row=1,col=1
        )

    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["air_humidity"],
            mode="lines",
            name="air_humidity"
        ),
        row=2,col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["air_temp"],
            mode="lines",
            name="air_temp"
        ),
        row=3,col=1
    )
    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["light_sensor"],
            mode="lines",
            name="light_sensor"
        ),
        row=4,col=1
    )
    fig.update_layout(
        height=1000,
        showlegend=False,
        title_text="Connected Garden",
    )

    fig['layout']['yaxis']['title']='Value'
    fig['layout']['yaxis2']['title']='%'
    fig['layout']['yaxis3']['title']='° F'
    fig['layout']['yaxis4']['title']='Lux'
    return fig.to_html()
