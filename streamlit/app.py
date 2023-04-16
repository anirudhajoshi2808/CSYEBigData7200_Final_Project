import pandas as pd
import plotly.express as px
import streamlit as st
from team import team as team_show
from driver import driver as driver_show
from circuit import circuit as circuit_show
# from page3 import show as page3_show
st. set_page_config(layout="wide")

def home_show():
    # st.set_page_config(
    #         page_title="F1 Championship Analytics",
    #         page_icon=":bar_chart:",
    #         layout="wide"
    #     )
    st.title("F1 Championship Analytics")



PAGES = {
    "Home": home_show,
    "Team": team_show,
    "Driver": driver_show,
    "Circuits": circuit_show
}

# Create radio buttons to allow user to select page
page = st.sidebar.selectbox("Select a page", list(PAGES.keys()))

# Call the selected page function
PAGES[page]()
# st.plotly_chart(fig)

# st.plotly_chart(fig1)



# st.subheader("Constructor's Points per Race")
# st.plotly_chart(plot_data(data))
