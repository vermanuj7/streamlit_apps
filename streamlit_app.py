'''
My First Streamlit App depoyed on cloud
'''
import streamlit
import pandas
import requests
import snowflake.connector

streamlit.header("Breakfast Menu")
streamlit.text("Omega 3 & Blueberry Oatmeal")
streamlit.text("Kale, Spinach & Rocket Smoothie")
streamlit.text("Hard-Boiled Free-Range Egg")
streamlit.header("Breakfast Favorites")
streamlit.text(" Omega 3 & Blueberry Oatmeal")
streamlit.text(" Kale, Spinach & Rocket Smoothie")
streamlit.text(" Hard-Boiled Free-Range Egg")
streamlit.text("0 Avocado Toast")

streamlit.header("&3 Build Your Own Fruit Smoothie")
my_fruit_list = pandas.read_csv(
    """https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt"""
)
my_fruit_list = my_fruit_list.set_index("Fruit")

fruits_selected = streamlit.multiselect(
    "Pick some fruits:", list(my_fruit_list.index), ["Avocado", "Strawberries"]
)
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)


streamlit.header("Fruityvice Fruit Advice!")

fruit_choice = streamlit.text_input("What fruit would you like information about?", 'Kiwi')
streamlit.write('The user entered', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# take the json response and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# output the normalized data
streamlit.dataframe(fruityvice_normalized)


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_data_rows = my_cur.fetchall()
my_cur.execute("select * from fruit_load_list")
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)