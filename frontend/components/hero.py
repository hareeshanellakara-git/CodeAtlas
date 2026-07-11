
import streamlit as st

from config import APP_NAME, APP_TAGLINE, APP_DESCRIPTION, LOGO_PATH2


def render_hero():
    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        st.image(

            "frontend/assets/logo2.png",
            use_container_width=True,
        )

    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-title">{APP_NAME}</div>
            <div class="hero-tagline">{APP_TAGLINE}</div>
            <div class="hero-description">{APP_DESCRIPTION}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )