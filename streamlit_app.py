# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


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


session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list = st.multiselect('Choose upto 5 ingredients:',
                                my_dataframe,
                                max_selections=5)
if ingredient_list:
    # st.write(ingredient_list)
    # st.text(ingredient_list)

    ingredient_str = ''
    for fruit_choosen in ingredient_list:
        ingredient_str += fruit_choosen + ' '
    st.write(ingredient_str)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredient_str + """','""" + name_on_order + """')"""

    time_to_submit = st.button('Submit Order')
    st.write(my_insert_stmt)
    if time_to_submit:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
