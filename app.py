import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load processed data
df = pd.read_csv("formatted_sales_data.csv")
df["Date"] = pd.to_datetime(df["Date"])

app = Dash(__name__)
server = app.server


def make_figure(region_value):
    if region_value == "all":
        filtered_df = df.copy()
        chart_title = "Pink Morsel Sales Over Time - All Regions"
    else:
        filtered_df = df[df["Region"].str.lower() == region_value].copy()
        chart_title = f"Pink Morsel Sales Over Time - {region_value.capitalize()} Region"

    daily_sales = (
        filtered_df.groupby("Date", as_index=False)["Sales"]
        .sum()
        .sort_values("Date")
    )

    fig = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        title=chart_title,
        labels={"Date": "Date", "Sales": "Total Sales"},
    )

    fig.update_traces(line=dict(width=3))
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(size=15),
        title=dict(x=0.5),
        margin=dict(l=40, r=40, t=80, b=40),
    )

    fig.add_vline(
        x="2021-01-15",
        line_dash="dash",
        line_color="red",
        line_width=2,
    )

    fig.add_annotation(
        x="2021-01-15",
        y=daily_sales["Sales"].max(),
        text="Price increase: 2021-01-15",
        showarrow=True,
        arrowhead=1,
        bgcolor="white",
    )

    return fig


app.layout = html.Div(
    className="page",
    children=[
        html.Div(
            className="card",
            children=[
                html.H1(
                    "Soul Foods Pink Morsel Sales Visualiser",
                    className="main-title"
                ),
                html.P(
                    "Explore Pink Morsel sales over time and compare regions before and after the price increase.",
                    className="subtitle"
                ),
                html.Div(
                    className="filter-section",
                    children=[
                        html.Label("Choose a region:", className="filter-label"),
                        dcc.RadioItems(
                            id="region-filter",
                            options=[
                                {"label": "All", "value": "all"},
                                {"label": "North", "value": "north"},
                                {"label": "East", "value": "east"},
                                {"label": "South", "value": "south"},
                                {"label": "West", "value": "west"},
                            ],
                            value="all",
                            inline=True,
                            className="radio-group",
                            inputClassName="radio-input",
                            labelClassName="radio-label",
                        ),
                    ],
                ),
                dcc.Graph(
                    id="sales-chart",
                    figure=make_figure("all"),
                    className="graph"
                ),
            ],
        )
    ],
)


@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value")
)
def update_chart(selected_region):
    return make_figure(selected_region)


if __name__ == "__main__":
    app.run(debug=True)