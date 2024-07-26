import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

# Register the page
dash.register_page(__name__, path='/gdp', name='GDP 💲')

# Load the datasets
df_gdp_countries = pd.read_excel(
    'https://github.com/TouradBaba/exploratory_data_analysis_and_visualization/raw/master/data/cleaned_gdp.xlsx')
df_gdp_regions = pd.read_excel(
    'https://github.com/TouradBaba/exploratory_data_analysis_and_visualization/raw/master/data/cleaned_gdp2.xlsx')
# Convert 'GDP in current prices (millions of US dollars)' to numeric, coercing errors
df_gdp_countries['GDP in current prices (millions of US dollars)'] = (
    pd.to_numeric(df_gdp_countries['GDP in current prices (millions of US dollars)'], errors='coerce'))
df_gdp_regions['GDP in current prices (millions of US dollars)'] = (
    pd.to_numeric(df_gdp_regions['GDP in current prices (millions of US dollars)'], errors='coerce'))

# Find the latest year for each country
latest_years_countries = df_gdp_countries.groupby('Region/Country/Area')['Year'].max().reset_index()

# Merge to get the latest data for each country
latest_data_gdp_countries = pd.merge(df_gdp_countries, latest_years_countries, on=['Region/Country/Area', 'Year'],
                                     how='inner')

# Get unique countries and regions for dropdown options
countries = latest_data_gdp_countries['Region/Country/Area'].unique()
regions = df_gdp_regions['Region/Country/Area'].unique()

# Available years for the flat map
available_years_countries = df_gdp_countries['Year'].unique()
available_years_regions = df_gdp_regions['Year'].unique()

# Define combined app layout with custom styling
layout = html.Div(
    className='container-fluid',
    children=[
        html.Div(
            className='jumbotron bg-dark text-white',
            children=[
                html.H1("GDP Data Dashboard", className='display-4', style={'fontSize': '3rem', 'textAlign': 'center'}),
                html.P(
                    "Explore GDP data over time by selecting a country or region.",
                    className='lead smaller-text', style={'textAlign': 'center'}
                )
            ]
        ),
        html.Hr(className='my-4'),

        html.Div(
            className='row',
            children=[
                html.Div(
                    className='col-md-6 map-container',
                    children=[
                        dcc.Graph(id='map', config={'scrollZoom': True})
                    ]
                ),
                html.Div(
                    className='col-md-6 details-container bg-light p-3',
                    children=[
                        html.Div(id='country-details', className='details'),
                        html.Hr(style={'backgroundColor': 'black'}),
                        dcc.Dropdown(
                            id='country-dropdown',
                            options=[{'label': country, 'value': country} for country in countries],
                            placeholder="Select a country",
                            className='mb-3'
                        ),
                        html.Div(
                            dcc.RangeSlider(
                                id='year-slider',
                                min=1995,
                                max=2020,
                                value=[1995, 2020],
                                marks={str(year): str(year) for year in df_gdp_countries['Year'].unique()},
                                step=None,
                                className='mb-3'
                            ),
                            style={'marginTop': '20px'}
                        ),
                        html.Div(
                            id='line-charts-container',
                            className='line-charts-container',
                            style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'wrap'}
                        )
                    ]
                )
            ]
        ),

        html.Hr(className='my-4'),

        html.Div(
            className='row',
            children=[
                html.Div(
                    className='col-md-6',
                    children=[
                        html.Div(
                            dcc.Dropdown(
                                id='gdp-pie-year-dropdown',
                                options=[{'label': year, 'value': year} for year in df_gdp_regions['Year'].unique()],
                                value=2021,
                                placeholder="Select a year",
                                className='mb-3'
                            )
                        ),
                        html.Div(
                            dcc.Graph(id='gdp-pie-chart', config={'displayModeBar': False})
                        ),
                        html.Div(
                            dcc.Graph(id='gdp-per-capita-bar-chart', config={'displayModeBar': False})
                        ),
                    ]
                ),
                html.Div(
                    className='col-md-6',
                    children=[
                        html.Div(
                            dcc.Dropdown(
                                id='gdp-region-dropdown',
                                options=[{'label': region, 'value': region} for region in regions],
                                placeholder="Select a region",
                                className='mb-3'
                            ),
                            style={'marginBottom': '20px', 'marginLeft': '20px', 'marginRight': '20px'}
                        ),
                        html.Div(
                            dcc.RangeSlider(
                                id='gdp-year-slider',
                                min=df_gdp_regions['Year'].min(),
                                max=df_gdp_regions['Year'].max(),
                                value=[df_gdp_regions['Year'].min(), df_gdp_regions['Year'].max()],
                                marks={str(year): str(year) for year in df_gdp_regions['Year'].unique()},
                                step=None,
                                className='mb-3'
                            ),
                            style={'marginTop': '20px'}
                        ),
                        html.Div(
                            id='gdp-line-plots-container',
                            children=[
                                dcc.Graph(id='gdp-line-plot', style={'height': '500px'}),
                                dcc.Graph(id='growth-rate-line-plot', style={'height': '500px'})
                            ],
                            style={'marginTop': '20px'}
                        )
                    ]
                )
            ]
        ),

        html.Hr(className='my-4'),

        html.Div(
            className='row',
            children=[
                html.P(
                    "The map below presents a global view of GDP data across various countries. "
                    "Use the play button to animate changes over time, or adjust the slider to focus on specific years.",
                    className='lead', style={'fontSize': 25, 'color': '#FFFFFF'}
                ),
                html.Div(
                    className='col-md-12 flat-map-container',
                    children=[
                        html.Div(
                            className='d-flex justify-content-between align-items-center',
                            children=[
                                html.Div([
                                    html.Button('Play', id='play-button', n_clicks=0,
                                                className='btn btn-primary ml-2 btn-lg'),
                                ]),
                                html.Div([
                                    dcc.RangeSlider(
                                        id='flat-map-year-slider',
                                        min=available_years_countries.min(),
                                        max=available_years_countries.max(),
                                        value=[available_years_countries.min(), available_years_countries.max()],
                                        marks={str(year): str(year) for year in available_years_countries},
                                        step=None,
                                        className='mb-3'
                                    ),
                                ], style={'marginTop': '20px', 'flex': '1', 'marginLeft': '20px'}),
                            ]
                        ),
                        dcc.Graph(id='flat-map'),
                        dcc.Interval(
                            id='interval-component',
                            interval=1000,  # in milliseconds
                            n_intervals=0,
                            disabled=True  # Start with the interval disabled
                        ),
                    ],
                    style={'height': '400px', 'marginBottom': '20px'}
                )
            ]
        )
    ]
)


# Callback to update the line charts and country details based on dropdown or map selection
@callback(
    [Output('line-charts-container', 'children'),
     Output('country-details', 'children'),
     Output('country-dropdown', 'value')],
    [Input('country-dropdown', 'value'),
     Input('map', 'clickData'),
     Input('year-slider', 'value')],
    [State('country-dropdown', 'value')]
)
def update_line_charts_and_details(country, clickData, selected_years, current_dropdown_value):
    triggered_by = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    if triggered_by == 'map' and clickData is not None:
        country = clickData['points'][0]['location']

    line_chart_figures = []
    country_details = html.P("Click on a country to see details.", className='placeholder-text')

    if country:
        selected_data_chart = df_gdp_countries[(df_gdp_countries['Region/Country/Area'] == country) &
                                     (df_gdp_countries['Year'] >= selected_years[0]) & (df_gdp_countries['Year'] <= selected_years[1])]

        if not selected_data_chart.empty:
            # Line plot for each feature
            features = ['GDP in current prices (millions of US dollars)',
                        'GDP per capita (US dollars)',
                        'GDP real rates of growth (percent)']

            for feature in features:
                if selected_data_chart[feature].isnull().all():
                    continue  # Skip this feature if all values are NaN

                line_chart_figure = px.line(selected_data_chart, x='Year', y=feature,
                                            labels={'Year': 'Year', 'Value': feature})

                line_chart_figure.update_layout(title=f'{country} {feature}',
                                                xaxis_title='Year',
                                                yaxis_title=feature,
                                                margin=dict(l=20, r=20, t=40, b=20),
                                                height=300)

                line_chart_figures.append(dcc.Graph(figure=line_chart_figure, style={'height': '300px', 'width': '50%'}))

            latest_data_country = latest_data_gdp_countries[latest_data_gdp_countries['Region/Country/Area'] == country]
            if not latest_data_country.empty:
                gdp = latest_data_country['GDP in current prices (millions of US dollars)'].values[0]
                latest_year_country = latest_data_country['Year'].values[0]

                country_details = html.Div([
                    html.H3(f"{country}", className='country-name'),
                    html.P(f"GDP: ${gdp} million", className='country-population'),
                    html.P(f"Year: {latest_year_country}", className='country-year')
                ], className='country-details')

    return line_chart_figures, country_details, country


# Callback to update the map based on country selection
@callback(
    Output('map', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_map(selected_country):
    if selected_country:
        selected_data_map = latest_data_gdp_countries[latest_data_gdp_countries['Region/Country/Area'] == selected_country]
    else:
        selected_data_map = latest_data_gdp_countries

    map_figure = px.choropleth(
        selected_data_map,
        locations='Region/Country/Area',
        locationmode='country names',
        color='GDP in current prices (millions of US dollars)',
        hover_name='Region/Country/Area',
        color_continuous_scale='Rainbow',
        projection='orthographic',
        title='Country GDP Data'
    )

    map_figure.update_geos(
        showcoastlines=True,
        coastlinecolor="Gray",
        showland=True,
        landcolor="LightGray",
        showocean=True,
        oceancolor="LightBlue"
    )

    if selected_country:
        center_lat = selected_data_map['Latitude'].mean()
        center_lon = selected_data_map['Longitude'].mean()
        map_figure.update_geos(
            projection_rotation_lon=center_lon,
            projection_rotation_lat=center_lat
        )

    map_figure.update_layout(
        margin={"r": 0, "t": 60, "l": 0, "b": 0},
        dragmode='pan',
        height=800
    )

    return map_figure


# Callback to update region line plots based on dropdown selection and year slider
@callback(
    Output('gdp-line-plot', 'figure'),
    [Input('gdp-region-dropdown', 'value'),
     Input('gdp-year-slider', 'value')]
)
def update_gdp_line_plot(region, selected_years):
    filtered_data = df_gdp_regions[(df_gdp_regions['Region/Country/Area'] == region) &
                                   (df_gdp_regions['Year'] >= selected_years[0]) & (df_gdp_regions['Year'] <= selected_years[1])]

    gdp_line_plot = px.line(filtered_data, x='Year', y='GDP in current prices (millions of US dollars)',
                            title=f'GDP in Current Prices Over Time for {region}')
    gdp_line_plot.update_layout(xaxis_title='Year', yaxis_title='GDP in current prices (millions of US dollars)',
                                height=510)

    return gdp_line_plot


# Callback to update the growth rate line plot based on dropdown selection and year slider
@callback(
    Output('growth-rate-line-plot', 'figure'),
    [Input('gdp-region-dropdown', 'value'),
     Input('gdp-year-slider', 'value')]
)
def update_growth_rate_line_plot(region, selected_years):
    filtered_data = df_gdp_regions[(df_gdp_regions['Region/Country/Area'] == region) &
                                   (df_gdp_regions['Year'] >= selected_years[0]) & (df_gdp_regions['Year'] <= selected_years[1])]

    growth_rate_line_plot = px.line(filtered_data, x='Year', y='GDP real rates of growth (percent)',
                                    title=f'GDP Real Rates of Growth Over Time for {region}')
    growth_rate_line_plot.update_layout(xaxis_title='Year', yaxis_title='GDP real rates of growth (percent)',
                                        height=510)

    return growth_rate_line_plot


# Callback to update the pie chart based on year dropdown selection
@callback(
    Output('gdp-pie-chart', 'figure'),
    [Input('gdp-pie-year-dropdown', 'value')]
)
def update_gdp_pie_chart(selected_year):
    selected_data = df_gdp_regions[df_gdp_regions['Year'] == selected_year]

    total_gdp = df_gdp_regions.groupby('Year')['GDP in current prices (millions of US dollars)'].sum()
    region_gdp = selected_data.groupby('Region/Country/Area')['GDP in current prices (millions of US dollars)'].sum()
    percentage_gdp = region_gdp / total_gdp.sum() * 100

    pie_figure = px.pie(values=percentage_gdp.values, names=percentage_gdp.index,
                        title=f'Percentage of Global GDP by Region in {selected_year}')

    pie_figure.update_traces(textposition='inside', textinfo='percent+label')
    pie_figure.update_layout(
        autosize=True,
        height=600,
    )
    return pie_figure


# Callback to update the GDP per capita bar chart based on year dropdown selection
@callback(
    Output('gdp-per-capita-bar-chart', 'figure'),
    [Input('gdp-pie-year-dropdown', 'value')]
)
def update_gdp_per_capita_bar_chart(selected_year):
    selected_data = df_gdp_regions[df_gdp_regions['Year'] == selected_year]
    bar_figure = px.bar(
        selected_data,
        x='Region/Country/Area',
        y='GDP per capita (US dollars)',
        title=f'GDP Per Capita by Region in {selected_year}',
        labels={'GDP per capita (US dollars)': 'GDP Per Capita (US$)', 'Region/Country/Area': 'Region'}
    )
    bar_figure.update_layout(
        height=474
    )
    return bar_figure


# Callback to update the flat map based on the interval or range slider
@callback(
    Output('flat-map', 'figure'),
    [Input('interval-component', 'n_intervals'),
     Input('flat-map-year-slider', 'value')],
    [State('interval-component', 'disabled')]
)
def update_flat_map(n_intervals, slider_value, interval_disabled):
    start_year, end_year = slider_value
    available_years_in_range = [year for year in available_years_countries if start_year <= year <= end_year]

    # Determine the year to display based on whether the interval is enabled
    if not interval_disabled:
        current_index = n_intervals % len(available_years_in_range)
        year = available_years_in_range[current_index]
    else:
        year = slider_value[1]  # Default to the end of the selected range

    # Filter the dataframe for the selected year
    filtered_df = df_gdp_countries[df_gdp_countries['Year'] == year]

    # Create the flat map figure
    fig = px.choropleth(
        filtered_df,
        locations="Region/Country/Area",
        locationmode='country names',
        color="GDP in current prices (millions of US dollars)",
        hover_name="Region/Country/Area",
        color_continuous_scale='Rainbow',
        title=f"GDP in {year}"
    )

    fig.update_layout(
        geo=dict(
            showcoastlines=True,
            coastlinecolor="Gray",
            showland=True,
            landcolor="LightGray"
        ),
        margin={"r": 0, "t": 60, "l": 0, "b": 0},
        height=800
    )
    return fig


# Callback to enable/disable the interval and update the play button text
@callback(
    Output('interval-component', 'disabled'),
    Output('play-button', 'children'),
    Input('play-button', 'n_clicks'),
    State('interval-component', 'disabled')
)
def toggle_play(n_clicks, interval_disabled):
    if n_clicks % 2 == 0:
        return True, 'Play'
    else:
        return False, 'Pause'
