import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objs as go

def circuit():
    st.title("F1 Championship Circuit Analysis")

    circuits = pd.read_csv('../data/circuits.csv')
    laptimes = pd.read_csv('../data/lap_times.csv')
    pitstops = pd.read_csv('../data/pit_stops.csv')
    races = pd.read_csv('../data/races.csv',parse_dates=['year'])
    
    results = pd.read_csv('../data/results.csv')
    status = pd.read_csv('../data/status.csv')


    @st.cache_data

    def load_fast_lap():
        df_merge = pd.merge(circuits, races, on='circuitId', how='left')
        df_merge = pd.merge(df_merge, results, on='raceId', how='left')
        df_merge = pd.merge(df_merge, status, on='statusId', how='left')

        # Subset and rename columns
        df_change = df_merge.drop(columns=['url_x', 'url_y', 'time_x', 'time_y'])
        df_rename = df_change.rename(columns={'name_x': 'name', 'time_y': 'time'})

        # Filter for specific statuses and years
        df_filter = df_rename.loc[df_rename['status'].isin(['Transmission', 'Engine', 'Overheating'])]
        df_filter = df_filter.loc[df_filter['year'] > '2015']

        # Group by name and altitude and count number of engine failures
        df_res = df_filter.groupby(['name', 'alt']).size().reset_index(name='NUMBER_OF_ENGINE_FAILURES')

        # Merge with circuits DataFrame and select relevant columns
        df_res = pd.merge(df_res, circuits, on=['name','alt'])
        df_res = df_res[['name', 'alt', 'NUMBER_OF_ENGINE_FAILURES', 'lat', 'lng']]

        # Sort by number of engine failures and select top 10
        df_res = df_res.sort_values(by='NUMBER_OF_ENGINE_FAILURES', ascending=False).head(10)

        # Rename altitude column
        df_res = df_res.rename(columns={'alt': 'altitude'})

        return df_res
    
    df_res = load_fast_lap()

    def plot_fast_lap(df_res):
        fig = px.scatter(df_res, x="name", y="altitude", size="NUMBER_OF_ENGINE_FAILURES",
                 color="NUMBER_OF_ENGINE_FAILURES", hover_name="name",
                 labels={"name": "Circuit Name", "alt": "Altitude", "NUMBER_OF_ENGINE_FAILURES": "Number of Engine Failures"},
                 title="Top 10 Circuits by Number of Engine Failures (2016-2017)")

        return fig

    fig = plot_fast_lap(df_res)

    st.plotly_chart(fig)

