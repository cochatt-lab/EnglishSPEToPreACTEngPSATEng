
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")
st.title("English JS vs Standardized Test Percentiles Dashboard")

# Load data
df = pd.read_csv("TEST for DASH Student Performance Evaluation for 20252026 Rising 912 Responses WIP Rising 11.csv")

x_column = "English JS"
y_columns = [
    "PreACT Composite Percentile PreACT",
    "PreACT Reading PreACT",
    "PreACT English Percentile PreACT",
    "PSAT Percentile Total",
    "PSAT EBRW percentile"
]

correlation_df = df[[x_column] + y_columns]
correlation_matrix = correlation_df.corr()

# Create subplots
fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=[f"{x_column} vs {y}" for y in y_columns] + ["Correlation Heatmap"],
    specs=[[{"type": "scatter"}, {"type": "scatter"}],
           [{"type": "scatter"}, {"type": "scatter"}],
           [{"colspan": 2}, None]]
)

for i, y_column in enumerate(y_columns):
    scatter = px.scatter(df, x=x_column, y=y_column, trendline="ols")
    for trace in scatter.data:
        fig.add_trace(trace, row=(i // 2) + 1, col=(i % 2) + 1)

heatmap = go.Heatmap(
    z=correlation_matrix.values,
    x=correlation_matrix.columns,
    y=correlation_matrix.index,
    colorscale='RdBu',
    zmin=-1, zmax=1,
    showscale=True
)
fig.add_trace(heatmap, row=3, col=1)

fig.update_layout(height=1200, width=1000, title_text="Dashboard: English JS vs Standardized Test Percentiles")
st.plotly_chart(fig, use_container_width=True)
