import pickle
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly
from plotly import graph_objs as go



# loading the trained model
### USD
pickle_usd_beli = open('USD/kurs-beli-USD-forecasting-using-LSTM.pkl', 'rb') 
pickle_usd_jual = open('USD/kurs-jual-USD-forecasting-using-LSTM.pkl', 'rb') 

### SGD
pickle_sgd_beli = open('SGD/kurs-beli-SGD-forecasting-using-LSTM.pkl', 'rb') 
pickle_sgd_jual = open('SGD/kurs-jual-SGD-forecasting-using-LSTM.pkl', 'rb') 

### EUR
pickle_eur_beli = open('EUR/kurs-beli-EUR-forecasting-using-LSTM.pkl', 'rb') 
pickle_eur_jual = open('EUR/kurs-jual-EUR-forecasting-using-LSTM.pkl', 'rb') 


@st.cache()

# defining the function which will make the prediction using the data which the user inputs 
def prediction(mata_uang,model_type,months):   
    # Pre-processing user input   
    if mata_uang == 'USD':
        df = pd.read_csv('USD/Kurs_Transaksi_USD.csv')
        df1 = df[-24*365:].reset_index(drop=True)
        if model_type == "Kurs Jual":
            model = pickle_usd_beli
        elif model_type == "Kurs Beli":
            model = pickle_usd_jual

    elif mata_uang == 'SGD':
        df = pd.read_csv('SGD/Kurs_Transaksi_SGD.csv')
        df1 = df[-24*365:].reset_index(drop=True)
        if model_type == "Kurs Jual":
            model = pickle_sgd_beli
        elif model_type == "Kurs Beli":
            model = pickle_sgd_jual

    elif mata_uang == 'EUR':
        df = pd.read_csv('EUR/Kurs_Transaksi_EUR.csv')
        df1 = df[-24*365:].reset_index(drop=True)
        if model_type == "Kurs Jual":
            model = pickle_eur_beli
        elif model_type == "Kurs Beli":
            model = pickle_eur_jual


# Making predictions     
    train_size = int(len(df1) * 0.7)
    test =df1[train_size:].reset_index(drop=True)
    
    n_future = 24*7
    date_future = pd.date_range(start=test['Tanggal'].values[-1], periods=n_future+1, freq='H')

    return df1, df


# this is the main function in which we define our webpage  
def main():       
    # front end elements of the web page 
    st.title("Forecast Tukar Mata Uang WebApp")
    html_temp = """
    <div style="background-color:brown;padding:7px">
    <h3 style="color:white;text-align:center;">USD - SGD - EUR</h3>
    </div>
    """
      
    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True) 
      
    # following lines create boxes in which user can enter data required to make prediction 
    mata_uang = st.selectbox('Mata Uang Asing',("USD", "SGD", "EUR")) 
    input_type = st.selectbox('Pilih Transaksi',("Kurs Jual","Kurs Beli")) 
    input_months = st.slider('Jumlah bulan yang akan di prediksi', min_value=1, max_value=6, step=1)
    result =""
    data2 =""
      
    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Prediksi"): 
        result, df = prediction(mata_uang,input_type,input_months)
        st.success(f'Hasil Forecasting untuk {input_months} bulan kemudian :\n')
        st.subheader('Forecast Result')
        #st.write(result)


        # Plot
        data2 = df[[input_type]]
        data2 = pd.concat([data2,result])

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data2.iloc[0:2547].index, y=data2[input_type].iloc[0:2547],mode='lines', name = 'Data'))
        fig.add_trace(go.Scatter(x=data2.iloc[2547:].index, y=data2[data2.columns[1]].iloc[2547:],mode='lines', name = 'Forecast'))
        fig.layout.update(title_text=mata_uang + " " + input_type, xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)


       
if __name__=='__main__': 
    main()