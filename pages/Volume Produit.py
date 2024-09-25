import streamlit as st
import pandas as pd
from PIL import Image
import base64
from io import BytesIO
import plotly.express as px
import json

from fonctions import Visualisation_des_paramètres,Comparaison_des_phases_de_traitement,unity_compare
from fonctions import labo_oper,labo_oper1,labo_oper2,vis_op,compare_op,compar_unity_op,visualisation_volume,visualisation_volume_op,send_notification
#--------------------------------------------------heradr-------------------------------------------------------------
st.markdown(f"<h1 style='text-align: center'>Productions</h1>", unsafe_allow_html=True)

don = st.sidebar.radio('Visualisation:',
                            [
                                "Volume produit (m3)",
                                "Volume & Paramètres de marche",
                                ])      
df = pd.read_excel('data/Copie de Résultat de Production et TRG - Eau Dessalement Mobile et Fixe au   25 08 2024.xlsb .xlsx',sheet_name="Volume")

if don == "Volume produit (m3)":
    df = pd.read_excel('data/Copie de Résultat de Production et TRG - Eau Dessalement Mobile et Fixe au   25 08 2024.xlsb .xlsx',sheet_name="Volume")
    col1,col2 = st.columns((2))

    startDate = pd.to_datetime(df["Date"]).min()
    endDate = pd.to_datetime(df["Date"]).max()

    with col1:
        date1 = pd.to_datetime(st.sidebar.date_input("Start Date", startDate))

    with col2:
        date2 = pd.to_datetime(st.sidebar.date_input("End Date", endDate))
    if st.sidebar.button("Aply"):
        visualisation_volume(df,date1,date2)
elif don == "Volume & Paramètres de marche":
    df = pd.read_excel('data/Copie de Résultat de Production et TRG - Eau Dessalement Mobile et Fixe au   25 08 2024.xlsb .xlsx',sheet_name="Volume")
    data_opertionel={}
    unity_to_compare = st.sidebar.radio('Unité:',
                                    [
                                    "QT",
                                    "ESLI",
                                    "ION",
                                    "MCT"
                                    ])
    if (unity_to_compare == "MCT"):
        data_opertionel["tr"] = pd.read_excel('data/SUIVI DP et Q et CIP des RO  MCT.xlsx',sheet_name="tr")
        phase = st.sidebar.radio('Phase:',
                                ["tr"])
    elif  (unity_to_compare == "QT"):
        sheets =["UF","FC","RO"]
        for sheet in sheets:
            data_opertionel[sheet] = pd.read_excel('data/Suivi contrôle qualité d\'eau de dessalement QT.xlsx',sheet_name=sheet)
        phase = st.sidebar.radio('Phase:',
                                ["UF","FC","RO"]
                                )
    elif(unity_to_compare == "ESLI"):
        sheets =["UF","FC","RO ZONE A","RO ZONE B","RO ZONE C"]
        for sheet in sheets:
            data_opertionel[sheet] = pd.read_excel('data/Suivi contrôle qualité d\'eau de dessalement ESLI.xlsx',sheet_name=sheet)
        phase = st.sidebar.radio('Phase:',
                                ["UF","FC","RO ZONE A","RO ZONE B","RO ZONE C"])
    paramètre = st.sidebar.selectbox(f"paramètres de {unity_to_compare}_{phase}",
                                                                                    data_opertionel[phase].columns[1:])
    
    volume = st.sidebar.selectbox('Volume produit (m3):',
                                    df.columns[1:]) 
    if st.sidebar.button("Aply"):
        visualisation_volume_op(data_opertionel,df,phase,volume,paramètre)