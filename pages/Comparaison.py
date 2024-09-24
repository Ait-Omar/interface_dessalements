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
uploaded_file = st.file_uploader("Choisissez un fichier Excel", type=["xlsx", "xls"])
if uploaded_file is None:
    st.info("Upload a file through config")
    st.stop()
st.markdown("<p style='text-align: center;'>Fichier téléchargé avec succès!</p>",unsafe_allow_html=True)
sheets =["QT_intake","QT_PERMEAT FILTRATION","QT_APRES FILTRES A CARTOUCHE","QT_PERMEAT RO","QT_sortie_global",
    "ESLI_intake","ESLI_PERMEAT FILTRATION", "ESLI_APRES FILTRES A CARTOUCHE","ESLI_PERMEAT RO",
    "ION_intake","ION_PERMEAT FILTRATION","ION_Bac_stockage","ION_APRES FILTRES A CARTOUCHE","ION_PERMEAT RO",
    "MCT_intake","MCT_APRES FILTRES A CARTOUCHE","MCT_PERMEAT RO"]
data = {}
for sheet in sheets:
        data[sheet] = pd.read_excel(uploaded_file,sheet_name=sheet)

unity = st.sidebar.radio('Unity:',
                                    [
                                    'QT',
                                    'ESLI',
                                    'MCT'
                                    ])
if unity == "QT":
    try:
        sheets =["UF","FC","RO"]
        data_opertionel = {}
        for sheet in sheets:
            data_opertionel[sheet] = pd.read_excel('data/Suivi contrôle qualité d\'eau de dessalement QT.xlsx',sheet_name=sheet)
        phase_op = st.sidebar.radio("Phase operationnelle:",["UF","FC","RO"])
        phase_labo = st.sidebar.radio('Phase laboratoire:',
                                    [
                                    'intake',
                                    'PERMEAT FILTRATION',
                                    'APRES FILTRES A CARTOUCHE',
                                    'PERMEAT RO',
                                    'sortie_global'])
        
        para_op = st.sidebar.selectbox("paramètres operationels:",data_opertionel[phase_op].columns[1:])
        para_labo = st.sidebar.selectbox("paramètres laboratoire:",data[f"QT_{phase_labo}"].columns[1:])
        if st.sidebar.button("Apply"):
            labo_oper(data,data_opertionel,f"QT_{phase_labo}",phase_op,para_labo,para_op)
    except Exception as e:
            st.markdown(f"<h3 style='text-align: center;color:red;'></h3>", unsafe_allow_html=True)  
elif unity =="ESLI":
    try:
        sheets =["UF","FC","RO ZONE A","RO ZONE B","RO ZONE C"]
        data_opertionel = {}
        for sheet in sheets:
            data_opertionel[sheet] = pd.read_excel('data/Suivi contrôle qualité d\'eau de dessalement ESLI.xlsx',sheet_name=sheet)
        phase_op = st.sidebar.radio("Phase operationnelle:",["UF","FC","RO ZONE A","RO ZONE B","RO ZONE C"])
        phase_labo = st.sidebar.radio('Phase laboratoire:',
                                    [
                                    'intake',
                                    'PERMEAT FILTRATION',
                                    'APRES FILTRES A CARTOUCHE',
                                    'PERMEAT RO'])
        
        para_op = st.sidebar.selectbox("paramètres operationels:",data_opertionel[phase_op].columns[1:])
        para_labo = st.sidebar.selectbox("paramètres laboratoire:",data[f"ESLI_{phase_labo}"].columns[1:])
        if st.sidebar.button("Apply"):
            labo_oper(data,data_opertionel,f"ESLI_{phase_labo}",phase_op,para_labo,para_op)
    except Exception as e:
            st.markdown(f"<h3 style='text-align: center;color:red;'></h3>", unsafe_allow_html=True)  
elif unity =="MCT":
    try:
        data_opertionel = {}
        data_opertionel["tr"] = pd.read_excel('data/SUIVI DP et Q et CIP des RO  MCT.xlsx',sheet_name="tr")
        phase_labo = st.sidebar.radio('Phase laboratoire:',
                                    [
                                    'intake',
                                    'APRES FILTRES A CARTOUCHE',
                                    'PERMEAT RO'])
        
        para_op = st.sidebar.selectbox("paramètres operationels:",data_opertionel["tr"].columns[1:])

        para_labo = st.sidebar.selectbox("paramètres laboratoire:",data[f"MCT_{phase_labo}"].columns[1:])
        if st.sidebar.button("Apply"):
            labo_oper2(data,data_opertionel,f"MCT_{phase_labo}",para_labo,para_op)
    except Exception as e:
            st.markdown(f"<h3 style='text-align: center;color:red;'></h3>", unsafe_allow_html=True) 