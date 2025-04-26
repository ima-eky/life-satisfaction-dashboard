import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load and prepare data
df = pd.read_csv('granger_causality_results_test_lag2.csv')

# Map country codes to full names for Plotly's choropleth
country_mapping = {
    'UK': 'United Kingdom',
    'IE': 'Ireland',
    # Add other European countries as needed
    'FR': 'France',
    'DE': 'Germany',
    'ES': 'Spain',
    'IT': 'Italy',
    'NL': 'Netherlands',
    'BE': 'Belgium',
    'CH': 'Switzerland',
    'SE': 'Sweden',
    'NO': 'Norway'
}

df['country_full'] = df['country'].map(country_mapping)

# Get unique causality directions
causality_from_options = sorted(df['causality_from'].unique())
causality_to_options = sorted(df['causality_to'].unique())

# Create Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Granger Causality P-Value Map", style={'textAlign': 'center'}),
    html.Div([
        dcc.Dropdown(
            id='causality-from',
            options=[{'label': x, 'value': x} for x in causality_from_options],
            value='bed',
            style={'width': '45%', 'display': 'inline-block'}
        ),
        dcc.Dropdown(
            id='causality-to',
            options=[{'label': x, 'value': x} for x in causality_to_options],
            value='dir',
            style={'width': '45%', 'display': 'inline-block', 'float': 'right'}
        )
    ]),
    dcc.Graph(id='choropleth-map', style={'height': '80vh'})
])

@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('causality-from', 'value'),
     Input('causality-to', 'value')]
)
def update_map(from_dir, to_dir):
    # Filter data for selected directions
    filtered_df = df[(df['causality_from'] == from_dir) & 
                    (df['causality_to'] == to_dir)]
    
    # Create base map with all European countries
    all_countries = pd.DataFrame({'country_full': list(country_mapping.values())})
    merged_df = all_countries.merge(filtered_df, on='country_full', how='left')

    # Create choropleth map
    fig = px.choropleth(
        merged_df,
        locations='country_full',
        locationmode='country names',
        color='p_value',
        scope='europe',
        color_continuous_scale='Viridis_r',  # Reverse scale: higher p-values = darker
        range_color=(0, 1),
        labels={'p_value': 'P-Value'},
        title=f'Causality: {from_dir} → {to_dir}'
    )
    
    fig.update_geos(
        resolution=50,
        showcountries=True, 
        countrycolor="Black",
        showsubunits=True, 
        subunitcolor="Gray"
    )
    
    fig.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0},
        coloraxis_colorbar=dict(
            title="P-Value",
            tickvals=[0, 0.2, 0.4, 0.6, 0.8, 1],
            thickness=20
        )
    )
    
    return fig

if __name__ == '__main__':
    import webbrowser
    port = 8050
    webbrowser.open_new(f"http://localhost:{port}")
    app.run_server(debug=True, port=port, use_reloader=False)