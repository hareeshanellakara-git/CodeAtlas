

import streamlit as st

from config import POWERED_BY


def render_footer():
    st.markdown(
    f"""
    <div class='footer'>
        CodeAtlas © 2026
        <br>
        Built with {' • '.join(POWERED_BY)}
        <br>
        Created by <strong>Hareesha N.</strong>
    </div>
    """,
    unsafe_allow_html=True,
)