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


# Titre de la page
st.title("Pramètres de marche")

#---------------------------------------------Chargement des données-----------------------------------------------------
don1 = st.sidebar.radio('Visualisation:',
                                [
                                    "Visualisation des paramètres",
                                    "Comparaison des phases de traitement",
                                    "Comparaison des unitées"
                                    ])       
if don1 == "Visualisation des paramètres":
    unity = st.sidebar.radio('Unité:',
                                    [
                                        "QT",
                                        "ESLI",
                                        "MCT"])
    data_opertionel = {}
    try:
        if (unity == "MCT"):
            data_opertionel["tr"] = pd.read_excel('data/SUIVI DP et Q et CIP des RO  MCT.xlsx',sheet_name="tr")
            phase = st.sidebar.radio('Phase:',
                                    ["tr"])
            df = pd.read_excel('data/SUIVI DP et Q et CIP des RO  MCT.xlsx',sheet_name="tr")
        elif  (unity == "QT"):
            sheets =["UF","FC","RO"]
            for sheet in sheets:
                data_opertionel[sheet] = pd.read_excel('data/Suivi contrôle qualité d\'eau de dessalement QT.xlsx',sheet_name=sheet)
            phase = st.sidebar.radio('Phase:',
                                    ["UF","FC","RO"]
                                    )
            df = pd.read_excel('data/Suivi contrôle qualité d\'eau de dessalement QT.xlsx',sheet_name="UF")
        elif(unity == "ESLI"):
            sheets =["UF","FC","RO ZONE A","RO ZONE B","RO ZONE C"]
            for sheet in sheets:
                data_opertionel[sheet] = pd.read_excel('data/Suivi contrôle qualité d\'eau de dessalement ESLI.xlsx',sheet_name=sheet)
            phase = st.sidebar.radio('Phase:',
                                    ["UF","FC","RO ZONE A","RO ZONE B","RO ZONE C"])
            df = pd.read_excel('data/Suivi contrôle qualité d\'eau de dessalement ESLI.xlsx',sheet_name="UF")
        

        col1,col2 = st.columns((2))

        startDate = pd.to_datetime(df["date"]).min()
        endDate = pd.to_datetime(df["date"]).max()

        with col1:
            date1 = pd.to_datetime(st.sidebar.date_input("Start Date", startDate))

        with col2:
            date2 = pd.to_datetime(st.sidebar.date_input("End Date", endDate))

        if st.sidebar.button("Apply"):
            vis_op(data_opertionel,phase,date1,date2) 
    except Exception as e:
            st.markdown(f"<h3 style='text-align: center;color:red;'></h3>", unsafe_allow_html=True) 
elif  don1 == "Comparaison des phases de traitement":
    unity = st.sidebar.radio('Unité:',
                                    [
                                        "QT",
                                        "ESLI",
                                        "MCT"]) 
    data_opertionel = {}
    try:
        if (unity == "MCT"):
            data_opertionel["tr"] = pd.read_excel('data/SUIVI DP et Q et CIP des RO  MCT.xlsx',sheet_name="tr")
            phase = st.sidebar.multiselect('Phase:',
                                    ["tr"])
        elif  (unity == "QT"):
            sheets =["UF","FC","RO"]
            for sheet in sheets:
                data_opertionel[sheet] = pd.read_excel('data/Suivi contrôle qualité d\'eau de dessalement QT.xlsx',sheet_name=sheet)
            phase = st.sidebar.multiselect('Phase:',
                                    ["UF","FC","RO"]
                                    )
        elif(unity == "ESLI"):
            sheets =["UF","FC","RO ZONE A","RO ZONE B","RO ZONE C"]
            for sheet in sheets:
                data_opertionel[sheet] = pd.read_excel('data/Suivi contrôle qualité d\'eau de dessalement ESLI.xlsx',sheet_name=sheet)
            phase = st.sidebar.multiselect('Phase:',
                                    ["UF","FC","RO ZONE A","RO ZONE B","RO ZONE C"])
            
        param_to_compare = {}

        if phase:
            for j in range(len(phase)):  
                param_to_compare[f"{phase[j]}"] = st.sidebar.multiselect(f'paramètres d\'{phase[j]}',
                                    data_opertionel[f"{phase[j]}"].columns[1:])
        df = pd.read_excel('data/Suivi contrôle qualité d\'eau de dessalement QT.xlsx',sheet_name="FC")

        col1,col2 = st.columns((2))
        df['date'] = pd.to_datetime(df['date'])

        startDate = pd.to_datetime(df["date"]).min()
        endDate = pd.to_datetime(df["date"]).max()

        with col1:
            date1 = pd.to_datetime(st.sidebar.date_input("Start Date", startDate))

        with col2:
            date2 = pd.to_datetime(st.sidebar.date_input("End Date", endDate))

        if st.sidebar.button("Apply"):
            compare_op(data_opertionel,phase,param_to_compare,date1,date2) 
    except Exception as e:
            st.markdown(f"<h3 style='text-align: center;color:red;'></h3>", unsafe_allow_html=True)                        
else:
    unity_to_compare = st.sidebar.multiselect('Unité:',
                            [
                                "QT",
                                "ESLI",
                                "MCT"])
    try:
        data_opertionel={}
        phase_traitement = {}
        paramètre = {}
        for i in range(len(unity_to_compare)):
            if unity_to_compare[i]  == "MCT":
                data_opertionel[f"{unity_to_compare[i]}_tr"] = pd.read_excel('data/SUIVI DP et Q et CIP des RO  MCT.xlsx',sheet_name="tr")
                phase_traitement[f"{unity_to_compare[i]}"] = st.sidebar.radio(f"phases de {unity_to_compare[i]}",
                                    [
                                    "tr"
                                ])
            elif unity_to_compare[i]  == "QT":
                sheets =["UF","FC","RO"]
                for sheet in sheets:
                    data_opertionel[f"{unity_to_compare[i]}_{sheet}"] = pd.read_excel('data/Suivi contrôle qualité d\'eau de dessalement QT.xlsx',sheet_name=sheet)
                phase_traitement[f"{unity_to_compare[i]}"] = st.sidebar.radio(f"phases de {unity_to_compare[i]}",
                                    ["UF","FC","RO"])
            else:
                sheets =["UF","FC","RO ZONE A","RO ZONE B","RO ZONE C"]
                for sheet in sheets:
                        data_opertionel[f"{unity_to_compare[i]}_{sheet}"] = pd.read_excel('data/Suivi contrôle qualité d\'eau de dessalement ESLI.xlsx',sheet_name=sheet)
                phase_traitement[f"{unity_to_compare[i]}"] = st.sidebar.radio(f"phases de {unity_to_compare[i]}",
                                    [
                                    "UF","FC","RO ZONE A","RO ZONE B","RO ZONE C"])

            paramètre[f"{unity_to_compare[i]}_{phase_traitement[unity_to_compare[i]]}"] = st.sidebar.multiselect(f"paramètres de {unity_to_compare[i]}_{phase_traitement[unity_to_compare[i]]}",
                                                                                    data_opertionel[f"{unity_to_compare[i]}_{phase_traitement[unity_to_compare[i]]}"].columns[1:])
        
        col1,col2 = st.columns((2))
        df = pd.read_excel('data/Suivi contrôle qualité d\'eau de dessalement QT.xlsx',sheet_name="UF")
        startDate = pd.to_datetime(df["date"]).min()
        endDate = pd.to_datetime(df["date"]).max() 
        with col1:
            date1 = pd.to_datetime(st.sidebar.date_input("de: ", startDate))

        with col2:
            date2 = pd.to_datetime(st.sidebar.date_input("à: ", endDate)) 

        if st.sidebar.button("Apply"):
            compar_unity_op(data_opertionel,unity_to_compare,phase_traitement,paramètre,date1,date2)
    except Exception as e:
        st.markdown(f"<h3 style='text-align: center;color:red;'></h3>", unsafe_allow_html=True)

