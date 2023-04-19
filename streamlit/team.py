import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import packcircles 

def team():
    # st.set_page_config(
    #     page_title="F1 Championship Team Analysis",
    #     page_icon=":bar_chart:",
    #     layout="wide"
    # )

    st.title("F1 Championship Team Analysis")
    st.write("In Formula 1, teams are the businesses, organizations, or producers in charge of designing and building the racing vehicles. Two racing drivers and a racing team from each constructor participate in each Grand Prix for World Championship points. A crucial component of the sport is the Formula 1 constructors. Without the constructor’s championship, no team would strive as hard for success as they do because the constructors are the teams that support the vehicles and the drivers.")
    # @st.cache_data

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

    @st.cache_data

    def load_data():

        team = constructors.merge(results,on='constructorId',how = 'left')

        best = team[['name','points','raceId']]
        best = best.groupby('name')['raceId'].nunique().sort_values(ascending=False).reset_index(name = 'races')
        best = best[best['races'] >= 100]

        func = lambda x: x.points.sum()/x.raceId.nunique()
        data = team[team['name'].isin(best.name)].groupby('name').apply(func).sort_values(ascending=False).reset_index(name = 'points_per_race')

        return data

    data = load_data()

    min_value = 0
    max_value = int(data['points_per_race'].max())
    step = 5
    default_value = 0
    min_points_per_race = st.sidebar.slider('Team minimum points per race', min_value=min_value, max_value=max_value, step=step, value=default_value)


    def load_team():
        team = constructors.merge(results,on='constructorId',how = 'left')

        return team

    team = load_team()

    

    def plot_data_constructor(data, min_points_per_race):
        filtered_data = data[data['points_per_race'] >= min_points_per_race]

        fig = px.bar(x=filtered_data['name'], y=filtered_data['points_per_race'], color_discrete_sequence=['red'])

        fig.update_layout(
            title="Team's Points per Race",
            xaxis=dict(title='Team', showgrid=False),
            yaxis=dict(title='Points Per Race', showgrid=False),
            font=dict(size=20),
            bargap=0.2,
            bargroupgap=0.1,
            margin=dict(l=50, r=50, t=80, b=50),
            plot_bgcolor="#000000",
        )

        fig.update_traces(
            marker=dict(
                line=dict(color='#000000', width=2)
            )
        )

        return fig

    fig = plot_data_constructor(data, min_points_per_race)

    historic_points = team.groupby('name').agg({'points':'sum'}).sort_values('points',ascending=False).reset_index().head(10)
    # historic_points

    def plot_data_historic(historic_points, min_points_overall):
        filtered_data = historic_points[historic_points['points'] >= min_points_overall]

        fig = px.bar(x=filtered_data['name'], y=filtered_data['points'], color_discrete_sequence=['red'])


        fig.update_layout(
            xaxis=dict(title='Team', showgrid=False),
            yaxis=dict(title='Historical Total Points', showgrid=False),
            title_text="Team's Historic Points"
        )

        fig.update_traces(
            textfont_size=20,
            marker=dict(line=dict(color='#000000', width=2))
        )

        return fig


    
    min_value = 0
    max_value = 10000
    step = 500
    default_value = 0
    min_points_overall = st.sidebar.slider('Team minimum points till now', min_value=min_value, max_value=max_value, step=step, value=default_value)


    

    fig1 = plot_data_historic(historic_points, min_points_overall)


    def load_comparison():
        # merging dataframes
        c_pt = pd.merge(constructors, constructor_results, on="constructorId")
        c_pt = pd.merge(races, c_pt, on="raceId")

        # calculating points per year sum
        c_pt = c_pt.groupby(['year', 'constructorId', 'name_y']).agg({'points': 'sum'}).reset_index()
        c_pt = c_pt.sort_values(by='points', ascending=False)

        # filtering top 4 teams
        c_pt = c_pt[c_pt['name_y'].isin(['Red Bull', 'Mercedes', 'McLaren', 'Ferrari'])]
        c_pt = c_pt[(c_pt['year'] >= '2010') & (c_pt['year'] <= '2021')]

        # renaming column
        c_pt = c_pt.rename(columns={'name_y': 'Team'})

        return c_pt
    
    c_pt = load_comparison()

    def plot_comparison(c_pt):
        fig2 = px.line(c_pt, x='points', y='year', color='Team', 
              facet_col='Team', facet_col_wrap=2,
              title='Points per Year Comparison for Top 4 Teams')

        fig2.update_layout(xaxis=dict(title='Years'),
                        yaxis=dict(title='Points per Year'),
                        legend_title='Team',
                        font=dict(size=12))

        return fig2
    
    fig2 = plot_comparison(c_pt)

    def load_team_wins():
        # merge datasets
        # Merge the results and constructors data
        p = pd.merge(results, constructors, on='constructorId', how='outer')

        # Select relevant columns and filter for first place finishes
        r = p.loc[p['position'] == '1', ['name', 'raceId', 'nationality','position']]

        # Convert position to numeric
        r['position'] = pd.to_numeric(r['position'])

        # Calculate number of first place finishes by nationality
        rsC = r.groupby('nationality').agg(first_places=('position', 'sum')) \
                .reset_index() \
                .sort_values('first_places', ascending=False)
        rsC['Percent_Of_Total'] = (rsC['first_places'] / rsC['first_places'].sum()) * 100

        # Add text column for hover information
        rsC['text'] = ("Nationality: " + rsC['nationality'] + "<br>" +
                    "Number of Wins: " + rsC['first_places'].astype(str) + "<br>" +
                    "Percentage of Total wins: " + rsC['Percent_Of_Total'].astype(str) + "%")


        return rsC

    rsC = load_team_wins()

    def plot_team_wins(rsC):
        # Generate circle packing layout
        # packing = px.pack(rsC, value='position', color='nationality')

       # layout
        fig3 = px.line(rsC, x='nationality', y='first_places', hover_name='nationality', 
              hover_data={'first_places': True, 'Percent_Of_Total': True, 'text': True},
              labels={'nationality': 'Nationality', 'first_places': 'Number of Wins'},
              title='Number of Wins by Constructor origin country')
        fig3.update_layout(xaxis_tickangle=-45)
        fig3.update_traces(marker=dict(color='red'))

        return fig3

    fig3 = plot_team_wins(rsC)

    left_column, right_column = st.columns(2)

    left_column.plotly_chart(fig, use_container_width=True)
    left_column.write("The bar graph shows top successful teams based on the total points earned.", use_container_width=True)
    right_column.plotly_chart(fig1, use_container_width=True)
    right_column.write("The bar graph shows top 10 successful teams based on the historical total points earned. Ferrari, Mercedes, Redbull, McLaren turn out to be the most successful teams with more than 5000 points.", use_container_width=True)

    left_column1, right_column1 = st.columns(2)

    left_column1.plotly_chart(fig2, use_container_width=True)
    left_column1.write("The graphic shows that Mercedes has regularly dominated the points, but in recent years, the other teams have begun to catch up and challenge them. It appears like Mercedes’ golden age is about to come to an end, or at the very least, they will have to battle hard to survive", use_container_width=True)
    right_column1.plotly_chart(fig3, use_container_width=True)
    right_column1.write("Bristish constructors has won more number of times (494 times) as compared to other nationalities. Constructors from Irish, Canadian and Japanese nationalities have won the lowest number of times", use_container_width=True)

