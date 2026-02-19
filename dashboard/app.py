import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Load data
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'experiment_data.csv')

# Helper to load data efficiently
def load_data():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        df['date'] = pd.to_datetime(df['date'])
        return df
    return pd.DataFrame()

df = load_data()

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

# Styles
card_style = {
    'backgroundColor': 'white',
    'borderRadius': '10px',
    'padding': '20px',
    'margin': '10px',
    'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'
}

# Layout
app.layout = html.Div(style={'backgroundColor': '#f0f2f5', 'padding': '20px', 'minHeight': '100vh'}, children=[
    html.H1("🚀 A/B Testing & Impact Analysis Dashboard", style={'textAlign': 'center', 'color': '#2c3e50'}),
    
    # Top Stats Row
    html.Div([
        html.Div([
            html.H4("Total Users"),
            html.H2(f"{len(df):,}", id='total-users')
        ], style=card_style, className='three columns'),
        
        html.Div([
            html.H4("Conversion Rate"),
            html.H2(f"{df['converted'].mean()*100:.2f}%", id='avg-conversion')
        ], style=card_style, className='three columns'),
        
        html.Div([
            html.H4("Total Revenue"),
            html.H2(f"${df['revenue'].sum():,.0f}", id='total-revenue')
        ], style=card_style, className='three columns'),
        
        html.Div([
            html.H4("Avg Session Time"),
            html.H2(f"{df['session_duration_sec'].mean():.0f} sec", id='avg-session')
        ], style=card_style, className='three columns'),
    ], className='row'),

    # Filters
    html.Div([
        html.H5("Segment Filters"),
        html.Div([
            dcc.Dropdown(
                id='segment-filter',
                options=[
                    {'label': 'Device', 'value': 'device'},
                    {'label': 'Country', 'value': 'country'},
                    {'label': 'Browser', 'value': 'browser'},
                    {'label': 'Source', 'value': 'source'},
                    {'label': 'Loyalty Tier', 'value': 'loyalty_tier'},
                    {'label': 'Age Group', 'value': 'age_group'}
                ],
                value='device',
                clearable=False
            )
        ], className='four columns')
    ], style={**card_style, 'height': '100px'}, className='row'),
    
    # Charts Row 1
    html.Div([
        html.Div([
            dcc.Graph(id='conversion-trend')
        ], style=card_style, className='six columns'),
        
        html.Div([
            dcc.Graph(id='uplift-by-segment')
        ], style=card_style, className='six columns'),
    ], className='row'),
    
    # Charts Row 2
    html.Div([
        html.Div([
            dcc.Graph(id='revenue-dist')
        ], style=card_style, className='six columns'),
        
        html.Div([
            dcc.Graph(id='engagement-bubble') # Scatter plot: pages visited vs duration
        ], style=card_style, className='six columns'),
    ], className='row'),
    
    # Data Table Preview
    html.Div([
        html.H5("Raw Data Preview (Top 50 Rows)"),
        dash_table.DataTable(
            data=df.head(50).to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns if i not in ['user_id']],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'},
            page_size=10
        )
    ], style=card_style, className='row')
])

# Callbacks
@app.callback(
    [Output('conversion-trend', 'figure'),
     Output('uplift-by-segment', 'figure'),
     Output('revenue-dist', 'figure'),
     Output('engagement-bubble', 'figure')],
    [Input('segment-filter', 'value')]
)
def update_graphs(segment):
    # 1. Trend Line
    daily = df.groupby(['date', 'group'])['converted'].mean().reset_index()
    fig_trend = px.line(daily, x='date', y='converted', color='group', 
                        title='Daily Conversion Rate Trend',
                        template='plotly_white',
                        color_discrete_map={'Control': '#EF553B', 'Treatment': '#636EFA'})
    
    # 2. Lift by Segment
    # Calculate conversion rate per segment per group
    seg_group = df.groupby([segment, 'group'])['converted'].mean().reset_index()
    fig_uplift = px.bar(seg_group, x=segment, y='converted', color='group', barmode='group',
                        title=f'Conversion Rate by {segment.title()}',
                        template='plotly_white',
                        text_auto='.1%',
                        color_discrete_map={'Control': '#EF553B', 'Treatment': '#636EFA'})
    
    # 3. Revenue Distribution
    fig_rev = px.histogram(df[df['converted']==1], x='revenue', color='group', barmode='overlay',
                           title='Revenue Distribution (Converted Users)',
                           nbins=50, opacity=0.7,
                           template='plotly_white')

    # 4. Bubble Chart (Engagement)
    # Aggregate by segment to avoid overplotting 200k points
    agg_eng = df.groupby([segment, 'group']).agg({
        'session_duration_sec': 'mean',
        'pages_visited': 'mean',
        'user_id': 'count',
        'converted': 'mean'
    }).rename(columns={'user_id': 'User Count', 'converted': 'Conv. Rate'}).reset_index()
    
    fig_bubble = px.scatter(agg_eng, x='session_duration_sec', y='pages_visited',
                            size='User Count', color='group', hover_name=segment,
                            title=f'Engagement: Duration vs Pages ({segment.title()})',
                            template='plotly_white')
    
    return fig_trend, fig_uplift, fig_rev, fig_bubble

if __name__ == '__main__':
    # FIXED: using app.run(debug=True) instead of app.run_server
    app.run(debug=True, port=8050)
