import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objs as go

def driver():
    # st.set_page_config(
    #     page_title="F1 Championship Driver Analysis",
    #     page_icon=":bar_chart:",
    #     layout="wide"
    # )

    st.title("F1 Championship Driver Analysis")

    drivers = pd.read_csv("../data/drivers.csv")
    results = pd.read_csv("../data/results.csv")
    races = pd.read_csv("../data/races.csv")
    driver_standings = pd.read_csv('../data/driver_standings.csv')

    @st.cache_data

    def load_top10_drivers():
        top_ten = pd.merge(results, drivers, on="driverId")
        top_ten = pd.merge(races, top_ten, on="raceId")
        top_ten = top_ten[top_ten["position"] == '1']
        top_ten["Driver_Name"] = top_ten["forename"] + " " + top_ten["surname"]
        top_ten = top_ten.groupby(["driverId", "Driver_Name"]).size().reset_index(name="Number_of_wins")
        top_ten = top_ten.sort_values(by="Number_of_wins", ascending=False).head(10)
        return top_ten
    top_ten = load_top10_drivers()

    min_value = 0
    max_value = 100
    step = 5
    default_value = 0
    min_no_of_wins = st.sidebar.slider('Driver with Minimum Number of Wins', min_value=min_value, max_value=max_value, step=step, value=default_value)


    def plot_top10_drivers(top_ten, min_no_of_wins):

        filtered_data = top_ten[top_ten['Number_of_wins'] >= min_no_of_wins]
        
        # fig = px.bar(x=top_ten['Driver_Name'], y=top_ten['Number_of_wins'])
        fig = px.bar(
                    x=filtered_data['Number_of_wins'], y=filtered_data['Driver_Name'],
                    color_discrete_sequence=['red'],
                    orientation='h')
        fig.update_layout(
            title="Driver Wins",
            xaxis=dict(title='Number of Wins', showgrid=False),
            yaxis=dict(title='Driver', showgrid=False),
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
    
    fig = plot_top10_drivers(top_ten, min_no_of_wins)



    # st.plotly_chart(fig)

    def load_national_champions():
        
        driver_nationality = drivers.groupby('nationality')['nationality'].count().sort_values(ascending = False).reset_index(name = 'number of drivers')
        driver_position = drivers.merge(driver_standings,left_on='driverId',right_on='driverId',how = 'left')
        driver_position = driver_position.merge(races,on = 'raceId',how = 'left')

        champion_drivers = driver_position.groupby(['nationality','year','surname'])[['points','wins']
                                            ].max().sort_values('points',ascending = False).reset_index()
        champion_drivers.drop_duplicates(subset=['year'], inplace=True)

        #grouping by nationality and counting the surname of drivers 

        final = champion_drivers.groupby('nationality')['surname'].nunique().reset_index(name = 'champions').sort_values(
            by='champions',ascending = False)

        #merging both the datasets and creating a column to calculate the ratio

        ratios = final.merge(driver_nationality,on='nationality',how='inner')
        ratios['perc_winners'] = (ratios.champions/ratios['number of drivers']*100).round(2)
        ratios = ratios.sort_values('perc_winners',ascending = False)
        return ratios

    ratios = load_national_champions()

    min_value = 0
    max_value = 30
    step = 5
    default_value = 0
    min_no_of_wins_nation = st.sidebar.slider('Nation with Minimum Number of Wins', min_value=min_value, max_value=max_value, step=step, value=default_value)


    def plot_national_champions(ratios):
        filtered_data = ratios[ratios['perc_winners'] >= min_no_of_wins_nation]

        fig2 = px.bar(
        filtered_data, x='perc_winners', y='nationality',
        color_discrete_sequence=['red'],
        orientation='h'
        )
        fig2.update_layout(
            title="Ratio of Drivers Winning Championships by Nationality",
            xaxis=dict(title='Percentage of Winners', showgrid=False),
            yaxis=dict(title='Nationality', showgrid=False),
            font=dict(size=20),
            bargap=0.2,
            bargroupgap=0.1,
            margin=dict(l=50, r=50, t=80, b=50),
            plot_bgcolor="#000000",
        )

        fig2.update_traces(
            marker=dict(
                line=dict(color='#000000', width=2)
            )
        )

    
        return fig2

    fig2 = plot_national_champions(ratios)

    def load_nationality():
        drivers_nationality = drivers.groupby('nationality') \
                        .size() \
                        .reset_index(name='Number_of_drivers') \
                        .sort_values('Number_of_drivers', ascending=False) \
                        .reset_index(drop=True)
        drivers_nationality = drivers_nationality.head(10)
        return drivers_nationality
    
    drivers_nationality = load_nationality()

# select top 10 nationalities with highest number of drivers

    def plot_nationality(drivers_nationality):
        colors = ["#4D0202", "#7C0B0B", "#920505", "#A70808","#BD0E0E","#C20808", 
          "#EC4848","#FA6363","#FB7676","#FF8A8A"]

        # create donut chart using plotly express
        fig3 = px.pie(drivers_nationality, values='Number_of_drivers', names='nationality',
                    color_discrete_sequence=colors, hole=0.6)

        # set chart layout
        fig3.update_layout(title='Historical Driver Nationality Distribution since 1950',
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))

        return fig3

    # st.plotly_chart(fig2)
    fig3 = plot_nationality(drivers_nationality)

    def load_most_wins():
        driver_position = pd.merge(drivers, driver_standings, on='driverId')
        driver_position = pd.merge(driver_position, races, on='raceId')

        # select data for drivers who finished in position 1, group by driver surname and year, and count number of wins
        positions = driver_position[driver_position['position'] == 1] \
            .groupby(['surname', 'year']) \
            .agg(Number_of_wins=('wins', 'max')) \
            .reset_index() \
            .sort_values('Number_of_wins', ascending=False) \
            .reset_index(drop=True)

        # select top 20 drivers with highest number of wins
        positions = positions.head(20)

        positions = positions.rename(columns={'surname': 'Name'})

        return positions
    
    positions = load_most_wins()

    def plot_most_wins(positions, driver_name=None):
        # colors = px.colors.qualitative.Pastel
        # positions['Name'] = pd.Categorical(positions['Name'], categories=positions['Name'].unique())

        # fig4 = px.scatter(positions, x='year', y='Number_of_wins', color='Name', size='Number_of_wins',
        #                 hover_data=['Name', 'Number_of_wins', 'year'],
        #                 color_discrete_sequence=colors,
        #                 title='Most wins by a driver in a single season')

        # fig4.update_layout(xaxis=dict(title='Year', showgrid=False), yaxis=dict(title='Number of Wins', showgrid=False))

        
        # return fig4

        colors = px.colors.qualitative.Pastel
    
        if driver_name is not None:
            filtered_data = positions[positions['Name'] == driver_name]
            filtered_data['Name'] = pd.Categorical(filtered_data['Name'], categories=filtered_data['Name'].unique())

            fig4 = px.scatter(filtered_data, x='year', y='Number_of_wins', color='Name', size='Number_of_wins',
                            hover_data=['Name', 'Number_of_wins', 'year'],
                            color_discrete_sequence=colors,
                            title=f"Most wins by {driver_name} in a single season")
        else:
            positions['Name'] = pd.Categorical(positions['Name'], categories=positions['Name'].unique())
            fig4 = px.scatter(positions, x='year', y='Number_of_wins', color='Name', size='Number_of_wins',
                            hover_data=['Name', 'Number_of_wins', 'year'],
                            color_discrete_sequence=colors,
                            title='Most wins by a driver in a single season')

        fig4.update_layout(xaxis=dict(title='Year', showgrid=False), yaxis=dict(title='Number of Wins', showgrid=False))

        return fig4

    driver_names = positions['Name'].unique()
    selected_driver = st.sidebar.selectbox('Select a driver to get the most wins in a season', ['All Drivers'] + list(driver_names))

    if selected_driver == 'All Drivers':
        fig4 = plot_most_wins(positions)
    else:
        fig4 = plot_most_wins(positions, selected_driver)



    left_column, right_column = st.columns(2)

    left_column.plotly_chart(fig, use_container_width=True)
    right_column.plotly_chart(fig2, use_container_width=True)

    left_column2, right_column2 = st.columns(2)
    left_column2.plotly_chart(fig3, use_container_width=True)
    right_column2.plotly_chart(fig4, use_container_width=True)


    # st.plotly_chart(fig3)
