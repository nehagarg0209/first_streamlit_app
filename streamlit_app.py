
import streamlit;
import pandas;
import requests;
import snowflake.connector;
from urllib.error import URLError

streamlit.title("My Mom's New Healthy Diner")
streamlit.header('Breakfast Menu')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥬 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard Boiled Free-range egg')
streamlit.text('🥑 Avacado Toast')
streamlit.header('🍌🥭 Build your own favourite fruit smoothie 🥝🍇 ')

my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt');
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)
 
  #======================= request api ================================ #
  
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice);
  # streamlit.text(fruityvice_response.json());
  # take the json version of response and normalize it 
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
     
streamlit.header("Fruityvice Fruit Advice!")

try:
 fruit_choice = streamlit.text_input('What fruit would you like information about?')
 #streamlit.write('The user entered ', fruit_choice)
 if not fruit_choice:
   streamlit.error("Please get a fruit to get infromation")
 else:
   back_from_function = get_fruityvice_data(fruit_choice)
   # output it in screen as the table
   streamlit.dataframe(back_from_function)
   
except URLError as e:
  streamlit.error()
# stop streamlit
#streamlit.stop();


#---------------- snowflake connection ------------
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)

streamlit.header("The fruit load list contains:")
#Snowflake related funcitons
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
   my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST;")
   # my_data_row = my_cur.fetchone()
   return my_cur.fetchall()

streamlit.stop();

# Add a button to load a fruit
if streamlit.button('Get Fruit Load List'):
 my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
 my_data_rows = get_fruit_load_list() 
 streamlit.dataframe(my_data_rows)

 #Allow user to add new fruit
def insert_row_snowflake(new_fruit):
 with my_cnx.cursor() as my_cur:
  my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES ('FROM STREAMLIT')")
  return "Thanks for adding " + new_fruit
  
add_my_fruit = streamlit.text_input('What fruit would you like to add ?')
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit) 
  streamlit.text(back_from_function)

# streamlit.stop();

