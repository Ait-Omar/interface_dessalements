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
def send_notifications(alerts):
    if not alerts:
        st.info("Aucun dépassement détecté.")
        return

    # Generate the email content
    message_body = f'''Bonjour,

Attention : Des dépassements critiques des seuils ont été détectés dans les dernières mesures des paramètres de qualité de l'eau. Veuillez prendre les mesures nécessaires immédiatement pour corriger ces anomalies.

Les détails des dépassements sont les suivants :

'''
    for alert in alerts:
        message_body += f"- {alert['param']} dans {alert['sheet']} a une valeur de {alert['value']} (seuil : {alert['threshold']}) le {alert['date']}.\n"
    
    message_body += '''
Ces dépassements peuvent indiquer un risque potentiel pour la qualité de l'eau traitée. Nous vous recommandons de vérifier le système de traitement de l'eau et de rectifier les niveaux des paramètres concernés immédiatement.

Des graphiques en pièce jointe montrent les tendances des paramètres au cours des derniers jours. Veuillez les consulter pour une analyse détaillée.

**Ceci est une situation urgente et nécessite une action rapide !**

Merci de nous tenir informés de vos actions pour remédier à ce problème.

Cordialement,

mohamed AIT-OMAR
Data Science'''

    # Create the email message
    msg = EmailMessage()
    msg['To'] = "aitomar.mip.97@gmail.com,quickandeasyrecips@gmail.com,abdellahsghir2000@gmail.com"
    msg['From'] = gmail_cfg['email']
    msg['Subject'] = f"URGENT - Alerte Dépassement des Seuils des Paramètres Critiques"
    msg.set_content(message_body)

    # Attach all the images to the email
    for alert in alerts:
        with open(alert['graph_path'], 'rb') as f:
            file_data = f.read()
            file_name = f.name
            msg.add_attachment(file_data, maintype='image', subtype='png', filename=file_name)
    
    # Send the email
    with smtplib.SMTP_SSL(gmail_cfg['serveur'], gmail_cfg['port']) as smtp:
        smtp.login(gmail_cfg['email'], gmail_cfg['pwd'])
        smtp.send_message(msg)
    st.success("Notification envoyée avec succès!")

    # Delete the images after sending
    for alert in alerts:
        os.remove(alert['graph_path'])

thresholds = {
    "QT_sortie_global": {"Cond. (mS/cm) à 25° C": 450, "Turb (NTU)": 0.1},
    "ESLI_PERMEAT RO": {"Cond A1": 450, "Cond A2": 450, "Cond B2": 450, "Cond A4": 450},
    # #-----------------------------------QT-------------------------------------------------
    # "QT_intake" : {'Cond. (mS/cm) à 25° C', 'pH', 'Turb (NTU)', 
    #                'PO43- (mg/l)','SiO2 (mg/l)','MES  (mg/l)','TDS (mg/l)'},

    # "QT_PERMEAT FILTRATION" : {'Turb (NTU)', 'SiO2 (mg/l)', 'MES (mg/l)', 'SDI 15'} ,

    # "QT_APRES FILTRES A CARTOUCHE" : {'pH', 'PO43-  (mg/l)', ' ORP (mV) P1', 'ORP (mV) P2',
    #                                    'SDI15','TDS (mg/l)'},

    # "QT_PERMEAT RO" : {'Cond A', 'pH A', 'Cond B', 'pH B', 'Cond C',
    #                     'pH C', 'Cond D','pH D', 'Cond E', 'pH E', 
    #                     'Cond F', 'pH F', 'Cond G', 'pH G', 'Cond H','pH H'},   

    # "QT_sortie_global": {'pH', 'Cond. (mS/cm) à 25° C', 'Turb (NTU)', 'TDS (mg/l)'},
    # #-----------------------------------ION-------------------------------------------------
    # "ION_intake" : {'Cond. (mS/cm) à 25° C', 'pH', 'Turb (NTU)', 
    #                'PO43- (mg/l)','SiO2 (mg/l)','MES  (mg/l)','TDS (mg/l)'},

    # "ION_PERMEAT FILTRATION" : {'Turb (NTU) HMMF A', 'SDI15 HMMF A', 'Turb (NTU) HMMF B',
    #                             'SDI15 HMMF B', 'Turb (NTU) HMMF C', 'SDI15 HMMF C',
    #                             'Turb (NTU) HMMF D', 'SDI15 HMMF D', 'Turb (NTU) HMMF E',
    #                             'SDI15 HMMF E', 'Turb (NTU) HMMF F', 'SDI15 HMMF F',
    #                             'Turb (NTU) HMMF G', 'SDI15 HMMF G', 'Turb (NTU) HMMF H',
    #                             'SDI15 HMMF H', 'Turb (NTU) HMMF I', 'SDI15 HMMF I',
    #                             'Turb (NTU) HMMF J', 'SDI15 HMMF J', 'SDI 15 Collecteur'} ,

    # "QT_APRES FILTRES A CARTOUCHE" : {'ORP (mV) Collecteur A,B,C,D,E','ORP (mV) Collecteur F,G,H,I,J',
    #                                    'SDI15 Collecteur A,B,C,D,E','SDI15 Collecteur F,G,H,I,J'},

    # "ION_PERMEAT RO" : {'Cond A', 'pH A', 'Cond B', 'pH B', 'Cond C', 'pH C', 
    #                     'Cond D','pH d ', 'Cond E', 'pH E', 'Cond F', 'pH F ',
    #                       'Cond G', 'pH G','Cond H', ' pH H'},                                     
    # #-----------------------------------ESLI-------------------------------------------------
    # "ESLI_intake":{'Cond. (mS/cm) à 25° C', 'pH', 'Turb (NTU)', 
    #                'PO43- (mg/l)','SiO2 (mg/l)','MES  (mg/l)','TDS (mg/l)'},

    # "ESLI_PERMEAT FILTRATION":{'Fe2+ (mg/l) Zone A', 'Fe3+ (mg/l) Zone A', 'MES (mg/l) Zone A',
    #                             'SDI15 Zone A', 'Fe2+ (mg/l) Zone B', 'Fe3+ (mg/l) Zone B',
    #                             'MES (mg/l) Zone B', 'SDI15 Zone B', 'Fe2+ (mg/l) Zone C',
    #                             'Fe3+ (mg/l) Zone C', 'MES (mg/l) Zone C', 'SDI15 Zone C'},

    # "ESLI_APRES FILTRES A CARTOUCHE":{'pH ZONE A', 'T (°C)  ZONE A', 'ORP (mV)  ZONE A',
    #                                 'SDI15  ZONE A', 'PO43-  (mg/l)  ZONE A', 'TDS (mg/l)  ZONE A',
    #                                 'pH  ZONE B', 'T (°C) ZONE B', 'ORP (mV) ZONE B', 'SDI15 ZONE B',
    #                                 'PO43-  (mg/l) ZONE B', 'TDS (mg/l) ZONE B', 'pH ZONE C',
    #                                 'T (°C) ZONE C', 'ORP (mV) ZONE C', 'SDI15 ZONE C',
    #                                 'PO43-  (mg/l) ZONE C', 'TDS (mg/l) ZONE C'},

    # "ESLI_PERMEAT RO":{'Cond A1', 'Ph A1', 'Cond A2', 'Ph A2', 'Cond A3', 'Ph A3',
    #                     'Cond A4', 'Ph A4', 'Cond B1', 'Ph B1', 'Cond B2', 'Ph b2', 'Cond B3',
    #                     'Ph B3', 'Cond B4', 'Ph B4', 'Cond C1', 'Ph C1', 'Cond C2', 'Ph C2',
    #                     'Cond C3', 'Ph C3', 'Cond C4', 'Ph C4'},
    # #-----------------------------------MCT-------------------------------------------------
    # "MCT_intake":{'Cond. (mS/cm) à 25° C', 'pH', 'Turb (NTU)', 
    #                'PO43- (mg/l)','SiO2 (mg/l)','MES  (mg/l)','TDS (mg/l)'},

    # "MCT_APRES FILTRES A CARTOUCHE":{ 'pH LIGNE 1', 'Turb (NTU) LIGNE 1', 'PO43-  (mg/l) LIGNE 1',
    #             'ORP (mV) LIGNE 1', 'SDI15 LIGNE 1', 'TOC (mg/l) LIGNE 1',
    #             'TDS (mg/l) LIGNE 1', 'pH LIGNE 2', 'Turb (NTU) LIGNE 2',
    #             'PO43-   (mg/l) LIGNE 2', 'ORP (mV) LIGNE 2', 'SDI15 LIGNE 2',
    #             'TOC (mg/l) LIGNE 2', 'TDS (mg/l) LIGNE 2', 'pH LIGNE 3',
    #             'Turb (NTU) LIGNE 3', 'PO43-  (mg/l) LIGNE 3', 'ORP (mV) LIGNE 3',
    #             'SDI15 LIGNE 3', 'TOC (mg/l) LIGNE 3', 'TDS (mg/l) LIGNE 3',
    #             'pH  LIGNE 4', 'Turb (NTU) LIGNE 4', 'PO43-  (mg/l) LIGNE 4',
    #             'ORP (mV) LIGNE 4', 'SDI15 LIGNE 4', 'TOC (mg/l) LIGNE 4',
    #             'TDS (mg/l) LIGNE 4'},

    # "MCT_PERMEAT RO":{'Cond LIGNE 1', 'pH LIGNE 1', 'Cond LIGNE 2', 'pH LIGNE 2',
    #                  'Cond LIGNE 3', 'pH LIGNE 3', 'Cond LIGNE 4', 'pH LIGNE 4'}
}

sheets = list(thresholds.keys())
data = {}

# Load data for each sheet
for sheet in sheets:
    data[sheet] = pd.read_excel("data/Suivi Analyse Mobile préparaé.xlsx", sheet_name=sheet)

# List to hold all alerts
alerts = [] 

# Iterate through each sheet and check if thresholds are exceeded
for sheet in sheets:
    df = data[sheet]
    for param, seuil in thresholds[sheet].items():
        if (df[param].iloc[-1] == "/" or df[param].iloc[-1] == "en cours"):
            continue
        else:
            valeur_actuelle = float(df[param].iloc[-1])
            if not isinstance(valeur_actuelle, float):
                continue
            if valeur_actuelle > seuil:
                # Extract the date of the exceedance
                date_depassement = df['date'].iloc[-1]  # assuming the 'date' column holds the dates
                date_depassement_str = pd.to_datetime(date_depassement).strftime("%d/%m/%Y")

                # Generate the graph
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

                # Save the graph as an image
                file_path = f'graph_{sheet}_{param}.png'
                pio.write_image(fig, file_path)

                # Add the alert to the list
                alerts.append({
                    "sheet": sheet,
                    "param": param,
                    "value": valeur_actuelle,
                    "threshold": seuil,
                    "graph_path": file_path,
                    "date": date_depassement_str
                })

# Display the title and section in Streamlit
st.markdown("<h1 style='text-align: center; color: blue;'>💧 Surveillance et Alertes Automatiques des Paramètres de Qualité de l'eau 💧</h1>", unsafe_allow_html=True)

# Display alert messages with dates
if alerts:
    st.markdown("<h2 style='color: red; text-align: center;'>⚠️ Attention : Dépassement de seuil détecté ! ⚠️</h2>", unsafe_allow_html=True)
    st.write("Veuillez consulter les détails des alertes ci-dessous et agir rapidement pour rectifier les anomalies.")

    # Display the date of exceedance for each alert
    for alert in alerts:
        st.markdown(f"🔔 **{alert['param']}** dans **{alert['sheet']}** a dépassé le seuil le **{alert['date']}** avec une valeur de **{alert['value']}** (seuil : {alert['threshold']}).")
    
    with st.expander("Afficher les détails des alertes", expanded=False):
        alert_data = pd.DataFrame(alerts)

        # Split the 'sheet' column into 'unité' and 'phase de traitement'
        # Use expand=True to create two columns, and fill any missing values
        alert_data[['unité', 'phase de traitement']] = alert_data['sheet'].str.split('_', n=1, expand=True)

        # Fill NaN values for cases where splitting didn't produce two columns
        alert_data['unité'] = alert_data['unité'].fillna('Inconnu')
        alert_data['phase de traitement'] = alert_data['phase de traitement'].fillna('Inconnu')

        # Add the 'date' column to alert_data
        alert_data['date'] = [alert['date'] for alert in alerts]

        
        alert_data = alert_data[['unité', 'phase de traitement', 'param', 'value', 'threshold', 'date']]
        # alert_data.set_index('date', inplace=True)
        st.table(alert_data)
    
    # Bouton d'envoi de notification avec spinner et style
    if st.button("🚨 Envoyer une notification d'alerte 🚨"):
        with st.spinner("Envoi des notifications..."):
            send_notifications(alerts)
else:
    st.info("Aucune alerte détectée pour le moment. Tout est sous contrôle. ✅")
