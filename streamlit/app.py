import pandas as pd
import plotly.express as px
import streamlit as st
from team import team as team_show
from driver import driver as driver_show
# from page3 import show as page3_show

st.set_page_config(
        page_title="F1 Championship Analytics",
        page_icon=":bar_chart:",
        layout="wide"
    )
st.title("F1 Championship Analytics")

# def home():
#     st.set_page_config(
#         page_title="F1 Championship Team Analysis",
#         page_icon=":bar_chart:",
#         layout="wide"
#     )

#     st.title("F1 Championship Team Analysis")

#     # @st.cache_data

#     circuits = pd.read_csv('../data/circuits.csv')
#     laptimes = pd.read_csv('../data/lap_times.csv')
#     pitstops = pd.read_csv('../data/pit_stops.csv')
#     seasons = pd.read_csv('../data/seasons.csv',parse_dates=['year'])
#     status = pd.read_csv('../data/status.csv')

#     constructor_standings = pd.read_csv('../data/constructor_standings.csv')
#     constructors = pd.read_csv('../data/constructors.csv')
#     driver_standings = pd.read_csv('../data/driver_standings.csv')
#     drivers = pd.read_csv('../data/drivers.csv')

#     races = pd.read_csv('../data/races.csv',parse_dates=['year'])
#     constructor_results = pd.read_csv('../data/constructor_results.csv')
#     results = pd.read_csv('../data/results.csv')
#     qualifying = pd.read_csv('../data/qualifying.csv')

#     @st.cache_data

#     def load_data():

#         team = constructors.merge(results,on='constructorId',how = 'left')

#         best = team[['name','points','raceId']]
#         best = best.groupby('name')['raceId'].nunique().sort_values(ascending=False).reset_index(name = 'races')
#         best = best[best['races'] >= 100]

#         func = lambda x: x.points.sum()/x.raceId.nunique()
#         data = team[team['name'].isin(best.name)].groupby('name').apply(func).sort_values(ascending=False).reset_index(name = 'points_per_race')

#         return data

#     data = load_data()

#     def load_team():
#         team = constructors.merge(results,on='constructorId',how = 'left')

#         return team

#     team = load_team()

#     def plot_data_constructor(data, min_points_per_race):
#         filtered_data = data[data['points_per_race'] >= min_points_per_race]

#         fig = px.bar(x=filtered_data['name'], y=filtered_data['points_per_race'])

#         fig.update_layout(
#             title="Team's Points per Race",
#             xaxis=dict(title='Team', showgrid=False),
#             yaxis=dict(title='Points Per Race', showgrid=False),
#             font=dict(size=20),
#             bargap=0.2,
#             bargroupgap=0.1,
#             margin=dict(l=50, r=50, t=80, b=50),
#             plot_bgcolor="#ffffff",
#         )

#         fig.update_traces(
#             marker=dict(
#                 line=dict(color='#000000', width=2)
#             )
#         )

#         return fig



#     historic_points = team.groupby('name').agg({'points':'sum'}).sort_values('points',ascending=False).reset_index().head(10)
#     # historic_points

#     def plot_data_historic(historic_points, min_points_overall):
#         filtered_data = historic_points[historic_points['points'] >= min_points_overall]

#         fig = px.bar(x=filtered_data['name'], y=filtered_data['points'])


#         fig.update_layout(
#             xaxis=dict(title='Team', showgrid=False),
#             yaxis=dict(title='Historical Total Points', showgrid=False),
#             title_text="Team's Historic Points"
#         )

#         fig.update_traces(
#             textfont_size=20,
#             marker=dict(line=dict(color='#000000', width=2))
#         )

#         return fig


#     min_value = 0
#     max_value = int(data['points_per_race'].max())
#     step = 1
#     default_value = 0
#     min_points_per_race = st.sidebar.slider('Team minimum points per race', min_value=min_value, max_value=max_value, step=step, value=default_value)

#     min_value = 0
#     max_value = int(historic_points['points'].max())
#     step = 1
#     default_value = 0
#     min_points_overall = st.sidebar.slider('Team minimum points till now', min_value=min_value, max_value=max_value, step=step, value=default_value)


#     fig = plot_data_constructor(data, min_points_per_race)

#     fig1 = plot_data_historic(historic_points, min_points_overall)

#     left_column, right_column = st.columns(2)

#     left_column.plotly_chart(fig, use_container_width=True)
#     right_column.plotly_chart(fig1, use_container_width=True)

# def about():
#     st.set_page_config(
#         page_title="F1 Championship Driver Analysis",
#         page_icon=":bar_chart:",
#         layout="wide"
#     )

#     st.title("F1 Championship Driver Analysis")



# Define the multi-app
# sm.multi_app({
#     "Home": home,
#     "About": about
# })

PAGES = {
    "Team": team_show,
    "Driver": driver_show
}

# Create radio buttons to allow user to select page
page = st.sidebar.selectbox("Select a page", list(PAGES.keys()))

# Call the selected page function
PAGES[page]()
# st.plotly_chart(fig)

# st.plotly_chart(fig1)



# st.subheader("Constructor's Points per Race")
# st.plotly_chart(plot_data(data))
