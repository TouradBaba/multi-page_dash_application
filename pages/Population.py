import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from dash_bootstrap_templates import load_figure_template


# Register the page with Dash app
dash.register_page(__name__, path='/', name='Population 📊')

load_figure_template("darkly")

# Load the dataset for countries
df = pd.read_csv('https://raw.githubusercontent.com/TouradBaba/exploratory_data_analysis_and_visualization/master/data/cleaned_df.csv')

# Find the latest year for each country
latest_years = df.groupby('Region/Country/Area')['Year'].max().reset_index()

# Merge to get the latest data for each country
latest_data = pd.merge(df, latest_years, on=['Region/Country/Area', 'Year'], how='inner')

# Get unique countries for dropdown options
regions1 = latest_data['Region/Country/Area'].unique()

# Load the dataset for regions
df_regions = pd.read_excel('https://github.com/TouradBaba/exploratory_data_analysis_and_visualization/raw/master/data/cleaned_df2.xlsx')

# Get unique regions for dropdown options
regions = df_regions['Region/Country/Area'].unique()

# Calculate percentage of global surface area by region
total_area = df_regions.groupby('Year')['Surface area (thousand km2)'].sum()
region_area = df_regions.groupby('Region/Country/Area')['Surface area (thousand km2)'].sum()
percentage_area = region_area / total_area.sum() * 100

# Create pie chart for area percentage
area_pie_figure = px.pie(values=percentage_area.values, names=percentage_area.index,
                         title=None)
area_pie_figure.update_traces(textposition='inside', textinfo='percent+label')
area_pie_figure.update_layout(margin=dict(l=20, r=20, t=40, b=20))

# Update layout with both population and area pie charts
layout = html.Div(
    className='container-fluid',
    children=[
        # Header section for countries
        html.Div(
            className='jumbotron bg-dark text-white',
            children=[
                html.H1("Population Data Dashboard", className='display-4'),
                html.P(
                    "Explore population data over time by selecting a country or region.",
                    className='lead'
                )
            ]
        ),
        html.Hr(className='my-4'),

        # Country section
        html.Div(
            className='row',
            children=[
                html.Div(
                    className='col-md-6 map-container',
                    children=[
                        dcc.Graph(id='map1', config={'scrollZoom': True})
                    ]
                ),
                html.Div(
                    className='col-md-6 details-container bg-light p-3',
                    children=[
                        html.Div(id='country-details1', className='details'),
                        dcc.Dropdown(
                            id='country-dropdown1',
                            options=[{'label': country, 'value': country} for country in regions1],
                            placeholder="Select a country",
                            className='mb-3'
                        ),
                        html.Div(
                            dcc.RangeSlider(
                                id='year-slider-country',
                                min=df['Year'].min(),
                                max=df['Year'].max(),
                                value=[df['Year'].min(), df['Year'].max()],
                                marks={str(year): str(year) for year in df['Year'].unique()},
                                step=None,
                                className='mb-3'
                            ),
                            style={'marginTop': '20px'}
                        ),
                        html.Div(
                            id='line-charts-container1',
                            className='line-charts-container',
                            style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'wrap'}
                        )
                    ]
                )
            ]
        ),
        html.Hr(className='my-4'),

        # Region section
        html.Div(
            className='row',
            children=[
                html.Div(
                    className='col-md-6 heatmap-container',
                    children=[
                        dcc.Graph(id='density-heatmap', config={'scrollZoom': True})
                    ]
                ),
                html.Div(
                    className='col-md-6 details-container bg-light p-3',
                    children=[
                        html.Div(id='region-details', className='details'),
                        html.Hr(style={'backgroundColor': 'black'}),
                        dcc.Dropdown(
                            id='region-dropdown',
                            options=[{'label': region, 'value': region} for region in regions],
                            placeholder="Select a region",
                            className='mb-3'
                        ),
                        html.Div(
                            dcc.RangeSlider(
                                id='year-slider-region',
                                min=df_regions['Year'].min(),
                                max=df_regions['Year'].max(),
                                value=[df_regions['Year'].min(), df_regions['Year'].max()],
                                marks={str(year): str(year) for year in df_regions['Year'].unique()},
                                step=None,
                                className='mb-3'
                            ),
                            style={'marginTop': '20px'}
                        )
                    ]
                )
            ]
        ),

        html.Hr(className='my-4'),

        # Additional charts section
        html.Div(
            className='row mt-4',
            children=[
                html.Div(
                    className='col-md-6',
                    children=[
                        dcc.Graph(id='line-plot')
                    ]
                ),
                html.Div(
                    className='col-md-6',
                    children=[
                        dcc.Graph(id='bar-plot')
                    ]
                )
            ]
        ),

        # Pie chart section

        html.Div(
            className='row mt-4 justify-content-end',
            children=[
                html.Div(
                    className='col-md-6',
                    children=[
                        dcc.Dropdown(
                            id='pie-year-dropdown',
                            options=[{'label': year, 'value': year} for year in df_regions['Year'].unique()],
                            value=2022,  # Default value
                            placeholder="Select a year",
                            className='mb-3'
                        ),
                        dcc.Graph(id='pie-chart', config={'displayModeBar': False}),
                    ],
                ),
                html.Div(
                    className='col-md-6',
                    children=[
                        html.P('Percentage of Global Surface Area by Region', className="text-center",
                               style={'fontSize': 24, 'color': '#FFFFFF'}),
                        dcc.Graph(
                            id='area-pie-chart',
                            figure=area_pie_figure,
                            config={'displayModeBar': False}
                        ),
                    ],
                )
            ]
        )
    ]
)


# Callback to update the line charts and country details based on dropdown or map selection
@callback(
    [Output('line-charts-container1', 'children'),
     Output('country-details1', 'children'),
     Output('country-dropdown1', 'value')],
    [Input('country-dropdown1', 'value'),
     Input('map1', 'clickData'),
     Input('year-slider-country', 'value')],
    [State('country-dropdown1', 'value')]
)
def update_line_charts_and_details(country, clickData, selected_years, current_dropdown_value):
    triggered_by = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    if triggered_by == 'map1' and clickData is not None:
        country = clickData['points'][0]['location']

    line_chart_figures = []
    country_details = html.P("Click on a country to see details.", className='placeholder-text')

    if country:
        selected_data_chart = df[(df['Region/Country/Area'] == country) &
                                 (df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])]

        if not selected_data_chart.empty:
            # Line plot for each feature
            features = ['Population aged 0 to 14 years old (percentage)',
                        'Population aged 60+ years old (percentage)',
                        'Sex ratio (males per 100 females)',
                        'Population mid-year estimates (millions)']

            for feature in features:
                line_chart_figure = px.line(selected_data_chart, x='Year', y=feature,
                                            labels={'Year': 'Year', 'Value': feature})

                line_chart_figure.update_layout(title=f'{country} {feature}',
                                                xaxis_title='Year',
                                                yaxis_title=feature,
                                                margin=dict(l=20, r=20, t=40, b=20),
                                                height=300)

                line_chart_figures.append(dcc.Graph(figure=line_chart_figure, style={'height': '300px', 'width': '50%'}))

            latest_data_country = latest_data[latest_data['Region/Country/Area'] == country]
            if not latest_data_country.empty:
                population = latest_data_country['Population mid-year estimates (millions)'].values[0]
                surface_area_km2 = latest_data_country['surface_area_km2'].values[0]
                latest_year_country = latest_data_country['Year'].values[0]

                country_details = html.Div([
                    html.H3(f"{country}", className='country-name'),
                    html.P(f"Population: {population} million", className='country-population'),
                    html.P(f"Surface Area KM2: {surface_area_km2}", className='country-area'),
                    html.P(f"Year: {latest_year_country}", className='country-year')
                ], className='country-details')

    return line_chart_figures, country_details, country


# Callback to update the map based on country selection
@callback(
    Output('map1', 'figure'),
    [Input('country-dropdown1', 'value')]
)
def update_map(selected_country):
    if selected_country:
        selected_data_map = latest_data[latest_data['Region/Country/Area'] == selected_country]
    else:
        selected_data_map = latest_data

    map_figure = px.choropleth(
        selected_data_map,
        locations='Region/Country/Area',
        locationmode='country names',
        color='Population mid-year estimates (millions)',
        hover_name='Region/Country/Area',
        color_continuous_scale='RdBu',
        projection='orthographic',
        title='Country Population Data',
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


# Callback to update the heatmap and region details based on selected region and years
@callback(
    [Output('density-heatmap', 'figure'),
     Output('region-details', 'children')],
    [Input('region-dropdown', 'value'),
     Input('year-slider-region', 'value')]
)
def update_heatmap_and_details(region, selected_years):
    if region:
        selected_data = df_regions[(df_regions['Region/Country/Area'] == region) &
                                   (df_regions['Year'] >= selected_years[0]) & (
                                               df_regions['Year'] <= selected_years[1])]
    else:
        selected_data = df_regions[
            (df_regions['Year'] >= selected_years[0]) & (df_regions['Year'] <= selected_years[1])]

    density_heatmap = px.imshow(
        selected_data.pivot_table(index='Year', columns='Region/Country/Area', values='Population density'),
        labels={'color': 'Population Density'},
        title=f'Density Heatmap for {region}' if region else 'Density Heatmap for All Regions')

    density_heatmap.update_layout(margin={"r": 0, "t": 60, "l": 0, "b": 0})

    if not selected_data.empty:
        # Region details
        if region:
            region_details = html.Div([
                html.H3(f"{region}", className='region-name'),
                html.P(f"Years: {selected_years[0]} - {selected_years[1]}", className='region-years')
            ], className='region-details')
        else:
            region_details = html.P("Select a region to see details.", className='placeholder-text')
    else:
        region_details = html.P("No data available for selected region and year range.", className='placeholder-text')

    return density_heatmap, region_details


# Callback to update line plot based on selected region and years
@callback(
    Output('line-plot', 'figure'),
    [Input('region-dropdown', 'value'),
     Input('year-slider-region', 'value')]
)
def update_line_plot(region, selected_years):
    selected_data = df_regions[(df_regions['Region/Country/Area'] == region) &
                                   (df_regions['Year'] >= selected_years[0]) & (
                                               df_regions['Year'] <= selected_years[1])]

    line_figure = px.line(selected_data, x='Year', y='Population mid-year estimates (millions)',
                          color='Region/Country/Area',
                          title=f'Population over Time for {region}')
    line_figure.update_layout(margin=dict(l=20, r=20, t=40, b=20))

    return line_figure


# Callback to update bar plot based on selected region and years
@callback(
    Output('bar-plot', 'figure'),
    [Input('region-dropdown', 'value'),
     Input('year-slider-region', 'value')]
)
def update_bar_plot(region, selected_years):
    selected_data = df_regions[(df_regions['Region/Country/Area'] == region) &
                                   (df_regions['Year'].isin([2010, 2015, 2021, 2022]))]

    # Create bar plot with separate bars for each population age group
    bar_figure = px.bar(selected_data, x='Year', y=['Population aged 0 to 14 years old (percentage)',
                                                    'Population aged 60+ years old (percentage)'],
                        color_discrete_sequence=['#1f77b4', '#ff7f0e'],
                        title=f'Population Distribution for {region}')

    bar_figure.update_layout(barmode='group', margin=dict(l=20, r=20, t=40, b=20))

    return bar_figure


# Callback to update pie chart based on selected years
@callback(
    Output('pie-chart', 'figure'),
    [Input('pie-year-dropdown', 'value')]
)
def update_pie_chart(selected_year):
    selected_data = df_regions[df_regions['Year'] == selected_year]

    total_population = df_regions.groupby('Year')['Population mid-year estimates (millions)'].sum()
    region_population = selected_data.groupby('Region/Country/Area')['Population mid-year estimates (millions)'].sum()
    percentage_population = region_population / total_population.sum() * 100

    pie_figure = px.pie(values=percentage_population.values, names=percentage_population.index,
                        title=f'Percentage of Global Population by Region in {selected_year}')

    pie_figure.update_traces(textposition='inside', textinfo='percent+label')
    pie_figure.update_layout(margin=dict(l=20, r=20, t=40, b=20))

    return pie_figure
