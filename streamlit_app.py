# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

#option = st.selectbox('What is your favourite fruit?',
#                     ('Banana','Strawberries','Peaches'))

#st.write('Your favorite fruit is:', option)

# Get the current credentials
#session = get_active_session()

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie:', name_on_order)

cnx = st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredient_list = st.multiselect('Choose upto 5 ingredients:',
                                my_dataframe,
                                max_selections=5)
if ingredient_list:
    # st.write(ingredient_list)
    # st.text(ingredient_list)

    ingredient_str = ''
    for fruit_choosen in ingredient_list:
        ingredient_str += fruit_choosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_choosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_choosen,' is ', search_on, '.')
      
        st.subheader(fruit_choosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ fruit_choosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    st.write(ingredient_str)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredient_str + """','""" + name_on_order + """')"""

    time_to_submit = st.button('Submit Order')
    st.write(my_insert_stmt)
    if time_to_submit:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")



