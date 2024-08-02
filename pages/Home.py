import dash
from dash import dcc, html

# Register the page
dash.register_page(__name__, path='/', name='Home 🏠')

layout = html.Div(
    className='container-fluid',
    children=[
        html.Div(
            className='jumbotron jumbotron-fluid bg-dark text-light',
            children=[
                html.Div(
                    className='container-fluid',
                    children=[
                        html.H1(
                            "Welcome to the Population and GDP Dashboards",
                            className='display-2 mb-4',
                            style={'fontWeight': 'bold', 'fontSize': '4rem'}
                        ),
                        html.P(
                            "Explore the interactive dashboards designed to provide valuable insights into "
                            "global and regional population and GDP data. Dive into trends, comparisons, and key "
                            "metrics.",
                            className='lead mb-4',
                            style={'fontSize': '1.5rem'}
                        ),
                        html.Hr(className='my-4', style={'borderColor': '#fff'}),
                        html.P(
                            "Our Population Dashboard allows you to analyze trends in population growth, "
                            "examine demographic breakdowns, and compare population statistics across various regions. "
                            "It offers visualizations and data points to help you understand how populations evolve "
                            "over time and across different geographies.",
                            className='mb-4',
                            style={'fontSize': '1.25rem'}
                        ),
                        html.P(
                            "The GDP Dashboard, on the other hand, provides a comprehensive view of economic "
                            "performance. You can explore GDP growth rates, per capita GDP, and regional economic "
                            "disparities. This dashboard helps you gain insights into economic trends and how "
                            "different regions compare in terms of economic development.",
                            className='mb-4',
                            style={'fontSize': '1.25rem'}
                        ),
                        html.Div(
                            className='row gx-5 my-4',
                            children=[
                                html.Div(
                                    className='col-lg-6 mb-4',
                                    children=[
                                        html.Img(
                                            src='/assets/Screenshots/GDP-Home.png',
                                            className='img-fluid rounded',
                                            style={
                                                'maxWidth': '100%',
                                                'border': '2px solid #ddd',
                                                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                                            }
                                        ),
                                        html.P(
                                            "The GDP Dashboard presents a detailed analysis of economic "
                                            "performance. Examine GDP growth, per capita GDP, and disparities to "
                                            "understand global economic trends better.",
                                            className='text-light mt-2',
                                            style={'fontSize': '1.25rem'}
                                        ),
                                        dcc.Link(
                                            html.Button(
                                                "Explore GDP Data",
                                                className='btn btn-secondary btn-lg mx-2',
                                                style={'padding': '15px 30px', 'fontSize': '1.5rem'}
                                            ),
                                            href='/gdp'
                                        )
                                    ]
                                ),
                                html.Div(
                                    className='col-lg-6 mb-4',
                                    children=[
                                        html.Img(
                                            src='/assets/Screenshots/Population-Home.png',
                                            className='img-fluid rounded',
                                            style={
                                                'maxWidth': '100%',
                                                'border': '2px solid #ddd',
                                                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                                            }
                                        ),
                                        html.P(
                                            "The Population Dashboard provides a detailed view of global "
                                            "population trends. Visualize how populations change over time and how "
                                            "they compare across different regions.",
                                            className='text-light mt-2',
                                            style={'fontSize': '1.25rem'}
                                        ),
                                        dcc.Link(
                                            html.Button(
                                                "Explore Population Data",
                                                className='btn btn-primary btn-lg mx-2',
                                                style={'padding': '15px 30px', 'fontSize': '1.5rem'}
                                            ),
                                            href='/population'
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)
