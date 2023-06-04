import pandas as pd
import streamlit as st
import numpy as np
from matplotlib import pyplot as plt
import pickle
import sklearn 
from PIL import Image

# Load the saved components
with open("export/dt_model.pkl", "rb") as f:
    components = pickle.load(f)

# Extract the individual components
num_imputer = components["num_imputer"]
cat_imputer = components["cat_imputer"]
encoder = components["encoder"]
scaler = components["scaler"]
dt_model = components["models"]

# Create the app
# Add an image or logo to the app
image = Image.open('C:\\Users\\Admin\\Desktop\\lp4_project\\project\\stock.jpg')

# Open the image file
st.image(image)



#add app title
st.title(":moneybag: SALES PREDICTION MACHINE LEARNING APP :moneybag:")


# Add some text
st.write("Enter some data for Prediction.")

 # Create the input fields
input_data = {}
col1,col2 = st.columns(2)
with col1:
    input_data['store_nbr'] = st.slider("store_nbr",0,54)
    input_data['products'] = st.selectbox("products", ['AUTOMOTIVE', 'CLEANING', 'BEAUTY', 'FOODS', 'STATIONERY',
       'CELEBRATION', 'GROCERY', 'HARDWARE', 'HOME', 'LADIESWEAR',
       'LAWN AND GARDEN', 'CLOTHING', 'LIQUOR,WINE,BEER', 'PET SUPPLIES'])
    input_data['onpromotion'] =st.number_input("onpromotion",step=1)
    input_data['state'] = st.selectbox("state", ['Pichincha', 'Cotopaxi', 'Chimborazo', 'Imbabura',
       'Santo Domingo de los Tsachilas', 'Bolivar', 'Pastaza',
       'Tungurahua', 'Guayas', 'Santa Elena', 'Los Rios', 'Azuay', 'Loja',
       'El Oro', 'Esmeraldas', 'Manabi'])
    input_data['store_type'] = st.selectbox("store_type",['D', 'C', 'B', 'E', 'A'])
    input_data['cluster'] = st.number_input("cluster",step=1)

with col2:
    input_data['dcoilwtico'] = st.number_input("dcoilwtico",step=1)
    input_data['year'] = st.number_input("year",step=1)
    input_data['month'] = st.slider("month",1,12)
    input_data['day'] = st.slider("day",1,31)
    input_data['dayofweek'] = st.number_input("dayofweek,0=Sun and 6=Sat",step=1)
    input_data['end_month'] = st.selectbox("end_month",['True','False'])


  # Create a button to make a prediction
    
if st.button("Predict"):
    # Convert the input data to a pandas DataFrame
        input_df = pd.DataFrame([input_data])


# Selecting categorical and numerical columns separately
        cat_columns = [col for col in input_df.columns if input_df[col].dtype == 'object']
        num_columns = [col for col in input_df.columns if input_df[col].dtype != 'object']


# Apply the imputers
        input_df_imputed_cat = cat_imputer.transform(input_df[cat_columns])
        input_df_imputed_num = num_imputer.transform(input_df[num_columns])

        
 # Encode the categorical columns
        input_encoded_df = pd.DataFrame(encoder.transform(input_df_imputed_cat).toarray(),
                                   columns=encoder.get_feature_names(cat_columns))

# Scale the numerical columns
        input_df_scaled = scaler.transform(input_df_imputed_num)
        input_scaled_df = pd.DataFrame(input_df_scaled , columns = num_columns)

#joining the cat encoded and num scaled
        final_df = pd.concat([input_encoded_df, input_scaled_df], axis=1)

# Make a prediction
        prediction =dt_model.predict(final_df)[0]

        
# Display the prediction
        st.write(f"The predicted sales are: {prediction}.")
        input_df.to_csv("data.csv", index=False)
        st.table(input_df)
        st.snow()


