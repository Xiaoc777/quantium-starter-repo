import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# Load the processed data
df = pd.read_csv("formatted_sales_data.csv")

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Group by date to get overall daily sales
daily_sales = (
    df.groupby("Date", as_index=False)["Sales"]
    .sum()
    .sort_values("Date")
)

# Create the line chart
fig = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    title="Pink Morsel Sales Over Time",
    labels={
        "Date": "Date",
        "Sales": "Total Sales"
    }
)

# Add a vertical line for the price increase date
fig.add_vline(
    x="2021-01-15",
    line_dash="dash",
    line_color="red"
)

fig.add_annotation(
    x="2021-01-15",
    y=daily_sales["Sales"].max(),
    text="Price increase: 2021-01-15",
    showarrow=True,
    arrowhead=1
)

# Build the Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Soul Foods Pink Morsel Sales Visualiser"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)