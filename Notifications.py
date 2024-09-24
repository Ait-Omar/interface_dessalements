import streamlit as st
import smtplib
import json
from email.message import EmailMessage
import plotly.express as px
import plotly.io as pio
import pandas as pd
import os

# Read Gmail configuration from config.json file
with open('config.json') as json_file:
    gmail_cfg = json.load(json_file)

# Define the function to send email notifications
def send_notification(df, seuil_po43, param):
    valeur_actuelle_po43 = df[param].iloc[-1]
    if valeur_actuelle_po43 > seuil_po43:
        # Generate the graph
        fig = px.line(df, x="date", y=param)
        fig.add_hline(y=seuil_po43, line_dash="dash", line_color="red", line_width=2)
        fig.add_annotation(
            x=df['date'].iloc[-1],
            y=seuil_po43,
            text=f"{param} doit être inférieur ou égal à {seuil_po43}",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-40
        )

        # Save the graph as an image
        file_path = f'graph.png'
        pio.write_image(fig, file_path)

        # Create the email message
        msg = EmailMessage()
        msg['To'] = "aitomar.mip.97@gmail.com"
        msg['From'] = gmail_cfg['email']
        msg['Subject'] = f"URGENT - Alerte Dépassement des Seuils des Paramètres Critiques"
        msg.set_content(f'''Bonjour,

        Attention : Des dépassements critiques des seuils ont été détectés dans les dernières mesures des paramètres de qualité de l'eau. Veuillez prendre les mesures nécessaires immédiatement pour corriger ces anomalies.

        Les détails des dépassements sont les suivants :

        - La valeur de {param} est de {valeur_actuelle_po43} et a dépassé le seuil de {seuil_po43}.

        Ces dépassements peuvent indiquer un risque potentiel pour la qualité de l'eau traitée. Nous vous recommandons de vérifier le système de traitement de l'eau et de rectifier les niveaux des paramètres concernés immédiatement.

        Des graphiques en pièce jointe montrent les tendances des paramètres au cours des derniers jours. Veuillez les consulter pour une analyse détaillée.

        **Ceci est une situation urgente et nécessite une action rapide !**

        Merci de nous tenir informés de vos actions pour remédier à ce problème.

        Cordialement,

        mohamed AIT-OMAR
        Data Science''')

        # Attach the image to the email
        with open(file_path, 'rb') as f:
            file_data = f.read()
            file_name = f.name
            msg.add_attachment(file_data, maintype='image', subtype='png', filename=file_name)

        # Send the email
        with smtplib.SMTP_SSL(gmail_cfg['serveur'], gmail_cfg['port']) as smtp:
            smtp.login(gmail_cfg['email'], gmail_cfg['pwd'])
            smtp.send_message(msg)
            st.success("Notification envoyée avec succès!")
        
        # Delete the image after sending
        os.remove(file_path)

    else:
        st.info(f"La valeur actuelle de {param} est inférieure ou égale au {seuil_po43}. Aucune notification envoyée.")

sheets =["QT_intake","QT_PERMEAT FILTRATION","QT_APRES FILTRES A CARTOUCHE","QT_PERMEAT RO","QT_sortie_global",
    "ESLI_intake","ESLI_PERMEAT FILTRATION", "ESLI_APRES FILTRES A CARTOUCHE","ESLI_PERMEAT RO",
    "ION_intake","ION_PERMEAT FILTRATION","ION_Bac_stockage","ION_APRES FILTRES A CARTOUCHE","ION_PERMEAT RO",
    "MCT_intake","MCT_APRES FILTRES A CARTOUCHE","MCT_PERMEAT RO"]

data = {}
for sheet in sheets:
        data[sheet] = pd.read_excel("data/Suivi Analyse Mobile préparaé.xlsx",sheet_name=sheet)
sheet = st.selectbox("Sélectionnez les données", sheets)
# Use default data
df = pd.read_excel("data/Suivi Analyse Mobile préparaé.xlsx",sheet_name=sheet)
# st.write("Aperçu des données par défaut:")
# st.write(df)

# Select parameter and threshold
param = st.selectbox("Sélectionnez le paramètre à surveiller", df.columns[1:])
seuil = st.number_input("Définissez le seuil pour le paramètre sélectionné", min_value=0.0, step=0.01, value=0.1)

# Button to send notification
if st.button("Envoyer une notification si le seuil est dépassé"):
    send_notification(df, seuil, param)
