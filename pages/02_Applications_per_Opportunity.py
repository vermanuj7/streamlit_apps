# from snowflake.snowpark.context import get_active_session
# from snowflake.snowpark.functions import sum, col
# import altair as alt
# from snowflake.snowpark import Session
# from pathlib import Path
# import os
import pandas as pd
import streamlit as st
import s3fs
import awswrangler as wr
import boto3

boto_session = boto3.Session(aws_access_key_id=st.secrets['credentials']['aws']['AWS_ACCESS_KEY_ID'],
                             aws_secret_access_key=st.secrets['credentials']['aws']['AWS_SECRET_ACCESS_KEY'],
                             region_name=st.secrets['credentials']['aws']['AWS_REGION'])
st.set_page_config(layout="wide")


@st.cache_data()
def load_data():
    # df = pd.read_pickle(opps_data_dir / 'opps_funnel.pkl')
    df = wr.s3.read_parquet('s3://nirvana-analytics-warehouse/opps-funnel/opps_funnel.parquet',
                            boto3_session=boto_session)
    # df = pd.read_parquet(s3.open('s3://nirvana-analytics-warehouse/opps-monitoring/opps_funnel.parquet'))
    return df


# Load and cache data


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
