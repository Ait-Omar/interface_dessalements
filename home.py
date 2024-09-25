import streamlit as st
import pandas as pd
from PIL import Image
import base64
from io import BytesIO
# Titre de l'application

st.set_page_config(page_title="Mon Application à plusieurs pages", page_icon=":tada:", layout="wide")

# st.markdown("<h1 style='text-align: center;color:#095DBA;'> Dessalement de l'eau de mer mobile à JORF LASFAR</h1>", unsafe_allow_html=True)


def image_to_base64(image_path):
    img = Image.open(image_path)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

logo_path1 = "static/home.png"  
logo_base641 = image_to_base64(logo_path1)


st.markdown(
    f"""
    <div style="text-align: center; padding-bottom: 40px;padding-top: 40px;">
        <img src="data:image/png;base64,{logo_base641}" alt="Logo" width="1200">
    </div>
    """, 
    unsafe_allow_html=True
)

st.markdown("""
    <div style="margin-left: 150px; margin-right: 150px; text-align: justify; font-size: 20px; color: #555;">
        <h2>Bienvenue sur l'application de dessalement d'eau de mer à Jorf Lasfar</h2>
        <p>Cette application présente une solution innovante pour répondre aux besoins croissants en eau potable dans la région de Jorf Lasfar, où les ressources en eau douce se font rares. Grâce à la technologie de dessalement mobile, nous utilisons les vastes ressources en eau de mer de l'océan Atlantique pour fournir de l'eau potable, répondant ainsi aux besoins des populations et des industries locales.</p>
        <p>Notre système est conçu pour être durable, efficient et respectueux de l'environnement, en optimisant l'utilisation de l'énergie et en minimisant l'impact écologique. Cette solution vise non seulement à satisfaire les besoins en eau actuels, mais aussi à anticiper les défis futurs liés aux changements climatiques et à la croissance démographique.</p>
        <p>Grâce à l'engagement de <strong>DIPS</strong>, nous mettons en œuvre des technologies de pointe pour garantir une gestion efficace et responsable des ressources en eau. Nous nous engageons à offrir une solution flexible, mobile et adaptée aux exigences spécifiques de chaque projet, tout en maintenant les standards les plus élevés de qualité et de sécurité.</p>
        <p>Explorez les différentes fonctionnalités de l'application pour découvrir comment nous contribuons à un avenir plus durable et comment nos solutions peuvent être adaptées à vos besoins.</p>
    </div>
""", unsafe_allow_html=True)


