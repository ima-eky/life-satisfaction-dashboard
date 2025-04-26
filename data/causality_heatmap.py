# Import necessary libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go  # Use Plotly's graph_objects for advanced control

# Load the dataset from CSV
df = pd.read_csv('visualisation/CH_causality_lag2.csv')

# Convert p_value column to numeric and handle errors
df['p_value'] = pd.to_numeric(df['p_value'], errors='coerce')

# Drop rows with missing p_value or country values
df = df.dropna(subset=['p_value', 'country'])

# Get unique countries and variables for dropdowns and matrix
countries = df['country'].unique()
variables = sorted(set(df['causality_from'].unique()).union(df['causality_to'].unique()))

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Granger Causality Heatmaps", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': c, 'value': c} for c in countries],  # Populate dropdown with countries
        value=countries[0],  # Default to the first country
        clearable=False,
        style={'width': '50%', 'margin': '20px auto'}  # Styling for dropdown
    ),
    dcc.Graph(
        id='heatmap-graph',
        style={'height': '90vh', 'width': '95vw'}  # Set graph dimensions
    )
])

# Callback to update the heatmap based on selected country
@app.callback(
    Output('heatmap-graph', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_heatmap(selected_country):
    # Filter data for the selected country
    filtered_df = df[df['country'] == selected_country].copy()
    
    # Replace insignificant p-values (p > 0.05) with 1
    filtered_df.loc[filtered_df['p_value'] > 0.05, 'p_value'] = 1.0
    
    # Create a pivot table for the heatmap
    pivot_table = filtered_df.pivot_table(
        index='causality_from',
        columns='causality_to',
        values='p_value',
        aggfunc='first'
    ).reindex(index=variables, columns=variables).fillna(1)  # Fill missing values with 1
    
    # Remove rows/columns with no significant p-values (< 0.05)
    significant_rows = (pivot_table < 1).any(axis=1)
    significant_cols = (pivot_table < 1).any(axis=0)
    filtered_pivot = pivot_table.loc[significant_rows, significant_cols]
    
    # Create the heatmap using Plotly's go.Heatmap
    fig = go.Figure(data=go.Heatmap(
        z=filtered_pivot.values,  # Heatmap values
        x=filtered_pivot.columns,  # Column labels
        y=filtered_pivot.index,    # Row labels
        colorscale='Viridis_r',    # Color scale
        zmin=0,                    # Minimum value for color scale
        zmax=1,                    # Maximum value for color scale
        hoverongaps=False,         # Show hover info for all cells
        text=filtered_pivot.values.round(2),  # Display rounded p-values
        texttemplate="%{text}",    # Format text display
        colorbar=dict(title="P-value", tickvals=[0, 0.05, 0.5, 1])  # Customize colorbar
    ))
    
    # Update layout for better readability and interactivity
    fig.update_layout(
        title=f'Granger Causality: {selected_country} (Only significant relationships shown)',
        title_x=0.5,  # Center the title
        xaxis_title="Effect To",
        yaxis_title="Cause From",
        xaxis=dict(
            tickangle=-45,  # Rotate x-axis labels
            tickfont=dict(size=10),  # Set font size
            automargin=True,  # Automatically adjust margins
            side='bottom'  # Place x-axis at the bottom
        ),
        yaxis=dict(
            tickfont=dict(size=10),  # Set font size
            automargin=True  # Automatically adjust margins
        ),
        margin=dict(l=150, r=50, b=150, t=50),  # Set margins
        autosize=True,  # Automatically resize the graph
        hovermode='closest'  # Show hover info for the closest point
    )
    
    # Enable zooming and panning
    fig.update_xaxes(fixedrange=False)
    fig.update_yaxes(fixedrange=False)
    
    return fig

# Run the app
if __name__ == '__main__':
    import webbrowser
    port = 8050
    webbrowser.open_new(f"http://localhost:{port}")  # Open the app in the browser
    app.run_server(debug=True, port=port, use_reloader=False)  # Start the server
