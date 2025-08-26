import pyodbc
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# -------------------------------
# 1️⃣ Connect to SQL Server
# -------------------------------
server = r'NBDBNPF3W63YL\DEVELOPER19'
database = 'Jabulani'
username = 'sa'
password = 'Mjey@yahoo1'

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};'
    f'SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=no'
)

query = "SELECT * FROM DeliveryData"
df = pd.read_sql(query, conn)




from sqlalchemy import create_engine
import urllib

params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=NBDBNPF3W63YL\DEVELOPER19;"
    "DATABASE=Jabulani;"
    "UID=sa;"
    "PWD=Mjey@yahoo1;"
    "TrustServerCertificate=yes"
)

engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

df = pd.read_sql(query, engine)

conn.close()
# -------------------------------
# 2️⃣ Preprocess Data
# -------------------------------
df['scheduled_datetime'] = pd.to_datetime(df['scheduled_datetime'])
df['month'] = df['scheduled_datetime'].dt.to_period('M')
df['delivery_status'] = df['delay_minutes'].apply(lambda x: 'On-time' if x == 0 else 'Late')

# -------------------------------
# 3️⃣ Initialize Dash App
# -------------------------------
app = dash.Dash(__name__)

# -------------------------------
# 4️⃣ Layout
# -------------------------------
app.layout = html.Div([
    html.H1("Delivery Data Dashboard", style={'textAlign': 'center'}),
    
    html.Div([
        html.Label("Select City:"),
        dcc.Dropdown(
            id='city-dropdown',
            options=[{'label': c, 'value': c} for c in df['city'].unique()],
            value=None,
            multi=True,
            placeholder="All Cities"
        )
    ], style={'width': '40%', 'margin': 'auto'}),
    
    dcc.Graph(id='status-bar'),
    dcc.Graph(id='avg-delay-bar'),
    dcc.Graph(id='monthly-trends-line'),
    dcc.Graph(id='scatter-distance-weight'),
    dcc.Graph(id='correlation-heatmap')
])

# -------------------------------
# 5️⃣ Callbacks for Interactivity
# -------------------------------
@app.callback(
    [
        dash.dependencies.Output('status-bar', 'figure'),
        dash.dependencies.Output('avg-delay-bar', 'figure'),
        dash.dependencies.Output('monthly-trends-line', 'figure'),
        dash.dependencies.Output('scatter-distance-weight', 'figure'),
        dash.dependencies.Output('correlation-heatmap', 'figure')
    ],
    [dash.dependencies.Input('city-dropdown', 'value')]
)
def update_charts(selected_cities):
    filtered_df = df if not selected_cities else df[df['city'].isin(selected_cities)]
    
    # Status Bar
    status_fig = px.bar(filtered_df['status'].value_counts().reset_index(),
                        x='index', y='status',
                        labels={'index':'Status', 'status':'Total Deliveries'},
                        title='Total Deliveries by Status')
    
    # Average Delay by City
    avg_delay_fig = px.bar(filtered_df.groupby('city')['delay_minutes'].mean().reset_index(),
                           x='city', y='delay_minutes',
                           title='Average Delay by City',
                           labels={'delay_minutes':'Avg Delay (min)'})
    
    # Monthly Delivery Trends
    monthly_df = filtered_df.groupby('month').size().reset_index(name='count')
    monthly_fig = px.line(monthly_df, x='month', y='count', title='Monthly Delivery Trends', markers=True)
    
    # Distance vs Weight Scatter
    scatter_fig = px.scatter(filtered_df, x='distance_km', y='weight_kg',
                             color='carrier', title='Distance vs Weight by Carrier')
    
    # Correlation Heatmap
    corr_df = filtered_df[['delay_minutes','distance_km','weight_kg']].corr().reset_index()
    heatmap_fig = px.imshow(filtered_df[['delay_minutes','distance_km','weight_kg']].corr(),
                            text_auto=True, title="Correlation Heatmap")
    
    return status_fig, avg_delay_fig, monthly_fig, scatter_fig, heatmap_fig

# -------------------------------
# 6️⃣ Run App
# -------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
