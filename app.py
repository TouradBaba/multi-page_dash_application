import dash
from dash import html
from dash import dcc
from dash_bootstrap_templates import load_figure_template

# Instantiate the Dash app
app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
server = app.server
load_figure_template("darkly")

# Define the overall layout of the app
app.layout = html.Div(
    [
        html.Br(),
        html.H1("Dash App for Population and GDP Data", style={'fontSize': 50, 'textAlign': 'center'}),

        # Additional text with instructions
        html.Div(
            [
                html.P("Click on 'Population' to visualize population data or 'GDP' to visualize GDP data.",
                       style={'fontSize': 20, 'textAlign': 'center'})
            ]
        ),

        html.Div(
            [
                dcc.Link(page['name'] + "  |  ", href=page['path'], className="btn btn-dark m-2 fs-5 btn-lg")
                for page in dash.page_registry.values()
            ],
            style={'textAlign': 'center'}  # Center the content horizontally
        ),
        html.Hr(),

        # Content of each page will be rendered here
        dash.page_container
    ]
)

# Run the app
if __name__ == "__main__":
    app.run_server()
