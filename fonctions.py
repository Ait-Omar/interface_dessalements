import streamlit as st 
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components
import random
from plotly.subplots import make_subplots
import smtplib
import json
from email.message import EmailMessage
import plotly.io as pio

def Visualisation_des_paramètres(df,unity,phase,date1,date2): 
    #filtrage selon l'unité QT
    if (unity == "QT") & (phase =="intake"):
        df = pd.read_excel(df,sheet_name="QT_intake")
        col1,col2 = st.columns((2))

        df = df[(df["date"] >= date1) & (df["date"] <= date2)]
        df.replace('/', np.nan, inplace=True)
        df.replace('en cours', np.nan, inplace=True)
        df['TDS (mg/l)'].replace(0, np.nan, inplace=True)
        df['TOC (mg/l)'] = df['TOC (mg/l)'].replace('<3',1)
        df['TOC (mg/l)'] = df['TOC (mg/l)'].astype(float)
        df.loc[df['TOC (mg/l)'] < 3, 'TOC (mg/l)'] = 1
        df.loc[df['TOC (mg/l)'] > 3, 'TOC (mg/l)'] = 0
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cond. (mS/cm) à 25° C moyen: {np.around(df['Cond. (mS/cm) à 25° C'].mean(),2)}</h2>", unsafe_allow_html=True)        
            fig = px.line(df,x="date",y="Cond. (mS/cm) à 25° C")
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Turb (NTU) moyen: {np.around(df['Turb (NTU)'].mean(),2)}</h2>", unsafe_allow_html=True)        
            fig = px.line(df,x="date",y="Turb (NTU)")
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>PO43- (mg/l) moyen: {np.around(df['PO43- (mg/l)'].mean(),2)}</h2>", unsafe_allow_html=True)        
            fig = px.line(df,x="date",y="PO43- (mg/l)")
            fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                    x=df['date'].iloc[-1], 
                    y=0.1, 
                    text="PO43- doit être inférieur ou égale à 0.1",  
                    showarrow=True, 
                    arrowhead=2,  
                    ax=0, 
                    ay=-40  
                )
            st.plotly_chart(fig,use_container_width=True,height = 200)
            with open('config.json') as json_file:
                gmail_cfg = json.load(json_file)
            seuil_po43 = 0.1

            # Vérification de la dernière valeur de PO43-
            valeur_actuelle_po43 =df['PO43- (mg/l)'].iloc[-1]

            if valeur_actuelle_po43 > seuil_po43:
                # Sauvegarde le graphique comme image
                pio.write_image(fig, 'graph_PO43.png')

                # Création du message e-mail
                msg = EmailMessage()
                msg['To'] = "lightupyourhome03@gmail.com"
                msg['From'] = gmail_cfg['email']
                msg['Subject'] = "Alerte PO43- Dépassement du Seuil"
                msg.set_content(f'La valeur de PO43- (mg/l) est de {valeur_actuelle_po43} et a dépassé le seuil de 0.1. Voir le graphique ci-joint.')

                # Ajout de l'image en pièce jointe
                with open('graph_PO43.png', 'rb') as f:
                    file_data = f.read()
                    file_name = f.name
                    msg.add_attachment(file_data, maintype='image', subtype='png', filename=file_name)

                # Envoi de l'e-mail
                with smtplib.SMTP_SSL(gmail_cfg['serveur'], gmail_cfg['port']) as smtp:
                    smtp.login(gmail_cfg['email'], gmail_cfg['pwd'])
                    smtp.send_message(msg)
                    print("Notification envoyée avec succès avec le graphique !")
            else:
                print("La valeur actuelle de PO43- est inférieure ou égale au seuil. Aucune notification envoyée.")
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SiO2 (mg/l) moyen: {np.around(df['SiO2 (mg/l)'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="SiO2 (mg/l)")
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>TOC (mg/l) moyenne: {np.around(df['TOC (mg/l)'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="TOC (mg/l)")
            fig.add_hline(y=1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                    x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                    y=1,  # Position Y (sur la ligne horizontale)
                    text="TOC doit être égale à 1",  # Texte de l'annotation
                    showarrow=True,  # Afficher une flèche pointant vers le point
                    arrowhead=2,  # Type de flèche
                    ax=0,  # Position X de la flèche par rapport au texte
                    ay=-40  # Position Y de la flèche par rapport au texte
                )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>MES  (mg/l) moyenne: {np.around(df['MES  (mg/l)'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="MES  (mg/l)")
            fig.add_hline(y=10, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                    x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                    y=10,  # Position Y (sur la ligne horizontale)
                    text="MES doit être inférieur ou égale à 10",  # Texte de l'annotation
                    showarrow=True,  # Afficher une flèche pointant vers le point
                    arrowhead=2,  # Type de flèche
                    ax=0,  # Position X de la flèche par rapport au texte
                    ay=-40  # Position Y de la flèche par rapport au texte
                )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cl2 libre (mg/l) moyenne: {np.around(df['Cl2 libre (mg/l)'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="Cl2 libre (mg/l)")
            fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                    x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                    y=0,  # Position Y (sur la ligne horizontale)
                    text="Cl2 libre doit être égale à 0",  # Texte de l'annotation
                    showarrow=True,  # Afficher une flèche pointant vers le point
                    arrowhead=2,  # Type de flèche
                    ax=0,  # Position X de la flèche par rapport au texte
                    ay=-40  # Position Y de la flèche par rapport au texte
                )
            st.plotly_chart(fig,use_container_width=True,height = 200)   
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>pH moyenne: {np.around(df['pH'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="pH")
            st.plotly_chart(fig,use_container_width=True,height = 200)   
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>TDS (mg/l) moyenne: {np.around(df['TDS (mg/l)'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="TDS (mg/l)")
            st.plotly_chart(fig,use_container_width=True,height = 200)   
    elif (unity == "QT") & (phase =="PERMEAT FILTRATION"):
        df = pd.read_excel(df,sheet_name="QT_PERMEAT FILTRATION")
        # print(df.columns)
        col1,col2 = st.columns((2))
        df = df[(df["date"] >= date1) & (df["date"] <= date2)]
        df.replace('/', np.nan, inplace=True)
        df.replace('en cours', np.nan, inplace=True)

        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Turb (NTU) moyenne: {np.around(df['Turb (NTU)'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="Turb (NTU)")
            fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                    x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                    y=0.1,  # Position Y (sur la ligne horizontale)
                    text="Turb doit être égale à 0.1",  # Texte de l'annotation
                    showarrow=True,  # Afficher une flèche pointant vers le point
                    arrowhead=2,  # Type de flèche
                    ax=0,  # Position X de la flèche par rapport au texte
                    ay=-40  # Position Y de la flèche par rapport au texte
                )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SiO2 (mg/l) moyenne: {np.around(df['SiO2 (mg/l)'].mean(),2)} mg/l</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="SiO2 (mg/l)")
            fig.add_hline(y=1.1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                    x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                    y=1.1,  # Position Y (sur la ligne horizontale)
                    text="SiO2 doit inférieur ou égale à 1.1",  # Texte de l'annotation
                    showarrow=True,  # Afficher une flèche pointant vers le point
                    arrowhead=2,  # Type de flèche
                    ax=0,  # Position X de la flèche par rapport au texte
                    ay=-40  # Position Y de la flèche par rapport au texte
                )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>MES  (mg/l) moyenne: {np.around(df['MES (mg/l)'].mean(),2)} mg/l</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="MES (mg/l)")
            fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                    x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                    y=0,  # Position Y (sur la ligne horizontale)
                    text="MES doit être égale à 0",  # Texte de l'annotation
                    showarrow=True,  # Afficher une flèche pointant vers le point
                    arrowhead=2,  # Type de flèche
                    ax=0,  # Position X de la flèche par rapport au texte
                    ay=-40  # Position Y de la flèche par rapport au texte
                )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SDI 15 moyenne: {np.around(df['SDI 15'].mean(),2)} mg/l</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="SDI 15")
            fig.add_hline(y=2.5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                    x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                    y=2.5,  # Position Y (sur la ligne horizontale)
                    text="SDI 15 doit inférieur ouêtre égale à 2.5",  # Texte de l'annotation
                    showarrow=True,  # Afficher une flèche pointant vers le point
                    arrowhead=2,  # Type de flèche
                    ax=0,  # Position X de la flèche par rapport au texte
                    ay=-40  # Position Y de la flèche par rapport au texte
                )
            st.plotly_chart(fig,use_container_width=True,height = 200)
    elif (unity == "QT") & (phase =="APRES FILTRES A CARTOUCHE"):
        df = pd.read_excel(df,sheet_name="QT_APRES FILTRES A CARTOUCHE")
        col1,col2 = st.columns((2))
        df = df[(df["date"] >= date1) & (df["date"] <= date2)]
        df.replace('/', np.nan, inplace=True)
        df.replace('en cours', np.nan, inplace=True)
        df['TOC (mg/l)'] = df['TOC (mg/l)'].replace('<3',1)
        df['TOC (mg/l)'] = df['TOC (mg/l)'].astype(float)
        df.loc[df['TOC (mg/l)'] < 3, 'TOC (mg/l)'] = 1
        df.loc[df['TOC (mg/l)'] > 3, 'TOC (mg/l)'] = 0
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>pH moyenne: {np.around(df['pH'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="pH")
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>PO43- (mg/l) moyenne: {np.around(df['PO43-  (mg/l)'].mean(),2)} mg/l</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="PO43-  (mg/l)")
            fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                    x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                    y=0,  # Position Y (sur la ligne horizontale)
                    text="PO43- doit être égale à 0",  # Texte de l'annotation
                    showarrow=True,  # Afficher une flèche pointant vers le point
                    arrowhead=2,  # Type de flèche
                    ax=0,  # Position X de la flèche par rapport au texte
                    ay=-40  # Position Y de la flèche par rapport au texte
                )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'> ORP (mV) P1 moyenne: {np.around(df[' ORP (mV) P1'].mean(),2)} mg/l</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y=" ORP (mV) P1")
            fig.add_hline(y=250, line_dash="dash", line_color="red", line_width=2)
            fig.add_hline(y=300, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                y=250,  # Position Y (sur la ligne horizontale à 250)
                text="Min: 250 mV",  # Texte de l'annotation
                showarrow=True,  # Afficher une flèche pointant vers le point
                arrowhead=2,  # Type de flèche
                ax=0,  # Position X de la flèche par rapport au texte
                ay=-40  # Position Y de la flèche par rapport au texte
            )

            fig.add_annotation(
                x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                y=300,  # Position Y (sur la ligne horizontale à 300)
                text="Max: 300 mV",  # Texte de l'annotation
                showarrow=True,  # Afficher une flèche pointant vers le point
                arrowhead=2,  # Type de flèche
                ax=0,  # Position X de la flèche par rapport au texte
                ay=40  # Position Y de la flèche par rapport au texte
            )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>ORP (mV) P2 moyenne: {np.around(df['ORP (mV) P2'].mean(),2)} mg/l</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="ORP (mV) P2")
            fig.add_hline(y=250, line_dash="dash", line_color="red", line_width=2)
            fig.add_hline(y=300, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                y=250,  # Position Y (sur la ligne horizontale à 250)
                text="Min: 250 mV",  # Texte de l'annotation
                showarrow=True,  # Afficher une flèche pointant vers le point
                arrowhead=2,  # Type de flèche
                ax=0,  # Position X de la flèche par rapport au texte
                ay=-40  # Position Y de la flèche par rapport au texte
            )

            fig.add_annotation(
                x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                y=300,  # Position Y (sur la ligne horizontale à 300)
                text="Max: 300 mV",  # Texte de l'annotation
                showarrow=True,  # Afficher une flèche pointant vers le point
                arrowhead=2,  # Type de flèche
                ax=0,  # Position X de la flèche par rapport au texte
                ay=40  # Position Y de la flèche par rapport au texte
            )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 moyenne: {np.around(df['SDI15'].mean(),2)} mg/l</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="SDI15")
            fig.add_hline(y=2.5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                    x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                    y=2.5,  # Position Y (sur la ligne horizontale)
                    text="PO43- doit être égale à 2.5",  # Texte de l'annotation
                    showarrow=True,  # Afficher une flèche pointant vers le point
                    arrowhead=2,  # Type de flèche
                    ax=0,  # Position X de la flèche par rapport au texte
                    ay=-40  # Position Y de la flèche par rapport au texte
                )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>TOC (mg/l) moyenne: {np.around(df['TOC (mg/l)'].mean(),2)} mg/l</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="TOC (mg/l)")
            fig.add_hline(y=1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=1,  # Position Y (sur la ligne horizontale)
                        text="TOC doit être égale à 1",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)   
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>TDS (mg/l) moyenne: {np.around(df['TDS (mg/l)'].mean(),2)} mg/l</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="TDS (mg/l)")
            fig.add_hline(y=40000, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=40000,  # Position Y (sur la ligne horizontale)
                        text="TDS (mg/l) doit être égale à 4 0000",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)       
    elif (unity == "QT") & (phase =="PERMEAT RO"): 
        df = pd.read_excel(df,sheet_name="QT_PERMEAT RO")
        col1,col2 = st.columns((2))
        df = df[(df["date"] >= date1) & (df["date"] <= date2)]
        df.replace('/', np.nan, inplace=True)
        df.replace('#VALEUR!', np.nan, inplace=True)
        df.replace('en cours', np.nan, inplace=True)
        with col1:
            st.markdown(F"<h2 style='text-align: center;'>Cond A moyen en (mS/cm): {np.around(df['Cond A'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond A')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond A doit être inférieure à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>pH A moyen : {np.around(df['pH A'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH A')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH A doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cond B moyen en (mS/cm): {np.around(df['Cond B'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond B')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond B doit être inférieure à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>pH B moyen : {np.around(df['pH B'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH B')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH B doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cond C moyen en (mS/cm): {np.around(df['Cond C'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond C')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond C doit être inférieure à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>pH C moyen : {np.around(df['pH C'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH C')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH C doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cond D moyen en (mS/cm): {np.around(df['Cond D'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond D')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond D doit être inférieure à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>pH D moyen : {np.around(df['pH D'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH D')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH D doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cond E moyen en (mS/cm): {np.around(df['Cond E'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond E')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond E doit être inférieure à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>pH E moyen : {np.around(df['pH E'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH E')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH E doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cond F moyen en (mS/cm): {np.around(df['Cond F'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond F')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond F doit être inférieure à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>pH F moyen : {np.around(df['pH F'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH F')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH F doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cond G moyen en (mS/cm): {np.around(df['Cond G'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond G')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond G doit être inférieure à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>pH G moyen : {np.around(df['pH G'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH G')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH G doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cond H moyen en (mS/cm): {np.around(df['Cond H'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond H')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond H doit être inférieure à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>pH H moyen : {np.around(df['pH H'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH H')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH H doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
    elif (unity == "QT") & (phase =="sortie_global"):
        df = pd.read_excel(df,sheet_name="QT_sortie_global")
        col1,col2 = st.columns((2))
        
        df = df[(df["date"] >= date1) & (df["date"] <= date2)]
        df.replace('/', np.nan, inplace=True)
        df.replace('en cours', np.nan, inplace=True)

        with col1:
            st.markdown(f"<h2 style='text-align: center;'>pH moyen: {np.around(df['pH'].mean(),2)}</h2>", unsafe_allow_html=True)        
            fig = px.line(df,x="date",y="pH")
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Cond. (mS/cm) à 25° C moyen: {np.around(df['Cond. (mS/cm) à 25° C'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="Cond. (mS/cm) à 25° C")
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond A doit être inférieure à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Turb (NTU) moyenne: {np.around(df['Turb (NTU)'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="Turb (NTU)")
            fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0.1,  # Position Y (sur la ligne horizontale)
                        text="Turb doit être inférieure à 0.1",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>TDS (mg/l) moyenne: {np.around(df['TDS (mg/l)'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="TDS (mg/l)")
            fig.add_hline(y=310, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=310,  # Position Y (sur la ligne horizontale)
                        text="TDS doit être inférieure à 310",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200) 
    #filtrage selon l'unité ESLI
    elif (unity == "ESLI") & (phase =="intake"):
        df = pd.read_excel(df,sheet_name="ESLI_intake")
        col1,col2 = st.columns((2))
        df = df[(df["date"] >= date1) & (df["date"] <= date2)]
        df.replace('/', np.nan, inplace=True)
        df.replace('en cours', np.nan, inplace=True)
        df['TDS (mg/l)'].replace(0, np.nan, inplace=True)
        df['TOC (mg/l)'] = df['TOC (mg/l)'].replace('<3',1)
        df['TOC (mg/l)'] = df['TOC (mg/l)'].astype(float)
        df.loc[df['TOC (mg/l)'] < 3, 'TOC (mg/l)'] = 1
        df.loc[df['TOC (mg/l)'] > 3, 'TOC (mg/l)'] = 0
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cond. (mS/cm) à 25° C moyen: {np.around(df['Cond. (mS/cm) à 25° C'].mean(),2)}</h2>", unsafe_allow_html=True)        
            fig = px.line(df,x="date",y="Cond. (mS/cm) à 25° C")
            # fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
            # fig.add_annotation(
            #         x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
            #         y=0.1,  # Position Y (sur la ligne horizontale)
            #         text="Cond. (mS/cm) à 25° C doit être inférieur ou égale à 0.1",  # Texte de l'annotation
            #         showarrow=True,  # Afficher une flèche pointant vers le point
            #         arrowhead=2,  # Type de flèche
            #         ax=0,  # Position X de la flèche par rapport au texte
            #         ay=-40  # Position Y de la flèche par rapport au texte
            #     )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Turb (NTU) moyen: {np.around(df['Turb (NTU)'].mean(),2)}</h2>", unsafe_allow_html=True)        
            fig = px.line(df,x="date",y="Turb (NTU)")
            # fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
            # fig.add_annotation(
            #         x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
            #         y=0.1,  # Position Y (sur la ligne horizontale)
            #         text="Turb (NTU) doit être inférieur ou égale à 0.1",  # Texte de l'annotation
            #         showarrow=True,  # Afficher une flèche pointant vers le point
            #         arrowhead=2,  # Type de flèche
            #         ax=0,  # Position X de la flèche par rapport au texte
            #         ay=-40  # Position Y de la flèche par rapport au texte
            #     )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>PO43- (mg/l) moyen: {np.around(df['PO43- (mg/l)'].mean(),2)}</h2>", unsafe_allow_html=True)        
            fig = px.line(df,x="date",y="PO43- (mg/l)")
            fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                    x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                    y=0.1,  # Position Y (sur la ligne horizontale)
                    text="PO43- doit être inférieur ou égale à 0.1",  # Texte de l'annotation
                    showarrow=True,  # Afficher une flèche pointant vers le point
                    arrowhead=2,  # Type de flèche
                    ax=0,  # Position X de la flèche par rapport au texte
                    ay=-40  # Position Y de la flèche par rapport au texte
                )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SiO2 (mg/l) moyen: {np.around(df['SiO2 (mg/l)'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="SiO2 (mg/l)")
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>TOC (mg/l) moyenne: {np.around(df['TOC (mg/l)'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="TOC (mg/l)")
            fig.add_hline(y=1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                    x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                    y=1,  # Position Y (sur la ligne horizontale)
                    text="TOC doit être égale à 1",  # Texte de l'annotation
                    showarrow=True,  # Afficher une flèche pointant vers le point
                    arrowhead=2,  # Type de flèche
                    ax=0,  # Position X de la flèche par rapport au texte
                    ay=-40  # Position Y de la flèche par rapport au texte
                )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>MES  (mg/l) moyenne: {np.around(df['MES  (mg/l)'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="MES  (mg/l)")
            fig.add_hline(y=10, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                    x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                    y=10,  # Position Y (sur la ligne horizontale)
                    text="MES doit être inférieur ou égale à 10",  # Texte de l'annotation
                    showarrow=True,  # Afficher une flèche pointant vers le point
                    arrowhead=2,  # Type de flèche
                    ax=0,  # Position X de la flèche par rapport au texte
                    ay=-40  # Position Y de la flèche par rapport au texte
                )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cl2 libre (mg/l) moyenne: {np.around(df['Cl2 libre (mg/l)'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="Cl2 libre (mg/l)")
            fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                    x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                    y=0,  # Position Y (sur la ligne horizontale)
                    text="Cl2 libre doit être égale à 0",  # Texte de l'annotation
                    showarrow=True,  # Afficher une flèche pointant vers le point
                    arrowhead=2,  # Type de flèche
                    ax=0,  # Position X de la flèche par rapport au texte
                    ay=-40  # Position Y de la flèche par rapport au texte
                )
            st.plotly_chart(fig,use_container_width=True,height = 200)   
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>pH moyenne: {np.around(df['pH'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="pH")
            # fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=2)
            # fig.add_annotation(
            #         x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
            #         y=0,  # Position Y (sur la ligne horizontale)
            #         text="Cl2 libre doit être égale à 0",  # Texte de l'annotation
            #         showarrow=True,  # Afficher une flèche pointant vers le point
            #         arrowhead=2,  # Type de flèche
            #         ax=0,  # Position X de la flèche par rapport au texte
            #         ay=-40  # Position Y de la flèche par rapport au texte
            #     )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>TDS (mg/l) moyenne: {np.around(df['TDS (mg/l)'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="TDS (mg/l)")
            st.plotly_chart(fig,use_container_width=True,height = 200)
    elif (unity == "ESLI") & (phase =="PERMEAT FILTRATION"):
        df = pd.read_excel(df,sheet_name="ESLI_PERMEAT FILTRATION")
        col1,col2, = st.columns((2))
        # df['date'] = pd.to_datetime(df['date'])

        # startDate = pd.to_datetime(df["date"]).min()
        # endDate = pd.to_datetime(df["date"]).max()

        # with col1:
        #     date1 = pd.to_datetime(st.date_input("Start Date", startDate))

        # with col2:
        #     date2 = pd.to_datetime(st.date_input("End Date", endDate))
        df = df[(df["date"] >= date1) & (df["date"] <= date2)]
        df.replace('/', np.nan, inplace=True)
        df.replace('en cours', np.nan, inplace=True)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Fe2+ (mg/l) Zone A  moyen : {np.around(df['Fe2+ (mg/l) Zone A'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Fe2+ (mg/l) Zone A')
            fig.add_hline(y=0.2, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0.2,  # Position Y (sur la ligne horizontale)
                        text="Fe2+ doit être inférieure à 0.2",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Fe3+ (mg/l) Zone A  moyen : {np.around(pd.to_numeric(df['Fe3+ (mg/l) Zone A'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Fe3+ (mg/l) Zone A')
            fig.add_hline(y=0.2, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0.2,  # Position Y (sur la ligne horizontale)
                        text="Fe3+ doit être inférieure à 0.2",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>MES (mg/l) Zone A moyen : {np.around(pd.to_numeric(df['MES (mg/l) Zone A'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='MES (mg/l) Zone A')
            fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0,  # Position Y (sur la ligne horizontale)
                        text="MES doit être égale à 0",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)

        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 Zone A moyen : {np.around(pd.to_numeric(df['SDI15 Zone A'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='SDI15 Zone A')
            fig.add_hline(y=2.5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=2.5,  # Position Y (sur la ligne horizontale)
                        text="SDI15 doit être inférieure à 2.5",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)

        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Fe2+ (mg/l) Zone B moyen : {np.around(pd.to_numeric(df['Fe2+ (mg/l) Zone B'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Fe2+ (mg/l) Zone B')
            fig.add_hline(y=0.2, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0.2,  # Position Y (sur la ligne horizontale)
                        text="Fe2+ doit être inférieure à 0.2",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Fe3+ (mg/l) Zone B moyen : {np.around(pd.to_numeric(df['Fe3+ (mg/l) Zone B'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Fe3+ (mg/l) Zone B')
            fig.add_hline(y=0.2, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0.2,  # Position Y (sur la ligne horizontale)
                        text="Fe3+ doit être inférieure à 0.2",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>MES (mg/l) Zone B moyen : {np.around(pd.to_numeric(df['MES (mg/l) Zone B'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='MES (mg/l) Zone B')
            fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0,  # Position Y (sur la ligne horizontale)
                        text="MES doit être égale à 0",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 Zone B moyen : {np.around(pd.to_numeric(df['SDI15 Zone B'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='SDI15 Zone B')
            fig.add_hline(y=2.5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=2.5,  # Position Y (sur la ligne horizontale)
                        text="SDI15 doit être inférieure à 2.5",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Fe2+ (mg/l) Zone C moyen : {np.around(pd.to_numeric(df['Fe2+ (mg/l) Zone C'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Fe2+ (mg/l) Zone C')
            fig.add_hline(y=0.2, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0.2,  # Position Y (sur la ligne horizontale)
                        text="Fe2+ doit être inférieure à 0.2",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Fe3+ (mg/l) Zone C moyen : {np.around(pd.to_numeric(df['Fe3+ (mg/l) Zone C'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Fe3+ (mg/l) Zone C')
            fig.add_hline(y=0.2, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0.2,  # Position Y (sur la ligne horizontale)
                        text="Fe3+ doit être inférieure à 0.2",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>MES (mg/l) Zone C moyen : {np.around(pd.to_numeric(df['MES (mg/l) Zone C'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='MES (mg/l) Zone C')
            fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0,  # Position Y (sur la ligne horizontale)
                        text="MES doit être égale à 0",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 Zone C moyen : {np.around(pd.to_numeric(df['SDI15 Zone C'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='SDI15 Zone C')
            fig.add_hline(y=2.5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=2.5,  # Position Y (sur la ligne horizontale)
                        text="SDI15 doit être inférieure à 2.5",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
    elif (unity == "ESLI") & (phase =="APRES FILTRES A CARTOUCHE"):
        df = pd.read_excel(df,sheet_name="ESLI_APRES FILTRES A CARTOUCHE")
        col1,col2 = st.columns((2))
        # df['date'] = pd.to_datetime(df['date'])

        # startDate = pd.to_datetime(df["date"]).min()
        # endDate = pd.to_datetime(df["date"]).max()

        # with col1:
        #     date1 = pd.to_datetime(st.date_input("Start Date", startDate))

        # with col2:
        #     date2 = pd.to_datetime(st.date_input("End Date", endDate))

        df = df[(df["date"] >= date1) & (df["date"] <= date2)]
        df.replace('/', np.nan, inplace=True)
        df.replace('en cours', np.nan, inplace=True)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>pH ZONE A moyen : {np.around(pd.to_numeric(df['pH ZONE A'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH ZONE A')
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>T (°C)  ZONE A moyen : {np.around(pd.to_numeric(df['T (°C)  ZONE A'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='T (°C)  ZONE A')
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>ORP (mV)  ZONE A moyen : {np.around(pd.to_numeric(df['ORP (mV)  ZONE A'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='ORP (mV)  ZONE A')
            fig.add_hline(y=300, line_dash="dash", line_color="red", line_width=2)
            fig.add_hline(y=250, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=250,  # Position Y (sur la ligne horizontale)
                        text="Min 250 mv",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=300,  # Position Y (sur la ligne horizontale)
                        text="Max 300 mv",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SDI15  ZONE A moyen : {np.around(pd.to_numeric(df['SDI15  ZONE A'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='SDI15  ZONE A')
            fig.add_hline(y=2.5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=2.50,  # Position Y (sur la ligne horizontale)
                        text="SDI15  doit être inférieur à 2.5",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>PO43-  (mg/l)  ZONE A moyen : {np.around(pd.to_numeric(df['PO43-  (mg/l)  ZONE A'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='PO43-  (mg/l)  ZONE A')
            fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0,  # Position Y (sur la ligne horizontale)
                        text="PO43-  doit être égale à 0",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>TDS (mg/l)  ZONE A moyen : {np.around(pd.to_numeric(df['TDS (mg/l)  ZONE A'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='TDS (mg/l)  ZONE A')
            fig.add_hline(y=40000, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=40000,  # Position Y (sur la ligne horizontale)
                        text="TDS  doit être inférieur à 40 000",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
            st.markdown(f"<h2 style='text-align: center;'>pH ZONE B moyen : {np.around(pd.to_numeric(df['pH  ZONE B'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH  ZONE B')
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>T (°C)  ZONE B moyen : {np.around(pd.to_numeric(df['T (°C) ZONE B'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='T (°C) ZONE B')
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>ORP (mV)  ZONE B moyen : {np.around(pd.to_numeric(df['ORP (mV) ZONE B'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='ORP (mV) ZONE B')
            fig.add_hline(y=300, line_dash="dash", line_color="red", line_width=2)
            fig.add_hline(y=250, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=250,  # Position Y (sur la ligne horizontale)
                        text="Min 250 mv",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=300,  # Position Y (sur la ligne horizontale)
                        text="Max 300 mv",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>SDI15  ZONE B moyen : {np.around(pd.to_numeric(df['SDI15 ZONE B'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='SDI15 ZONE B')
            fig.add_hline(y=2.5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=2.50,  # Position Y (sur la ligne horizontale)
                        text="SDI15  doit être inférieur à 2.5",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>PO43-  (mg/l)  ZONE B moyen : {np.around(pd.to_numeric(df['PO43-  (mg/l) ZONE B'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='PO43-  (mg/l) ZONE B')
            fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0,  # Position Y (sur la ligne horizontale)
                        text="PO43-  doit être égale à 0",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>TDS (mg/l)  ZONE B moyen : {np.around(pd.to_numeric(df['TDS (mg/l) ZONE B'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='TDS (mg/l) ZONE B')
            fig.add_hline(y=40000, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=40000,  # Position Y (sur la ligne horizontale)
                        text="TDS  doit être inférieur à 40 000",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
            st.markdown(f"<h2 style='text-align: center;'>pH ZONE C moyen : {np.around(pd.to_numeric(df['pH ZONE C'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH ZONE C')
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>T (°C)  ZONE C moyen : {np.around(pd.to_numeric(df['T (°C) ZONE C'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='T (°C) ZONE C')
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>ORP (mV)  ZONE C moyen : {np.around(pd.to_numeric(df['ORP (mV) ZONE C'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='ORP (mV) ZONE C')
            fig.add_hline(y=300, line_dash="dash", line_color="red", line_width=2)
            fig.add_hline(y=250, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=250,  # Position Y (sur la ligne horizontale)
                        text="Min 250 mv",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=300,  # Position Y (sur la ligne horizontale)
                        text="Max 300 mv",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SDI15  ZONE C moyen : {np.around(pd.to_numeric(df['SDI15 ZONE C'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='SDI15 ZONE C')
            fig.add_hline(y=2.5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=2.50,  # Position Y (sur la ligne horizontale)
                        text="SDI15  doit être inférieur à 2.5",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>PO43-  (mg/l)  ZONE C moyen : {np.around(pd.to_numeric(df['PO43-  (mg/l) ZONE C'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='PO43-  (mg/l) ZONE C')
            fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0,  # Position Y (sur la ligne horizontale)
                        text="PO43-  doit être égale à 0",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>TDS (mg/l)  ZONE C moyen : {np.around(pd.to_numeric(df['TDS (mg/l) ZONE C'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='TDS (mg/l) ZONE C')
            fig.add_hline(y=40000, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=40000,  # Position Y (sur la ligne horizontale)
                        text="TDS  doit être inférieur à 40 000",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
    elif (unity == "ESLI") & (phase =="PERMEAT RO"):
        df = pd.read_excel(df,sheet_name="ESLI_PERMEAT RO")
        col1,col2 = st.columns((2))
        df = df[(df["date"] >= date1) & (df["date"] <= date2)]
        df.replace('/', np.nan, inplace=True)
        df.replace('#VALEUR!', np.nan, inplace=True)
        df.replace('en cours', np.nan, inplace=True)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cond A1 moyen : {np.around(pd.to_numeric(df['Cond A1'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond A1')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond doit être inférieur à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Cond A2 moyen : {np.around(pd.to_numeric(df['Cond A2'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond A2')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond doit être inférieur à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cond A3 moyen : {np.around(pd.to_numeric(df['Cond A3'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond A3')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond doit être inférieur à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Cond A4 moyen : {np.around(pd.to_numeric(df['Cond A4'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond A4')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond doit être inférieur à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cond B1 moyen : {np.around(pd.to_numeric(df['Cond B1'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond B1')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond doit être inférieur à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Cond B2 moyen : {np.around(pd.to_numeric(df['Cond B2'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond B2')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond doit être inférieur à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cond B3 moyen : {np.around(pd.to_numeric(df['Cond B3'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond B3')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond doit être inférieur à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Cond B4 moyen : {np.around(pd.to_numeric(df['Cond B4'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond B4')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond doit être inférieur à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cond C1 moyen : {np.around(pd.to_numeric(df['Cond C1'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond C1')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond doit être inférieur à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Cond C2 moyen : {np.around(pd.to_numeric(df['Cond C2'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond C2')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond doit être inférieur à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cond C3 moyen : {np.around(pd.to_numeric(df['Cond C3'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond C3')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond doit être inférieur à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Cond C4 moyen : {np.around(pd.to_numeric(df['Cond C4'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond C4')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond doit être inférieur à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Ph A1 moyen : {np.around(pd.to_numeric(df['Ph A1'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Ph A1')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Ph A2 moyen : {np.around(pd.to_numeric(df['Ph A2'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Ph A2')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Ph A3 moyen : {np.around(pd.to_numeric(df['Ph A3'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Ph A3')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Ph A4 moyen : {np.around(pd.to_numeric(df['Ph A4'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Ph A4')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Ph B1 moyen : {np.around(pd.to_numeric(df['Ph B1'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Ph B1')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Ph B2 moyen : {np.around(pd.to_numeric(df['Ph b2'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Ph b2')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Ph B3 moyen : {np.around(pd.to_numeric(df['Ph B3'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Ph B3')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Ph B4 moyen : {np.around(pd.to_numeric(df['Ph B4'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Ph B4')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Ph C1 moyen : {np.around(pd.to_numeric(df['Ph C1'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Ph C1')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Ph C2 moyen : {np.around(pd.to_numeric(df['Ph C2'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Ph C2')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Ph C3 moyen : {np.around(pd.to_numeric(df['Ph C3'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Ph C3')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Ph C4 moyen : {np.around(pd.to_numeric(df['Ph C4'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Ph C4')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
    #filtrage selon l'unité ION EXCHANGE
    elif (unity == "ION EXCHANGE") & (phase =="intake"):
        df = pd.read_excel(df,sheet_name="ION_intake")
        # print(df.columns)
        col1,col2 = st.columns((2))
        df = df[(df["date"] >= date1) & (df["date"] <= date2)]
        df.replace('/', np.nan, inplace=True)
        df.replace('en cours', np.nan, inplace=True)
        df['TDS (mg/l)'].replace(0, np.nan, inplace=True)
        df['TOC (mg/l)'] = df['TOC (mg/l)'].replace('<3',1)
        df['TOC (mg/l)'] = df['TOC (mg/l)'].astype(float)
        df.loc[df['TOC (mg/l)'] < 3, 'TOC (mg/l)'] = 1
        df.loc[df['TOC (mg/l)'] > 3, 'TOC (mg/l)'] = 0
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cond. (mS/cm) à 25° C moyen: {np.around(df['Cond. (mS/cm) à 25° C'].mean(),2)}</h2>", unsafe_allow_html=True)        
            fig = px.line(df,x="date",y="Cond. (mS/cm) à 25° C")
            # fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
            # fig.add_annotation(
            #         x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
            #         y=0.1,  # Position Y (sur la ligne horizontale)
            #         text="Cond. (mS/cm) à 25° C doit être inférieur ou égale à 0.1",  # Texte de l'annotation
            #         showarrow=True,  # Afficher une flèche pointant vers le point
            #         arrowhead=2,  # Type de flèche
            #         ax=0,  # Position X de la flèche par rapport au texte
            #         ay=-40  # Position Y de la flèche par rapport au texte
            #     )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Turb (NTU) moyen: {np.around(df['Turb (NTU)'].mean(),2)}</h2>", unsafe_allow_html=True)        
            fig = px.line(df,x="date",y="Turb (NTU)")
            # fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
            # fig.add_annotation(
            #         x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
            #         y=0.1,  # Position Y (sur la ligne horizontale)
            #         text="Turb (NTU) doit être inférieur ou égale à 0.1",  # Texte de l'annotation
            #         showarrow=True,  # Afficher une flèche pointant vers le point
            #         arrowhead=2,  # Type de flèche
            #         ax=0,  # Position X de la flèche par rapport au texte
            #         ay=-40  # Position Y de la flèche par rapport au texte
            #     )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>PO43- (mg/l) moyen: {np.around(df['PO43- (mg/l)'].mean(),2)}</h2>", unsafe_allow_html=True)        
            fig = px.line(df,x="date",y="PO43- (mg/l)")
            fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                    x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                    y=0.1,  # Position Y (sur la ligne horizontale)
                    text="PO43- doit être inférieur ou égale à 0.1",  # Texte de l'annotation
                    showarrow=True,  # Afficher une flèche pointant vers le point
                    arrowhead=2,  # Type de flèche
                    ax=0,  # Position X de la flèche par rapport au texte
                    ay=-40  # Position Y de la flèche par rapport au texte
                )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SiO2 (mg/l) moyen: {np.around(df['SiO2 (mg/l)'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="SiO2 (mg/l)")
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>TOC (mg/l) moyenne: {np.around(df['TOC (mg/l)'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="TOC (mg/l)")
            fig.add_hline(y=1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                    x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                    y=1,  # Position Y (sur la ligne horizontale)
                    text="TOC doit être égale à 1",  # Texte de l'annotation
                    showarrow=True,  # Afficher une flèche pointant vers le point
                    arrowhead=2,  # Type de flèche
                    ax=0,  # Position X de la flèche par rapport au texte
                    ay=-40  # Position Y de la flèche par rapport au texte
                )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>MES  (mg/l) moyenne: {np.around(df['MES  (mg/l)'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="MES  (mg/l)")
            fig.add_hline(y=10, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                    x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                    y=10,  # Position Y (sur la ligne horizontale)
                    text="MES doit être inférieur ou égale à 10",  # Texte de l'annotation
                    showarrow=True,  # Afficher une flèche pointant vers le point
                    arrowhead=2,  # Type de flèche
                    ax=0,  # Position X de la flèche par rapport au texte
                    ay=-40  # Position Y de la flèche par rapport au texte
                )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cl2 libre (mg/l) moyenne: {np.around(df['Cl2 libre (mg/l)'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="Cl2 libre (mg/l)")
            fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                    x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                    y=0,  # Position Y (sur la ligne horizontale)
                    text="Cl2 libre doit être égale à 0",  # Texte de l'annotation
                    showarrow=True,  # Afficher une flèche pointant vers le point
                    arrowhead=2,  # Type de flèche
                    ax=0,  # Position X de la flèche par rapport au texte
                    ay=-40  # Position Y de la flèche par rapport au texte
                )
            st.plotly_chart(fig,use_container_width=True,height = 200)   
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>pH moyenne: {np.around(df['pH'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="pH")
            # fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=2)
            # fig.add_annotation(
            #         x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
            #         y=0,  # Position Y (sur la ligne horizontale)
            #         text="Cl2 libre doit être égale à 0",  # Texte de l'annotation
            #         showarrow=True,  # Afficher une flèche pointant vers le point
            #         arrowhead=2,  # Type de flèche
            #         ax=0,  # Position X de la flèche par rapport au texte
            #         ay=-40  # Position Y de la flèche par rapport au texte
            #     )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>TDS (mg/l) moyenne: {np.around(df['TDS (mg/l)'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="TDS (mg/l)")
            st.plotly_chart(fig,use_container_width=True,height = 200)
    elif (unity == "ION EXCHANGE") & (phase =="PERMEAT FILTRATION"):
        df = pd.read_excel(df,sheet_name="ION_PERMEAT FILTRATION")
        col1,col2, = st.columns((2))

        df = df[(df["date"] >= date1) & (df["date"] <= date2)]
        df.replace('/', np.nan, inplace=True)
        df.replace('en cours', np.nan, inplace=True)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Turb (NTU) HMMF A moyen : {np.around(pd.to_numeric(df['Turb (NTU) HMMF A'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Turb (NTU) HMMF A')
            fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0.1,  # Position Y (sur la ligne horizontale)
                        text="Turb doit être inférieur à 0.1",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 HMMF A moyen : {np.around(pd.to_numeric(df['SDI15 HMMF A'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='SDI15 HMMF A')
            fig.add_hline(y=5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5,  # Position Y (sur la ligne horizontale)
                        text="SDI15 doit être inférieur à 5",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 HMMF B moyen : {np.around(pd.to_numeric(df['Turb (NTU) HMMF B'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Turb (NTU) HMMF B')
            fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0.1,  # Position Y (sur la ligne horizontale)
                        text="Turb doit être inférieur à 0.1",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 HMMF B moyen : {np.around(pd.to_numeric(df['SDI15 HMMF B'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='SDI15 HMMF B')
            fig.add_hline(y=5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5,  # Position Y (sur la ligne horizontale)
                        text="SDI15 doit être inférieur à 5",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 HMMF C moyen : {np.around(pd.to_numeric(df['Turb (NTU) HMMF C'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Turb (NTU) HMMF C')
            fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0.1,  # Position Y (sur la ligne horizontale)
                        text="Turb doit être inférieur à 0.1",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 HMMF C moyen : {np.around(pd.to_numeric(df['SDI15 HMMF C'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='SDI15 HMMF C')
            fig.add_hline(y=5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5,  # Position Y (sur la ligne horizontale)
                        text="SDI15 doit être inférieur à 5",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200) 
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 HMMF D moyen : {np.around(pd.to_numeric(df['Turb (NTU) HMMF D'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Turb (NTU) HMMF D')
            fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0.1,  # Position Y (sur la ligne horizontale)
                        text="Turb doit être inférieur à 0.1",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 HMMF D moyen : {np.around(pd.to_numeric(df['SDI15 HMMF D'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='SDI15 HMMF D')
            fig.add_hline(y=5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5,  # Position Y (sur la ligne horizontale)
                        text="SDI15 doit être inférieur à 5",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)  
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 HMMF E moyen : {np.around(pd.to_numeric(df['Turb (NTU) HMMF B'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Turb (NTU) HMMF B')
            fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0.1,  # Position Y (sur la ligne horizontale)
                        text="Turb doit être inférieur à 0.1",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 HMMF E moyen : {np.around(pd.to_numeric(df['SDI15 HMMF E'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='SDI15 HMMF E')
            fig.add_hline(y=5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5,  # Position Y (sur la ligne horizontale)
                        text="SDI15 doit être inférieur à 5",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 HMMF F moyen : {np.around(pd.to_numeric(df['Turb (NTU) HMMF F'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Turb (NTU) HMMF F')
            fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0.1,  # Position Y (sur la ligne horizontale)
                        text="Turb doit être inférieur à 0.1",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 HMMF F moyen : {np.around(pd.to_numeric(df['SDI15 HMMF F'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='SDI15 HMMF F')
            fig.add_hline(y=5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5,  # Position Y (sur la ligne horizontale)
                        text="SDI15 doit être inférieur à 5",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 HMMF G moyen : {np.around(pd.to_numeric(df['Turb (NTU) HMMF G'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Turb (NTU) HMMF G')
            fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0.1,  # Position Y (sur la ligne horizontale)
                        text="Turb doit être inférieur à 0.1",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 HMMF G moyen : {np.around(pd.to_numeric(df['SDI15 HMMF G'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='SDI15 HMMF G')
            fig.add_hline(y=5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5,  # Position Y (sur la ligne horizontale)
                        text="SDI15 doit être inférieur à 5",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 HMMF H moyen: moyen : {np.around(pd.to_numeric(df['Turb (NTU) HMMF H'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Turb (NTU) HMMF H')
            fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0.1,  # Position Y (sur la ligne horizontale)
                        text="Turb doit être inférieur à 0.1",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 HMMF H moyen : {np.around(pd.to_numeric(df['SDI15 HMMF H'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='SDI15 HMMF H')
            fig.add_hline(y=5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5,  # Position Y (sur la ligne horizontale)
                        text="SDI15 doit être inférieur à 5",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 HMMF I moyen : {np.around(pd.to_numeric(df['Turb (NTU) HMMF I'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Turb (NTU) HMMF I')
            fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0.1,  # Position Y (sur la ligne horizontale)
                        text="Turb doit être inférieur à 0.1",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 HMMF I moyen : {np.around(pd.to_numeric(df['SDI15 HMMF I'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='SDI15 HMMF I')
            fig.add_hline(y=5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5,  # Position Y (sur la ligne horizontale)
                        text="SDI15 doit être inférieur à 5",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 HMMF J moyen : {np.around(pd.to_numeric(df['Turb (NTU) HMMF J'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Turb (NTU) HMMF J')
            fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0.1,  # Position Y (sur la ligne horizontale)
                        text="Turb doit être inférieur à 0.1",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 HMMF J moyen : {np.around(pd.to_numeric(df['SDI15 HMMF J'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='SDI15 HMMF J')
            fig.add_hline(y=5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5,  # Position Y (sur la ligne horizontale)
                        text="SDI15 doit être inférieur à 5",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SDI 15 Collecteur moyen: {np.around(df['SDI 15 Collecteur'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='SDI 15 Collecteur')
            fig.add_hline(y=5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5,  # Position Y (sur la ligne horizontale)
                        text="SDI15 doit être inférieur à 5",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
    elif (unity == "ION EXCHANGE") & (phase =="Bac_stockage"):
        df = pd.read_excel(df,sheet_name="ION_Bac_stockage")
        # print(df.columns)
        col1,col2 = st.columns((2))
        # df['date'] = pd.to_datetime(df['date'])

        # startDate = pd.to_datetime(df["date"]).min()
        # endDate = pd.to_datetime(df["date"]).max()

        # with col1:
        #     date1 = pd.to_datetime(st.date_input("Start Date", startDate))

        # with col2:
        #     date2 = pd.to_datetime(st.date_input("End Date", endDate))
        df = df[(df["date"] >= date1) & (df["date"] <= date2)]
        df.replace('/', np.nan, inplace=True)
        df.replace('en cours', np.nan, inplace=True)
        df['TOC (mg/l)'] = df['TOC (mg/l)'].replace('<3',1)
        df['TOC (mg/l)'] = df['TOC (mg/l)'].astype(float)
        df.loc[df['TOC (mg/l)'] < 3, 'TOC (mg/l)'] = 1
        df.loc[df['TOC (mg/l)'] > 3, 'TOC (mg/l)'] = 0
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>pH moyen : {np.around(pd.to_numeric(df['pH'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH')
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Turb (NTU) moyen : {np.around(pd.to_numeric(df['Turb (NTU)'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Turb (NTU)')
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Fe2+ (mg/l) moyen : {np.around(pd.to_numeric(df['Fe2+ (mg/l)'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Fe2+ (mg/l)')
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Fe3+ (mg/l) moyen : {np.around(pd.to_numeric(df['Fe3+ (mg/l)'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Fe3+ (mg/l)')
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>TOC (mg/l) moyen : {np.around(pd.to_numeric(df['TOC (mg/l)'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='TOC (mg/l)')
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SiO2 (mg/l) moyen : {np.around(pd.to_numeric(df['SiO2 (mg/l)'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='SiO2 (mg/l)')
            st.plotly_chart(fig,use_container_width=True,height = 200) 
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>PO43- (mg/l) moyen : {np.around(pd.to_numeric(df['PO43- (mg/l)'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='PO43- (mg/l)')
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Cl2 libre (mg/l) moyen : {np.around(pd.to_numeric(df['Cl2 libre (mg/l)'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cl2 libre (mg/l)')
            st.plotly_chart(fig,use_container_width=True,height = 200)  
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>TDS (mg/l) moyen : {np.around(pd.to_numeric(df['TDS (mg/l)'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='TDS (mg/l)')
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 moyen : {np.around(pd.to_numeric(df['SDI15'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='SDI15')
            st.plotly_chart(fig,use_container_width=True,height = 200)
    elif (unity == "ION EXCHANGE") & (phase =="APRES FILTRES A CARTOUCHE"):
        df = pd.read_excel(df,sheet_name="ION_APRES FILTRES A CARTOUCHE")
        col1,col2 = st.columns((2))
        # df['date'] = pd.to_datetime(df['date'])

        # startDate = pd.to_datetime(df["date"]).min()
        # endDate = pd.to_datetime(df["date"]).max()

        # with col1:
        #     date1 = pd.to_datetime(st.date_input("Start Date", startDate))

        # with col2:
        #     date2 = pd.to_datetime(st.date_input("End Date", endDate))

        df = df[(df["date"] >= date1) & (df["date"] <= date2)]
        df.replace('/', np.nan, inplace=True)
        df.replace('en cours', np.nan, inplace=True)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>ORP (mV) Collecteur A,B,C,D,E moyen : {np.around(pd.to_numeric(df['ORP (mV) Collecteur A,B,C,D,E'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='ORP (mV) Collecteur A,B,C,D,E')
            fig.add_hline(y=250, line_dash="dash", line_color="red", line_width=2)
            fig.add_hline(y=300, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=300,  # Position Y (sur la ligne horizontale)
                        text="Max 250 mv",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=250,  # Position Y (sur la ligne horizontale)
                        text="Min 250 mv",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>ORP (mV) Collecteur F,G,H,I,J moyen : {np.around(pd.to_numeric(df['ORP (mV) Collecteur F,G,H,I,J'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='ORP (mV) Collecteur F,G,H,I,J')
            fig.add_hline(y=250, line_dash="dash", line_color="red", line_width=2)
            fig.add_hline(y=300, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=300,  # Position Y (sur la ligne horizontale)
                        text="Max 250 mv",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=250,  # Position Y (sur la ligne horizontale)
                        text="Min 250 mv",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 Collecteur A,B,C,D,E moyen: {np.around(pd.to_numeric(df['SDI15 Collecteur A,B,C,D,E'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='SDI15 Collecteur A,B,C,D,E')
            fig.add_hline(y=5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5,  # Position Y (sur la ligne horizontale)
                        text="SDI15 doit être inférieur à 5",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 Collecteur F,G,H,I,J moyen: {np.around(pd.to_numeric(df['SDI15 Collecteur F,G,H,I,J'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='SDI15 Collecteur F,G,H,I,J')
            fig.add_hline(y=5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5,  # Position Y (sur la ligne horizontale)
                        text="SDI15 doit être inférieur à 5",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
    elif (unity == "ION EXCHANGE") & (phase =="PERMEAT RO"):
        df = pd.read_excel(df,sheet_name="ION_PERMEAT RO")
        col1,col2 = st.columns((2))
        df = df[(df["date"] >= date1) & (df["date"] <= date2)]
        df.replace('/', np.nan, inplace=True)
        df.replace('#VALEUR!', np.nan, inplace=True)
        df.replace('en cours', np.nan, inplace=True)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cond A moyen : {np.around(pd.to_numeric(df['Cond A'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond A')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond doit être inférieur à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Cond B moyen : {np.around(pd.to_numeric(df['Cond B'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond B')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond doit être inférieur à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cond C moyen : {np.around(pd.to_numeric(df['Cond C'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond C')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond doit être inférieur à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Cond D moyen : {np.around(pd.to_numeric(df['Cond D'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond D')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond doit être inférieur à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cond E moyen : {np.around(pd.to_numeric(df['Cond E'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond E')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond doit être inférieur à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Cond F moyen : {np.around(pd.to_numeric(df['Cond F'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond F')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond doit être inférieur à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cond G moyen : {np.around(pd.to_numeric(df['Cond G'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond G')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond doit être inférieur à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Cond H moyen : {np.around(pd.to_numeric(df['Cond H'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond H')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond doit être inférieur à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)

        with col1:
            st.markdown(f"<h2 style='text-align: center;'>pH A moyen : {np.around(pd.to_numeric(df['pH A'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH A')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>pH B moyen : {np.around(pd.to_numeric(df['pH B'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH B')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>pH C moyen : {np.around(pd.to_numeric(df['pH C'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH C')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>pH D moyen : {np.around(pd.to_numeric(df['pH d '], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH d ')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>pH E moyen : {np.around(pd.to_numeric(df['pH E'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH E')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>pH F moyen : {np.around(pd.to_numeric(df['pH F '], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH F ')
            fig.add_hline(y=5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5,  # Position Y (sur la ligne horizontale)
                        text="pH doit être inférieur à 5",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>pH G moyen : {np.around(pd.to_numeric(df['pH G'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH G')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>pH H moyen : {np.around(pd.to_numeric(df[' pH H'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y=' pH H')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
    # filtrage selon l'unité MCT
    elif (unity == "MCT") & (phase =="intake"):
        df = pd.read_excel(df,sheet_name="MCT_intake")
        col1,col2 = st.columns((2))

        df = df[(df["date"] >= date1) & (df["date"] <= date2)]
        df.replace('/', np.nan, inplace=True)
        df.replace('en cours', np.nan, inplace=True)
        df['TDS (mg/l)'].replace(0, np.nan, inplace=True)
        df['TOC (mg/l)'] = df['TOC (mg/l)'].replace('<3',1)
        df['TOC (mg/l)'] = df['TOC (mg/l)'].astype(float)
        df.loc[df['TOC (mg/l)'] < 3, 'TOC (mg/l)'] = 1
        df.loc[df['TOC (mg/l)'] > 3, 'TOC (mg/l)'] = 0
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cond. (mS/cm) à 25° C moyen: {np.around(df['Cond. (mS/cm) à 25° C'].mean(),2)}</h2>", unsafe_allow_html=True)        
            fig = px.line(df,x="date",y="Cond. (mS/cm) à 25° C")
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Turb (NTU) moyen: {np.around(df['Turb (NTU)'].mean(),2)}</h2>", unsafe_allow_html=True)        
            fig = px.line(df,x="date",y="Turb (NTU)")
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>PO43- (mg/l) moyen: {np.around(df['PO43- (mg/l)'].mean(),2)}</h2>", unsafe_allow_html=True)        
            fig = px.line(df,x="date",y="PO43- (mg/l)")
            fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                    x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                    y=0.1,  # Position Y (sur la ligne horizontale)
                    text="PO43- doit être inférieur ou égale à 0.1",  # Texte de l'annotation
                    showarrow=True,  # Afficher une flèche pointant vers le point
                    arrowhead=2,  # Type de flèche
                    ax=0,  # Position X de la flèche par rapport au texte
                    ay=-40  # Position Y de la flèche par rapport au texte
                )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SiO2 (mg/l) moyen: {np.around(df['SiO2 (mg/l)'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="SiO2 (mg/l)")
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>TOC (mg/l) moyenne: {np.around(df['TOC (mg/l)'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="TOC (mg/l)")
            fig.add_hline(y=1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                    x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                    y=1,  # Position Y (sur la ligne horizontale)
                    text="TOC doit être égale à 1",  # Texte de l'annotation
                    showarrow=True,  # Afficher une flèche pointant vers le point
                    arrowhead=2,  # Type de flèche
                    ax=0,  # Position X de la flèche par rapport au texte
                    ay=-40  # Position Y de la flèche par rapport au texte
                )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>MES  (mg/l) moyenne: {np.around(df['MES  (mg/l)'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="MES  (mg/l)")
            fig.add_hline(y=10, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                    x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                    y=10,  # Position Y (sur la ligne horizontale)
                    text="MES doit être inférieur ou égale à 10",  # Texte de l'annotation
                    showarrow=True,  # Afficher une flèche pointant vers le point
                    arrowhead=2,  # Type de flèche
                    ax=0,  # Position X de la flèche par rapport au texte
                    ay=-40  # Position Y de la flèche par rapport au texte
                )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cl2 libre (mg/l) moyenne: {np.around(df['Cl2 libre (mg/l)'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="Cl2 libre (mg/l)")
            fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                    x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                    y=0,  # Position Y (sur la ligne horizontale)
                    text="Cl2 libre doit être égale à 0",  # Texte de l'annotation
                    showarrow=True,  # Afficher une flèche pointant vers le point
                    arrowhead=2,  # Type de flèche
                    ax=0,  # Position X de la flèche par rapport au texte
                    ay=-40  # Position Y de la flèche par rapport au texte
                )
            st.plotly_chart(fig,use_container_width=True,height = 200)   
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>pH moyenne: {np.around(df['pH'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="pH")
            st.plotly_chart(fig,use_container_width=True,height = 200)   
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>TDS (mg/l) moyenne: {np.around(df['TDS (mg/l)'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y="TDS (mg/l)")
            st.plotly_chart(fig,use_container_width=True,height = 200)
    elif (unity == "MCT") & (phase =="APRES FILTRES A CARTOUCHE"):
        df = pd.read_excel(df, sheet_name="MCT_APRES FILTRES A CARTOUCHE")

        col1,col2 = st.columns((2))

        df = df[(df["date"] >= date1) & (df["date"] <= date2)]
        df.replace('/', np.nan, inplace=True)
        df.replace('en cours', np.nan, inplace=True)
   
        df['TOC (mg/l) LIGNE 1'] = df['TOC (mg/l) LIGNE 1'].replace('<3',1)
        df['TOC (mg/l) LIGNE 1'] = df['TOC (mg/l) LIGNE 1'].replace(0,1)
        df['TOC (mg/l) LIGNE 1'] = df['TOC (mg/l) LIGNE 1'].astype(float)
        df.loc[df['TOC (mg/l) LIGNE 1'] < 3, 'TOC (mg/l) LIGNE 1'] = 1
        df.loc[df['TOC (mg/l) LIGNE 1'] > 3, 'TOC (mg/l) LIGNE 1'] = 0

        df['TOC (mg/l) LIGNE 2'] = df['TOC (mg/l) LIGNE 2'].replace('<3',1)
        df['TOC (mg/l) LIGNE 2'] = df['TOC (mg/l) LIGNE 2'].replace(0,1)
        df['TOC (mg/l) LIGNE 2'] = df['TOC (mg/l) LIGNE 2'].astype(float)
        df.loc[df['TOC (mg/l) LIGNE 2'] < 3, 'TOC (mg/l) LIGNE 2'] = 1
        df.loc[df['TOC (mg/l) LIGNE 2'] > 3, 'TOC (mg/l) LIGNE 2'] = 0

        df['TOC (mg/l) LIGNE 3'] = df['TOC (mg/l) LIGNE 3'].replace('<3',1)
        df['TOC (mg/l) LIGNE 3'] = df['TOC (mg/l) LIGNE 3'].replace(0,1)
        df['TOC (mg/l) LIGNE 3'] = df['TOC (mg/l) LIGNE 3'].astype(float)
        df.loc[df['TOC (mg/l) LIGNE 3'] < 3, 'TOC (mg/l) LIGNE 3'] = 1
        df.loc[df['TOC (mg/l) LIGNE 3'] > 3, 'TOC (mg/l) LIGNE 3'] = 0

        df['TOC (mg/l) LIGNE 4'] = df['TOC (mg/l) LIGNE 4'].replace('<3',1)
        df['TOC (mg/l) LIGNE 4'] = df['TOC (mg/l) LIGNE 4'].astype(float)
        df.loc[df['TOC (mg/l) LIGNE 4'] < 3, 'TOC (mg/l) LIGNE 4'] = 1
        df.loc[df['TOC (mg/l) LIGNE 4'] > 3, 'TOC (mg/l) LIGNE 4'] = 0
    #LIGNE 1
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>pH LIGNE 1 moyen: {np.around(df['pH LIGNE 1'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH LIGNE 1')
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Turb (NTU) LIGNE 1 moyen: {np.around(pd.to_numeric(df['Turb (NTU) LIGNE 1'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Turb (NTU) LIGNE 1')
            fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0.1,  # Position Y (sur la ligne horizontale)
                        text="Turb LIGNE 1 doit être inférieur à 0.1",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>PO43-  (mg/l) LIGNE 1 moyen: {np.around(pd.to_numeric(df['PO43-  (mg/l) LIGNE 1'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='PO43-  (mg/l) LIGNE 1')
            fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0,  # Position Y (sur la ligne horizontale)
                        text="PO43- LIGNE 1 doit être égale à 0",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>ORP (mV) LIGNE 1 moyen: {np.around(pd.to_numeric(df['ORP (mV) LIGNE 1'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='ORP (mV) LIGNE 1')
            fig.add_hline(y=250, line_dash="dash", line_color="red", line_width=2)
            fig.add_hline(y=300, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=250,  # Position Y (sur la ligne horizontale)
                        text="Min 250 mv",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=300,  # Position Y (sur la ligne horizontale)
                        text="Max 300 mv",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 LIGNE 1 moyen: {np.around(pd.to_numeric(df['SDI15 LIGNE 1'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='SDI15 LIGNE 1')
            fig.add_hline(y=2.5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=2.5,  # Position Y (sur la ligne horizontale)
                        text="SDI15 LIGNE 1 doit être inférieur à 2.5",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>TOC (mg/l) LIGNE 1 moyen: {np.around(pd.to_numeric(df['TOC (mg/l) LIGNE 1'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='TOC (mg/l) LIGNE 1')
            fig.add_hline(y=1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=1,  # Position Y (sur la ligne horizontale)
                        text="TOC LIGNE 1 doit être égale à 1 (1 pour les valeurs <3 et 0 sinon)",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>TDS (mg/l) LIGNE 1 moyen: {np.around(pd.to_numeric(df['TDS (mg/l) LIGNE 1'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='TDS (mg/l) LIGNE 1')
            fig.add_hline(y=40000, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=40000,  # Position Y (sur la ligne horizontale)
                        text="TDS LIGNE 1 doit être inférieur à 40 000",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
    #LIGNE 2      
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>pH LIGNE 2 moyen: {np.around(df['pH LIGNE 2'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH LIGNE 2')
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Turb (NTU) LIGNE 2 moyen: {np.around(pd.to_numeric(df['Turb (NTU) LIGNE 2'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Turb (NTU) LIGNE 2')
            fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0.1,  # Position Y (sur la ligne horizontale)
                        text="Turb LIGNE 2 doit être inférieur à 0.1",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>PO43-  (mg/l) LIGNE 2 moyen: {np.around(pd.to_numeric(df['PO43-   (mg/l) LIGNE 2'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='PO43-   (mg/l) LIGNE 2')
            fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0,  # Position Y (sur la ligne horizontale)
                        text="PO43- LIGNE 2 doit être égale à 0",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>ORP (mV) LIGNE 2 moyen: {np.around(pd.to_numeric(df['ORP (mV) LIGNE 2'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='ORP (mV) LIGNE 2')
            fig.add_hline(y=250, line_dash="dash", line_color="red", line_width=2)
            fig.add_hline(y=300, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=250,  # Position Y (sur la ligne horizontale)
                        text="Min 250 mv",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=300,  # Position Y (sur la ligne horizontale)
                        text="Max 300 mv",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 LIGNE 2 moyen: {np.around(pd.to_numeric(df['SDI15 LIGNE 2'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='SDI15 LIGNE 2')
            fig.add_hline(y=2.5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=2.5,  # Position Y (sur la ligne horizontale)
                        text="SDI15 LIGNE 2 doit être inférieur à 2.5",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>TOC (mg/l) LIGNE 2 moyen: {np.around(pd.to_numeric(df['TOC (mg/l) LIGNE 2'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='TOC (mg/l) LIGNE 2')
            fig.add_hline(y=1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=1,  # Position Y (sur la ligne horizontale)
                        text="TOC LIGNE 2 doit être égale à 1 (1 pour les valeurs <3 et 0 sinon)",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>TDS (mg/l) LIGNE 2 moyen: {np.around(pd.to_numeric(df['TDS (mg/l) LIGNE 2'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='TDS (mg/l) LIGNE 2')
            fig.add_hline(y=40000, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=40000,  # Position Y (sur la ligne horizontale)
                        text="TDS LIGNE 2 doit être inférieur à 40 000",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
    #LIGNE 3
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>pH LIGNE 3 moyen: {np.around(df['pH LIGNE 3'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH LIGNE 3')
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Turb (NTU) LIGNE 3 moyen: {np.around(pd.to_numeric(df['Turb (NTU) LIGNE 3'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Turb (NTU) LIGNE 3')
            fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0.1,  # Position Y (sur la ligne horizontale)
                        text="Turb LIGNE 3 doit être inférieur à 0.1",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>PO43-  (mg/l) LIGNE 3 moyen: {np.around(pd.to_numeric(df['PO43-  (mg/l) LIGNE 3'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='PO43-  (mg/l) LIGNE 3')
            fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0,  # Position Y (sur la ligne horizontale)
                        text="PO43- LIGNE 3 doit être égale à 0",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>ORP (mV) LIGNE 13 moyen: {np.around(pd.to_numeric(df['ORP (mV) LIGNE 3'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='ORP (mV) LIGNE 3')
            fig.add_hline(y=250, line_dash="dash", line_color="red", line_width=2)
            fig.add_hline(y=300, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=250,  # Position Y (sur la ligne horizontale)
                        text="Min 250 mv",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=300,  # Position Y (sur la ligne horizontale)
                        text="Max 300 mv",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 LIGNE 3 moyen: {np.around(pd.to_numeric(df['SDI15 LIGNE 3'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='SDI15 LIGNE 3')
            fig.add_hline(y=2.5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=2.5,  # Position Y (sur la ligne horizontale)
                        text="SDI15 LIGNE 3 doit être inférieur à 2.5",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>TOC LIGNE 3 moyen: {np.around(pd.to_numeric(df['TOC (mg/l) LIGNE 3'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='TOC (mg/l) LIGNE 3')
            fig.add_hline(y=1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=1,  # Position Y (sur la ligne horizontale)
                        text="TOC LIGNE 3 doit être égale à 1 (1 pour les valeurs <3 et 0 sinon)",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>TDS (mg/l) LIGNE 3 moyen: {np.around(pd.to_numeric(df['TDS (mg/l) LIGNE 3'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='TDS (mg/l) LIGNE 3')
            fig.add_hline(y=40000, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=40000,  # Position Y (sur la ligne horizontale)
                        text="TDS LIGNE 3 doit être inférieur à 40 000",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
    #LIGNE 4
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>pH LIGNE 4 moyen: {np.around(df['pH  LIGNE 4'].mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH  LIGNE 4')
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Turb (NTU) LIGNE 4 moyen: {np.around(pd.to_numeric(df['Turb (NTU) LIGNE 4'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Turb (NTU) LIGNE 4')
            fig.add_hline(y=0.1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0.1,  # Position Y (sur la ligne horizontale)
                        text="Turb LIGNE 4 doit être inférieur à 0.1",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>PO43-  (mg/l) LIGNE 4 moyen: {np.around(pd.to_numeric(df['PO43-  (mg/l) LIGNE 4'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='PO43-  (mg/l) LIGNE 4')
            fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=0,  # Position Y (sur la ligne horizontale)
                        text="PO43- LIGNE 4 doit être égale à 0",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>ORP (mV) LIGNE 4 moyen: {np.around(pd.to_numeric(df['ORP (mV) LIGNE 4'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='ORP (mV) LIGNE 4')
            fig.add_hline(y=250, line_dash="dash", line_color="red", line_width=2)
            fig.add_hline(y=300, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=250,  # Position Y (sur la ligne horizontale)
                        text="Min 250 mv",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=300,  # Position Y (sur la ligne horizontale)
                        text="Max 300 mv",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>SDI15 LIGNE 4 moyen: {np.around(pd.to_numeric(df['SDI15 LIGNE 4'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='SDI15 LIGNE 4')
            fig.add_hline(y=2.5, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=2.5,  # Position Y (sur la ligne horizontale)
                        text="SDI15 LIGNE 4 doit être inférieur à 2.5",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>TOC (mg/l) LIGNE 4 moyen: {np.around(pd.to_numeric(df['TOC (mg/l) LIGNE 4'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='TOC (mg/l) LIGNE 4')
            fig.add_hline(y=1, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=1,  # Position Y (sur la ligne horizontale)
                        text="TOC LIGNE 4 doit être égale à 1 (1 pour les valeurs <3 et 0 sinon)",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>TDS (mg/l) LIGNE 4 moyen: {np.around(pd.to_numeric(df['TDS (mg/l) LIGNE 4'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='TDS (mg/l) LIGNE 2')
            fig.add_hline(y=40000, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=40000,  # Position Y (sur la ligne horizontale)
                        text="TDS LIGNE 4 doit être inférieur à 40 000",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)   
    elif (unity == "MCT") & (phase =="PERMEAT RO"): 
        df = pd.read_excel(df,sheet_name="MCT_PERMEAT RO")
        col1,col2 = st.columns((2))
        df = df[(df["date"] >= date1) & (df["date"] <= date2)]
        df.replace('/', np.nan, inplace=True)
        df.replace('#VALEUR!', np.nan, inplace=True)
        df.replace('en cours', np.nan, inplace=True)
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cond LIGNE 1 moyen: {np.around(pd.to_numeric(df['Cond LIGNE 1'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond LIGNE 1')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond LIGNE 1 doit être inférieur à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>pH LIGNE 1 moyen: {np.around(pd.to_numeric(df['pH LIGNE 1'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH LIGNE 1')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH LIGNE 1 doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)

        with col1:
                st.markdown(f"<h2 style='text-align: center;'>Cond LIGNE 2 moyen: {np.around(pd.to_numeric(df['Cond LIGNE 2'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
                fig = px.line(df,x="date",y='Cond LIGNE 2')
                fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
                fig.add_annotation(
                            x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                            y=450,  # Position Y (sur la ligne horizontale)
                            text="Cond LIGNE 2 doit être inférieur à 450",  # Texte de l'annotation
                            showarrow=True,  # Afficher une flèche pointant vers le point
                            arrowhead=2,  # Type de flèche
                            ax=0,  # Position X de la flèche par rapport au texte
                            ay=-40  # Position Y de la flèche par rapport au texte
                        )
                st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>pH LIGNE 2 moyen: {np.around(pd.to_numeric(df['pH LIGNE 2'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH LIGNE 2')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH LIGNE 2 doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)

        with col1:
                st.markdown(f"<h2 style='text-align: center;'>Cond LIGNE 3 moyen: {np.around(pd.to_numeric(df['Cond LIGNE 3'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
                fig = px.line(df,x="date",y='Cond LIGNE 3')
                fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
                fig.add_annotation(
                            x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                            y=450,  # Position Y (sur la ligne horizontale)
                            text="Cond LIGNE 3 doit être inférieur à 450",  # Texte de l'annotation
                            showarrow=True,  # Afficher une flèche pointant vers le point
                            arrowhead=2,  # Type de flèche
                            ax=0,  # Position X de la flèche par rapport au texte
                            ay=-40  # Position Y de la flèche par rapport au texte
                        )
                st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>pH LIGNE 3 moyen: {np.around(pd.to_numeric(df['pH LIGNE 3'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH LIGNE 3')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH LIGNE 3 doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)

        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Cond LIGNE 4 moyen: {np.around(pd.to_numeric(df['Cond LIGNE 4'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='Cond LIGNE 4')
            fig.add_hline(y=450, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=450,  # Position Y (sur la ligne horizontale)
                        text="Cond LIGNE 4 doit être inférieur à 450",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)
        with col2:
            st.markdown(f"<h2 style='text-align: center;'>pH LIGNE 4 moyen: {np.around(pd.to_numeric(df['pH LIGNE 4'], errors='coerce').mean(),2)}</h2>", unsafe_allow_html=True)
            fig = px.line(df,x="date",y='pH LIGNE 4')
            fig.add_hline(y=5.4, line_dash="dash", line_color="red", line_width=2)
            fig.add_annotation(
                        x=df['date'].iloc[-1],  # Position X (la dernière date dans ce cas)
                        y=5.4,  # Position Y (sur la ligne horizontale)
                        text="pH LIGNE 4 doit être supérieur à 5.4",  # Texte de l'annotation
                        showarrow=True,  # Afficher une flèche pointant vers le point
                        arrowhead=2,  # Type de flèche
                        ax=0,  # Position X de la flèche par rapport au texte
                        ay=-40  # Position Y de la flèche par rapport au texte
                    )
            st.plotly_chart(fig,use_container_width=True,height = 200)            
def Comparaison_des_phases_de_traitement(t,data,date1,date2,graphique):
    df ={}
    params = data[2]
    for j in range(len(data[1])):
        df[f"{data[0]}_{data[1][j]}"] = pd.read_excel(t,sheet_name=f"{data[0]}_{data[1][j]}")
    c = f"{data[0]}_{data[1][0]}"
    for k in df.keys():
        df[k]['date'] = pd.to_datetime(df[k]['date'])
        df[k] = df[k][(df[k]["date"] >= date1) & (df[k]["date"] <= date2)]
        df[k].replace('/', np.nan, inplace=True)
        df[k].replace('#VALEUR!', np.nan, inplace=True)
        df[k].replace('en cours', np.nan, inplace=True) 
        if k.endswith("_intake"):
            df[k]['TDS (mg/l)'].replace(0, np.nan, inplace=True)

    df1 = {'date':df[c]["date"]}
    legend = []
    for data, value in params.items():
            if value:
                for param in params[data]:
                    df1[f"{param}_{data}"] = df[data][param]
                    legend.append(f"{param}_{data}")
                    title = param  
           
    df1 = pd.DataFrame(df1)
    df1 =  df1[(df1["date"] >= date1) & (df1["date"] <= date2)] 
    if (df1.columns[1][:2] != df1.columns[2][:2] ):
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Scatter(x=df1['date'], y=df1[df1.columns[1]], name=df1.columns[1],line=dict(color='#095DBA', width=2)),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(x=df1['date'], y=df1[df1.columns[2]], name=df1.columns[2],line=dict(color='#FF4B4A', width=2),),
            secondary_y=True,
        )

        fig.update_layout(
            title_text=f"Corellation entre {df1.columns[1][:4]} et {df1.columns[2][:4]}",
            title_x=0.3,
            height=600
        )

        fig.update_xaxes(title_text="Date")

        fig.update_yaxes(title_text=df1.columns[1][:4], secondary_y=False)
        fig.update_yaxes(title_text=df1.columns[2][:4], secondary_y=True)

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown(f"<h3 style='text-align: center;'>Variation de {title[:4]} pendant les phases séléctionner</h3>", unsafe_allow_html=True)        
        fig = px.line(df1,x="date",y=df1.columns[1:])
        fig.update_traces(line=dict(color='#095DBA'), selector=dict(name=df1.columns[1]))
        fig.update_traces(line=dict(color='#FF4B4A'), selector=dict(name=df1.columns[2]))
        st.plotly_chart(fig,use_container_width=True,height = 200)
     
        list_phase = ['intake','PERMEAT FILTRATION','Bac_stockage','APRES FILTRES A CARTOUCHE','PERMEAT RO','sortie_global']
        x,y = find_elements(list_phase,list(df1.columns))
        elem = ((df1[x]-df1[y])/df1[x])*100
        df1["Pourcentage"] = np.round(elem,2)
        for i in range(len(df1["Pourcentage"])):
           if df1["Pourcentage"].iloc[i] <0:
               df1["Pourcentage"].iloc[i] = np.nan

        if graphique == "Graphique à barres":
            # selected_color = st.color_picker(f'Choisissez une couleur', '#FF4B4A')
            st.markdown(f"<h3 style='text-align: center;'>Pourcentage d'élémination moyenne de {title[:4]} :{np.round(df1['Pourcentage'].mean(),2)}  %</h3>", unsafe_allow_html=True)        
            fig = px.bar(df1,x="date",y="Pourcentage",color_discrete_sequence=['#FF4B4A'],height = 450)
            fig.update_traces(text=df1["Pourcentage"], textposition='outside')
            st.plotly_chart(fig,use_container_width=True)
        elif graphique == "Graphique en lignes":
            graphique_pourcentage_elimination(df1,"date","Pourcentage",title,px.line)
        elif graphique == "Graphique en aires":
            graphique_pourcentage_elimination(df1,"date","Pourcentage",title,px.area)

        elif graphique == "Graphique à points":
            graphique_pourcentage_elimination(df1,"date","Pourcentage",title,px.scatter)    
def generate_hex_colors(n):
    colors = []
    for _ in range(n):
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        colors.append(color)
    return colors
def unity_compare(t,unity,phase,params,date1,date2):
    df ={}
    for i in range(len(unity)):
            df[f"{unity[i]}_{phase[unity[i]]}"] = pd.read_excel(t,sheet_name=f"{unity[i]}_{phase[unity[i]]}")
    for k in df.keys():
        df[k]['date'] = pd.to_datetime(df[k]['date'])
        df[k] = df[k][(df[k]["date"] >= date1) & (df[k]["date"] <= date2)]
        df[k].replace('/', np.nan, inplace=True)
        df[k].replace('#VALEUR!', np.nan, inplace=True)
        df[k].replace('en cours', np.nan, inplace=True)
 
    c = f"{unity[0]}_{phase[unity[0]]}"
    df1 = {'date':df[c]["date"]}
    for k in df.keys():
        for i in range(len(params[k])):
            df1[f"{params[k][i]} -- {k}"] = df[k][params[k][i]]                       
    df1 = pd.DataFrame(df1)
    st.markdown(f"<h3 style='text-align: center;'>Variation de {df1.columns[1][:4]} dans les unitées séléctionnées</h3>", unsafe_allow_html=True)        
    fig = px.line(df1,x="date",y=df1.columns[1:])
    st.plotly_chart(fig,use_container_width=True,height = 200)  

    fig = px.bar(df1,x="date",y=df1.columns[1:])
    st.plotly_chart(fig,use_container_width=True,height = 200)
def graphique_pourcentage_elimination(df,x,y,title,graph):
    st.markdown(f"<h3 style='text-align: center;'>Pourcentage d'élémination de {title[:4]} en %</h3>", unsafe_allow_html=True)        
    fig = graph(df,x=x,y=y)
    st.plotly_chart(fig,use_container_width=True,height = 200)
    #  for i in range(len(df1.columns)):
    #     fig = make_subplots(rows=3, cols=1, shared_xaxes=True)
    #     fig.add_trace(go.Scatter(x=df1['date'], y=df1[df1.columns[i]], name=df1.columns[i]), row=1, col=1)
    # st.plotly_chart(fig, use_container_width=True)
def find_elements(fixed_list, dynamic_list):
    first_element = None
    last_element = None

    # Rechercher le premier élément
    for element in fixed_list:
        for dynamic_element in dynamic_list:
            print(dynamic_element)
            if element in dynamic_element:
                first_element = dynamic_element
                break
        if first_element is not None:
            break

    # Rechercher le dernier élément
    for element in reversed(fixed_list):
        for dynamic_element in dynamic_list:
            if element in dynamic_element:
                last_element = dynamic_element
                break
        if last_element is not None:
            break

    return first_element, last_element
def labo_oper(d1,d2,phase1,phase2,x,y):
    df = pd.DataFrame({'date':d2[phase2]['date'],x:d1[phase1][x],y:d2[phase2][y]})
    
    df.replace(0, np.nan, inplace=True)
    df.replace('/', np.nan, inplace=True)
    df.replace('-', np.nan, inplace=True)
    df.replace('CIP', np.nan, inplace=True)
    df.replace('erroné', np.nan, inplace=True)
    df.replace('en cours', np.nan, inplace=True)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=df['date'], y=df[df.columns[1]], name=df.columns[1],line=dict(color='#095DBA', width=2)),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df['date'], y=df[df.columns[2]], name=df.columns[2],line=dict(color='#FF4B4A', width=2),),
        secondary_y=True,
    )

    fig.update_layout(
        title_text=f"Corellation entre {df.columns[1][:4]} et {df.columns[2][:4]}",
        title_x=0.3,
        height=600
    )

    fig.update_xaxes(title_text="Date")

    fig.update_yaxes(title_text=x, secondary_y=False)
    fig.update_yaxes(title_text=y, secondary_y=True)

    st.plotly_chart(fig, use_container_width=True)
def labo_oper1(d1,d2,phase1,phase2,x,y):
    df = pd.DataFrame({'date':d1[phase1]['date'],x:d1[phase1][x],y:d2[phase2][y]})
    df.replace(0, np.nan, inplace=True)
    df.replace('/', np.nan, inplace=True)
    df.replace('CIP', np.nan, inplace=True)
    df.replace('erroné', np.nan, inplace=True)
    df.replace('-', np.nan, inplace=True)
    df.replace('en cours', np.nan, inplace=True)
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=df['date'], y=df[df.columns[1]], name=df.columns[1],line=dict(color='#095DBA', width=2)),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df['date'], y=df[df.columns[2]], name=df.columns[2],line=dict(color='#FF4B4A', width=2),),
        secondary_y=True,
    )

    fig.update_layout(
        title_text=f"Corellation entre {df.columns[1][:4]} et {df.columns[2][:4]}",
        title_x=0.3,
        height=600
    )

    fig.update_xaxes(title_text="Date")

    fig.update_yaxes(title_text=x, secondary_y=False)
    fig.update_yaxes(title_text=y, secondary_y=True)

    st.plotly_chart(fig, use_container_width=True)
def labo_oper2(d1,d2,phase1,x,y):
    df = pd.DataFrame({'date':d1[phase1]['date'],x:d1[phase1][x],y:d2["tr"][y]})
    df.replace(0, np.nan, inplace=True)
    df.replace('/', np.nan, inplace=True)
    df.replace('CIP', np.nan, inplace=True)
    df.replace('erroné', np.nan, inplace=True)
    df.replace('-', np.nan, inplace=True)
    df.replace('en cours', np.nan, inplace=True)
    # df.replace('', np.nan, inplace=True)
    # col1,col2 = st.columns((2))
    # with col1:
    #     selected_color1 = st.color_picker(f'Choisissez la couleur de {x}', '#095DBA')
    # with col2:
    #     selected_color2 = st.color_picker(f'Choisissez la couleur de {y}', '#FF4B4A')
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=df['date'], y=df[df.columns[1]], name=df.columns[1],line=dict(color='#095DBA', width=2)),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df['date'], y=df[df.columns[2]], name=df.columns[2],line=dict(color='#FF4B4A', width=2),),
        secondary_y=True,
    )

    fig.update_layout(
        title_text=f"Corellation entre {df.columns[1][:4]} et {df.columns[2][:4]}",
        title_x=0.3,
        height=600
    )

    fig.update_xaxes(title_text="Date")

    fig.update_yaxes(title_text=x, secondary_y=False)
    fig.update_yaxes(title_text=y, secondary_y=True)

    st.plotly_chart(fig, use_container_width=True)
def vis_op(data,phase,date1,date2):
    df = data[phase]

    col1,col2 = st.columns((2))

    df = df[(df["date"] >= date1) & (df["date"] <= date2)]

    df.replace(0, np.nan, inplace=True)
    df.replace('/', np.nan, inplace=True)
    df.replace('-', np.nan, inplace=True)
    df.replace('CIP', np.nan, inplace=True)
    df.replace('erroné', np.nan, inplace=True)
    df.replace('en cours', np.nan, inplace=True)
    df.replace('', np.nan, inplace=True)
    df.replace('***', np.nan, inplace=True)
    df.replace('NA', np.nan, inplace=True)
    df.replace('HS', np.nan, inplace=True)

    # Create a container to manage layout
    container = st.container()

    # Loop through the DataFrame columns by index
    for i in range(1, len(df.columns), 2):
        col1, col2 = container.columns(2)  # Create two columns
        
        # Display the chart for the first column in the pair
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>{df.columns[i]}</h2>", unsafe_allow_html=True)        
            fig = px.line(df, x="date", y=df.columns[i])
            st.plotly_chart(fig, use_container_width=True, height=200)
        
        # Display the chart for the second column in the pair, if it exists
        if i+1 < len(df.columns):
            with col2:
                st.markdown(f"<h2 style='text-align: center;'>{df.columns[i+1]}</h2>", unsafe_allow_html=True)
                fig = px.line(df, x="date", y=df.columns[i+1])
                st.plotly_chart(fig, use_container_width=True, height=200)
def compare_op(data,phase,params,d1,d2):
    df ={}
    for k in range(len(phase)):
        df[phase[k]] = data[phase[k]]
    for k in df.keys():
        df[k]['date'] = pd.to_datetime(df[k]['date'])
        df[k] = df[k][(df[k]["date"] >= d1) & (df[k]["date"] <= d2)]
        df[k].replace('/', np.nan, inplace=True)
        df[k].replace('#VALEUR!', np.nan, inplace=True)
        df[k].replace('en cours', np.nan, inplace=True) 
        df[k].replace(0, np.nan, inplace=True) 
    c= f"{phase[0]}"
    df1 = {'date':df[c]["date"]}
    
    df1 = pd.DataFrame(df1)
    df1 =  df1[(df1["date"] >= d1) & (df1["date"] <= d2)] 
    for k in df.keys():
        df1[params[k]] = df[k][params[k]]
    # col1,col2 = st.columns((2))
    # with col1:
    #     selected_color1 = st.color_picker(f'Choisissez la couleur de {df1.columns[1][:4]}', '#095DBA')
    # with col2:
    #     selected_color2 = st.color_picker(f'Choisissez la couleur de {df1.columns[2][:4]}', '#FF4B4A')
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=df1['date'], y=df1[df1.columns[1]], name=df1.columns[1],line=dict(color='#095DBA', width=2)),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df1['date'], y=df1[df1.columns[2]], name=df1.columns[2],line=dict(color='#FF4B4A', width=2),),
        secondary_y=True,
    )

    fig.update_layout(
        title_text=f"Corellation entre {df1.columns[1][:6]} et {df1.columns[2][:6]}",
        title_x=0.3,
        height=600
    )

    fig.update_xaxes(title_text="Date")

    fig.update_yaxes(title_text=df1.columns[1][:6], secondary_y=False)
    fig.update_yaxes(title_text=df1.columns[2][:6], secondary_y=True)

    st.plotly_chart(fig, use_container_width=True)
def compar_unity_op(data,unity,phase,params,date1,date2):
    df ={}
    for i in range(len(unity)):
            df[f"{unity[i]}_{phase[unity[i]]}"] = data[f"{unity[i]}_{phase[unity[i]]}"]
    for k in df.keys():
        df[k]['date'] = pd.to_datetime(df[k]['date'])
        df[k] = df[k][(df[k]["date"] >= date1) & (df[k]["date"] <= date2)]
        df[k].replace('/', np.nan, inplace=True)
        df[k].replace('#VALEUR!', np.nan, inplace=True)
        df[k].replace('en cours', np.nan, inplace=True)
        df[k].replace(0, np.nan, inplace=True)
 
    c = f"{unity[0]}_{phase[unity[0]]}"
    df1 = {'date':df[c]["date"]}
    for k in df.keys():
        for i in range(len(params[k])):
            df1[f"{params[k][i]}---{k}"] = df[k][params[k][i]]                       
    df1 = pd.DataFrame(df1)
    st.markdown(f"<h3 style='text-align: center;'>Variation de {df1.columns[1][:6]} dans les unitées séléctionnées</h3>", unsafe_allow_html=True)        
    fig = px.line(df1,x="date",y=df1.columns[1:],height = 400)
    st.plotly_chart(fig, use_container_width=True) 


    fig = px.bar(df1,x="date",y=df1.columns[1:])
    st.plotly_chart(fig,use_container_width=True,height = 200)
def visualisation_volume(df,date1,date2):
    df = df[(df["Date"] >= date1) & (df["Date"] <= date2)]
    st.markdown(f"<h2 style='text-align: center;'>Volume Produit de chaque unitée en m3</h2>", unsafe_allow_html=True)        
    fig1 = px.line(df,x="Date",y=df.columns[1:df.shape[1]-1])
    st.plotly_chart(fig1,use_container_width=True,height = 200)
    
    st.markdown(f"<h2 style='text-align: center;'>Volume Total en m3</h2>", unsafe_allow_html=True)        
    fig2 = px.line(df,x="Date",y=df.columns[-1])
    st.plotly_chart(fig2,use_container_width=True,height = 200)
    # st.markdown(f"<h2 style='text-align: center;'>Volume Produit de {df.columns[1]} en m3</h2>", unsafe_allow_html=True)        
    # fig = px.line(df, x="Date", y=df.columns[1], text=df[df.columns[1]])
    # fig.update_traces(mode='lines+markers+text', textposition='top right')
    # st.plotly_chart(fig, use_container_width=True, height=200)
    
    # st.markdown(f"<h2 style='text-align: center;'>Volume Produit de {df.columns[2]} en m3</h2>", unsafe_allow_html=True)        
    # fig = px.line(df, x="Date", y=df.columns[2], text=df[df.columns[2]])
    # fig.update_traces(mode='lines+markers+text', textposition='top right')
    # st.plotly_chart(fig, use_container_width=True, height=200)
    
    # st.markdown(f"<h2 style='text-align: center;'>Volume Produit de {df.columns[3]} en m3</h2>", unsafe_allow_html=True)        
    # fig = px.line(df, x="Date", y=df.columns[3], text=df[df.columns[3]])
    # fig.update_traces(mode='lines+markers+text', textposition='top right')
    # st.plotly_chart(fig, use_container_width=True, height=200)
    
    # st.markdown(f"<h2 style='text-align: center;'>Volume Produit de {df.columns[4]} en m3</h2>", unsafe_allow_html=True)        
    # fig = px.line(df, x="Date", y=df.columns[4], text=df[df.columns[4]])
    # fig.update_traces(mode='lines+markers+text', textposition='top right')
    # st.plotly_chart(fig, use_container_width=True, height=200)
    
    # st.markdown(f"<h2 style='text-align: center;'>Volume Produit de {df.columns[5]} en m3</h2>", unsafe_allow_html=True)        
    # fig = px.line(df, x="Date", y=df.columns[5], text=df[df.columns[5]])
    # fig.update_traces(mode='lines+markers+text', textposition='top right')
    # st.plotly_chart(fig, use_container_width=True, height=200)
def visualisation_volume_op(data1,data2,phase,volume, param):
    df1 = {'date':data2['Date']}
    # df['date'] = data2['Date']
    df1[param] = data1[phase][param]
    df1[volume] = data2[volume]
    df1 = pd.DataFrame(df1)
    df1.replace(0, np.nan, inplace=True)
    # # st.markdown(f"<h2 style='text-align: center;'>ION moyen: {np.around(df['Volume total (m3) ION'].mean(),2)} m3</h2>", unsafe_allow_html=True)        
    # fig = px.line(df1,x="date",y=df1.columns[1:])
    # st.plotly_chart(fig,use_container_width=True,height = 200)
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=df1['date'], y=df1[df1.columns[1]], name=df1.columns[1],line=dict(color='#095DBA', width=2)),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df1['date'], y=df1[df1.columns[2]], name=df1.columns[2],line=dict(color='#FF4B4A', width=2),),
        secondary_y=True,
    )

    fig.update_layout(
        title_text=f"Corellation entre {df1.columns[1][:6]} et {df1.columns[2][:6]}",
        title_x=0.3,
        height=600
    )

    fig.update_xaxes(title_text="Date")

    fig.update_yaxes(title_text=df1.columns[1][:6], secondary_y=False)
    fig.update_yaxes(title_text=df1.columns[2][:6], secondary_y=True)

    st.plotly_chart(fig, use_container_width=True)
def send_notification(df,seuil,param,gmail_cfg):
    df.replace('/', np.nan, inplace=True)
    df.replace('en cours', np.nan, inplace=True)
    df['TDS (mg/l)'].replace(0, np.nan, inplace=True)
    df['TOC (mg/l)'] = df['TOC (mg/l)'].replace('<3',1)
    df['TOC (mg/l)'] = df['TOC (mg/l)'].astype(float)
    df.loc[df['TOC (mg/l)'] < 3, 'TOC (mg/l)'] = 1
    df.loc[df['TOC (mg/l)'] > 3, 'TOC (mg/l)'] = 0

    # Vérification de la dernière valeur de PO43-
    valeur_actuelle = float(df[param].iloc[-1])
 
    if valeur_actuelle > seuil:
        # Génération de l'image du graphique
        fig = px.line(df, x="date", y=param)
        fig.add_hline(y=seuil, line_dash="dash", line_color="red", line_width=2)
        fig.add_annotation(
            x=df['date'].iloc[-1],
            y=seuil,
            text=f"{param} doit être inférieur ou égal à {seuil}",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-40
        )

        # Sauvegarde le graphique comme image
        pio.write_image(fig, f"graph_{param[:5]}.png")

        # Création du message e-mail
        msg = EmailMessage()
        msg['To'] = "aitomar.mip.97@gmail.com"
        msg['From'] = gmail_cfg['email']
        msg['Subject'] = f"URGENT - Alerte Dépassement des Seuils des Paramètres Critiques"
        msg.set_content(f'''Bonjour,

        Attention : Des dépassements critiques des seuils ont été détectés dans les dernières mesures des paramètres de qualité de l'eau. Veuillez prendre les mesures nécessaires immédiatement pour corriger ces anomalies.

        Les détails des dépassements sont les suivants :

        - La valeur de {param} est de {valeur_actuelle} et a dépassé le seuil de {seuil}.

        Ces dépassements peuvent indiquer un risque potentiel pour la qualité de l'eau traitée. Nous vous recommandons de vérifier le système de traitement de l'eau et de rectifier les niveaux des paramètres concernés immédiatement.

        Des graphiques en pièce jointe montrent les tendances des paramètres au cours des derniers jours. Veuillez les consulter pour une analyse détaillée.

        **Ceci est une situation urgente et nécessite une action rapide !**

        Merci de nous tenir informés de vos actions pour remédier à ce problème.

        Cordialement,

        mohamed AIT-OMAR
        Data Science''')

        # Ajout de l'image en pièce jointe
        with open(f'graph_{param[:5]}.png', 'rb') as f:
            file_data = f.read()
            file_name = f.name
            msg.add_attachment(file_data, maintype='image', subtype='png', filename=file_name)

        # Envoi de l'e-mail
        with smtplib.SMTP_SSL(gmail_cfg['serveur'], gmail_cfg['port']) as smtp:
            smtp.login(gmail_cfg['email'], gmail_cfg['pwd'])
            smtp.send_message(msg)
            print("Notification envoyée avec succès avec le graphique !")
    else:
        print(f"La valeur actuelle de {param} est inférieure ou égale au seuil. Aucune notification envoyée.")
