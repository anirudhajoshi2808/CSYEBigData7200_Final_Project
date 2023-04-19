import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objs as go
import glob

def prediction():

    st.title("F1 Championship Prediction")
    st.title("Driver Position Prediction")
    hungarian_drivers_path = glob.glob("../prediction/ML/DriverPred/HungarianDriver/*.csv")
    hungarian_drivers = pd.read_csv(hungarian_drivers_path[0])
    british_drivers_path = glob.glob("../prediction/ML/DriverPred/BritishDriver/*.csv")
    british_drivers = pd.read_csv(british_drivers_path[0])
    hungarian_team_path = glob.glob("../prediction/ML/TeamPred/HungarianTeam/*.csv")
    hungarian_team = pd.read_csv(hungarian_team_path[0])
    british_team_path = glob.glob("../prediction/ML/TeamPred/BritishTeam/*.csv")
    british_team = pd.read_csv(british_team_path[0])

    def load_hungarian_driver():
        hungarian_drivers_final = hungarian_drivers.loc[:, ['surname', 'prediction_driver']].rename(columns={'surname': 'Driver Name', 'prediction_driver': 'Predicted Position'})
        
        return hungarian_drivers_final
    hungarian_drivers_final = load_hungarian_driver()

    def plot_hungarian_driver(hungarian_drivers_final):
        hungarian_drivers_final = hungarian_drivers_final.sort_values('Predicted Position', ascending=False)
    
        # Create the plot using plotly express
        fig = px.bar(
            x=hungarian_drivers_final['Predicted Position'], 
            y=hungarian_drivers_final['Driver Name'],
            color_discrete_sequence=['red'],
            orientation='h',
            # width=hungarian_drivers_final['bar_widths']
        )
        fig.update_layout(
            title="Hungarian Driver Position Prediction",
            xaxis=dict(title='Predicted Position', showgrid=False,
                tickmode='linear',
                tick0=0,
                dtick=1
            ),
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
    
    fig = plot_hungarian_driver(hungarian_drivers_final)

    def load_british_driver():
        british_drivers_final = british_drivers.loc[:, ['surname', 'prediction_driver']].rename(columns={'surname': 'Driver Name', 'prediction_driver': 'Predicted Position'})
        
        return british_drivers_final
    british_drivers_final = load_british_driver()

    def plot_british_driver(british_drivers_final):
        british_drivers_final = british_drivers_final.sort_values('Predicted Position', ascending=False)
    
        # Create the plot using plotly express
        fig1 = px.bar(
            x=british_drivers_final['Predicted Position'], 
            y=british_drivers_final['Driver Name'],
            color_discrete_sequence=['red'],
            orientation='h',
            # width=hungarian_drivers_final['bar_widths']
        )
        fig1.update_layout(
            title="British Driver Position Prediction",
            xaxis=dict(title='Predicted Position', showgrid=False,
                tickmode='linear',
                tick0=0,
                dtick=1
            ),
            yaxis=dict(title='Driver', showgrid=False),
            font=dict(size=20),
            bargap=0.2,
            bargroupgap=0.1,
            margin=dict(l=50, r=50, t=80, b=50),
            plot_bgcolor="#000000",
            
        )
        fig1.update_traces(
            marker=dict(
                line=dict(color='#000000', width=2)
            )
        )

        return fig1
    
    
    fig1 = plot_british_driver(british_drivers_final)


    left_column, right_column = st.columns(2)
    st.title("Team Position Prediction")
    left_column.plotly_chart(fig, use_container_width=True)
    left_column.write("This bar graph represents the Predicted Position of Driver for Hungarian Grand Prix", use_container_width=True)
    right_column.plotly_chart(fig1, use_container_width=True)
    right_column.write("This bar graph represents the Predicted Position of Driver for Britian Grand Prix", use_container_width=True)
    
    def load_hungarian_team():
        hungarian_team_final = hungarian_team.loc[:, ['name', 'prediction_team']].rename(columns={'name': 'Team Name', 'prediction_team': 'Predicted Position'})
        
        return hungarian_team_final
    hungarian_team_final = load_hungarian_team()

    def plot_hungarian_team(hungarian_team_final):
        hungarian_team_final = hungarian_team_final.sort_values('Predicted Position', ascending=False)
    
        # Create the plot using plotly express
        fig2 = px.bar(
            x=hungarian_team_final['Predicted Position'], 
            y=hungarian_team_final['Team Name'],
            color_discrete_sequence=['red'],
            orientation='h',
            # width=hungarian_drivers_final['bar_widths']
        )
        fig2.update_layout(
            title="Hungarian Team Position Prediction",
            xaxis=dict(title='Predicted Position', showgrid=False,
                tickmode='linear',
                tick0=0,
                dtick=1
            ),
            yaxis=dict(title='Team', showgrid=False),
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
    
    fig2 = plot_hungarian_team(hungarian_team_final)

    def load_british_team():
        british_team_final = british_team.loc[:, ['name', 'prediction_team']].rename(columns={'name': 'Team Name', 'prediction_team': 'Predicted Position'})
        
        return british_team_final
    british_team_final = load_british_team()

    def plot_british_team(british_team_final):
        british_team_final = british_team_final.sort_values('Predicted Position', ascending=False)
    
        # Create the plot using plotly express
        fig3 = px.bar(
            x=british_team_final['Predicted Position'], 
            y=british_team_final['Team Name'],
            color_discrete_sequence=['red'],
            orientation='h',
            # width=hungarian_drivers_final['bar_widths']
        )
        fig3.update_layout(
            title="British Team Position Prediction",
            xaxis=dict(title='Predicted Position', showgrid=False,
                tickmode='linear',
                tick0=0,
                dtick=1
            ),
            yaxis=dict(title='Team', showgrid=False),
            font=dict(size=20),
            bargap=0.2,
            bargroupgap=0.1,
            margin=dict(l=50, r=50, t=80, b=50),
            plot_bgcolor="#000000",
            
        )
        fig3.update_traces(
            marker=dict(
                line=dict(color='#000000', width=2)
            )
        )

        return fig3
    
    fig3 = plot_british_team(british_team_final)

    left_column, right_column = st.columns(2)

    left_column.plotly_chart(fig2, use_container_width=True)
    left_column.write("This bar graph represents the Predicted Position of Team for Hungarian Grand Prix", use_container_width=True)
    right_column.plotly_chart(fig3, use_container_width=True)
    right_column.write("This bar graph represents the Predicted Position of Team for Britian Grand Prix", use_container_width=True)