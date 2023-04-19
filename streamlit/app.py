import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image
from team import team as team_show
from driver import driver as driver_show
from circuit import circuit as circuit_show
from prediction import prediction as prediction_show
# from page3 import show as page3_show
st.set_page_config(
            page_title="F1 Championship Analytics",
            page_icon=":racing_car:",
            layout="wide"
        )

def home_show():
    
    st.markdown(
        """
        <style>
        .container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.write('<div class="container">', unsafe_allow_html=True)
    st.title("F1 Championship Analytics")
    image = Image.open('resources/f1.png')

    # Resize the image to a new width and height
    new_size = (800, 400)
    resized_image = image.resize(new_size)
    st.image(resized_image)
    st.write('</div>', unsafe_allow_html=True)
    st.write("Formula One F1 is one of the most popular sports in the world It is the highest class of international racing for singleseater formula racing cars Formula One is sanctioned by the Fdration Internationale de lAutomobile FIA which was established on 20 June 1904 Formula One was inaugurated on 13 May 1950 as the World Drivers Championship at Silverstone in the United Kingdom In 1981 it became known as the FIA Formula One World Championship.\n\nSeveral races called Grand Prix are held all over the world over a season These races taken together are called a Formula One season The word Formula refers to a set of rules that all participating teams have to adhere to Grand Prix is a French word that translates as grand prize in English The races are run of tracks that are graded 1 by the FIA Hence the name Formula One was adopted.\n\nThe races take place on purposebuilt tracks certified by the FIA Most tracks are situated in remote locations well connected with cities There are a few races such as the British Grand Prix and the Singapore Grand Prix that are held on closed public roads Formula One is one of the premium forms of racing around the world and draws huge audiences.\n\n.A driver participating in a Formula One race should hold a valid Super Licence issued by the FIA The performance of the drivers and the constructors of the car are evaluated at the end of each race by a points system At the end of a season the FIA aggregates the points scored by each and awards two annual World Championships one each for the drivers and the constructors.\n\nFormula 1 has fans all over the world and has been multi billion dollar business The reason behind for us to pick this dataset is to bring some valuable insights from the dataset inorder to understand the performance of Formula 1 over the years and to extract key features")


PAGES = {
    "Home": home_show,
    "Team": team_show,
    "Driver": driver_show,
    "Circuits": circuit_show,
    "Prediction": prediction_show
}



# Create radio buttons to allow user to select page
page = st.sidebar.selectbox("Select a page", list(PAGES.keys()))

# Call the selected page function
PAGES[page]()

