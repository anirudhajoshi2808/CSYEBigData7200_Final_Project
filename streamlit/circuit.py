import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objs as go
import plotly.subplots as sp

def circuit():
    st.title("F1 Championship Circuit Analysis")

    circuits = pd.read_csv('../data/circuits.csv')
    laptimes = pd.read_csv('../data/lap_times.csv')
    pitstops = pd.read_csv('../data/pit_stops.csv')
    races = pd.read_csv('../data/races.csv',parse_dates=['year'])
    
    results = pd.read_csv('../data/results.csv')
    status = pd.read_csv('../data/status.csv')
    drivers = pd.read_csv('../data/drivers.csv')

    @st.cache_data

    def load_engine_failure():
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
    
    df_res = load_engine_failure()

    def plot_engine_failure(df_res):
        circuit_names = df_res['name'].unique()
        selected_circuits = st.sidebar.multiselect('Select Circuits', circuit_names, default=circuit_names)
        df_res_filtered = df_res[df_res['name'].isin(selected_circuits)]

        fig1 = px.scatter(df_res_filtered, x="name", y="altitude", size="NUMBER_OF_ENGINE_FAILURES",
                color="NUMBER_OF_ENGINE_FAILURES", hover_name="name",
                labels={"name": "Circuit Name", "alt": "Altitude", "NUMBER_OF_ENGINE_FAILURES": "Number of Engine Failures"},
                title="Top 10 Circuits by Number of Engine Failures (2016-2017)")

        return fig1
    fig1 = plot_engine_failure(df_res)

    def load_circuit_perf():
        df_t3 = (circuits.merge(races, on="circuitId")
         .loc[:, ["circuitId", "circuitRef", "name_x", "raceId"]]
         .merge(results, on="raceId")
         .loc[:, ["circuitId", "circuitRef", "name_x", "raceId", "driverId"]]
         .merge(drivers, on="driverId")
         .loc[:, ["circuitId", "circuitRef", "name_x", "raceId", "driverId", "driverRef", "forename", "surname"]])

        df_t3_res = (df_t3.groupby(["driverRef", "circuitRef"])
                    .size()
                    .reset_index(name="Number_of_wins")
                    .sort_values(by="Number_of_wins", ascending=False)
                    .query("Number_of_wins > 10"))

        return df_t3_res
    
    df_t3_res = load_circuit_perf()

    def plot_circuit_perf(df_t3_res):
        # filter data for each driver
        df_ham = df_t3_res[df_t3_res['driverRef'] == 'hamilton']
        df_vet = df_t3_res[df_t3_res['driverRef'] == 'vettel']
        df_alo = df_t3_res[df_t3_res['driverRef'] == 'alonso']
        df_bar = df_t3_res[df_t3_res['driverRef'] == 'barrichello']

        # create subplots
        fig = sp.make_subplots(rows=2, cols=2, subplot_titles=("Number of Wins by Circuit- Lewis Hamilton", 
                                                            "Number of Wins by Circuit-Sebastian Vettel",
                                                            "Number of Wins by Circuit-Fernando Alonso",
                                                            "Number of Wins by Circuit-Rubens Barrichello"))

        # plot data for each driver
        fig.add_trace(go.Bar(x=df_ham['circuitRef'], y=df_ham['Number_of_wins'], name='Hamilton', marker_color='#87CEFA'), row=1, col=1)
        fig.add_trace(go.Bar(x=df_vet['circuitRef'], y=df_vet['Number_of_wins'], name='Vettel', marker_color='#FF1744'), row=1, col=2)
        fig.add_trace(go.Bar(x=df_alo['circuitRef'], y=df_alo['Number_of_wins'], name='Alonso', marker_color='#E0FFFF'), row=2, col=1)
        fig.add_trace(go.Bar(x=df_bar['circuitRef'], y=df_bar['Number_of_wins'], name='Barrichello', marker_color='#EF5350'), row=2, col=2)

        # update layout
        fig.update_layout(title='Number of Wins by Circuit', height=800, width=800,
                        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
        fig.update_xaxes(title_text='Circuit Names', row=1, col=1)
        fig.update_xaxes(title_text='Circuit Names', row=1, col=2)
        fig.update_xaxes(title_text='Circuit Names', row=2, col=1)
        fig.update_xaxes(title_text='Circuit Names', row=2, col=2)
        fig.update_yaxes(title_text='Total Wins', row=1, col=1)
        fig.update_yaxes(title_text='Total Wins', row=1, col=2)
        fig.update_yaxes(title_text='Total Wins', row=2, col=1)
        fig.update_yaxes(title_text='Total Wins', row=2, col=2)

        return fig
    
    fig = plot_circuit_perf(df_t3_res)

    def load_fast_lap():
        df_t2 = (results[results['statusId'] == 1]
         .merge(races, on='raceId')
         .merge(circuits, on='circuitId')
         .loc[:, ['circuitId', 'circuitRef', 'name_y', 'fastestLapSpeed']]
         .replace('\\N', pd.NA)
         .dropna()
         .astype({'fastestLapSpeed': float})
         .groupby(['circuitId', 'circuitRef', 'name_y'])
         .agg(fastestLapSpeeds=('fastestLapSpeed', 'max'))
         .reset_index()
         .sort_values('fastestLapSpeeds', ascending=False)
         .head(10))

        return df_t2
    
    df_t2 = load_fast_lap()

    def plot_fast_lap(df_t2):
        df_monza = df_t2[df_t2['circuitRef'] == "monza"]
        df_st = df_t2[df_t2['circuitRef'] == "silverstone"]
        df_rb = df_t2[df_t2['circuitRef'] == "red_bull_ring"]
        df_bh = df_t2[df_t2['circuitRef'] == "bahrain"]

        # create list to store figures
        figures = []

        # loop through circuits and create figure for each
        for df_circuit, circuit_name in zip([df_monza, df_st, df_rb, df_bh], 
                                            ["Monza", "Silverstone", "Red Bull Ring", "Bahrain"]):
            # create gauge figure
            fig = go.Figure(go.Indicator(
                            domain = {'x': [0, 1], 'y': [0, 1]},
                            value = df_circuit['fastestLapSpeeds'].iloc[0],
                            title = {'text': f"Fastest Lap Speed (km/h)- {circuit_name} Circuit"},
                            gauge = {
                                'axis': {'range': [None, 400], 'tickcolor': 'red', 'tickwidth': 1},
                                'bar': {'color': 'red'},
                                'bgcolor': 'white',
                                'bordercolor': 'gray',
                                'borderwidth': 2,
                                'steps': [
                                    {'range': [0, 150], 'color': 'lightgray'},
                                    {'range': [150, 250], 'color': 'gray'}
                                ]
                            },
                            mode = 'gauge+number'
                            ))

            # add figure to list
            figures.append(fig)

        return figures

    figures = plot_fast_lap(df_t2)
    st.plotly_chart(fig1)
    st.plotly_chart(fig)

    # left_column, right_column = st.columns(2)

    # left_column.plotly_chart(fig1, use_container_width=True)
    # right_column.plotly_chart(fig, use_container_width=True)
    # for i in figures:
    #     st.plotly_chart(i)

    rows = 2
    cols = 2
    fig_grid = []
    for i in range(rows):
        row = []
        for j in range(cols):
            fig = figures[i*cols + j] if i*cols + j < len(figures) else None
            row.append(fig)
        fig_grid.append(row)

    for row in fig_grid:
        cols = st.columns(len(row))
        for i, col in enumerate(cols):
            with col:
                if row[i] is not None:
                    st.plotly_chart(row[i])

    