import pandas as pd
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import sum, col
import altair as alt
import streamlit as st
from snowflake.snowpark import Session
from pathlib import Path
import os
data_dir = os.getenv("data_dir")
data_dir = Path(f"{data_dir}/portfolio-monitoring")
opps_data_dir = Path('~/nirvanatech/manthan/data/portfolio-monitoring')
st.set_page_config(layout="wide")



@st.cache_data()
def load_data():
    df = pd.read_pickle(opps_data_dir / 'opps_funnel.pkl')
    return df


# Load and cache data



def answer1():
    st.subheader('Monthly Bound Opportunities')

    st.markdown("___")

    # Display an interactive chart to visualize CO2 emissions over time by the selected countries

    opps = load_data()
    opps['EFFECTIVE_DATE'] = pd.to_datetime(opps['EFFECTIVE_DATE'])
    opps['month_year'] = opps['EFFECTIVE_DATE'].dt.strftime('%Y-%m')
    oppsg = opps.groupby(opps['month_year']).agg({'IS_BOUND': 'sum', 'IS_QUOTED': 'sum'
                                                         , 'IS_SUB': 'sum', 'IS_REVIEWED': 'sum'
                                                         }).convert_dtypes()
    oppsg.reset_index(inplace=True)

    st.line_chart(oppsg,
                  x='month_year', y= ['IS_BOUND', 'IS_QUOTED', 'IS_SUB', 'IS_REVIEWED'], color='IS_BOUND',
                  use_container_width=True)

    # --
    # line_chart = alt.Chart(oppsg).mark_line().encode(x='month_year', y='IS_BOUND', color='IS_BOUND')
    # st.altair_chart(line_chart, use_container_width=True)


# Display header
st.header("Drop-off Funnel: Dot Opportunities")

# Create sidebar and load the first page
page_names_to_funcs = {
    "Monthly Bound Opportunities": answer1,
        }
selected_page = st.sidebar.selectbox("Select", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
