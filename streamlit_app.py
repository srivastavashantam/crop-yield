import streamlit as st 
import pickle
import pandas as pd
import numpy as np
import base64

# Function to encode the image
def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

# Encode the image
img_base64 = get_base64_encoded_image("f1.jpg")

# Set the page configuration for a more immersive experience
st.set_page_config(page_title="Crop Yield Predictor", layout="wide")

# Add the background image using the base64 encoded string
background_html = f"""
<style>
.stApp {{
    background: linear-gradient(rgba(0, 0, 0, 0), rgba(0, 0, 0, 0)), 
                url("data:image/jpg;base64,{img_base64}") no-repeat center center fixed;
    background-size: cover;
    background-attachment: fixed;
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 100vh;
}}

footer {{
    margin-top: auto;
    text-align: center;
    padding: 100px;
}}

h1, h2, h3 {{
    color: white;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.9);
}}

.reportview-container {{
    background: rgba(0, 0, 0, 0.7);  /* Semi-transparent background */
    padding: 10px;
    border-radius: 10px;
}}

.sidebar .sidebar-content {{
    background: rgba(255, 255, 255, 0.6);  /* Semi-transparent sidebar background */
    border-radius: 10px;
    padding: 10px;
}}

</style>
"""

st.markdown(background_html, unsafe_allow_html=True)

# Modify the title and subtitle
st.markdown("<h1 style='text-align: center; font-size: 3em; color: #DC143C;'>🌾 Crop Yield Predictor</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-size: 1.75em; color: violet;'>🌱 Predict the yield of your crops based on your input resources!<br>अपने खेत की उपज जानने के लिए यहाँ क्लिक करें!</h3>", unsafe_allow_html=True)

# Load the model and data
with open('pipe.pkl', 'rb') as pipe_file, open('df.pkl', 'rb') as df_file:
    pipe = pickle.load(pipe_file)
    df = pickle.load(df_file)

# Sidebar for input parameters with icons
st.sidebar.markdown("<h2 style='color: Navy; text-shadow: none;'>🌿 Input Parameters</h2>", unsafe_allow_html=True)

# Crop selection
st.sidebar.markdown("#### Select Crop")
crop = st.sidebar.selectbox("🌾 फसल चुनें", sorted(df['Crop'].unique()), key='crop')

# Season selection
st.sidebar.markdown("#### Select Season")
season = st.sidebar.selectbox("🗓️ मौसम चुनें", sorted(df['Season'].unique()), key='season')

# State selection
st.sidebar.markdown("#### Select State")
state = st.sidebar.selectbox("🏞️ राज्य चुनें", sorted(df['State'].unique()), key='state')

# Area input
st.sidebar.markdown("#### Area (in hectares)")
area = st.sidebar.number_input('🌍 खेत का क्षेत्रफल (हेक्टेयर में)', min_value=0.0, step=0.1, key='area')

# Fertilizer input
st.sidebar.markdown("#### Fertilizer Usage (in Kgs)")
fertilizer = st.sidebar.number_input('🧪 उर्वरक की मात्रा (किलोग्राम)', min_value=0.0, step=0.1, key='fertilizer')

# Pesticide input
st.sidebar.markdown("#### Pesticide Usage (in Kgs)")
pesticide = st.sidebar.number_input('🛡️ कीटनाशक की मात्रा (किलोग्राम)', min_value=0.0, step=0.1, key='pesticide')

# Annual Rainfall input
st.sidebar.markdown("#### Annual Rainfall (mm)")
rainfall = st.sidebar.number_input('☔ वार्षिक वर्षा (मिलीमीटर में)', min_value=0.0, step=0.1, key='rainfall')

# Production
st.sidebar.markdown("#### Production (in tons)")
production = st.sidebar.number_input('🏭 वार्षिक उत्पादन (टन में)', min_value=0.0, step=1.0, key='production')

# Prediction button with animation
if st.button('🌟 Predict Yield (production per unit area) | फसल का अनुमान लगाएँ'):
    # Applying transformations as per your model
    input_df = pd.DataFrame({
        'Crop': [crop],
        'Season': [season],
        'State': [state],
        'Area': [np.log1p(area)],
        'Fertilizer': [np.log1p(fertilizer)],
        'Pesticide': [np.log1p(pesticide)],
        'Annual_Rainfall': [rainfall],
        'Production': [np.log1p(production)]
    })

    # Show spinner during prediction
    with st.spinner('गणना हो रही है...'):
        predicted_log_yield = pipe.predict(input_df)[0]
        predicted_yield = np.exp(predicted_log_yield)  # transformation to get the log yield

    # Display results
    st.markdown("<h3>📈 अनुमानित उपज</h3>", unsafe_allow_html=True)
    # Display results with a better contrast for visibility
    result_html = f"""
    <hr>
    <div style='background-color: rgba(0, 71, 152, 0.8); padding: 10px; border-radius: 10px; text-align: center;'>
      <h4 style='color: white;'>🌿 Predicted crop yield = <strong>{round(predicted_yield, 2)} Tons/Hectares</strong></h4>
      <p style='color: white;'>आपकी मेहनत का फल: प्रति हेक्टेयर अनुमानित उपज</p>
    </div>
    """

    st.markdown(result_html, unsafe_allow_html=True)

    # Fun encouragement messages
    if predicted_yield > 20:
        st.balloons()
        st.markdown("<h3>🎉 Excellent yield prediction! Great going! 🌱<br>वाह! बंपर फसल की संभावना है। बधाई हो!</h3>", unsafe_allow_html=True)
    elif predicted_yield > 3:
        st.balloons()
        st.markdown("<h3>🌳 Decent yield prediction! Go ahead! 🌱<br>अच्छी फसल की उम्मीद है। मेहनत रंग लाई!</h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h3>☘️ Yield prediction is low. Consider optimizing your resources. 🌧️<br>फसल कम होने की आशंका है। कुछ सुधार की जरूरत है।</h3>", unsafe_allow_html=True)

# Footer with additional information
footer_html = """
<footer>
  <hr>
  <div style='text-align: center;'>
    <h4 style='color: violet;'>Boost Your Harvest: Optimize your resources for precise yield and farm prosperity!</h4>
    <p style='font-size: 1.275em; color: white;'>अपनी उपज को बढ़ाएं: संसाधनों का सही उपयोग कर खेती को समृद्धि की ओर ले जाएं\u0964</p>
    <p style='font-size: 1.3em; color: violet;'>
      <strong style='color: red;'>Disclaimer:</strong> While this web app provides data-driven crop yield predictions, it is essential to consult with a local agricultural expert for personalized advice and the most accurate guidance tailored to your specific farming conditions.
    </p>
    <p style='font-size: 1.275em; color: white;'>
      <strong style='color: red;'> अस्वीकरण:</strong> यह वेब ऐप आपको डेटा के आधार पर फसल उत्पादन की भविष्यवाणी देता है, लेकिन आपकी विशिष्ट खेती की परिस्थितियों के अनुसार सटीक मार्गदर्शन के लिए स्थानीय कृषि विशेषज्ञ से परामर्श अवश्य करें।\u0964</p>
    <p style='font-size: 1.5em; color: yellow; margin-top: 100px;'>
      <strong>&copy; 2024. Developed by Suyash Sharma for iNeuron.ai</strong>
    </p>
  </div>
</footer>
"""



st.markdown(footer_html, unsafe_allow_html=True)
