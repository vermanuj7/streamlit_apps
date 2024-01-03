import pandas as pd
import streamlit as st
import s3fs
import awswrangler as wr
import boto3

boto_session = boto3.Session(aws_access_key_id=st.secrets['credentials']['aws']['AWS_ACCESS_KEY_ID'],
                             aws_secret_access_key=st.secrets['credentials']['aws']['AWS_SECRET_ACCESS_KEY'],
                             region_name=st.secrets['credentials']['aws']['AWS_REGION'])

st.set_page_config(layout="wide")


@st.cache_data
def load_data():
    df = wr.s3.read_parquet('s3://nirvana-analytics-warehouse/opps-funnel/opps_funnel.parquet',
                            boto3_session=boto_session)
    return df


st.subheader('Monthly Bound Opportunities')
st.markdown("___")

opps = load_data()
opps['EFFECTIVE_DATE'] = pd.to_datetime(opps['EFFECTIVE_DATE'])
opps['month_year'] = opps['EFFECTIVE_DATE'].dt.strftime('%Y-%m')
oppsg = opps.groupby(opps['month_year']).agg({
                                                    'IS_SUB': 'sum',
                                                    'IS_SUB_COMPLETED': 'sum',
                                                     'IS_REVIEWED': 'sum',
                                                    'IS_QUOTED': 'sum',
                                                     'IS_BOUND': 'sum',
                                                     }).convert_dtypes()

oppsg = oppsg.reset_index()

st.line_chart(oppsg, x='month_year', y=['IS_SUB', 'IS_SUB_COMPLETED', 'IS_REVIEWED', 'IS_QUOTED', 'IS_BOUND', ], color='IS_BOUND',
              use_container_width=True)
st.write(oppsg)
