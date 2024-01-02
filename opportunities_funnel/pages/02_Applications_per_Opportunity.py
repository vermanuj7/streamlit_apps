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


tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
data = load_data()

tab1.subheader("Average Applications per Opportunity")
dg = data.groupby(data['DOT']).agg({'EFFECTIVE_DATE': 'count', 'APP_COUNT': 'sum'}).reset_index()
dg['apps_per_op'] = dg['APP_COUNT'] / dg['EFFECTIVE_DATE']
dg['apps_per_op_bkt'] = pd.cut(dg['apps_per_op'], bins=[0, 1, 2, 3, 4, 5], right=False)
dg.head()
dg = dg.groupby('apps_per_op_bkt').agg({'DOT': 'count'}).reset_index()
dg['apps_per_op_bkt'] = dg['apps_per_op_bkt'].astype(str)
tab1.bar_chart(dg, x='apps_per_op_bkt', y='DOT', use_container_width=True)

tab2.subheader("A tab with the data")
tab2.write(dg)

with st.expander("See explanation"):
    st.write("""
    The chart above shows how the number of applications per opportunity is distributed.
    """)
