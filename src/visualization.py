import plotly.express as px
import plotly.graph_objects as go

def plot_conversion_rates(df):
    """Plot conversion rates by group over time"""
    daily = df.groupby(['date', 'group'])['converted'].mean().reset_index()
    fig = px.line(daily, x='date', y='converted', color='group', title='Daily Conversion Rate by Group')
    return fig

def plot_revenue_distribution(df):
    """Plot revenue distribution (histogram)"""
    fig = px.histogram(df[df['revenue'] > 0], x='revenue', color='group', barmode='overlay', title='Revenue Distribution (Payers Only)')
    return fig

def plot_uplift_by_segment(df, segment='device'):
    """Bar chart of uplift by segment"""
    res = df.groupby([segment, 'group'])['converted'].mean().reset_index()
    # Calculate lif per segment
    # ...
    fig = px.bar(res, x=segment, y='converted', color='group', barmode='group', title=f'Conversion Rate by {segment}')
    return fig
