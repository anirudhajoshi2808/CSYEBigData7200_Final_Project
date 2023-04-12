import pandas as pd
import plotly.express as px
import streamlit as st

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

    def plot_top10_drivers(top_ten):
        
        fig = px.bar(x=top_ten['Driver_Name'], y=top_ten['Number_of_wins'])

        fig.update_layout(
            title="Driver Wins",
            xaxis=dict(title='Name', showgrid=False),
            yaxis=dict(title='Number of Wins', showgrid=False),
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
    
    fig = plot_top10_drivers(top_ten)

    st.plotly_chart(fig)

    def load_top10_drivers_as_per_races():
        top_ten = pd.merge(results, drivers, on="driverId")
        top_ten = pd.merge(races, top_ten, on="raceId")
        top_ten = top_ten[top_ten["position"] == '1']
        top_ten["Driver_Name"] = top_ten["forename"] + " " + top_ten["surname"]
        top_ten = top_ten.groupby(["driverId", "Driver_Name"]).size().reset_index(name="Number_of_wins")
        top_ten = top_ten.sort_values(by="Number_of_wins", ascending=False).head(10)
        no_of_races = pd.merge(results, drivers, on="driverId")
        no_of_races = no_of_races.groupby("driverId").size().reset_index(name="Number_of_races")
        top_ten_drivers_races = pd.merge(top_ten, no_of_races, on="driverId")
        return top_ten_drivers_races
    top_ten_drivers_races = load_top10_drivers_as_per_races()

    def plot_top10_drivers_as_per_races(top_ten_drivers_races):
        
        

        top_ten_drivers_races = top_ten_drivers_races[['Driver_Name', 'Number_of_wins', 'Number_of_races']]
        pivot_top_ten = pd.melt(top_ten_drivers_races, id_vars=['Driver_Name'], value_vars=['Number_of_wins', 'Number_of_races'], var_name='name', value_name='value')
        lable = [103,310,32,358,53,300,91,308,31,192,41,162,51,202,25,174,27,100,35,163]
        pivot_top_ten['lable'] = lable

        fig2 = px.bar(pivot_top_ten.sort_values('value', ascending=False), 
                    x='value', y='Driver_Name', color='name',
                    color_discrete_map={'Number_of_wins':'#FC5353', 'Number_of_races':'#A90505'},
                    text='lable', orientation='h')
        fig2.update_layout(
            title="Top 10 Drivers Wins Vs Races",
            font=dict(size=20),
            margin=dict(l=100, r=100, t=80, b=50),
            plot_bgcolor="#ffffff",
            xaxis=dict(title='Number of Wins/Races', showgrid=False),
            yaxis=dict(title='Drivers', showgrid=False)
        )
        fig2.update_traces(textposition='inside')


        return fig2
    
    

    fig2 = plot_top10_drivers_as_per_races(top_ten_drivers_races)

    st.plotly_chart(fig2)

