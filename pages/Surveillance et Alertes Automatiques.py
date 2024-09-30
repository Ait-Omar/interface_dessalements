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
    msg['To'] = "aitomar.mip.97@gmail.com"
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

# Define the threshold dictionary (example)
thresholds = {
    "QT_sortie_global": {"Cond. (mS/cm) à 25° C": 450,"Turb (NTU)": 0.1},
     "ESLI_PERMEAT RO": {"Cond A1": 450, "Cond A2": 450,"Cond B2": 450, "Cond A4": 450},
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

        # Reorder the columns if needed
        alert_data = alert_data[['unité', 'phase de traitement', 'param', 'value', 'threshold', 'date']]

        st.table(alert_data)
    
    # Bouton d'envoi de notification avec spinner et style
    if st.button("🚨 Envoyer une notification d'alerte 🚨"):
        with st.spinner("Envoi des notifications..."):
            send_notifications(alerts)
else:
    st.info("Aucune alerte détectée pour le moment. Tout est sous contrôle. ✅")
