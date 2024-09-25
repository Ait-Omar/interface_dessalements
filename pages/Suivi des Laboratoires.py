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

st.markdown(f"<h1 style='text-align: center'>Suivi des analyses laboratoires</h1>", unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader("Charger les données laboratoires", type=["xlsx", "xls"])

#---------------------------------------------Chargement des données-----------------------------------------------------
if uploaded_file is None:
    st.sidebar.info("Upload a file through config")
    st.stop()

st.sidebar.markdown("<p style='text-align: center;'>Fichier téléchargé avec succès!</p>",unsafe_allow_html=True)
sheets =["QT_intake","QT_PERMEAT FILTRATION","QT_APRES FILTRES A CARTOUCHE","QT_PERMEAT RO","QT_sortie_global",
    "ESLI_intake","ESLI_PERMEAT FILTRATION", "ESLI_APRES FILTRES A CARTOUCHE","ESLI_PERMEAT RO",
    "ION_intake","ION_PERMEAT FILTRATION","ION_Bac_stockage","ION_APRES FILTRES A CARTOUCHE","ION_PERMEAT RO",
    "MCT_intake","MCT_APRES FILTRES A CARTOUCHE","MCT_PERMEAT RO"]
data = {}
for sheet in sheets:
        data[sheet] = pd.read_excel(uploaded_file,sheet_name=sheet)
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
                                        "ION EXCHANGE",
                                        "MCT"])
    try:
        if (unity == "MCT"):
            phase = st.sidebar.radio('Phase:',
                                    [
                                    'intake',
                                    'APRES FILTRES A CARTOUCHE',
                                    'PERMEAT RO'])
        elif  (unity == "QT"):
            phase = st.sidebar.radio('Phase:',
                                    [
                                    'intake',
                                    'PERMEAT FILTRATION',
                                    'APRES FILTRES A CARTOUCHE',
                                    'PERMEAT RO',
                                    'sortie_global'])
        elif (unity == "ION EXCHANGE"):
            phase = st.sidebar.radio('Phase:',
                                    [
                                    'intake',
                                    'PERMEAT FILTRATION',
                                    'Bac_stockage',
                                    'APRES FILTRES A CARTOUCHE',
                                    'PERMEAT RO',
                                    ])
        elif(unity == "ESLI"):
            phase = st.sidebar.radio('Phase:',
                                    [
                                    'intake',
                                    'PERMEAT FILTRATION',
                                    'APRES FILTRES A CARTOUCHE',
                                    'PERMEAT RO',
                                    ])
        df = pd.read_excel(uploaded_file,sheet_name="QT_intake")
        col1,col2 = st.columns((2))
        df['date'] = pd.to_datetime(df['date'])

        startDate = pd.to_datetime(df["date"]).min()
        endDate = pd.to_datetime(df["date"]).max()

        with col1:
            date1 = pd.to_datetime(st.sidebar.date_input("Start Date", startDate))
        with col2:
            date2 = pd.to_datetime(st.sidebar.date_input("End Date", endDate))

        if st.sidebar.button("Apply"):
            Visualisation_des_paramètres(uploaded_file,unity,phase,date1,date2)         
    except Exception as e:
        st.markdown(f"<h3 style='text-align: center;color:red;'></h3>", unsafe_allow_html=True)  
elif don1 == "Comparaison des phases de traitement":          
    phase_to_compare = []

    unity_to_compare = st.sidebar.radio('Unité :',
                            [
                                "QT",
                                "ESLI",
                                "ION",
                                "MCT"])
    try:
        if unity_to_compare == "MCT":
            phase_to_compare = st.sidebar.multiselect('Phase de traitement:',
                                        [
                                        'intake',
                                        'APRES FILTRES A CARTOUCHE',
                                        'PERMEAT RO'])
        elif  ( unity_to_compare == "QT"):
            phase_to_compare = st.sidebar.multiselect('Phase de traitement:',
                                        [
                                        'intake',
                                        'PERMEAT FILTRATION',
                                        'APRES FILTRES A CARTOUCHE',
                                        'PERMEAT RO',
                                        'sortie_global'])
        elif (unity_to_compare == "ION"):
            phase_to_compare = st.sidebar.multiselect('Phase de traitement:',
                                        [
                                        'intake',
                                        'PERMEAT FILTRATION',
                                        'Bac_stockage',
                                        'APRES FILTRES A CARTOUCHE',
                                        'PERMEAT RO',
                                        ])
        elif(unity_to_compare == "ESLI"):
            phase_to_compare = st.sidebar.multiselect('Phase de traitement:',
                                        [
                                        'intake',
                                        'PERMEAT FILTRATION',
                                        'APRES FILTRES A CARTOUCHE',
                                        'PERMEAT RO',
                                        ])
            
        param_to_compare = {}

        if phase_to_compare:
            for j in range(len(phase_to_compare)):  
                param_to_compare[f"{unity_to_compare}_{phase_to_compare[j]}"] = st.sidebar.multiselect(f'paramètres d\'{phase_to_compare[j]}',
                                    data[f"{unity_to_compare}_{phase_to_compare[j]}"].columns[1:]) 
        col1,col2 = st.columns((2))
        startDate = pd.to_datetime(data["QT_intake"]["date"]).min()
        endDate = pd.to_datetime(data["QT_intake"]["date"]).max() 
        
        with col1:
            date1 = pd.to_datetime(st.sidebar.date_input("Start date: ", startDate))

        with col2:
            date2 = pd.to_datetime(st.sidebar.date_input("End date:", endDate))  
        graphique = st.sidebar.selectbox('Type du graphique :',
            ['Graphique à barres','Graphique en lignes','Graphique en aires','Graphique à points']) 
        if st.sidebar.button("Apply"):
            Comparaison_des_phases_de_traitement(uploaded_file,[unity_to_compare, phase_to_compare, param_to_compare],date1,date2,graphique) 
    except Exception as e:
        st.markdown(f"<h3 style='text-align: center;color:red;'></h3>", unsafe_allow_html=True)
else:
    unity_to_compare1 = st.sidebar.multiselect('Unité:',
                            [
                                "QT",
                                "ESLI",
                                "ION",
                                "MCT"])
    try:
        phase_traitement = {}
        paramètre = {}
        for i in range(len(unity_to_compare1)):
            if unity_to_compare1[i]  == "MCT":
                phase_traitement[f"{unity_to_compare1[i]}"] = st.sidebar.radio(f"phase de traitement de {unity_to_compare1[i]}",
                                    [
                                    "intake",
                                    'APRES FILTRES A CARTOUCHE',
                                    'PERMEAT RO'])
            elif unity_to_compare1[i]  == "ION":
                phase_traitement[f"{unity_to_compare1[i]}"] = st.sidebar.radio(f"phase de traitement de {unity_to_compare1[i]}",
                                    [
                                    "intake",
                                    "PERMEAT FILTRATION",
                                    "Bac_stockage",
                                    'APRES FILTRES A CARTOUCHE',
                                    'PERMEAT RO'])
            elif unity_to_compare1[i]  == "QT":
                phase_traitement[f"{unity_to_compare1[i]}"] = st.sidebar.radio(f"phase de traitement de {unity_to_compare1[i]}",
                                    [
                                    "intake",
                                    "PERMEAT FILTRATION",
                                    'APRES FILTRES A CARTOUCHE',
                                    'PERMEAT RO',
                                    "sortie_global"])
            elif unity_to_compare1[i]  == "ESLI":
                phase_traitement[f"{unity_to_compare1[i]}"] = st.sidebar.radio(f"phase de traitement de {unity_to_compare1[i]}",
                                    [
                                    "intake",
                                    "PERMEAT FILTRATION",
                                    'APRES FILTRES A CARTOUCHE',
                                    'PERMEAT RO'])
            

            paramètre[f"{unity_to_compare1[i]}_{phase_traitement[unity_to_compare1[i]]}"] = st.sidebar.multiselect(f"paramètres de {unity_to_compare1[i]}_{phase_traitement[unity_to_compare1[i]]}",
                                                                                    data[f"{unity_to_compare1[i]}_{phase_traitement[unity_to_compare1[i]]}"].columns[1:]     )
        col1,col2 = st.columns((2))
        startDate = pd.to_datetime(data["QT_intake"]["date"]).min()
        endDate = pd.to_datetime(data["QT_intake"]["date"]).max() 
        with col1:
            date1 = pd.to_datetime(st.sidebar.date_input("de: ", startDate))

        with col2:
            date2 = pd.to_datetime(st.sidebar.date_input("à: ", endDate)) 

        if st.sidebar.button("Apply"):
            unity_compare(uploaded_file,unity_to_compare1,phase_traitement,paramètre,date1,date2)
    except Exception as e:
        st.markdown(f"<h3 style='text-align: center;color:red;'></h3>", unsafe_allow_html=True)