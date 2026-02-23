import streamlit as st
from models.models import Styles_manager

Styles_manager.load_css()

st.markdown("""
<div class="metric-card metric-card-green" style="padding:30px; border-radius:15px;">
    <h1 style="margin:0;">Feedback Utilisateur</h1> 
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


col1, col2 = st.columns([2, 1], gap="medium")

with col1:
    st.subheader("Formulaire d'évaluation")
    choix = st.segmented_control("Choisir la plateforme", ["KoboToolbox", "Google Form"], default="KoboToolbox")
    
    if choix == "KoboToolbox":
        url_embed = "https://ee.kobotoolbox.org/single/rLn3vxI4"
    else:
        url_embed = "https://docs.google.com/forms/d/e/1FAIpQLSfktCraWmBBH42vrm6UpSMRtqYqVngkArz5P4hPUqkqM_hZkw/viewform?embedded=true"

    # Intégration de l'iframe
    st.components.v1.html(f"""
        <iframe src="{url_embed}" width="100%" height="700" frameborder="0" style="border:1px solid #eee; border-radius:10px;">
            Chargement…
        </iframe>
    """, height=720)

with col2:
    st.subheader("Liens Externes")
    st.info("Si le formulaire ne s'affiche pas correctement, utilisez les boutons ci-dessous pour l'ouvrir dans un nouvel onglet.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Boutons stylisés
    st.link_button(
        "Ouvrir Google Form", 
        "https://forms.gle/5KT1j7qKMEPrpKqt9", 
        use_container_width=True,
        type="primary"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.link_button(
        "Ouvrir KoboToolbox", 
        "https://ee.kobotoolbox.org/single/rLn3vxI4", 
        use_container_width=True
    )
