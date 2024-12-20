
#Dash lab

python3.11 -m pip install pandas dash
wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/spacex_dash_app.py"
python3.11 spacex_dash_app.py

python3 -m pip install pandas plotly dash
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load data
df = pd.read_csv('spacex_launch_dash.csv')

# Get unique launch sites and payload range
launch_sites = df['Launch Site'].unique()
min_payload = df['Payload Mass (kg)'].min()
max_payload = df['Payload Mass (kg)'].max()

# Dropdown options
dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in launch_sites]

# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    # Dropdown for launch site selection
    dcc.Dropdown(id='site-dropdown', options=dropdown_options, value='ALL', placeholder="Select a Launch Site here", searchable=True),
    dcc.Graph(id='success-pie-chart'),
    dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, value=[min_payload, max_payload], marks={i: str(i) for i in range(0, 10001, 2500)}),
    dcc.Graph(id='success-payload-scatter-chart')])

# Callback for pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Data for all sites
        pie_data = df.groupby('class').size().reset_index(name='count')
        fig = px.pie(pie_data, names='class', values='count', title='Total Success Launches for All Sites')
    else:
        # Filter data for the selected site
        filtered_df = df[df['Launch Site'] == selected_site]
        pie_data = filtered_df.groupby('class').size().reset_index(name='count')
        fig = px.pie(pie_data, names='class', values='count', title=f'Total Success Launches for Site {selected_site}')
    return fig

# Callback for scatter plot
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),[Input(component_id='site-dropdown', component_property='value'),Input(component_id='payload-slider', component_property='value')])
def update_scatter(site_dropdown_value, payload_range):
    # Filter data based on payload range
    filtered_df_s = df[(df['Payload Mass (kg)'] >= payload_range[0]) & (df['Payload Mass (kg)'] <= payload_range[1])]

    if site_dropdown_value == 'ALL':
        # Scatter plot for all sites
        fig = px.scatter(filtered_df_s, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload and Outcome for All Sites', labels={'class': 'Launch Outcome'})
    else:
        # Filter data for the selected site
        site_data = filtered_df_s[filtered_df_s['Launch Site'] == site_dropdown_value]
        # Scatter plot for the specific site
        fig = px.scatter(site_data, x='Payload Mass (kg)', y='class', color='Booster Version Category', title=f'Correlation between Payload and Outcome for {site_dropdown_value}',labels={'class': 'Launch Outcome'})
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
