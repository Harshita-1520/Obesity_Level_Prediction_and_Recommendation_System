import streamlit as st
import joblib
import numpy as np
import base64
import pandas as pd
st.set_page_config(layout = 'wide',page_title="OBESITY LEVEL PREDICTION AND RECOMMENDATION SYSTEM", page_icon='🌟')
def set_bg_hack(main_bg):
    # set bg name
    main_bg_ext = "png"
    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-repeat: no-repeat;
             background-position: right 50% bottom 95% ;
             background-size: cover;
             background-attachment: scroll;
         }}
         </style>
         """,
        unsafe_allow_html=True,
    )

set_bg_hack('nude colour bg.png')
first_co, second_co,third_co,fourth_co,fifth_co = st.columns(5)
with third_co:
    st.image("logo.png", width = 100)
st.markdown("<h1><center>OBESITY LEVEL PREDICTION AND RECOMMENDATION SYSTEM</center></h1>",unsafe_allow_html=True)
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
with st.container(height = 880, border = True):
    # Centered heading
    st.markdown("<h1><center>Please fill your details</center></h1>",unsafe_allow_html=True)
    cont1, cont2 = st.columns(2)
    with cont1:
        with st.container(height = 750, border = True):
            st.markdown("<h1><center>Personal Details</center></h1>",unsafe_allow_html=True)
            Age = st.number_input("**Age**", min_value=10, max_value=90,value=30, step=1)
            Gender = st.selectbox('**Gender**',('Male', 'Female'))
            Height = st.number_input("**Enter Your Height in meters**", min_value=0.6, max_value=2.0, value=1.45,step = 0.01)
            Weight = st.number_input("**Enter Your Weight in kg**", min_value=25, max_value=200, value=80, step=1)
            bmi = Weight/(Height)**2
            BMI = st.number_input('**Body Mass Index(BMI)**',bmi,placeholder = 'Self calculated field')
            family_history_with_overweight = st.selectbox('**Does a history of overweight run in your family?**',('Yes', 'No'))
    
    with cont2:
        with st.container(height = 750, border = True):
            st.markdown("<h1><center>Daily Habits</center></h1>",unsafe_allow_html=True)
            NCP = st.selectbox('**No. of Meals per Day?**',(1,2,3,4))
            CAEC = st.selectbox('**What is your frequnecy of consuming food between meals?**',('Always','Frequently','Sometimes','No'))
            CH2O = st.slider('**What is your daily consumption of water in liters?**',min_value=1.0, max_value = 3.0)
            FCVC = st.slider("**What is your frequency of consuming vegetable?**",min_value=1.0, max_value = 3.0)
            FAF = st.slider("**What is your frequency of doing Physical Activity?**",min_value=1.0, max_value = 3.0)
            st.write("(less than 1 = Low, 1-2 = Moderate, 2-3 = High)")
            TUE = st.slider("**Time spent using technology devices(in hours)?**",min_value= 0.0, max_value = 2.0)

with st.container():
        # Centered "Get Quote" button
        ex_col_l, ex_2, button_col, ex_col_r = st.columns([0.7, 0.7, 1 ,1])
        y_pred = None

        with button_col:
            st.write('')
            
            if st.button('Know your Obesity Level'):
                temp_df = pd.DataFrame(data =[[Age,Gender,Height,Weight,BMI,
                                               family_history_with_overweight.lower(),
                                               NCP,CAEC,CH2O,FCVC,FAF,TUE]],
                                    columns=['Age', 'Gender', 'Height', 'Weight', 'BMI',       'family_history_with_overweight','NCP','CAEC','CH2O','FCVC','FAF','TUE'])
                model = joblib.load(open('obesity_level_predictor.joblib', 'rb'))
                y_pred = model.predict(temp_df)
                prob = round((model.predict_proba(temp_df).max())*100,2)
                target_order = ['Insufficient_Weight', 'Normal_Weight', 'Obesity_Type_I','Obesity_Type_II', 'Obesity_Type_III', 'Overweight_Level_I','Overweight_Level_II']
        if y_pred != None:
            with st.container(border = True):
                st.write(f"### Your Obesity Level is : **{target_order[(y_pred)[0]]}**")
                st.write(f'#### Result Accuracy: **{prob}%**')
                st.write('*the result accuracy refers to the surity of the model for obesity level')
rec = pd.read_excel('recommendation.xlsx')

with st.container():
    st.markdown("<h3><center>We have some Recommnedations for you</center></h3>",unsafe_allow_html=True)
    st.markdown("<h3><center>Click here to view them</center></h3>",unsafe_allow_html=True)
with st.container():
        # Centered "Get Quote" button
        ex_col_l, ex_2, button_col, ex_col_r = st.columns([0.7, 0.7, 1 ,1])

        with button_col:
            st.write('')
            k_value = None
            
            if st.button('RECOMMENDATIONS'):
                temp_df = pd.DataFrame(data = 
                                [[Age,Gender,Height,Weight,BMI,family_history_with_overweight.lower(),NCP,CAEC,CH2O,FCVC,FAF,TUE]],
                                columns=['Age', 'Gender', 'Height', 'Weight', 'BMI',       'family_history_with_overweight','NCP','CAEC','CH2O','FCVC','FAF','TUE'])
                model_2 = joblib.load(open('obesity_clustering.joblib', 'rb'))
                k_value = model_2.predict(temp_df)
        with st.container(border = True):
            for i in range(4):
                if (k_value == i):
                    df = rec[rec['Cluster'] == i]
                    for idx in df.index:
                        with st.container(border = True):
                            st.write(f"{df['Recommendation'][idx]}")
                            st.write(f"### Article to refer: ***[{df['Title'][idx]}]({df['Link'][idx]})***")
                            # st.write(f"{df['Link'][idx]}")
                            st.write('------')
                    st.write('**Disclaimer**: The recommendations above are only for informational purposes. One should consult a healthcare expert in case of any obesity related issues or for detailed information and health tips. These are just generic tips that individual can refer to')
       


                         



