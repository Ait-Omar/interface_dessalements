import streamlit as st
import pandas as pd
from PIL import Image
import base64
from io import BytesIO
# Titre de l'application

st.set_page_config(page_title="Mon Application à plusieurs pages", page_icon=":tada:", layout="wide")

st.markdown("<h1 style='text-align: center;color:#095DBA;'> Dessalement de l'eau de mer mobile à JORF LASFAR</h1>", unsafe_allow_html=True)


def image_to_base64(image_path):
    img = Image.open(image_path)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

logo_path1 = "static/mix.png"  
logo_base641 = image_to_base64(logo_path1)


st.markdown(
    f"""
    <div style="text-align: center; padding-bottom: 40px;padding-top: 40px;">
        <img src="data:image/png;base64,{logo_base641}" alt="Logo" width="400">
    </div>
    """, 
    unsafe_allow_html=True
)

st.markdown(
    """
  <p style="text-align: center; font-size: 18px; color: #555;">
        Face à la pénurie d'eau douce qui menace de nombreuses régions, Jorf Lasfar se distingue par son initiative novatrice 
        en matière de dessalement mobile de l'eau de mer. Grâce à des technologies avancées, cette solution permet de transformer 
        l'eau salée en une ressource potable, tout en s'adaptant rapidement aux besoins de la communauté.
    </p>
    <p style="text-align: center; font-size: 18px; color: #555;">
        L'entreprise DIPS joue un rôle clé dans ce processus, assurant un suivi rigoureux et une mise en œuvre efficace des 
        unités de dessalement. Ces systèmes mobiles peuvent être déployés rapidement pour répondre aux exigences variées 
        des secteurs résidentiels et agricoles, garantissant ainsi une gestion optimale des ressources en eau.
    </p>
    <p style="text-align: center; font-size: 18px; color: #555;">
        En combinant expertise technique et innovation, DIPS contribue à minimiser l'impact environnemental tout en maximisant 
        l'accès à l'eau potable. Cette démarche proactive illustre comment la technologie peut aider à relever les défis 
        liés à l'eau, tout en soutenant le développement durable à Jorf Lasfar et au-delà. Ensemble, nous pouvons faire 
        en sorte que chaque goutte d'eau compte.
    </p>
    """,
    unsafe_allow_html=True
)


