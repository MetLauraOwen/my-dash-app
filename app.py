# %%
import pandas as pd
from pathlib import Path
import socket
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pyreadr
import pickle

# %%
#paths
fig_path = Path("figures")
df_path = Path("dataframes")

#read in UK wide dfs
duration_df = pd.read_csv(df_path / "duration_df.csv")
tha_df = pd.read_csv(df_path / "tha_df.csv")
mhwt_df = pd.read_csv(df_path / "mhwt_df.csv")
severity_df = pd.read_csv(df_path / "severity_df.csv")
mseverity_df = pd.read_csv(df_path / "mseverity_df.csv")
peakvalue_df = pd.read_csv(df_path / "peakvalue_df.csv")

#read in city dfs 
with open("dataframes/duration_dataframes_dict.pkl", "rb") as file:
    duration_dataframes = pickle.load(file)
with open("dataframes/th_mhwt_dataframes_dict.pkl", "rb") as file:
    th_mhwt_dataframes = pickle.load(file)
with open("dataframes/levxally_dataframes_dict.pkl", "rb") as file:
    severity_dataframes = pickle.load(file)
    
#read in city coord df and get wanted cities
result = pyreadr.read_r('dataframes/UK_top30_cities.Rda')
city_df = result['city_df']
city_names_in_dataframes = set(duration_dataframes.keys())
city_df = city_df[city_df['city'].isin(city_names_in_dataframes)].copy()
#remove city=Islington as its the same as London
city_df = city_df[~((city_df['city'] == 'Islington'))]

#edit duration df so that its the no. of days per year/season (need to divide by 100,000)
duration_cols = [col for col in duration_df.columns if col.startswith("duration")]
duration_df[duration_cols] = duration_df[duration_cols] / 100000
for city, df in duration_dataframes.items():
    df["nduration"] /= 100000

RPy = [0.5, 2, 5, 10, 20, 50, 100, 200, 500, 1000]

# %%
def find_free_port(start_port=8050, max_port=8100):
    port = start_port
    while port <= max_port:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                port += 1
    raise RuntimeError("No free ports available")

#for city timeseries fig
def update_city_plot(city_name, duration_label):
    df = duration_dataframes[city_name]
    duration_value = int(duration_label.split()[0])
    df_sub = df[df['duration'] == duration_value]
    y_min = df_sub['nduration'].min()
    y_max = df_sub['nduration'].max()
    fig = px.line(
        df_sub,
        x='year',
        y='nduration',
        color='ensemble',
        markers=True,
        title=f"{duration_label} Heatwave Events at {city_name.replace('_', ' ')}"
    )
    for trace in fig.data:
        if trace.name == "mean":
            trace.line.color = "black"
            trace.line.dash = "dash"
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='No. of days per season',
        yaxis=dict(range=[y_min, y_max]),
        height=600
    )
    return fig

#for city threshold fig
def update_thresh_plot(city_name):
    df = th_mhwt_dataframes[city_name]
    y_min = df['threshold'].min()
    y_max = df['threshold'].max()
    fig = px.line(
        df,
        x='year',
        y='threshold',
        color='ensemble',
        markers=True,
        title=f"Threshold (°C) at {city_name.replace('_', ' ')}"
    )
    for trace in fig.data:
        if trace.name == "mean":
            trace.line.color = "black"
            trace.line.dash = "dash"
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Threshold (°C)',
        yaxis=dict(range=[y_min, y_max]),
        height=600
    )
    return fig

#for city mhwt fig
def update_mhwt_plot(city_name):
    df = th_mhwt_dataframes[city_name]
    y_min = df['mhwt'].min()
    y_max = df['mhwt'].max()
    fig = px.line(
        df,
        x='year',
        y='mhwt',
        color='ensemble',
        markers=True,
        title=f"Mean Heatwave Temp (°C) at {city_name.replace('_', ' ')}"
    )
    for trace in fig.data:
        if trace.name == "mean":
            trace.line.color = "black"
            trace.line.dash = "dash"
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Mean Heatwave Temp (°C)',
        yaxis=dict(range=[y_min, y_max]),
        height=600
    )
    return fig

#for city severity fig
def update_severity_plot(city_name, rp_label):
    df = severity_dataframes[city_name]
    df = df[df['severity_type'] == 1]
    rp_value = float(rp_label.split()[0])
    rp_index = RPy.index(rp_value) + 1
    df_sub = df[df['rp_level'] == rp_index]
    y_min = df_sub['severity_value'].min()
    y_max = df_sub['severity_value'].max()
    fig = px.line(
        df_sub,
        x='year',
        y='severity_value',
        color='ensemble',
        markers=True,
        title=f"{rp_label} Severity at {city_name.replace('_', ' ')}"
    )
    for trace in fig.data:
        if trace.name == "mean":
            trace.line.color = "black"
            trace.line.dash = "dash"
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Severity',
        yaxis=dict(range=[y_min, y_max]),
        height=600
    )
    return fig

#for mean severity fig
def update_mseverity_plot(city_name, rp_label):
    df = severity_dataframes[city_name]
    df = df[df['severity_type'] == 2]
    rp_value = float(rp_label.split()[0])
    rp_index = RPy.index(rp_value) + 1
    df_sub = df[df['rp_level'] == rp_index]
    y_min = df_sub['severity_value'].min()
    y_max = df_sub['severity_value'].max()
    fig = px.line(
        df_sub,
        x='year',
        y='severity_value',
        color='ensemble',
        markers=True,
        title=f"{rp_label} Mean Severity at {city_name.replace('_', ' ')}"
    )
    for trace in fig.data:
        if trace.name == "mean":
            trace.line.color = "black"
            trace.line.dash = "dash"
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Mean Severity',
        yaxis=dict(range=[y_min, y_max]),
        height=600
    )
    return fig

#for peak severity fig
def update_peakvalue_plot(city_name, rp_label):
    df = severity_dataframes[city_name]
    df = df[df['severity_type'] == 3]
    rp_value = float(rp_label.split()[0])
    rp_index = RPy.index(rp_value) + 1
    df_sub = df[df['rp_level'] == rp_index]
    y_min = df_sub['severity_value'].min()
    y_max = df_sub['severity_value'].max()
    fig = px.line(
        df_sub,
        x='year',
        y='severity_value',
        color='ensemble',
        markers=True,
        title=f"{rp_label} Peak Severity at {city_name.replace('_', ' ')}"
    )
    for trace in fig.data:
        if trace.name == "mean":
            trace.line.color = "black"
            trace.line.dash = "dash"
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Peak Severity',
        yaxis=dict(range=[y_min, y_max]),
        height=600
    )
    return fig



# %%
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Heatwave Metrics: 1980 vs 2080"),
    
    #dropdown for metric selection
    dcc.Dropdown(
        id='metric-dropdown',
        options=[
            {'label': 'Duration', 'value': 'duration'},
            {'label': 'Threshold', 'value': 'threshold'},
            {'label': 'MHWT', 'value': 'mhwt'},
            {'label': 'Severity', 'value': 'severity'},
            {'label': 'Mean Severity', 'value': 'mseverity'},
            {'label': 'Peak Value', 'value': 'peakvalue'}
        ],
        value='duration',
        clearable=False
  ),
    # Wrapped duration dropdown so it can be shown/hidden
    html.Div(id='duration-dropdown-container', children=[
        dcc.Dropdown(
            id='duration-dropdown',
            options=[{'label': f'{i} day', 'value': i} for i in range(1, 10)],
            value=1,
            clearable=False,
            style={'width': '300px'}
        )
    ]),

    # Wrapped rp dropdown so it can be shown/hidden
    html.Div(id='rp-dropdown-container', children=[
        dcc.Dropdown(
            id='rp-dropdown',
            options=[{'label': f'{rp} year RP level', 'value': rp} for rp in RPy],
            value=RPy[0], 
            clearable=False,
            style={'width': '300px'}
        )
    ]),

    html.Div([
        # Left column: difference map
        html.Div([
            dcc.Graph(id='difference-heatmap', style={'height': '80vh', 'width': '80%'}),
        ], style={'display': 'flex', 'flexDirection': 'row', 'gap': '10px', 'flex': '1'}),

        # Right column: timeseries 
        html.Div([
            dcc.Dropdown(
                id='city-dropdown',
                options=[{'label': name.replace("_", " "), 'value': name} for name in duration_dataframes.keys()],
                value=None,
                placeholder="Select a city",
                clearable=True
            ),
            dcc.Graph(id='timeseries-plot', style={'height': '100vh', 'width': '100%'})
        ], style={'flex': '1', 'marginLeft': '20px'})
    ], style={'display': 'flex', 'flexDirection': 'row', 'height': '80vh'}),
])

@app.callback(
    Output('duration-dropdown-container', 'style'),
    Input('metric-dropdown', 'value')
)
def toggle_duration_dropdown(selected_metric):
    if selected_metric == 'duration':
        return {'display': 'block'}
    else:
        return {'display': 'none'}
    
@app.callback(
    Output('rp-dropdown-container', 'style'),
    Input('metric-dropdown', 'value')
)
def toggle_rp_dropdown(selected_metric):
    if selected_metric in ['severity', 'mseverity', 'peakvalue']:
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
    Output('difference-heatmap', 'figure'),
    [Input('duration-dropdown', 'value'),
     Input('rp-dropdown', 'value'),
     Input('metric-dropdown', 'value')]
)
def update_difference_heatmap(selected_duration, selected_rp, selected_metric):

    if selected_metric == 'duration':
        df = duration_df
        col_1980 = f'duration{selected_duration}_1980'
        col_2080 = f'duration{selected_duration}_2080'
        title = f'Difference in {selected_duration}-day Duration events: 2080 − 1980'
        colorbar_title = "Δ no. of days per season"
    elif selected_metric == 'threshold':
        df = tha_df
        col_1980 = 'tha1980'
        col_2080 = 'tha2080'
        title = f'Difference in Threshold: 2080 − 1980'
        colorbar_title = "Δ Threshold (°C)"
    elif selected_metric == 'mhwt':
        df = mhwt_df
        col_1980 = 'mhwt1980' 
        col_2080 = 'mhwt2080'
        title = f'Difference in MHWT: 2080 − 1980'
        colorbar_title = "Δ MHWT (°C)"
    elif selected_metric == 'severity':
        df = severity_df
        rp_idx = RPy.index(selected_rp) + 1 
        col_1980 = f'rp{rp_idx}_1980'
        col_2080 = f'rp{rp_idx}_2080'
        title = f'Difference in Severity: 2080 − 1980'
        colorbar_title = "Δ Severity"
    elif selected_metric == 'mseverity':
        df = mseverity_df
        rp_idx = RPy.index(selected_rp) + 1 
        col_1980 = f'rp{rp_idx}_1980'
        col_2080 = f'rp{rp_idx}_2080'
        title = f'Difference in Mean Severity: 2080 − 1980'
        colorbar_title = "Δ Mean Severity"
    elif selected_metric == 'peakvalue':
        df = peakvalue_df
        rp_idx = RPy.index(selected_rp) + 1 
        col_1980 = f'rp{rp_idx}_1980'
        col_2080 = f'rp{rp_idx}_2080'
        title = f'Difference in Peak Value: 2080 − 1980'
        colorbar_title = "Δ Peak Value"

    #get differences
    df['diff'] = df[col_2080] - df[col_1980]
    max_abs_diff = max(abs(df['diff'].min()), abs(df['diff'].max()))

    # Set color range and scale based on metric
    if selected_metric in ['duration', 'severity', 'mseverity']:
        range_color = [-max_abs_diff, max_abs_diff]
        color_scale = 'RdBu_r'  # diverging red-blue
    elif selected_metric in ['mhwt', 'peakvalue', 'threshold']:
        min_val = max(0, df['diff'].min())
        max_val = max_abs_diff
        range_color = [min_val, max_val]
        #color_scale = 'redor' 
        color_scale = [
            [0.0, 'white'],        # zero value
            [0.05, '#fff7bc'],     # very pale yellow
            [0.15, '#fee391'],     # pale yellow
            [0.30, '#fec44f'],     # bright yellow-orange
            [0.50, '#fe9929'],     # orange
            [0.70, '#ec7014'],     # dark orange
            [0.85, '#cc4c02'],     # reddish-orange
            [1.0,  '#99000d']      # deep red
        ]

    fig_diff = px.density_heatmap(
        df, x='xco', y='yco', z='diff',
        nbinsx=131, nbinsy=211,
        color_continuous_scale=color_scale,
        range_color=range_color,
        title=title
    )
    fig_diff.update_xaxes(range=[df["xco"].min(), df["xco"].max()])
    fig_diff.update_yaxes(range=[df["yco"].min(), df["yco"].max()])

    fig_diff.update_layout(
        xaxis_title='lon', yaxis_title='lat',
        coloraxis_colorbar=dict(title=colorbar_title),
    )
    fig_diff.add_trace(go.Scatter(
        x=city_df["lon_index"], y=city_df["lat_index"],
        mode='markers',
        marker=dict(color='black', size=8),
        text=city_df["city"],
        customdata=city_df["city"],
        name='Cities',
        hoverinfo='text',
    ))

    return fig_diff

@app.callback(
    Output('city-dropdown', 'value'),
    Input('difference-heatmap', 'clickData'),
    prevent_initial_call=True
)
def update_city_from_click(clickData):
    if clickData and 'points' in clickData:
        return clickData['points'][0].get('customdata')
    return None

@app.callback(
    Output('timeseries-plot', 'figure'),
    [Input('difference-heatmap', 'clickData'),
     Input('city-dropdown', 'value'),
     Input('duration-dropdown', 'value'),
     Input('rp-dropdown', 'value'),
     Input('metric-dropdown', 'value')]
)
def update_timeseries(clickData, dropdown_city, selected_duration, selected_rp, selected_metric):
    # Determine city
    city_name = None
    if clickData and 'points' in clickData and clickData['points'][0].get('customdata'):
        city_name = clickData['points'][0]['customdata']
    elif dropdown_city:
        city_name = dropdown_city

    if not city_name or not selected_duration or not selected_metric:
        return go.Figure()

    duration_label = f"{selected_duration} day"
    rp_label = f"{selected_rp} year RP level"

    if selected_metric == 'duration':
        return update_city_plot(city_name, duration_label)
    elif selected_metric == 'threshold':
        return update_thresh_plot(city_name)
    elif selected_metric == 'mhwt':
        return update_mhwt_plot(city_name)
    elif selected_metric == 'severity':
        return update_severity_plot(city_name, rp_label)
    elif selected_metric == 'mseverity':
        return update_mseverity_plot(city_name, rp_label)
    elif selected_metric == 'peakvalue':
        return update_peakvalue_plot(city_name, rp_label)

if __name__ == '__main__':
    free_port = find_free_port()
    url = f"http://127.0.0.1:{free_port}"
    print(f"Starting Dash app at: {url}")
    app.run(debug=True, port=free_port)



