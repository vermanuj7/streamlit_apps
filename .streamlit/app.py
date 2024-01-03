import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="⌲",
)

st.header("Opportunities Funnel Analysis! 📈")

st.sidebar.success("Choose analysis from the sidebar")

st.markdown("--")
st.markdown(
    """
    This app is built for the purpose of analyzing the opportunities funnel where
    each opportunity is represented by a dot-application that is at least 30 days later than the previous dot-application 
    of the same dot. 
    """
)
