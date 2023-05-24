import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the csv into a dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Store the max and min payload
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()


app = dash.Dash(__name__)
server = app.server

# Create a list of unique launch sites
uniquelaunchsites = spacex_df["Launch Site"].unique().tolist()

# Create a dictionary for each unique site
lsites = []
lsites.append({"label": "All Sites", "value": "All Sites"})
for site in uniquelaunchsites:
    lsites.append({"label": site, "value": site})


# HTML CODE
app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        # Dropdown with lsites
        dcc.Dropdown(
            id="site_dropdown",
            options=lsites,
            placeholder="Select a Launch Site here",
            searchable=True,
            value="All Sites",
        ),
        html.Br(),
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),
        html.P("Payload range (Kg):"),
        # Range Slider with min and max payload as calculated before
        dcc.RangeSlider(
            id="payload_slider",
            min=0,
            max=10000,
            step=1000,
            marks={
                0: "0 kg",
                1000: "1000 kg",
                2000: "2000 kg",
                3000: "3000 kg",
                4000: "4000 kg",
                5000: "5000 kg",
                6000: "6000 kg",
                7000: "7000 kg",
                8000: "8000 kg",
                9000: "9000 kg",
                10000: "10000 kg",
            },
            value=[min_payload, max_payload],
        ),
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ]
)


# Code to handle the dropdown select and output pie chart
@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    [Input(component_id="site_dropdown", component_property="value")],
)
def update_graph(site_dropdown):
    if site_dropdown == "All Sites":
        df = spacex_df[spacex_df["class"] == 1]
        fig = px.pie(
            df,
            names="Launch Site",
            title="Total Success Launches By all sites",
        )
    else:
        df = spacex_df.loc[spacex_df["Launch Site"] == site_dropdown]
        fig = px.pie(
            df,
            names="class",
            title="Total Success Launches for site " + site_dropdown,
        )
    return fig


# Code to handle dropdown and slider input and output scatter chart
@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [
        Input(component_id="site_dropdown", component_property="value"),
        Input(component_id="payload_slider", component_property="value"),
    ],
)
def update_scattergraph(site_dropdown, payload_slider):
    low, high = payload_slider #Returns 2 values that need to be destructured
    if site_dropdown == "All Sites":
        df = spacex_df
    else:
        df = spacex_df.loc[spacex_df["Launch Site"] == site_dropdown]
    mask = (df["Payload Mass (kg)"] > low) & (df["Payload Mass (kg)"] < high)
    fig = px.scatter(
        df[mask],
        x="Payload Mass (kg)",
        y="class",
        color="Booster Version",
        size="Payload Mass (kg)",
        hover_data=["Payload Mass (kg)"],
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=False)
    