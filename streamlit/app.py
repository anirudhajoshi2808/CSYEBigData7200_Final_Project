import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="F1 Championship Analysis",
    page_icon=":bar_chart:",
    layout="wide"
)

st.title("F1 Championship Analysis")

@st.cache_data
def load_data():
    circuits = pd.read_csv('../data/circuits.csv')
    laptimes = pd.read_csv('../data/lap_times.csv')
    pitstops = pd.read_csv('../data/pit_stops.csv')
    seasons = pd.read_csv('../data/seasons.csv',parse_dates=['year'])
    status = pd.read_csv('../data/status.csv')

    constructor_standings = pd.read_csv('../data/constructor_standings.csv')
    constructors = pd.read_csv('../data/constructors.csv')
    driver_standings = pd.read_csv('../data/driver_standings.csv')
    drivers = pd.read_csv('../data/drivers.csv')

    races = pd.read_csv('../data/races.csv',parse_dates=['year'])
    constructor_results = pd.read_csv('../data/constructor_results.csv')
    results = pd.read_csv('../data/results.csv')
    qualifying = pd.read_csv('../data/qualifying.csv')

    team = constructors.merge(results,on='constructorId',how = 'left')

    best = team[['name','points','raceId']]
    best = best.groupby('name')['raceId'].nunique().sort_values(ascending=False).reset_index(name = 'races')
    best = best[best['races'] >= 100]

    func = lambda x: x.points.sum()/x.raceId.nunique()
    data = team[team['name'].isin(best.name)].groupby('name').apply(func).sort_values(ascending=False).reset_index(name = 'points_per_race')
    
    return data

def plot_data(data):
    fig = px.bar(x=data.name, y=data['points_per_race'])
    

    fig.update_layout(
        title="Constructor's Points per Race",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        font=dict(size=20),
        bargap=0.2,
        bargroupgap=0.1,
        margin=dict(l=50, r=50, t=80, b=50),
        plot_bgcolor="#ffffff",
    )

    fig.update_traces(
        marker=dict(
            line=dict(color='#000000', width=2)
        )
    )

    return fig

data = load_data()

# st.set_page_config(
#     page_title="F1 Championship Analysis",
#     page_icon=":bar_chart:",
#     layout="wide"
# )


# # Filter by name
# names = data.name.unique().tolist()
# selected_name = st.sidebar.selectbox("Select a name", names)
# filtered_data = data[data.name == selected_name]

# # Filter by minimum races
# min_races = st.sidebar.slider("Minimum number of races", min_value=1, max_value=filtered_data.races.max(), value=100)
# # filtered_data = filtered_data[filtered_data.races >= min_races]
# filtered_data = filtered_data[filtered_data['raceId'].nunique() >= min_races]

st.subheader("Constructor's Points per Race")
st.plotly_chart(plot_data(data))
